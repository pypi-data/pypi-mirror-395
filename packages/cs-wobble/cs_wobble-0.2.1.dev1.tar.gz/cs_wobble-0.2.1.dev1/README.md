# Wobble

Centralized testing package for Cracking Shells

## Installation

### From Source

```bash
git clone https://github.com/CrackingShells/Wobble.git
cd Wobble
pip install -e .
```

### From PyPI

```bash
pip install cs-wobble
```

## Quick Start

```bash
# Install wobble
pip install -e .

# Run all tests
wobble

# Run specific test categories
wobble --category regression
wobble --category integration

# Save results to file
wobble --log-file test_results.json

# CI/CD integration with file output
wobble --format json --log-file ci_results.json --log-verbosity 3

# Enhanced test discovery
wobble --discover-only                    # Show test counts by category
wobble --discover-only --discover-verbosity 2  # Show uncategorized test details
wobble --discover-only --discover-verbosity 3  # Show all tests with decorators

# Test execution with decorator display
wobble --verbose                          # Shows [@decorator_name] for each test

# Get help
wobble --help
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/CrackingShells/Wobble.git
cd Wobble

# Install in development mode
pip install -e .

# Install Node.js dependencies for semantic release
npm install
```

### Running Tests

```bash
# Run all tests with wobble
wobble

# Run tests by category
wobble --category regression

# Run with verbose output
wobble --verbose

# Alternative: use unittest directly
python -m unittest discover tests
```

### Enhanced Discovery Features

Wobble provides enhanced test discovery with multiple verbosity levels and decorator display:

```bash
# Discovery verbosity levels
wobble --discover-only --discover-verbosity 1  # Test counts by category (default)
wobble --discover-only --discover-verbosity 2  # + Uncategorized test details
wobble --discover-only --discover-verbosity 3  # + All tests with decorator info

# Test execution with decorator display
wobble --verbose                                # Shows [@decorator_name] for tests
wobble --category regression --verbose          # Regression tests with decorators
```

**Decorator Display Examples:**
- `[@regression_test]` - Regression test
- `[@integration_test]` - Integration test
- `[@slow_test]` - Slow-running test
- `[@regression_test, @slow_test]` - Multiple decorators

### Making Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) for automated versioning:

```bash
# Use commitizen for guided commits
npm run commit

# Or commit manually with conventional format
git commit -m "feat: add new feature"
git commit -m "fix: resolve issue with X"
git commit -m "docs: update README"
```

## Documentation

Complete documentation is available in the [docs/articles/](docs/articles/) directory:

- **[Getting Started](docs/articles/users/GettingStarted.md)** - Installation and basic usage
- **[CLI Reference](docs/articles/users/CLIReference.md)** - Complete command reference
- **[Test Organization](docs/articles/users/TestOrganization.md)** - Test categorization strategies
- **[Integration Guide](docs/articles/users/IntegrationGuide.md)** - Repository integration
- **[Architecture Overview](docs/articles/devs/architecture/Overview.md)** - System design
- **[Contributing Guidelines](docs/articles/devs/contribution_guidelines/Contributing.md)** - Development workflow

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/articles/devs/contribution_guidelines/Contributing.md) for details on:

- Development workflow
- Code style guidelines
- Testing requirements
- Pull request process

## License

This project is licensed under the GNU Affero General Public License v3 - see the [LICENSE](LICENSE) file for details.

## Links

- **Homepage**: https://github.com/CrackingShells/Wobble
- **Bug Reports**: https://github.com/CrackingShells/Wobble/issues
- **Documentation**: [docs/articles/](docs/articles/)
