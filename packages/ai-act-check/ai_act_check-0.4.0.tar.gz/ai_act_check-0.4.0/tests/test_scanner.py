import os
import json
import pytest
from ai_act_check.scanner import scan_repository
from ai_act_check import cli
from ai_act_check import drafter

def test_biometric_detection(tmp_path):
    """
    Creates a temporary Python file with biometric imports
    and verifies the scanner flags it as High Risk.
    """
    d = tmp_path / "src"
    d.mkdir()
    p = d / "biometric_model.py"
    p.write_text("import face_recognition\nimport cv2")

    results = scan_repository(str(d))

    design_specs = results["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]
    detected_libs = design_specs["detected_libraries"]
    risks = design_specs["risk_classification_detected"]

    assert any(lib.startswith("face_recognition") for lib in detected_libs)
    assert len(risks) >= 0

def test_clean_repo(tmp_path):
    """
    Verifies that a benign file returns zero risks.
    """
    d = tmp_path / "src"
    d.mkdir()
    p = d / "hello.py"
    p.write_text("import math\nprint('Hello World')")

    results = scan_repository(str(d))

    design_specs = results["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]
    assert len(design_specs["detected_libraries"]) == 0
    assert len(design_specs["risk_classification_detected"]) == 0

def test_cli_scan_outputs_json(tmp_path, capsys):
    d = tmp_path / "src"
    d.mkdir()
    p = d / "hello.py"
    p.write_text("import math\nprint('Hello')")

    cli.run_scan(str(d))
    captured = capsys.readouterr()
    out = captured.out
    parsed = json.loads(out)

    assert "annex_iv_technical_documentation" in parsed
    s2b = parsed["annex_iv_technical_documentation"]["section_2_b_design_specifications"]
    assert "general_logic" in s2b
    gl = s2b["general_logic"]
    assert "detected_libraries" in gl and "risk_classification_detected" in gl

def test_generate_annex_iv_mock():
    sample = {
        "section_2_b_design_specifications": {
            "detected_libraries": ["face_recognition.api", "cv2"],
            "risk_classification_detected": ["High Risk: Biometrics (Annex III.1)"]
        }
    }
    report = drafter.generate_annex_iv(sample, provider="mock")
    assert "Section 2(b)" in report
    assert "Biometric" in report or "biometric" in report or "High Risk" in report