"""Test file format compliance for enhanced discovery features.

Tests text and JSON format validation as specified in the comprehensive
test definition report.
"""

import json
import os
import subprocess
import unittest
from pathlib import Path

from tests.test_data_utils import WobbleTestBase


class TestFileFormatCompliance(WobbleTestBase):
    """Test file format compliance for discovery output."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.test_suite_dir = self.test_data_loader.create_comprehensive_test_suite()
    
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
    
    def test_text_format_basic_structure(self):
        """Test basic text format structure compliance."""
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".txt")
        
        # Execute: Generate text format output
        result = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file,
            '--log-file-format', 'txt',
            '--log-verbosity', '1'
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: Text format matches specification
        file_content = self.read_file(temp_file)
        
        # Check basic content presence
        self.assertIn("Total tests discovered:", file_content)
        self.assertRegex(file_content, r"Total tests discovered: \d+")
        
        # Should contain category information
        self.assertIn("Regression:", file_content)
        self.assertIn("Uncategorized:", file_content)
    
    def test_text_format_detailed_structure(self):
        """Test detailed text format structure compliance."""
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".txt")
        
        # Execute: Generate detailed text format output
        result = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file,
            '--log-file-format', 'txt',
            '--log-verbosity', '3'
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: Detailed text format
        file_content = self.read_file(temp_file)
        
        # Check complete listing format
        self.assertIn("Total tests discovered:", file_content)
        
        # Should contain test details for level 3
        self.assertIn("test_", file_content)  # Should have test file references
        
        # Verify proper structure
        lines = file_content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        self.assertGreater(len(non_empty_lines), 5, "Should have substantial content")
    
    def test_json_format_schema_compliance(self):
        """Test JSON format compliance with defined schema."""
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".json")
        
        # Execute: Generate JSON format output
        result = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file,
            '--log-file-format', 'json',
            '--log-verbosity', '3'
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: File output is valid JSON
        file_content = self.read_file(temp_file)
        json_data = self.assert_valid_json(file_content)
        
        # Verify: JSON structure matches specification from section 1.3
        self.assertIn('discovery_summary', json_data)
        summary = json_data['discovery_summary']
        
        # Required top-level fields
        required_fields = ['timestamp', 'total_tests', 'categories']
        for field in required_fields:
            self.assertIn(field, summary, f"Missing required field: {field}")
        
        # Verify data types
        self.assertIsInstance(summary['total_tests'], int)
        self.assertIsInstance(summary['categories'], dict)
        self.assertIsInstance(summary['timestamp'], str)
        
        # Verify categories structure
        categories = summary['categories']
        for category_name, count in categories.items():
            self.assertIsInstance(category_name, str)
            self.assertIsInstance(count, int)
    
    def test_json_format_level_2_structure(self):
        """Test JSON format level 2 structure with uncategorized tests."""
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".json")
        
        # Execute: Generate JSON format output level 2
        result = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file,
            '--log-file-format', 'json',
            '--log-verbosity', '2'
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: File output is valid JSON
        file_content = self.read_file(temp_file)
        json_data = self.assert_valid_json(file_content)
        
        # Verify: Level 2 specific structure
        summary = json_data['discovery_summary']
        
        # Should have uncategorized tests for level 2 (but not tests_by_category)
        if summary['categories'].get('uncategorized', 0) > 0:
            self.assertIn('uncategorized', summary)
            uncategorized = summary['uncategorized']
            self.assertIsInstance(uncategorized, list)

            # Verify test structure
            for test in uncategorized:
                self.assertIsInstance(test, dict)
                # Should have basic test information
                self.assertIn('name', test)

        # Level 2 should NOT have tests_by_category (that's level 3 only)
        self.assertNotIn('tests_by_category', summary)
    
    def test_json_format_level_3_structure(self):
        """Test JSON format level 3 structure with all test details."""
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".json")
        
        # Execute: Generate JSON format output level 3
        result = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file,
            '--log-file-format', 'json',
            '--log-verbosity', '3'
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: File output is valid JSON
        file_content = self.read_file(temp_file)
        json_data = self.assert_valid_json(file_content)
        
        # Verify: Level 3 specific structure
        summary = json_data['discovery_summary']
        
        # Should have tests_by_category for level 3
        self.assertIn('tests_by_category', summary)
        tests_by_category = summary['tests_by_category']
        self.assertIsInstance(tests_by_category, dict)

        # Level 3 should NOT have duplicate uncategorized field at root level
        self.assertNotIn('uncategorized', summary)

        # Verify test structure in categories
        for category, tests in tests_by_category.items():
            self.assertIsInstance(tests, list)
            for test in tests:
                self.assertIsInstance(test, dict)
                # Required test fields as per specification
                required_test_fields = ['name', 'class', 'module', 'file']
                for field in required_test_fields:
                    self.assertIn(field, test, f"Missing test field: {field}")

                # Level 3 tests should have decorators field
                self.assertIn('decorators', test)
                self.assertIsInstance(test['decorators'], list)
    
    def test_json_format_unicode_handling(self):
        """Test JSON format handling of unicode characters."""
        # Create test suite with unicode
        unicode_suite_dir = self.test_data_loader.create_unicode_test_suite()
        
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".json")
        
        # Execute: Generate JSON output with unicode tests
        cmd = ['wobble'] + [
            '--discover-only',
            '--log-file', temp_file,
            '--log-file-format', 'json',
            '--log-verbosity', '3',
            str(unicode_suite_dir)
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: File output is valid JSON with unicode
        file_content = self.read_file(temp_file)
        json_data = self.assert_valid_json(file_content)
        
        # Verify: Unicode characters are properly encoded
        json_str = json.dumps(json_data, ensure_ascii=False)
        self.assertIn('ñ', json_str)  # Should contain unicode character
        
        # Verify: JSON can be re-parsed (round-trip test)
        reparsed = json.loads(json_str)
        self.assertEqual(json_data, reparsed)

    def test_json_structure_regression_protection(self):
        """Comprehensive regression test to prevent JSON structure changes."""
        # Test all verbosity levels to ensure consistent structure
        for verbosity in [1, 2, 3]:
            with self.subTest(verbosity=verbosity):
                temp_file = self.create_temp_file("", suffix=".json")

                # Execute: Generate JSON output
                result = self.run_discovery_command([
                    '--discover-only',
                    '--log-file', temp_file,
                    '--log-file-format', 'json',
                    '--log-verbosity', str(verbosity)
                ])

                self.assertEqual(result.returncode, 0, f"Command failed for verbosity {verbosity}: {result.stderr}")

                # Verify: Valid JSON structure
                file_content = self.read_file(temp_file)
                json_data = self.assert_valid_json(file_content)

                # Verify: Required root structure
                self.assertIn('discovery_summary', json_data)
                summary = json_data['discovery_summary']

                # Required fields for all verbosity levels
                required_fields = ['timestamp', 'total_tests', 'categories']
                for field in required_fields:
                    self.assertIn(field, summary, f"Missing required field '{field}' at verbosity {verbosity}")

                # Verify: No duplicate data structures
                if verbosity == 1:
                    # Level 1: Only basic fields
                    self.assertNotIn('uncategorized', summary)
                    self.assertNotIn('tests_by_category', summary)
                elif verbosity == 2:
                    # Level 2: Should have uncategorized but NOT tests_by_category
                    if summary['categories'].get('uncategorized', 0) > 0:
                        self.assertIn('uncategorized', summary)
                    self.assertNotIn('tests_by_category', summary)
                elif verbosity == 3:
                    # Level 3: Should have tests_by_category but NOT duplicate uncategorized
                    self.assertIn('tests_by_category', summary)
                    self.assertNotIn('uncategorized', summary)

                # Clean up
                os.unlink(temp_file)

    def test_json_field_naming_consistency(self):
        """Test that all category field names follow consistent naming conventions."""
        temp_file = self.create_temp_file("", suffix=".json")

        # Execute: Generate JSON output level 3 (most comprehensive)
        result = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file,
            '--log-file-format', 'json',
            '--log-verbosity', '3'
        ])

        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")

        # Verify: Valid JSON structure
        file_content = self.read_file(temp_file)
        json_data = self.assert_valid_json(file_content)

        summary = json_data['discovery_summary']

        # Verify: Consistent category naming in categories field
        categories = summary['categories']
        expected_categories = ['regression', 'integration', 'development', 'uncategorized']
        for category in expected_categories:
            if category in categories:
                # Category names should be consistent (no _tests suffix)
                self.assertNotIn(f'{category}_tests', categories,
                    f"Found inconsistent naming: '{category}_tests' should be '{category}'")

        # Verify: Consistent category naming in tests_by_category field
        if 'tests_by_category' in summary:
            tests_by_category = summary['tests_by_category']
            for category in tests_by_category.keys():
                # Category keys should be consistent (no _tests suffix)
                self.assertNotIn('_tests', category,
                    f"Found inconsistent category key: '{category}' should not contain '_tests'")

        # Clean up
        os.unlink(temp_file)

    def test_invalid_format_handling(self):
        """Test handling of invalid format specifications."""
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".txt")
        
        # Execute: Try invalid format
        result = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file,
            '--log-file-format', 'xml',  # Invalid format
            '--log-verbosity', '2'
        ])
        
        # Verify: Command should fail with invalid format
        self.assertNotEqual(result.returncode, 0, "Should fail with invalid format")
        self.assertIn("invalid choice: 'xml'", result.stderr)
    
    def test_file_creation_and_permissions(self):
        """Test file creation and permission handling."""
        # Create temporary file for output
        temp_file = self.create_temp_file("", suffix=".txt")
        
        # Execute: Generate output
        result = self.run_discovery_command([
            '--discover-only',
            '--log-file', temp_file,
            '--log-file-format', 'txt',
            '--log-verbosity', '1'
        ])
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        
        # Verify: File was created and is readable
        self.assertTrue(Path(temp_file).exists(), "Output file should exist")
        
        file_content = self.read_file(temp_file)
        self.assertGreater(len(file_content), 0, "File should not be empty")


if __name__ == '__main__':
    unittest.main()
