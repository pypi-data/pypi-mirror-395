"""Tests for command replay functionality.

This module tests the command reconstruction and replay utilities
for wobble test results.
"""

import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add the parent directory to the path for imports during testing
sys.path.insert(0, str(Path(__file__).parent.parent))

from wobble.replay import (
    TestResultParser, CommandReplayRunner, CommandReplayError,
    create_replay_parser, main
)
from wobble.cli import reconstruct_command, create_parser


class TestCommandReconstruction(unittest.TestCase):
    """Test command reconstruction functionality."""
    
    def test_basic_command_reconstruction(self):
        """Test basic command reconstruction."""
        parser = create_parser()
        args = parser.parse_args(['tests/'])
        
        command = reconstruct_command(args)
        self.assertEqual(command, 'wobble')  # Default path is not included
    
    def test_command_reconstruction_with_options(self):
        """Test command reconstruction with various options."""
        parser = create_parser()
        args = parser.parse_args([
            '--path', '/custom/path',
            '--category', 'integration',
            '--format', 'json',
            '--verbose', '--verbose',
            '--exclude-slow',
            '--no-color'
        ])
        
        command = reconstruct_command(args)
        expected_parts = [
            'wobble',
            '--path', '/custom/path',
            '--category', 'integration',
            '--format', 'json',
            '--exclude-slow',
            '--no-color',
            '-v', '-v'
        ]
        
        for part in expected_parts:
            self.assertIn(part, command)
    
    def test_command_reconstruction_with_file_output(self):
        """Test command reconstruction with file output options."""
        parser = create_parser()
        args = parser.parse_args([
            '--log-file', 'test_output.json',
            '--log-file-format', 'json',
            '--log-verbosity', '2',
            '--log-append'
        ])
        
        command = reconstruct_command(args)
        
        self.assertIn('--log-file test_output.json', command)
        self.assertIn('--log-file-format json', command)
        self.assertIn('--log-verbosity 2', command)
        self.assertIn('--log-append', command)
    
    def test_command_reconstruction_auto_timestamped(self):
        """Test command reconstruction with auto-timestamped file."""
        parser = create_parser()
        args = parser.parse_args(['--log-file'])
        
        command = reconstruct_command(args)
        self.assertIn('--log-file', command)
        # Should not include a filename for auto-timestamped


