# Contributing to PatternForge

Thank you for your interest in contributing to PatternForge! 🎉

This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/patternforge.git
   cd patternforge
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/idrissbado/patternforge.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Verify installation:
   ```bash
   python -c "import patternforge; print(patternforge.__version__)"
   ```

## How to Contribute

### Reporting Bugs

- **Check existing issues** to avoid duplicates
- Use the bug report template
- Include:
  - Python version
  - PatternForge version
  - Operating system
  - Minimal reproducible example
  - Expected vs. actual behavior

### Suggesting Enhancements

- Use the feature request template
- Clearly describe the problem and proposed solution
- Provide examples and use cases

### Code Contributions

1. **Find or create an issue** describing the change
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** with clear commit messages
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Push to your fork** and submit a pull request

## Coding Standards

### Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for code formatting:
  ```bash
  black src/ tests/
  ```
- Use type hints where appropriate
- Maximum line length: 100 characters

### Documentation

- Write clear docstrings (NumPy style):
  ```python
  def function_name(param1: int, param2: str) -> bool:
      """
      Brief description.
      
      Longer description if needed.
      
      Parameters
      ----------
      param1 : int
          Description of param1
      param2 : str
          Description of param2
      
      Returns
      -------
      bool
          Description of return value
      """
  ```

- Add inline comments for complex logic
- Update README.md for user-facing changes

### Naming Conventions

- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=patternforge tests/

# Run specific test file
pytest tests/test_core.py
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files: `test_*.py`
- Name test functions: `test_*`
- Use fixtures for common setup
- Aim for high coverage (>80%)

Example:
```python
import pytest
from patternforge import PatternForge

def test_feature():
    pf = PatternForge()
    result = pf.analyze(data)
    assert result is not None
```

## Documentation

### Building Documentation

```bash
cd docs/
make html
```

View in browser: `docs/_build/html/index.html`

### Adding Examples

- Place examples in `examples/` directory
- Include clear comments and expected output
- Keep examples simple and focused

## Pull Request Process

1. **Update your branch** with latest upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Ensure all tests pass**:
   ```bash
   pytest tests/
   ```

3. **Format code**:
   ```bash
   black src/ tests/
   ```

4. **Update CHANGELOG.md** (if applicable)

5. **Submit pull request**:
   - Use clear, descriptive title
   - Reference related issues
   - Describe changes and motivation
   - Include screenshots for UI changes

6. **Address review feedback** promptly

### PR Review Criteria

- Code quality and style
- Test coverage
- Documentation updates
- Breaking changes clearly noted
- Commit message clarity

## Project Structure

```
patternforge/
├── src/patternforge/       # Source code
│   ├── analysis/           # Analysis engines
│   ├── loaders/           # Data loaders
│   ├── reporting/         # Reporting modules
│   └── utils/             # Utilities
├── tests/                 # Test suite
├── examples/              # Usage examples
├── docs/                  # Documentation
└── setup.py              # Package setup
```

## Questions?

- Open a discussion on GitHub
- Email: idrissbadoolivier@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to PatternForge!** 🚀
