import unittest
import sys
import os
from pathlib import Path

# Ensure we can import the module from src without installing it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from llmmd2pdf.app import preprocess_markdown


class TestPreprocessing(unittest.TestCase):

    def _load_fixture(self, filename):
        """Helper to load text files from the tests/test_data directory."""
        # Use Path for cleaner path handling relative to this script
        base_path = Path(__file__).parent / "test_data"
        file_path = base_path / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Test fixture not found: {file_path}")
            
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()


    def test_gemini_block_cleanup(self):
        """Rule 1: Should collapse the Gemini header block to just Activity and Location."""
        
        test_cases = [
            ("gemini_input_header_1.md", "gemini_expected_header_1.md"),
            ("gemini_input_header_2.md", "gemini_expected_header_2.md")
        ]

        for input_file, expected_file in test_cases:
            
            with self.subTest(input_file=input_file):
                input_text = self._load_fixture(input_file)
                expected_output = self._load_fixture(expected_file)
                self.assertEqual(preprocess_markdown(input_text), expected_output)


    def test_profile_picture_removal(self):
        """Rule 3: Should remove lines starting with ![profile picture]."""
        input_text = self._load_fixture("gemini_input_profile_image.md")
        expected_output = self._load_fixture("gemini_expected_profile_image.md")
        self.assertEqual(preprocess_markdown(input_text), expected_output)


    def test_exported_content_cleanup(self):
        """Rule 6: Should clean the 'Exported on' footer."""
        input_text = self._load_fixture("gemini_input_export.md")
        expected_output = self._load_fixture("gemini_expected_export.md")
        self.assertEqual(preprocess_markdown(input_text), expected_output)


    def test_combined_cleanup_from_files(self):
        """
        Should apply multiple rules correctly in one pass.
        (Loads input/output from external .md files in tests/test_data/)
        """
        input_text = self._load_fixture("gemini_input_all.md")
        expected_output = self._load_fixture("gemini_expected_all.md")
        
        # Determine actual output
        actual_output = preprocess_markdown(input_text)

        # Assert equality
        # Using maxDiff=None helps see the exact mismatch in large file comparisons
        self.maxDiff = None 
        self.assertEqual(actual_output, expected_output)


    def test_horizontal_rule_spacing(self):
        """Rule 2: Should add an empty line between '---' and '**'."""
        input_text = self._load_fixture("claude_input_linebreak.md")
        expected_output = self._load_fixture("claude_expected_linebreak.md")        
        self.assertEqual(preprocess_markdown(input_text), expected_output)

    def test_undefined_artefact(self):
        """Remove: {{@CAPTURE_ARTIFACT_CONTENT:undefined}}"""
        test_cases = [
            ("gemini_input_header_1.md", "gemini_expected_header_1.md"),
            ("gemini_input_header_2.md", "gemini_expected_header_2.md")
        ]

        for input_file, expected_file in test_cases:
            
            with self.subTest(input_file=input_file):
                input_text = self._load_fixture(input_file)
                expected_output = self._load_fixture(expected_file)
                self.assertEqual(preprocess_markdown(input_text), expected_output)

    def test_remove_tools_show_thinking(self):
        """Rule 6 & 7: Remove lines exclusively containing "Tools" or "Show Thinking"."""
        input_text = self._load_fixture("gemini_input_tools_show_thinking.md")
        expected_output = self._load_fixture("gemini_expected_tools_show_thinking.md")
        self.assertEqual(preprocess_markdown(input_text), expected_output)

if __name__ == '__main__':
    unittest.main()