class TestTestResultParser(unittest.TestCase):
    """Test TestResultParser functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.json_file = Path(self.temp_dir) / 'test_results.json'
        self.text_file = Path(self.temp_dir) / 'test_results.txt'
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_parser_creation_with_existing_file(self):
        """Test parser creation with existing file."""
        self.json_file.write_text('{}')
        parser = TestResultParser(str(self.json_file))
        self.assertEqual(parser.file_path, self.json_file)
    
    def test_parser_creation_with_nonexistent_file(self):
        """Test parser creation with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            TestResultParser(str(self.json_file))
    
    def test_parse_json_command(self):
        """Test parsing command from JSON file."""
        test_data = {
            'run_info': {
                'summary': {
                    'command': 'wobble tests/ --verbose'
                }
            },
            'test_results': []
        }
        
        self.json_file.write_text(json.dumps(test_data))
        parser = TestResultParser(str(self.json_file))
        
        command = parser.parse_command()
        self.assertEqual(command, 'wobble tests/ --verbose')
    
    def test_parse_json_command_alternative_structure(self):
        """Test parsing command from JSON with alternative structure."""
        test_data = {
            'run_info': {
                'command': 'wobble tests/ --format json'
            },
            'test_results': []
        }
        
        self.json_file.write_text(json.dumps(test_data))
        parser = TestResultParser(str(self.json_file))
        
        command = parser.parse_command()
        self.assertEqual(command, 'wobble tests/ --format json')
    
    def test_parse_json_command_not_found(self):
        """Test parsing command from JSON when not found."""
        test_data = {
            'test_results': []
        }
        
        self.json_file.write_text(json.dumps(test_data))
        parser = TestResultParser(str(self.json_file))
        
        command = parser.parse_command()
        self.assertIsNone(command)
    
    def test_parse_text_command_running_pattern(self):
        """Test parsing command from text file with 'Running:' pattern."""
        text_content = """
=== Wobble Test Run ===
Running: wobble tests/ --verbose
Started: 2024-01-15 14:30:00

✓ TestClass.test_example (0.123s)

=== Summary ===
Total: 1
Passed: 1
        """
        
        self.text_file.write_text(text_content, encoding='utf-8')
        parser = TestResultParser(str(self.text_file))
        
        command = parser.parse_command()
        self.assertEqual(command, 'wobble tests/ --verbose')
    
    def test_parse_text_command_command_pattern(self):
        """Test parsing command from text file with 'Command:' pattern."""
        text_content = """
=== Detailed Test Run Summary ===
Command: wobble tests/ --format verbose
Start Time: 2024-01-15T14:30:25

Test: TestClass.test_example
Status: PASS
        """
        
        self.text_file.write_text(text_content)
        parser = TestResultParser(str(self.text_file))
        
        command = parser.parse_command()
        self.assertEqual(command, 'wobble tests/ --format verbose')
    
    def test_parse_text_command_not_found(self):
        """Test parsing command from text when not found."""
        text_content = """
Some test output without command information.
        """
        
        self.text_file.write_text(text_content)
        parser = TestResultParser(str(self.text_file))
        
        command = parser.parse_command()
        self.assertIsNone(command)
    
    def test_parse_json_results(self):
        """Test parsing test results from JSON file."""
        test_data = {
            'run_info': {
                'summary': {
                    'total_tests': 2,
                    'passed': 1,
                    'failed': 1
                }
            },
            'test_results': [
                {'name': 'test_pass', 'status': 'PASS'},
                {'name': 'test_fail', 'status': 'FAIL'}
            ]
        }
        
        self.json_file.write_text(json.dumps(test_data))
        parser = TestResultParser(str(self.json_file))
        
        results = parser.parse_test_results()
        
        self.assertEqual(results['format'], 'json')
        self.assertEqual(results['total_tests'], 2)
        self.assertEqual(len(results['test_results']), 2)
    
    def test_parse_text_results(self):
        """Test parsing test results from text file."""
        text_content = """
=== Test Run Summary ===
Total: 5
Passed: 3
Failed: 1
Errors: 1
Skipped: 0
        """
        
        self.text_file.write_text(text_content)
        parser = TestResultParser(str(self.text_file))
        
        results = parser.parse_test_results()
        
        self.assertEqual(results['format'], 'text')
        self.assertEqual(results['stats']['total_tests'], 5)
        self.assertEqual(results['stats']['passed'], 3)
        self.assertEqual(results['stats']['failed'], 1)


