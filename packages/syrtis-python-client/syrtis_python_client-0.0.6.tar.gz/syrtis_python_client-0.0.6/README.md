# syrtis-python-client

Version: 0.0.6

## Table of Contents

- [Status Compatibility](#status-compatibility)
- [Tests](#tests)
- [Roadmap](#roadmap)
- [Useful Links](#useful-links)
- [Suite Signature](#suite-signature)


## Status & Compatibility

**Maturity**: Production-ready

**Python Support**: >=3.10

**OS Support**: Linux, macOS, Windows

**Status**: Actively maintained

## Tests

This project uses `pytest` for testing and `pytest-cov` for code coverage analysis.

### Installation

First, install the required testing dependencies:
```bash
.venv/bin/python -m pip install pytest pytest-cov
```

### Basic Usage

Run all tests with coverage:
```bash
.venv/bin/python -m pytest --cov --cov-report=html
```

### Common Commands
```bash
# Run tests with coverage for a specific module
.venv/bin/python -m pytest --cov=your_module

# Show which lines are not covered
.venv/bin/python -m pytest --cov=your_module --cov-report=term-missing

# Generate an HTML coverage report
.venv/bin/python -m pytest --cov=your_module --cov-report=html

# Combine terminal and HTML reports
.venv/bin/python -m pytest --cov=your_module --cov-report=term-missing --cov-report=html

# Run specific test file with coverage
.venv/bin/python -m pytest tests/test_file.py --cov=your_module --cov-report=term-missing
```

### Viewing HTML Reports

After generating an HTML report, open `htmlcov/index.html` in your browser to view detailed line-by-line coverage information.

### Coverage Threshold

To enforce a minimum coverage percentage:
```bash
.venv/bin/python -m pytest --cov=your_module --cov-fail-under=80
```

This will cause the test suite to fail if coverage drops below 80%.

## Known Limitations & Roadmap

Current limitations and planned features are tracked in the GitHub issues.

See the [project roadmap](https://github.com/wexample/python-python_client/issues) for upcoming features and improvements.

## Useful Links

- **Homepage**: https://github.com/wexample/python-python-client
- **Documentation**: [docs.wexample.com](https://docs.wexample.com)
- **Issue Tracker**: https://github.com/wexample/python-python-client/issues
- **Discussions**: https://github.com/wexample/python-python-client/discussions
- **PyPI**: [pypi.org/project/syrtis-python-client](https://pypi.org/project/syrtis-python-client/)

# About us

[Syrtis AI](https://syrtis.ai) helps organizations turn artificial intelligence from an idea into reliable, measurable systems. We are a team of engineers and practitioners focused on implementing AI services inside real businesses — from strategy and architecture to deployment, integration, and long-term operations. Our goal is simple: deliver AI that works in production, fits your constraints, and earns its keep.

We build practical solutions that connect to existing tools, data, and processes, with an emphasis on security, performance, and governance. Whether it’s automating workflows, enhancing decision-making, or creating new product capabilities, Syrtis AI designs implementations that are maintainable, scalable, and aligned with business outcomes — not demos.

Syrtis AI promotes a culture of rigor and responsibility. Every delivery reflects a commitment to clear engineering, transparent communication, and trustworthy AI practices, so teams can adopt, operate, and evolve their AI services with confidence.

