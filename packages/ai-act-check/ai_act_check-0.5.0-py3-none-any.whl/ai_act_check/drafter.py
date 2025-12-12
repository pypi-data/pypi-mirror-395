import os
import json
from typing import Any, Dict

def _mock_draft(scan_data: Dict[str, Any]) -> str:
    libs = scan_data.get("section_2_b_design_specifications", {}).get("detected_libraries", [])
    risks = scan_data.get("section_2_b_design_specifications", {}).get("risk_classification_detected", [])
    intended = "Undetermined"
    if any(l.startswith("face_recognition") or l.startswith("dlib") or l.startswith("cv2") for l in libs):
        intended = "Biometric identification (facial recognition)"
    elif any("sklearn" in l or "spacy" in l or "nltk" in l for l in libs):
        intended = "General ML / Text processing (potential employment-related processing)"
    comps = "\n".join(f"- {l}" for l in libs) if libs else "- None detected"
    risk_line = risks[0] if risks else "Low Risk / No Annex III match detected"
    draft = (
        "Section 2(b): Design Specifications\n\n"
        f"Intended Purpose:\nThe system is intended for: {intended}.\n\n"
        "Software Components:\n"
        f"{comps}\n\n"
        "Risk Determination:\n"
        f"Based on the detected software components, the assessed classification is: {risk_line}.\n"
    )
    return draft

def generate_annex_iv(scan_data: Dict[str, Any], provider: str = "openrouter") -> str:
    """
    Generate an Annex IV draft from scanner output.

    provider: "openrouter", "openai", or "mock"
    """
    if provider == "mock":
        return _mock_draft(scan_data)

    if provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("MANUAL_OPENROUTER_KEY")
        if not api_key:
            raise RuntimeError("No OpenRouter API key found in OPENROUTER_API_KEY or MANUAL_OPENROUTER_KEY")
        try:
            from openai import OpenAI
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            model = "google/gemini-2.0-flash-exp:free"
            system = "You are a compliance assistant. Help the user with their documentation."
            user = "Draft Section 2(b): Design Specifications.\n\nEVIDENCE:\n" + json.dumps(scan_data, indent=2)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role":"system","content":system}, {"role":"user","content":user}],
                temperature=0.1
            )
            return resp.choices[0].message.content
        except Exception as e:
            fallback = _mock_draft(scan_data)
            return f"(Fallback mock draft due to API error: {e})\n\n" + fallback

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("No OpenAI API key found in OPENAI_API_KEY")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            model = "gpt-4o"
            system = "You are a compliance assistant. Help the user with their documentation."
            user = "Draft Section 2(b): Design Specifications.\n\nEVIDENCE:\n" + json.dumps(scan_data, indent=2)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role":"system","content":system}, {"role":"user","content":user}],
                temperature=0.1
            )
            return resp.choices[0].message.content
        except Exception as e:
            fallback = _mock_draft(scan_data)
            return f"(Fallback mock draft due to API error: {e})\n\n" + fallback

    raise RuntimeError(f"Unknown provider: {provider}")

if __name__ == "__main__":
    # quick smoke test
    sample = {
        "section_2_b_design_specifications": {
            "detected_libraries": ["face_recognition.api", "sklearn", "cv2", "dlib"],
            "risk_classification_detected": ["High Risk: Biometrics (Annex III.1)"]
        }
    }
    print(generate_annex_iv(sample, provider="mock"))