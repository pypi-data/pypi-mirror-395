import pytest
from ai_act_check.scanner import scan_libraries
from ai_act_check import cli
import json
from unittest.mock import patch

def test_scan_libraries_high_risk():
    libs = ["face_recognition", "tensorflow"]
    results = scan_libraries(libs)
    
    design_specs = results["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]
    detected_libs = design_specs["detected_libraries"]
    risks = design_specs["risk_classification_detected"]
    
    assert "face_recognition" in detected_libs
    assert "tensorflow" in detected_libs
    assert any("Biometrics" in r for r in risks)
    assert any("Deep Learning" in r for r in risks)

def test_scan_libraries_no_risk():
    libs = ["requests", "numpy"]
    results = scan_libraries(libs)
    
    design_specs = results["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]
    detected_libs = design_specs["detected_libraries"]
    risks = design_specs["risk_classification_detected"]
    
    assert len(detected_libs) == 0
    assert len(risks) == 0

def test_cli_scan_libs(capsys):
    # Test the --libs flag
    cli.run_scan(repo_path=None, libs="face-api.js, torch")
    captured = capsys.readouterr()
    out = captured.out
    parsed = json.loads(out)
    
    design_specs = parsed["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]
    detected_libs = design_specs["detected_libraries"]
    
    assert "face-api.js" in detected_libs
    assert "torch" in detected_libs

def test_cli_manual_mode(monkeypatch, capsys):
    # Mock user input for manual mode
    monkeypatch.setattr('builtins.input', lambda _: "tensorflow.js, onnx")
    
    cli.run_manual()
    captured = capsys.readouterr()
    out = captured.out
    
    # The output contains more than just JSON, so we need to find the JSON part or check for strings
    assert "tensorflow.js" in out
    assert "onnx" in out
    assert "Deep Learning (Browser-based)" in out