class TestCommandReplayRunner(unittest.TestCase):
    """Test CommandReplayRunner functionality."""
    
    def test_runner_creation(self):
        """Test runner creation with options."""
        runner = CommandReplayRunner(dry_run=True, verbose=True)
        self.assertTrue(runner.dry_run)
        self.assertTrue(runner.verbose)
    
    def test_dry_run_replay(self):
        """Test dry run command replay."""
        runner = CommandReplayRunner(dry_run=True)
        
        result = runner.replay_command('wobble tests/')
        
        self.assertTrue(result['dry_run'])
        self.assertEqual(result['command'], 'wobble tests/')
        self.assertIn('timestamp', result)
    
    @patch('subprocess.run')
    def test_actual_command_replay(self, mock_run):
        """Test actual command replay."""
        # Mock successful subprocess execution
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'Test output'
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        runner = CommandReplayRunner(dry_run=False)
        result = runner.replay_command('wobble tests/')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['return_code'], 0)
        self.assertEqual(result['stdout'], 'Test output')
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_failed_command_replay(self, mock_run):
        """Test failed command replay."""
        # Mock failed subprocess execution
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ''
        mock_result.stderr = 'Error message'
        mock_run.return_value = mock_result
        
        runner = CommandReplayRunner(dry_run=False)
        result = runner.replay_command('wobble tests/')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['return_code'], 1)
        self.assertEqual(result['stderr'], 'Error message')
    
    def test_replay_from_file(self):
        """Test replaying command from file."""
        temp_dir = tempfile.mkdtemp()
        json_file = Path(temp_dir) / 'test_results.json'
        
        try:
            test_data = {
                'run_info': {
                    'summary': {
                        'command': 'wobble tests/ --verbose'
                    }
                },
                'test_results': []
            }
            
            json_file.write_text(json.dumps(test_data))
            
            runner = CommandReplayRunner(dry_run=True)
            result = runner.replay_from_file(str(json_file))
            
            self.assertEqual(result['command'], 'wobble tests/ --verbose')
            self.assertEqual(result['original_file'], str(json_file))
            self.assertIn('original_results', result)
            
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_replay_from_file_no_command(self):
        """Test replaying from file with no command."""
        temp_dir = tempfile.mkdtemp()
        json_file = Path(temp_dir) / 'test_results.json'
        
        try:
            test_data = {'test_results': []}
            json_file.write_text(json.dumps(test_data))
            
            runner = CommandReplayRunner()
            
            with self.assertRaises(CommandReplayError):
                runner.replay_from_file(str(json_file))
                
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_validate_replay_compatibility(self):
        """Test command validation for replay compatibility."""
        runner = CommandReplayRunner()
        
        # Safe command
        warnings = runner.validate_replay_compatibility('wobble tests/')
        self.assertEqual(len(warnings), 0)
        
        # Command with file output
        warnings = runner.validate_replay_compatibility('wobble tests/ --log-file output.json')
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any('file output' in w for w in warnings))
        
        # Command with overwrite flag
        warnings = runner.validate_replay_compatibility('wobble tests/ --log-overwrite')
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any('overwrite' in w for w in warnings))


class TestReplayUtilityMain(unittest.TestCase):
    """Test replay utility main function."""
    
    def test_create_replay_parser(self):
        """Test replay argument parser creation."""
        parser = create_replay_parser()
        
        # Test basic parsing
        args = parser.parse_args(['test_results.json'])
        self.assertEqual(args.file, 'test_results.json')
        self.assertFalse(args.dry_run)
        self.assertFalse(args.verbose)
        
        # Test with options
        args = parser.parse_args([
            'test_results.json',
            '--dry-run',
            '--verbose',
            '--working-dir', '/tmp',
            '--validate-only'
        ])
        self.assertTrue(args.dry_run)
        self.assertTrue(args.verbose)
        self.assertEqual(args.working_dir, '/tmp')
        self.assertTrue(args.validate_only)
    
    @patch('wobble.replay.TestResultParser')
    def test_main_with_valid_file(self, mock_parser_class):
        """Test main function with valid file."""
        # Mock parser
        mock_parser = MagicMock()
        mock_parser.parse_command.return_value = 'wobble tests/'
        mock_parser_class.return_value = mock_parser
        
        # Test dry run
        with patch('sys.argv', ['wobble-replay', 'test_results.json', '--dry-run']):
            exit_code = main()
        
        self.assertEqual(exit_code, 0)
        mock_parser_class.assert_called_once_with('test_results.json')
    
    @patch('wobble.replay.TestResultParser')
    def test_main_with_no_command(self, mock_parser_class):
        """Test main function when no command found."""
        # Mock parser with no command
        mock_parser = MagicMock()
        mock_parser.parse_command.return_value = None
        mock_parser_class.return_value = mock_parser
        
        with patch('sys.argv', ['wobble-replay', 'test_results.json']):
            exit_code = main()
        
        self.assertEqual(exit_code, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
