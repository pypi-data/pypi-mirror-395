# 0. Sync documentation to bundled data/ directory
cp AGENTS.md PROJECTSPEC.md README.md src/diagramagic/data/

# 1. Clean
rm -rf dist/ target/

# 2. Build source distribution only
maturin sdist

# 3. Collect to dist/
mkdir -p dist
cp target/wheels/*.tar.gz dist/

# 4. Check
twine check dist/*

# 5. Upload to PyPI (only the .tar.gz)
twine upload dist/*.tar.gz