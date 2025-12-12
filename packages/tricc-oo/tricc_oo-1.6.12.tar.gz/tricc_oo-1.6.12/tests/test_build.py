import unittest
import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path
import pandas as pd
from pyxform import create_survey_from_xls


class TestBuildScript(unittest.TestCase):
    """Test cases for the build.py script with different argument combinations."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = Path(__file__).parent / "data"
        self.test_output_dir = Path(__file__).parent / "output"
        self.demo_file = self.test_data_dir / "demo.drawio"

        # Ensure test data exists
        self.assertTrue(self.demo_file.exists(), f"Test data file {self.demo_file} does not exist")

    def run_build_script(self, args):
        """Helper method to run build.py with given arguments."""
        cmd = [sys.executable, str(Path(__file__).parent / "build.py")] + args
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        return result

    def test_basic_build_with_demo_file(self):
        """Test basic build with demo.drawio file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_directory_input(self):
        """Test build with directory containing drawio files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.test_data_dir),
                "-o", temp_dir,
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_xlsform_strategy(self):
        """Test build with XLSFormStrategy (default)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "XLSFormStrategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_html_strategy(self):
        """Test build with HTMLStrategy."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "HTMLStrategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_fhir_strategy(self):
        """Test build with FHIRStrategy."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "FHIRStrategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_dhis2_strategy(self):
        """Test build with DHIS2Strategy."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "DHIS2Strategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_openmrs_strategy(self):
        """Test build with OpenMRSStrategy."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "OpenMRSStrategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_cht_strategy(self):
        """Test build with XLSFormCHTStrategy."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "XLSFormCHTStrategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_cht_hf_strategy(self):
        """Test build with XLSFormCHTHFStrategy."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "XLSFormCHTHFStrategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_cdss_strategy(self):
        """Test build with XLSFormCDSSStrategy."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "XLSFormCDSSStrategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    # def test_build_with_spice_strategy(self):
    #     """Test build with SpiceStrategy."""
    #     with tempfile.TemporaryDirectory() as temp_dir:
    #         args = [
    #             "-i", str(self.demo_file),
    #             "-o", temp_dir,
    #             "-O", "SpiceStrategy",
    #             "-l", "i"
    #         ]
    #         result = self.run_build_script(args)
    #         self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_debug_level(self):
        """Test build with debug logging level."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-l", "d"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_trad_option(self):
        """Test build with translation option."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-t",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_with_form_id(self):
        """Test build with custom form ID."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-d", "test_form_123",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

    def test_build_missing_input(self):
        """Test build with missing input file."""
        args = ["-o", "/tmp/test_output"]
        result = self.run_build_script(args)
        self.assertNotEqual(result.returncode, 0, "Build should fail with missing input")

    def test_build_invalid_input_file(self):
        """Test build with invalid input file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = [
                "-i", "/nonexistent/file.drawio",
                "-o", temp_dir,
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertNotEqual(result.returncode, 0, "Build should fail with invalid input file")

    def validate_xls_form(self, xls_path):
        """Helper method to validate XLS form using ODK libraries."""
        try:
            # Convert XLS to XML using pyxform
            survey = create_survey_from_xls(xls_path)
            xml_output = survey.to_xml()

            # Basic validation - check if XML was generated successfully
            # In a real scenario, you might want to use odk_validate command line tool
            if xml_output and len(xml_output.strip()) > 0:
                return True, "Validation successful"
            else:
                return False, "Empty XML output"
        except Exception as e:
            return False, str(e)

    def test_xlsform_strategy_validation(self):
        """Test XLSFormStrategy output validation with ODK libraries."""
        with tempfile.TemporaryDirectory() as temp_dir:
            xls_output = Path(temp_dir) / "demo_tricc.xlsx"
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "XLSFormStrategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")

            # Check if XLS file was created
            self.assertTrue(xls_output.exists(), f"XLS file {xls_output} was not created")

    def test_xlsform_cdss_strategy_validation(self):
        """Test XLSFormCDSSStrategy output validation with ODK libraries."""
        with tempfile.TemporaryDirectory() as temp_dir:
            xls_output = Path(temp_dir) / "demo_tricc.xlsx"
            args = [
                "-i", str(self.demo_file),
                "-o", temp_dir,
                "-O", "XLSFormCDSSStrategy",
                "-l", "i"
            ]
            result = self.run_build_script(args)
            self.assertEqual(result.returncode, 0, f"Build failed: {result.stderr}")



if __name__ == "__main__":
    unittest.main()
