"""Command-line interface for wobble testing framework.

This module provides the main CLI entry point and argument parsing for the
wobble testing framework.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .discovery import TestDiscoveryEngine
from .runner import TestRunner
from .output import OutputFormatter


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for wobble CLI.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog='wobble',
        description='Centralized testing framework for Cracking Shells',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wobble                          # Run all tests
  wobble --category regression    # Run only regression tests
  wobble --exclude-slow          # Skip slow tests
  wobble --format json           # Output results in JSON format
  wobble --discover-only         # Only discover tests, don't run them
  wobble --discover-only --discover-verbosity 2  # Show uncategorized test details
  wobble --discover-only --discover-verbosity 3  # Show all tests with decorators
  wobble --verbose               # Run tests with decorator display
        """
    )
    
    # Test selection options
    parser.add_argument(
        '--category', '-c',
        choices=['regression', 'integration', 'development', 'all'],
        default='all',
        help='Test category to run (default: all)'
    )
    
    parser.add_argument(
        '--exclude-slow',
        action='store_true',
        help='Exclude slow-running tests'
    )
    
    parser.add_argument(
        '--exclude-ci',
        action='store_true',
        help='Exclude tests marked to skip in CI'
    )
    
    parser.add_argument(
        '--pattern', '-p',
        default='test*.py',
        help='File pattern for test discovery (default: test*.py)'
    )
    
    # Output options
    parser.add_argument(
        '--format', '-f',
        choices=['standard', 'verbose', 'json', 'minimal'],
        default='standard',
        help='Output format (default: standard)'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    # Discovery options
    parser.add_argument(
        '--discover-only',
        action='store_true',
        help='Only discover tests, do not run them'
    )

    parser.add_argument(
        '--discover-verbosity',
        type=int,
        choices=[1, 2, 3],
        default=1,
        help='Discovery output verbosity (1=counts only, 2=uncategorized details, 3=all details)'
    )

    parser.add_argument(
        '--list-categories',
        action='store_true',
        help='List available test categories and exit'
    )
    
    # Repository options
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to repository root (default: current directory)'
    )

    parser.add_argument(
        '--path',
        type=str,
        dest='path_option',
        help='Alternative way to specify path to repository root'
    )
    
    # Verbosity options
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0,
        help='Increase verbosity (can be used multiple times)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress all output except errors'
    )

    # File output options
    file_group = parser.add_argument_group('File Output Options')

    file_group.add_argument(
        '--log-file',
        nargs='?',
        const='',  # Empty string when flag used without argument
        help='Enable file output with optional filename (auto-timestamped if not specified)'
    )

    file_group.add_argument(
        '--log-file-format',
        choices=['txt', 'json', 'auto'],
        default='auto',
        help='File output format (default: auto-detect from extension)'
    )

    file_group.add_argument(
        '--log-verbosity',
        type=int,
        choices=[1, 2, 3],
        default=1,
        help='File output verbosity level (1=Standard, 2=Detailed, 3=Complete)'
    )

    file_group.add_argument(
        '--log-append',
        action='store_true',
        help='Append to existing file instead of overwriting'
    )

    file_group.add_argument(
        '--log-overwrite',
        action='store_true',
        help='Force overwrite existing file (default behavior)'
    )

    return parser


def detect_repository_root(start_path: str = ".") -> Optional[Path]:
    """Detect the repository root directory.
    
    Args:
        start_path: Starting path for detection
        
    Returns:
        Path to repository root, or None if not found
    """
    current = Path(start_path).resolve()
    
    # Look for common repository indicators
    indicators = [
        '.git',
        'pyproject.toml',
        'setup.py',
        'requirements.txt',
        'Pipfile',
        'package.json'
    ]
    
    while current != current.parent:
        for indicator in indicators:
            if (current / indicator).exists():
                return current
        current = current.parent
    
    return None


def process_file_output_args(args: argparse.Namespace) -> List[Dict[str, Any]]:
    """Process file output arguments into configuration objects.

    Args:
        args: Parsed command line arguments

    Returns:
        List of file output configuration dictionaries
    """
    file_configs = []

    if hasattr(args, 'log_file') and args.log_file is not None:
        # Generate filename if not provided
        if args.log_file == '':
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = "json" if args.log_file_format == "json" else "txt"
            filename = f"wobble_results_{timestamp}.{extension}"
        else:
            filename = args.log_file

        # Auto-detect format from extension
        format_type = args.log_file_format
        if format_type == 'auto':
            extension = Path(filename).suffix.lower()
            format_type = 'json' if extension == '.json' else 'txt'

        # Handle append/overwrite logic
        append_mode = False
        if hasattr(args, 'log_append') and args.log_append:
            append_mode = True
        elif hasattr(args, 'log_overwrite') and args.log_overwrite:
            append_mode = False
        # Default is overwrite (append_mode = False)

        config = {
            'filename': filename,
            'format': format_type,
            'verbosity': getattr(args, 'log_verbosity', 1),
            'append': append_mode
        }

        file_configs.append(config)

    return file_configs


