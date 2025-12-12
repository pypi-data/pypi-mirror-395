# Trajectory SDK - Development Guide

This guide explains how to set up the Trajectory SDK for development with editable installs and proper configuration.

## 📦 Package Structure

```
sdk/
├── pyproject.toml          # Package configuration
├── src/
│   └── trajectory/         # Main module (imported as 'trajectory')
│       ├── __init__.py
│       ├── tracer/
│       ├── integrations/
│       └── ...
└── README_DEV.md          # This file
```

## 🔧 Development Setup

### 1. Install in Editable Mode

#### Using uv (Recommended)
```bash
# From the backend directory
cd /path/to/backend
uv add --editable ../sdk

# Or add to pyproject.toml manually
[tool.uv.sources]
trajectoryevals = { path = "../sdk", editable = true }
```

#### Using pip
```bash
# From the SDK directory
cd /path/to/sdk
pip install -e .

# Or from backend directory
pip install -e ../sdk
```

### 2. Verify Installation
```bash
# Test that package name and import name work correctly
python -c "from trajectory import Tracer; print('✅ Package: trajectoryevals, Import: trajectory - Works!')"
```

## ⚙️ Configuration

### Package Name vs Import Name

The SDK uses a **package alias** pattern:
- **Package name**: `trajectoryevals` (what you install)
- **Import name**: `trajectory` (what you import in code)

### pyproject.toml Configuration

```toml
[project]
name = "trajectoryevals"  # Package name for installation
version = "0.0.2"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/trajectory"]
include = [
    "/src/trajectory",
    "/src/trajectory/**/*.py",
]

# This is the key configuration for package aliasing
[tool.hatch.build.targets.wheel.package-dir]
"trajectory" = "src/trajectory"  # Maps import 'trajectory' to 'src/trajectory/'

[tool.hatch.build]
directory = "dist"
artifacts = ["src/trajectory/**/*.py"]
exclude = [
    "src/e2etests/*",
    "src/tests/*", 
    "src/demo/*"
]
```

### Backend pyproject.toml Configuration

```toml
[project]
dependencies = [
    # ... other dependencies
    "trajectoryevals>=0.0.2",  # Install as trajectoryevals
]

[tool.uv.sources]
trajectoryevals = { path = "../sdk", editable = true }  # Local editable install
```

## 🚫 Avoiding File Copying to Python Packages

### Problem
Without proper configuration, files get copied to the Python packages directory, making development difficult.

### Solution

#### 1. Use Editable Installs
```bash
# Always use editable mode for development
uv add --editable ../sdk
# or
pip install -e ../sdk
```

#### 2. Proper pyproject.toml Configuration
```toml
[tool.hatch.build.targets.wheel]
# Only include source files, not development files
packages = ["src/trajectory"]
include = [
    "/src/trajectory",
    "/src/trajectory/**/*.py",
]

# Exclude development files
exclude = [
    "src/e2etests/*",
    "src/tests/*",
    "src/demo/*",
    "*.md",
    "*.txt",
    ".git*",
    "__pycache__/*",
    "*.pyc",
    "*.pyo"
]
```

#### 3. Use .gitignore and .dockerignore
```gitignore
# .gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
```

## 🔄 Development Workflow

### 1. Make Changes
```bash
# Edit files in sdk/src/trajectory/
vim sdk/src/trajectory/tracer/core.py
```

### 2. Test Changes
```bash
# From backend directory
cd /path/to/backend
uv run python -c "from trajectory import Tracer; print('Changes reflected!')"
```

### 3. No Reinstallation Needed
With editable installs, changes are immediately available without reinstalling.

## 📦 Version Management

### Updating Package Version

The SDK includes a script to easily update the version number in `pyproject.toml`:

#### Using the Update Script
```bash
# From the SDK directory
cd /path/to/sdk

# Update to a specific version
python update_version.py 0.0.3

# Update to a new patch version
python update_version.py 0.1.0

# Update to a new minor version
python update_version.py 1.0.0
```

#### Manual Version Update
```bash
# Edit pyproject.toml directly
vim pyproject.toml
# Change: version = "0.0.2" to version = "0.0.3"
```

#### How the Update Script Works
- **Input**: Takes the new version as a command-line argument
- **Process**: Uses regex to find and replace the version line in `pyproject.toml`
- **Output**: Updates the file and provides confirmation
- **Format**: Preserves the existing formatting and structure

#### Example Output
```bash
$ python update_version.py 0.0.3
Successfully updated version to 0.0.3
```

#### Version Update Workflow
```bash
# 1. Update version
python update_version.py 0.0.3

# 2. Commit changes
git add pyproject.toml
git commit -m "Bump version to 0.0.3"

# 3. Push to trigger PyPI publish
git push origin main
```

### Version in CI/CD
The GitHub workflow automatically publishes to PyPI when you push to main. The version is read from `pyproject.toml`, so make sure to update it before pushing.

## 🎨 Code Formatting & Linting

### Ruff Configuration

The project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and formatting. Ruff is configured to focus on essential checks only.

### Basic Commands

