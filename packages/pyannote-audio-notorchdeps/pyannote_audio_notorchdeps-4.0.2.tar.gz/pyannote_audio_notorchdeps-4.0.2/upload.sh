# Clean previous builds
rm -rf dist/ build/

# Build using pyproject.toml
python -m build

# Upload to PyPI
twine upload dist/*
