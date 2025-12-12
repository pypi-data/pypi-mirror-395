# Releasing jaxmesh

Minimal checklist to cut a new version to PyPI. The `.pypi_token.env` carries `PYPI_API_TOKEN` for automation.

1) Bump version
   - Edit `pyproject.toml` `[project].version`.

2) Sanity + tests
   - `JAX_PLATFORMS=cpu uv run pytest tests -q`

3) Build artifacts
   - `uv run python -m build`

4) Publish
   - `source .pypi_token.env && uv run python -m twine upload dist/* -u __token__ -p "$PYPI_API_TOKEN"`

5) Tag
   - `git tag -a vX.Y.Z -m "jaxmesh vX.Y.Z"` and push tags if desired.

6) Downstream update
   - Update survi to depend on the new version (change path dependency to PyPI).