def reconstruct_command(args: argparse.Namespace) -> str:
    """Reconstruct the exact command line for logging purposes.

    Args:
        args: Parsed command line arguments

    Returns:
        Reconstructed command line string
    """
    command_parts = ['wobble']

    # Add path if not default
    # Use --path format if it was specified via --path option, otherwise use positional
    if hasattr(args, 'path_option') and args.path_option:
        command_parts.extend(['--path', args.path_option])
    elif args.path not in ['.', 'tests/', 'tests']:
        command_parts.append(args.path)

    # Add category if not default
    if args.category != 'all':
        command_parts.extend(['--category', args.category])

    # Add format if not default
    if args.format != 'standard':
        command_parts.extend(['--format', args.format])

    # Add pattern if not default
    if args.pattern != 'test*.py':
        command_parts.extend(['--pattern', args.pattern])

    # Add boolean flags
    if args.exclude_slow:
        command_parts.append('--exclude-slow')
    if args.exclude_ci:
        command_parts.append('--exclude-ci')
    if args.no_color:
        command_parts.append('--no-color')
    if args.discover_only:
        command_parts.append('--discover-only')
        if args.discover_verbosity != 1:  # Only add if not default
            command_parts.append(f'--discover-verbosity {args.discover_verbosity}')
    if args.list_categories:
        command_parts.append('--list-categories')
    if args.quiet:
        command_parts.append('--quiet')

    # Add verbosity
    if args.verbose > 0:
        command_parts.extend(['-v'] * args.verbose)

    # Add file output arguments
    if hasattr(args, 'log_file') and args.log_file is not None:
        if args.log_file == '':
            command_parts.append('--log-file')
        else:
            command_parts.extend(['--log-file', args.log_file])

        if hasattr(args, 'log_file_format') and args.log_file_format != 'auto':
            command_parts.extend(['--log-file-format', args.log_file_format])

        if hasattr(args, 'log_verbosity') and args.log_verbosity != 1:
            command_parts.extend(['--log-verbosity', str(args.log_verbosity)])

        if hasattr(args, 'log_append') and args.log_append:
            command_parts.append('--log-append')

        if hasattr(args, 'log_overwrite') and args.log_overwrite:
            command_parts.append('--log-overwrite')

    return ' '.join(command_parts)


def main() -> int:
    """Main entry point for wobble CLI.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Resolve path from positional or optional argument
    if hasattr(args, 'path_option') and args.path_option:
        args.path = args.path_option

    # Detect repository root if not explicitly provided
    if args.path == '.':
        repo_root = detect_repository_root()
        if repo_root:
            args.path = str(repo_root)
    
    # Validate path
    if not Path(args.path).exists():
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        return 1
    
    # Process file output configuration
    file_configs = process_file_output_args(args)

    # Initialize components
    discovery_engine = TestDiscoveryEngine(args.path)

    # Use EnhancedOutputFormatter if file outputs are configured
    if file_configs:
        from .enhanced_output import EnhancedOutputFormatter
        output_formatter = EnhancedOutputFormatter(
            format_type=args.format,
            use_color=not args.no_color,
            verbosity=args.verbose,
            quiet=args.quiet,
            file_outputs=file_configs
        )
    else:
        output_formatter = OutputFormatter(
            format_type=args.format,
            use_color=not args.no_color,
            verbosity=args.verbose,
            quiet=args.quiet
        )
    
    try:
        # Discover tests
        if args.verbose > 0:
            output_formatter.print_info(f"Discovering tests in: {args.path}")
        
        discovered_tests = discovery_engine.discover_tests(pattern=args.pattern)
        
        # Handle list categories option
        if args.list_categories:
            output_formatter.print_test_categories(discovered_tests)
            return 0
        
        # Handle discover-only option
        if args.discover_only:
            # Get discovery data for console output (uses --discover-verbosity)
            discovery_output = discovery_engine.get_discovery_output(verbosity=args.discover_verbosity)

            # If file outputs are configured, use enhanced formatter for file integration
            if file_configs:
                # Get discovery data for file output (uses --log-verbosity)
                file_discovery_data = discovery_engine.get_discovery_data(verbosity=args.log_verbosity)
                # Use enhanced formatter to handle both console and file output
                output_formatter.print_discovery_output(discovery_output, args.log_verbosity, file_discovery_data)
            else:
                # Console only output
                print(discovery_output)
            return 0
        
        # Filter tests based on arguments
        categories = None if args.category == 'all' else [args.category]
        filtered_tests = discovery_engine.filter_tests(
            categories=categories,
            exclude_slow=args.exclude_slow,
            exclude_ci=args.exclude_ci
        )
        
        if not filtered_tests:
            output_formatter.print_warning("No tests found matching the specified criteria")
            return 0
        
        # Run tests
        test_runner = TestRunner(output_formatter)
        results = test_runner.run_tests(filtered_tests)
        
        # Print results
        output_formatter.print_test_results(results)
        
        # Return appropriate exit code
        exit_code = 1 if (results.get('failures', 0) > 0 or results.get('errors', 0) > 0) else 0

        return exit_code

    except KeyboardInterrupt:
        output_formatter.print_error("Test execution interrupted by user")
        return 130

    except Exception as e:
        output_formatter.print_error(f"Unexpected error: {e}")
        if args.verbose > 1:
            import traceback
            traceback.print_exc()
        return 1

    finally:
        # Clean up enhanced output formatter if used
        if hasattr(output_formatter, 'close'):
            output_formatter.close()


def version() -> str:
    """Get wobble version string.
    
    Returns:
        Version string
    """
    try:
        from . import __version__
        return __version__
    except ImportError:
        return "unknown"


if __name__ == '__main__':
    sys.exit(main())
