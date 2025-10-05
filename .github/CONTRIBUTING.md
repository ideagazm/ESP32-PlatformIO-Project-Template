# Contributing to ESP32 PlatformIO Project Template

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** from `main`
4. **Make your changes** following our guidelines
5. **Test thoroughly** on your target platform
6. **Submit a pull request** with a clear description

## 📋 Development Setup

### Prerequisites
- Python 3.13 or higher (recommended for compatibility with CI/CD)
- Git
- ESP32 development board (for hardware testing)
- Windows, Linux, or macOS

### Environment Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ESP32-PlatformIO-Project-Template.git
cd ESP32-PlatformIO-Project-Template

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Run setup
.\build.ps1 setup  # Windows
python scripts/setup.py  # Cross-platform

# Verify installation
.\build.ps1 status
```

## 🎯 Contribution Guidelines

### Code Style

#### Python Code
- Follow PEP 8 style guidelines
- Use `black` for code formatting: `black scripts/`
- Use `flake8` for linting: `flake8 scripts/ --max-line-length=100`
- Add type hints where appropriate
- Include docstrings for functions and classes

#### PowerShell Code
- Use consistent indentation (4 spaces)
- Follow PowerShell best practices
- Include help comments for functions
- Use descriptive variable names

#### C++ Code (ESP32)
- Follow Arduino/ESP32 coding conventions
- Use consistent indentation (2 or 4 spaces)
- Include header comments
- Use meaningful variable and function names

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no functional changes)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes
- `perf`: Performance improvements
- `build`: Build system changes

**Examples:**
```
feat(wifi): add WPA3 support to configuration generator
fix(monitor): resolve serial port connection timeout
docs(readme): update installation instructions
```

### Branch Naming
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

## 🧪 Testing Requirements

### Before Submitting
1. **Run all builds**: `.\build.ps1 build` for all environments
2. **Test scripts**: Verify all Python scripts work correctly
3. **Check formatting**: Run `black` and `flake8` on Python code
4. **Validate documentation**: Ensure README and docs are updated
5. **Cross-platform testing**: Test on Windows/Linux if possible

### Test Categories

#### Unit Tests
- Test individual script functions
- Mock hardware dependencies where needed
- Verify error handling

#### Integration Tests
- Test complete workflows
- Verify script interactions
- Test with real ESP32 hardware when possible

#### Platform Tests
- Windows PowerShell compatibility
- Linux/macOS bash compatibility
- Cross-platform Python script functionality

## 📁 Project Structure

```
├── .github/                 # GitHub workflows and templates
│   ├── workflows/          # CI/CD workflows
│   ├── ISSUE_TEMPLATE/     # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
├── scripts/                # Python automation scripts
├── src/                    # ESP32 source code
├── docs/                   # Documentation
├── build.ps1              # Main build script
├── platformio.ini         # PlatformIO configuration
└── README.md              # Main documentation
```

## 🔧 Adding New Features

### New Scripts
1. Create script in `scripts/` directory
2. Follow existing naming conventions
3. Add comprehensive error handling
4. Include help/usage information
5. Update `build.ps1` with new commands
6. Document in README.md

### New Build Commands
1. Add command to `build.ps1`
2. Update help text
3. Test on Windows PowerShell
4. Document usage and examples

### New Documentation
1. Use clear, concise language
2. Include code examples
3. Add troubleshooting sections
4. Update table of contents if needed

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and logs
- ESP32 board type if relevant

Use the bug report template in GitHub Issues.

## 💡 Feature Requests

For new features, please:
- Describe the use case and problem it solves
- Provide implementation suggestions if possible
- Consider backward compatibility
- Discuss potential breaking changes

Use the feature request template in GitHub Issues.

## 📖 Documentation

### Writing Guidelines
- Use clear, simple language
- Include practical examples
- Add troubleshooting information
- Keep formatting consistent
- Update table of contents

### Documentation Types
- **README.md**: Main project documentation
- **Code comments**: Inline documentation
- **Script help**: Built-in help text
- **Guides**: Step-by-step tutorials in `docs/`

## 🔄 Pull Request Process

### Before Submitting
1. **Rebase** your branch on latest `main`
2. **Squash** related commits if appropriate
3. **Test** thoroughly on your platform
4. **Update** documentation
5. **Fill out** PR template completely

### Review Process
1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Testing** on multiple platforms if needed
4. **Documentation review**
5. **Final approval** and merge

### PR Requirements
- Clear description of changes
- Link to related issues
- Test results and screenshots
- Updated documentation
- Backward compatibility consideration

## 🏷️ Release Process

### Versioning
We use [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### Release Workflow
1. Create release branch from `main`
2. Update version numbers
3. Update CHANGELOG.md
4. Create GitHub release
5. Automated workflows build and publish artifacts

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn
- Maintain professional communication

### Getting Help
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Request Comments**: Code-specific discussions

### Recognition
Contributors are recognized in:
- GitHub contributor graphs
- Release notes for significant contributions
- README acknowledgments for major features

## 📚 Resources

### ESP32 Development
- [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/)
- [PlatformIO Documentation](https://docs.platformio.org/)
- [Arduino ESP32 Core](https://github.com/espressif/arduino-esp32)

### Tools and Standards
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Python PEP 8](https://pep8.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 📞 Contact

For questions about contributing:
- Open a GitHub Issue for technical questions
- Use GitHub Discussions for general questions
- Check existing issues and documentation first

Thank you for contributing to make this project better! 🎉