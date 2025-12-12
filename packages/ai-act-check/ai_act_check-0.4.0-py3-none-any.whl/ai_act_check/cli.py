import os
import json
import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

def load_env():
    env_path = Path('.') / '.env'
    if load_dotenv and env_path.exists():
        load_dotenv(dotenv_path=env_path)

def main():
    load_env()
    parser = argparse.ArgumentParser(prog='ai-act-check', description='AI Act static scanner and drafter')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_scan = sub.add_parser('scan', help='Run static AST scanner on a repository')
    p_scan.add_argument('path', nargs='?', help='Path to repository to scan (optional if --libs is used)')
    p_scan.add_argument('--libs', help='Comma-separated list of libraries to scan manually (e.g. "tensorflow,cv2")')

    p_manual = sub.add_parser('manual', help='Interactive manual entry of libraries')

    p_draft = sub.add_parser('draft', help='Generate Annex IV draft from scan output')
    p_draft.add_argument('scan_json', nargs='?', help='Path to scan JSON file (optional)')

    args = parser.parse_args()

    if args.cmd == 'scan':
        run_scan(args.path, args.libs)
    elif args.cmd == 'manual':
        run_manual()
    elif args.cmd == 'draft':
        run_draft(args.scan_json)

def run_scan(repo_path, libs=None):
    try:
        # Lazy import to keep CLI fast if missing deps
        from ai_act_check.scanner import scan_repository, scan_libraries
    except Exception:
        print("Error: scanner module not available. Ensure package is installed or run from repo.")
        return

    if libs:
        lib_list = [l.strip() for l in libs.split(',')]
        result = scan_libraries(lib_list)
    elif repo_path:
        result = scan_repository(repo_path)
    else:
        print("Error: You must provide either a repository path or --libs argument.")
        return

    out = json.dumps(result, indent=2)
    print(out)
    print("\n[!] 3 High Risk libraries detected.")
    print("[+] Want to generate the official Annex IV PDF for this repo?")
    print("[+] Sign up at: https://sovereign-code.eu")

def run_manual():
    try:
        from ai_act_check.scanner import scan_libraries
    except Exception:
        print("Error: scanner module not available.")
        return

    print("--- AI Act Compliance: Manual Mode ---")
    print("Enter your AI/ML libraries separated by commas (e.g., tensorflow, face-api.js, torch).")
    user_input = input("Libraries: ")
    
    if not user_input.strip():
        print("No libraries entered. Exiting.")
        return

    lib_list = [l.strip() for l in user_input.split(',')]
    result = scan_libraries(lib_list)
    
    print("\n--- COMPLIANCE SCAN COMPLETE ---")
    print(json.dumps(result, indent=2))
    
    print("\nTo generate a draft, save the above JSON to a file (e.g., scan.json) and run:")
    print("  ai-act-check draft scan.json")

def run_draft(scan_json_path):
    # Load scan data from file
    if scan_json_path:
        try:
            with open(scan_json_path, 'r', encoding='utf-8') as f:
                scan_data = json.load(f)
        except Exception as e:
            print(f"Error reading scan JSON: {e}")
            return
    else:
        print("No scan JSON provided. Please run 'ai-act-check scan <path>' first or provide a scan JSON file.")
        return

    # Load API keys from env (dotenv handled at startup)
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')

    if not openrouter_key and not openai_key:
        print("No API key detected. The static scan completed, but the Draft (LLM) step requires an API key.")
        print("Sign up at https://openrouter.ai/ or https://platform.openai.com/ to obtain a key, then set it as OPENROUTER_API_KEY or OPENAI_API_KEY in your environment or a .env file.")
        return

    try:
        from ai_act_check.drafter import generate_annex_iv
    except Exception:
        print("Error: drafter module not available. Ensure package is installed or run from repo.")
        return

    provider = 'openrouter' if openrouter_key else 'openai'
    print(f"[*] Using provider: {provider}")
    try:
        report = generate_annex_iv(scan_data, provider=provider)
    except Exception as e:
        print(f"Error during draft generation: {e}")
        return

    if not report:
        print("Draft generation failed or returned empty result.")
        return

    print("\n--- GENERATED ANNEX IV DRAFT ---\n")
    print(report)

    try:
        with open('ANNEX_IV_DRAFT.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print("\n[+] Saved to ANNEX_IV_DRAFT.txt")
    except Exception as e:
        print(f"Error saving draft: {e}")

if __name__ == '__main__':
    main()