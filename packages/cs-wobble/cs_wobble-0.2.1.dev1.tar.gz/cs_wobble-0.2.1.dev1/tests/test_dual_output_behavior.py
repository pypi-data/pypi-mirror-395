"""Test dual output behavior for enhanced discovery features.

Tests console vs file output independence as specified in the comprehensive
test definition report.
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_data_utils import WobbleTestBase


class TestDualOutputBehavior(WobbleTestBase):
    """Test console vs file output independence."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.test_suite_dir = self.test_data_loader.create_mixed_test_suite()
    
    def run_discovery_command(self, args: list) -> subprocess.CompletedProcess:
        """Run wobble discovery command with given arguments.

        Args:
            args: Command line arguments for wobble

        Returns:
            Completed process result
        """
        cmd = ['wobble'] + args + [str(self.test_suite_dir)]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        return result
    
    def test_dual_output_verbosity_independence(self):
        """Test that console and file verbosity are independent."""
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".txt")
        
        # Execute: Console verbosity 1, file verbosity 3
        result = self.run_discovery_command([
            '--discover-only',
            '--discover-verbosity', '1',
            '--log-file', temp_file,
            '--log-verbosity', '3'
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: Console output is minimal (level 1)
        self.assertIn("Total tests discovered:", result.stdout)
        self.assertNotIn("Complete Test Discovery Report", result.stdout)
        self.assertNotIn("::", result.stdout)
        
        # Verify: File output is detailed (level 3)
        file_content = self.read_file(temp_file)
        self.assertIn("Total tests discovered:", file_content)
        # Should contain detailed test listings for level 3
        self.assertIn("test_auth.py", file_content)
        self.assertIn("TestAuth", file_content)
    
    def test_dual_output_format_independence(self):
        """Test that console and file formats are independent."""
        # Create temporary JSON file for output
        temp_file = self.create_temp_file("", suffix=".json")
        
        # Execute: Console standard format, file JSON format
        result = self.run_discovery_command([
            '--discover-only',
            '--discover-verbosity', '2',
            '--log-file', temp_file,
            '--log-file-format', 'json',
            '--log-verbosity', '2'
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: Console output is standard text format
        self.assertIn("Total tests discovered:", result.stdout)
        self.assertIn("Uncategorized", result.stdout)
        
        # Verify: File output is valid JSON
        file_content = self.read_file(temp_file)
        json_data = self.assert_valid_json(file_content)  # Should not raise exception
        
        # Verify JSON structure matches specification
        self.assertIn('discovery_summary', json_data)
        summary = json_data['discovery_summary']
        self.assertIn('timestamp', summary)
        self.assertIn('total_tests', summary)
        self.assertIn('categories', summary)
    
    def test_console_only_output(self):
        """Test discovery output without file output."""
        # Execute: Console only
        result = self.run_discovery_command([
            '--discover-only',
            '--discover-verbosity', '2'
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: Console output is present
        self.assertIn("Total tests discovered:", result.stdout)
        self.assertIn("Uncategorized", result.stdout)
        
        # Verify: No file output created
        # (This is implicit - no file specified)
    
    def test_file_only_output_quiet_mode(self):
        """Test file output with quiet console mode."""
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".txt")
        
        # Execute: Quiet console, file output
        result = self.run_discovery_command([
            '--discover-only',
            '--discover-verbosity', '1',  # This affects console
            '--quiet',
            '--log-file', temp_file,
            '--log-verbosity', '2'  # This affects file
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: Console output is minimal due to quiet mode
        # (Quiet mode should suppress most console output)
        console_lines = [line for line in result.stdout.split('\n') if line.strip()]
        self.assertLessEqual(len(console_lines), 3, "Too much console output in quiet mode")
        
        # Verify: File output is present and detailed
        file_content = self.read_file(temp_file)
        self.assertIn("Total tests discovered:", file_content)
        self.assertGreater(len(file_content), 50, "File output too minimal")
    
    def test_different_verbosity_levels_same_format(self):
        """Test different verbosity levels with same format."""
        # Create temporary files for different verbosity levels
        temp_file_1 = self.create_temp_file("", suffix="_v1.txt")
        temp_file_2 = self.create_temp_file("", suffix="_v2.txt")
        temp_file_3 = self.create_temp_file("", suffix="_v3.txt")
        
        # Test verbosity level 1
        result1 = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file_1,
            '--log-verbosity', '1'
        ])
        self.assertEqual(result1.returncode, 0)
        
        # Test verbosity level 2
        result2 = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file_2,
            '--log-verbosity', '2'
        ])
        self.assertEqual(result2.returncode, 0)
        
        # Test verbosity level 3
        result3 = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file_3,
            '--log-verbosity', '3'
        ])
        self.assertEqual(result3.returncode, 0)
        
        # Verify: Different levels produce different amounts of detail
        content_1 = self.read_file(temp_file_1)
        content_2 = self.read_file(temp_file_2)
        content_3 = self.read_file(temp_file_3)
        
        # Level 1 should be shortest
        self.assertLess(len(content_1), len(content_2), "Level 1 should be less detailed than level 2")
        
        # Level 3 should be most detailed
        self.assertLessEqual(len(content_2), len(content_3), "Level 3 should be most detailed")
        
        # All should contain basic summary
        for content in [content_1, content_2, content_3]:
            self.assertIn("Total tests discovered:", content)
    
    def test_auto_format_detection(self):
        """Test automatic format detection based on file extension."""
        # Create temporary files with different extensions
        temp_txt = self.create_temp_file("", suffix=".txt")
        temp_json = self.create_temp_file("", suffix=".json")
        
        # Test .txt file with auto format
        result_txt = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_txt,
            '--log-file-format', 'auto',
            '--log-verbosity', '2'
        ])
        self.assertEqual(result_txt.returncode, 0)
        
        # Test .json file with auto format
        result_json = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_json,
            '--log-file-format', 'auto',
            '--log-verbosity', '2'
        ])
        self.assertEqual(result_json.returncode, 0)
        
        # Verify: .txt file contains text format
        txt_content = self.read_file(temp_txt)
        self.assertIn("Total tests discovered:", txt_content)
        # Should not be JSON
        with self.assertRaises(json.JSONDecodeError):
            json.loads(txt_content)
        
        # Verify: .json file contains valid JSON
        json_content = self.read_file(temp_json)
        json_data = self.assert_valid_json(json_content)
        self.assertIn('discovery_summary', json_data)


if __name__ == '__main__':
    unittest.main()
