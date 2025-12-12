import ast
import os
import json
import sys
import re
from typing import Dict, Set, Tuple, List, Any

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RISK_MAP_PATH = os.path.join(CURRENT_DIR, "data", "risk_map.json")

try:
    with open(RISK_MAP_PATH, "r", encoding="utf-8") as f:
        RISK_LIBRARY_MAP: Dict[str, str] = json.load(f)
except FileNotFoundError:
    print(f"[!] CRITICAL: Could not find risk_map.json at {RISK_MAP_PATH}")
    RISK_LIBRARY_MAP = {}
except Exception as e:
    print(f"[!] Error loading risk_map.json: {e}")
    RISK_LIBRARY_MAP = {}

class CodeScanner(ast.NodeVisitor):
    """Scans Python source code (AST) for imports matching risk map."""
    def __init__(self) -> None:
        self.detected: Set[str] = set()
        self.risks: Set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self._check(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            self._check(node.module)
        self.generic_visit(node)

    def _check(self, name: str) -> None:
        for lib, risk in RISK_LIBRARY_MAP.items():
            if name.startswith(lib):
                self.detected.add(name)
                self.risks.add(risk)

def scan_dependency_files(repo_path: str) -> Tuple[Set[str], Set[str]]:
    detected: Set[str] = set()
    risks: Set[str] = set()

    target_files = {
        "requirements.txt", "package.json", "pyproject.toml", "Pipfile",
        "go.mod", "Cargo.toml", "pom.xml", "Gemfile", "composer.json", "build.gradle"
    }

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file in target_files:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        for risk_lib, risk_desc in RISK_LIBRARY_MAP.items():
                            if risk_lib in content:
                                # heuristic to reduce false positives for manifests
                                # We look for the library name surrounded by quotes, whitespace, or common delimiters
                                pattern = rf'(?:^|[\s"\'/<>.-])({re.escape(risk_lib)})(?:$|[\s"\'/:>=<>.-])'
                                if re.search(pattern, content):
                                    detected.add(risk_lib)
                                    risks.add(risk_desc)
                except Exception:
                    # ignore unreadable files
                    continue

    return detected, risks

def scan_libraries(libs: List[str]) -> Dict[str, Any]:
    """
    Scans a list of library names against the risk map.
    """
    detected: Set[str] = set()
    risks: Set[str] = set()

    for lib_name in libs:
        # Check if the library name matches any key in the risk map
        # We check both exact match and if the library starts with a risk map key
        for risk_lib, risk_desc in RISK_LIBRARY_MAP.items():
            if lib_name == risk_lib or lib_name.startswith(risk_lib):
                detected.add(lib_name)
                risks.add(risk_desc)

    return _format_results(sorted(list(detected)), sorted(list(risks)))

def scan_repository(repo_path: str) -> Dict[str, Any]:
    ast_scanner = CodeScanner()
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        source = f.read()
                        if len(source) > 5_000_000:
                            continue
                        tree = ast.parse(source)
                        ast_scanner.visit(tree)
                except Exception:
                    continue

    dep_libs, dep_risks = scan_dependency_files(repo_path)

    final_libs = sorted(list(ast_scanner.detected.union(dep_libs)))
    final_risks = sorted(list(ast_scanner.risks.union(dep_risks)))

    return _format_results(final_libs, final_risks)

def _format_results(detected_libs: List[str], detected_risks: List[str]) -> Dict[str, Any]:
    return {
        "annex_iv_technical_documentation": {
            "section_2_b_design_specifications": {
                "general_logic": {
                    "detected_libraries": detected_libs,
                    "risk_classification_detected": detected_risks,
                    "model_architecture": None
                },
                "key_design_choices": {
                    "framework": None,
                    "loss_functions": []
                }
            }
        }
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m ai_act_check.scanner <path_to_repo>")
        sys.exit(1)
    repo_path = sys.argv[1]
    results = scan_repository(repo_path)
    print("\n--- COMPLIANCE SCAN COMPLETE ---")
    print(json.dumps(results, indent=2))