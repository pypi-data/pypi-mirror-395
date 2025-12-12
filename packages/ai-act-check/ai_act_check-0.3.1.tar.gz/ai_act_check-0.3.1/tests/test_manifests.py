import os
import pytest
from ai_act_check.scanner import scan_repository

def test_go_mod_scan(tmp_path):
    d = tmp_path / "go_project"
    d.mkdir()
    p = d / "go.mod"
    p.write_text('module example.com/my-project\n\ngo 1.16\n\nrequire (\n\tgorgonia.org/gorgonia v0.9.17\n)')
    
    results = scan_repository(str(d))
    detected = results["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]["detected_libraries"]
    
    assert "gorgonia" in detected

def test_cargo_toml_scan(tmp_path):
    d = tmp_path / "rust_project"
    d.mkdir()
    p = d / "Cargo.toml"
    p.write_text('[package]\nname = "my-project"\n\n[dependencies]\ntch = "0.4.1"')
    
    results = scan_repository(str(d))
    detected = results["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]["detected_libraries"]
    
    assert "tch" in detected

def test_pom_xml_scan(tmp_path):
    d = tmp_path / "java_project"
    d.mkdir()
    p = d / "pom.xml"
    p.write_text('<project>\n<dependencies>\n<dependency>\n<groupId>org.deeplearning4j</groupId>\n<artifactId>deeplearning4j-core</artifactId>\n<version>1.0.0-beta7</version>\n</dependency>\n</dependencies>\n</project>')
    
    results = scan_repository(str(d))
    detected = results["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]["detected_libraries"]
    
    assert "deeplearning4j" in detected

def test_gemfile_scan(tmp_path):
    d = tmp_path / "ruby_project"
    d.mkdir()
    p = d / "Gemfile"
    p.write_text("source 'https://rubygems.org'\ngem 'torch-rb'")
    
    results = scan_repository(str(d))
    detected = results["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]["detected_libraries"]
    
    assert "torch-rb" in detected

def test_composer_json_scan(tmp_path):
    d = tmp_path / "php_project"
    d.mkdir()
    p = d / "composer.json"
    p.write_text('{\n"require": {\n"php-ai/php-ml": "^0.9.0"\n}\n}')
    
    results = scan_repository(str(d))
    detected = results["annex_iv_technical_documentation"]["section_2_b_design_specifications"]["general_logic"]["detected_libraries"]
    
    assert "php-ai/php-ml" in detected
