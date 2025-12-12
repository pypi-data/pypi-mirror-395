"""Command replay utility for wobble test results.

This module provides functionality to replay test commands from
logged test results, enabling debugging and automation workflows.
"""

import json
import subprocess
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class CommandReplayError(Exception):
    """Exception raised when command replay fails."""
    pass


class TestResultParser:
    """Parser for wobble test result files."""
    
    def __init__(self, file_path: str):
        """Initialize the parser.
        
        Args:
            file_path: Path to the test result file
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Test result file not found: {file_path}")
    
    def parse_command(self) -> Optional[str]:
        """Parse the command from the test result file.
        
        Returns:
            The command string if found, None otherwise
        """
        if self.file_path.suffix.lower() == '.json':
            return self._parse_json_command()
        else:
            return self._parse_text_command()
    
    def _parse_json_command(self) -> Optional[str]:
        """Parse command from JSON test result file.
        
        Returns:
            The command string if found, None otherwise
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check for command in run_info
            if 'run_info' in data and 'summary' in data['run_info']:
                return data['run_info']['summary'].get('command')
            
            # Alternative structure
            if 'run_info' in data and 'command' in data['run_info']:
                return data['run_info']['command']
            
            return None
            
        except (json.JSONDecodeError, KeyError, IOError) as e:
            raise CommandReplayError(f"Failed to parse JSON file: {e}")
    
    def _parse_text_command(self) -> Optional[str]:
        """Parse command from text test result file.
        
        Returns:
            The command string if found, None otherwise
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for command patterns in text output
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                
                # Pattern: "Running: wobble ..."
                if line.startswith('Running: '):
                    return line[9:]  # Remove "Running: " prefix
                
                # Pattern: "Command: wobble ..."
                if line.startswith('Command: '):
                    return line[9:]  # Remove "Command: " prefix
            
            return None
            
        except IOError as e:
            raise CommandReplayError(f"Failed to read text file: {e}")
    
    def parse_test_results(self) -> Dict[str, Any]:
        """Parse test results from the file.
        
        Returns:
            Dictionary containing test results and metadata
        """
        if self.file_path.suffix.lower() == '.json':
            return self._parse_json_results()
        else:
            return self._parse_text_results()
    
    def _parse_json_results(self) -> Dict[str, Any]:
        """Parse test results from JSON file.
        
        Returns:
            Dictionary containing test results
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                'format': 'json',
                'run_info': data.get('run_info', {}),
                'test_results': data.get('test_results', []),
                'total_tests': len(data.get('test_results', [])),
                'file_path': str(self.file_path)
            }
            
        except (json.JSONDecodeError, IOError) as e:
            raise CommandReplayError(f"Failed to parse JSON results: {e}")
    
    def _parse_text_results(self) -> Dict[str, Any]:
        """Parse test results from text file.
        
        Returns:
            Dictionary containing basic test results info
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract basic statistics from text
            lines = content.split('\n')
            stats = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith('Total: '):
                    stats['total_tests'] = int(line.split(': ')[1])
                elif line.startswith('Passed: '):
                    stats['passed'] = int(line.split(': ')[1])
                elif line.startswith('Failed: '):
                    stats['failed'] = int(line.split(': ')[1])
                elif line.startswith('Errors: '):
                    stats['errors'] = int(line.split(': ')[1])
                elif line.startswith('Skipped: '):
                    stats['skipped'] = int(line.split(': ')[1])
            
            return {
                'format': 'text',
                'stats': stats,
                'content': content,
                'file_path': str(self.file_path)
            }
            
        except (IOError, ValueError) as e:
            raise CommandReplayError(f"Failed to parse text results: {e}")


class CommandReplayRunner:
    """Runner for replaying wobble test commands."""
    
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        """Initialize the replay runner.
        
        Args:
            dry_run: If True, only show what would be executed
            verbose: If True, show detailed output
        """
        self.dry_run = dry_run
        self.verbose = verbose
    
    def replay_command(self, command: str, working_dir: Optional[str] = None) -> Dict[str, Any]:
        """Replay a wobble test command.
        
        Args:
            command: The command to replay
            working_dir: Working directory for command execution
            
        Returns:
            Dictionary containing replay results
        """
        if self.verbose:
            print(f"Replaying command: {command}")
            if working_dir:
                print(f"Working directory: {working_dir}")
        
        if self.dry_run:
            return {
                'command': command,
                'dry_run': True,
                'working_dir': working_dir,
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Execute the command
            result = subprocess.run(
                command.split(),
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                'command': command,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'working_dir': working_dir,
                'timestamp': datetime.now().isoformat(),
                'success': result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            raise CommandReplayError(f"Command timed out: {command}")
        except subprocess.SubprocessError as e:
            raise CommandReplayError(f"Failed to execute command: {e}")
    
    def replay_from_file(self, file_path: str, working_dir: Optional[str] = None) -> Dict[str, Any]:
        """Replay command from a test result file.
        
        Args:
            file_path: Path to the test result file
            working_dir: Working directory for command execution
            
        Returns:
            Dictionary containing replay results
        """
        parser = TestResultParser(file_path)
        command = parser.parse_command()
        
        if not command:
            raise CommandReplayError(f"No command found in file: {file_path}")
        
        if self.verbose:
            print(f"Parsed command from {file_path}: {command}")
        
        # Parse original results for comparison
        original_results = parser.parse_test_results()
        
        # Replay the command
        replay_result = self.replay_command(command, working_dir)
        replay_result['original_file'] = file_path
        replay_result['original_results'] = original_results
        
        return replay_result
    
    def validate_replay_compatibility(self, command: str) -> List[str]:
        """Validate that a command can be safely replayed.
        
        Args:
            command: The command to validate
            
        Returns:
            List of validation warnings/issues
        """
        warnings = []
        
        # Check for potentially dangerous flags
        dangerous_flags = ['--log-overwrite', '--log-append']
        for flag in dangerous_flags:
            if flag in command:
                warnings.append(f"Command contains {flag} which may overwrite files")
        
        # Check for file output flags
        if '--log-file' in command:
            warnings.append("Command contains file output which may create/overwrite files")
        
        # Check for path arguments
        if '--path' in command:
            warnings.append("Command specifies custom path - ensure it exists in replay environment")
        
        return warnings


def create_replay_parser() -> argparse.ArgumentParser:
    """Create argument parser for replay utility.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='Replay wobble test commands from result files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wobble-replay results.json                    # Replay command from JSON file
  wobble-replay results.txt --dry-run           # Show what would be executed
  wobble-replay results.json --working-dir /tmp # Execute in specific directory
  wobble-replay results.json --verbose          # Show detailed output
        """
    )
    
    parser.add_argument(
        'file',
        help='Test result file to replay command from'
    )
    
    parser.add_argument(
        '--working-dir',
        help='Working directory for command execution'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be executed without running'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate command compatibility without executing'
    )
    
    return parser


def main() -> int:
    """Main entry point for replay utility.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = create_replay_parser()
    args = parser.parse_args()
    
    try:
        # Parse the command from file
        result_parser = TestResultParser(args.file)
        command = result_parser.parse_command()
        
        if not command:
            print(f"Error: No command found in file: {args.file}", file=sys.stderr)
            return 1
        
        # Validate command
        runner = CommandReplayRunner(dry_run=args.dry_run, verbose=args.verbose)
        warnings = runner.validate_replay_compatibility(command)
        
        if warnings:
            print("Validation warnings:")
            for warning in warnings:
                print(f"  - {warning}")
            print()
        
        if args.validate_only:
            print(f"Command: {command}")
            print("Validation complete.")
            return 0
        
        # Replay the command (avoid re-parsing file by passing parsed data)
        if args.dry_run:
            # For dry run, we don't need to re-parse the file
            result = {
                'dry_run': True,
                'command': command,
                'working_dir': args.working_dir,
                'timestamp': time.time()
            }
        else:
            result = runner.replay_from_file(args.file, args.working_dir)
        
        if args.dry_run:
            print(f"Would execute: {result['command']}")
            if result.get('working_dir'):
                print(f"In directory: {result['working_dir']}")
            return 0
        
        # Show results
        if result['success']:
            print(f"Command executed successfully (exit code: {result['return_code']})")
            if args.verbose and result['stdout']:
                print("STDOUT:")
                print(result['stdout'])
        else:
            print(f"Command failed (exit code: {result['return_code']})", file=sys.stderr)
            if result['stderr']:
                print("STDERR:", file=sys.stderr)
                print(result['stderr'], file=sys.stderr)
            return result['return_code']
        
        return 0
        
    except CommandReplayError as e:
        print(f"Replay error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Replay interrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
