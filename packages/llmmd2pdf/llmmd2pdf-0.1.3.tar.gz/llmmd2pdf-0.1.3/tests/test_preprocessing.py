import sys
import os
import pytest
from pathlib import Path

# Ensure we can import the module from src without installing it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from llmmd2pdf.app import preprocess_markdown

# --- Helper Function ---
def load_fixture(filename):
    """Helper to load text files from the tests/test_data directory."""
    base_path = Path(__file__).parent / "test_data"
    file_path = base_path / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Test fixture not found: {file_path}")
        
    return file_path.read_text(encoding="utf-8")

# --- Test Data Definitions ---

# Schema: (Test Name/ID, Input Filename, Expected Output Filename)
GEMINI_CASES = [
    ("header_1",       "gemini_input_header_1.md",            "gemini_expected_header_1.md"),
    ("header_2",       "gemini_input_header_2.md",            "gemini_expected_header_2.md"),
    ("profile_pic",    "gemini_input_profile_image.md",       "gemini_expected_profile_image.md"),
    ("export_footer",  "gemini_input_export.md",              "gemini_expected_export.md"),
    ("image_links",    "gemini_input_image_links.md",         "gemini_expected_image_links.md"),
    ("combined_all",   "gemini_input_all.md",                 "gemini_expected_all.md"),
    ("tools_thinking", "gemini_input_tools_show_thinking.md", "gemini_expected_tools_show_thinking.md"),
]

CLAUDE_CASES = [
    ("hr_spacing",         "claude_input_linebreak.md",              "claude_expected_linebreak.md"),
    ("undefined_art_1",    "claude_input_undefined_artefact_1.md",   "claude_expected_undefined_artefact_1.md"),
    ("undefined_art_2",    "claude_input_undefined_artefact_2.md",   "claude_expected_undefined_artefact_2.md"),
]

# --- Test Functions ---

@pytest.mark.parametrize("test_id, input_file, expected_file", GEMINI_CASES)
def test_gemini_preprocessing(test_id, input_file, expected_file):
    """
    Tests specific rules for Gemini exports.
    The 'test_id' argument allows pytest to label specific cases in the output.
    """
    input_text = load_fixture(input_file)
    expected_output = load_fixture(expected_file)
    
    assert preprocess_markdown(input_text) == expected_output

@pytest.mark.parametrize("test_id, input_file, expected_file", CLAUDE_CASES)
def test_claude_preprocessing(test_id, input_file, expected_file):
    """
    Tests specific rules for Claude exports.
    """
    input_text = load_fixture(input_file)
    expected_output = load_fixture(expected_file)
    
    assert preprocess_markdown(input_text) == expected_output
