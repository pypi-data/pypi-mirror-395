# 0. Sync documentation to bundled data/ directory
cp AGENTS.md PROJECTSPEC.md README.md src/diagramagic/data/

# 1. Clean
rm -rf dist/ target/

# 2. Build wheel for current platform
maturin build --release --locked

# 3. Build source distribution
maturin sdist

# 4. Collect to dist/
mkdir -p dist
cp target/wheels/* dist/

# 5. Check
twine check dist/*

# 6. Upload to PyPI (both .whl and .tar.gz)
twine upload dist/*