```bash
# Check for linting issues
uv run ruff check src/

# Fix auto-fixable issues
uv run ruff check --fix src/

# Format code
uv run ruff format src/

# Check and format together
uv run ruff check --fix src/ && uv run ruff format src/

# Check specific file
uv run ruff check src/trajectory/common/tracer/core.py

# Check formatting without applying changes
uv run ruff format --check src/
```

### Pre-commit Hooks

Ruff runs automatically before each commit:

```bash
# Install pre-commit hooks (already done)
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files

# Run pre-commit on staged files only
uv run pre-commit run
```

### Ruff Rules

**Enabled rules:**
- `E` - pycodestyle errors (syntax errors, indentation issues)
- `W` - pycodestyle warnings (style issues)
- `F` - pyflakes (undefined names, unused imports)
- `I` - isort (import sorting)
- `UP` - pyupgrade (modernize Python syntax)
- `Q` - flake8-quotes (consistent quote usage)
- `RUF` - Ruff-specific rules (basic ones only)

**Ignored rules:**
- Unused variables, imports (too noisy for development)
- Complex type annotations
- Unicode character warnings
- Collection concatenation suggestions
- Mutable class defaults
- And other style preferences

### Configuration

Ruff settings are in `pyproject.toml`:

```toml
[tool.ruff]
exclude = ["src/e2etests", "src/tests"]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "Q", "RUF"]
ignore = [
    "E501",  # line too long, handled by formatter
    "F401",  # imported but unused (too noisy)
    "F841",  # unused variable (too noisy)
    # ... other ignored rules
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

## 🧪 Testing

### Running Tests

#### Unit Tests
```bash
# Run all unit tests
pytest

# Run specific test file
pytest src/tests/test_chatbot.py

# Run with verbose output
pytest -v

# Run from the SDK directory
cd /path/to/sdk
pytest
```

#### E2E Tests
```bash
# Run end-to-end tests
pytest src/e2etests/

# Run specific e2e test
pytest src/e2etests/test_tracer.py
```

#### Examples
```bash
# Run tracing example
python src/examples/tracing_example.py

# Run chatbot test
python src/tests/test_chatbot.py
```

### Test Package Installation
```bash
# Test basic import
python -c "from trajectory import Tracer"

# Test specific modules
python -c "from trajectory.integrations.langgraph import TrajectoryCallbackHandler"

# Test with your application
uv run python test_trajectory_tracing.py
```

### Test Package Alias
```bash
# Verify package name vs import name
pip list | grep trajectory
# Should show: trajectoryevals

python -c "import trajectory; print(trajectory.__file__)"
# Should point to your local SDK directory
```

## 🐛 Troubleshooting

### Import Errors
```bash
# If imports fail, check installation
pip list | grep trajectory
uv pip list | grep trajectory

# Reinstall if needed
uv sync --reinstall
```

### File Not Found
```bash
# Check if files are in the right location
ls -la sdk/src/trajectory/
ls -la .venv/lib/python*/site-packages/trajectory/
```

### Package Not Found
```bash
# Check uv sources
uv pip list --source

# Reinstall with editable mode
uv add --editable ../sdk
```

## 📁 Directory Structure Best Practices

```
sdk/
├── pyproject.toml          # Package configuration
├── README.md              # User documentation
├── README_DEV.md          # This development guide
├── pytest.ini            # Pytest configuration
├── .gitignore             # Git ignore rules
├── .dockerignore          # Docker ignore rules
├── src/
│   ├── trajectory/        # Main package (imported as 'trajectory')
│   │   ├── __init__.py
│   │   ├── tracer/
│   │   ├── integrations/
│   │   └── ...
│   ├── tests/             # Unit tests (excluded from package)
│   │   ├── test_chatbot.py
│   │   └── test_sanity.py
│   ├── e2etests/          # End-to-end tests (excluded from package)
│   │   ├── test_tracer.py
│   │   └── ...
│   └── examples/          # Example code (excluded from package)
│       └── tracing_example.py
├── docs/                  # Documentation (excluded from package)
└── feature_docs/          # Feature documentation
```

## 🔗 Integration Examples

### With LangGraph
```python
from trajectory import Tracer
from trajectory.integrations.langgraph import TrajectoryCallbackHandler

# Initialize tracing
tracer = Tracer(
    project_name="my_project",
    enable_monitoring=True,
    enable_evaluations=False
)

# Use with LangGraph
callback_handler = TrajectoryCallbackHandler(tracer)
```

### With uv
```toml
# In your project's pyproject.toml
[tool.uv.sources]
trajectoryevals = { path = "../sdk", editable = true }
```

## 📝 Notes

- **Package name**: `trajectoryevals` (for installation)
- **Import name**: `trajectory` (for code)
- **Editable installs**: Always use for development
- **File exclusions**: Configure properly to avoid copying dev files
- **Thread IDs**: Use for grouping related traces in Trajectory AI dashboard

## 🆘 Support

If you encounter issues:
1. Check this README first
2. Verify your pyproject.toml configuration
3. Ensure you're using editable installs
4. Check that the package alias is working correctly
