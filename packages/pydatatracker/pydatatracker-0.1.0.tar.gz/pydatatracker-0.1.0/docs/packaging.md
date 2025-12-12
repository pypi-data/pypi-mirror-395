# Release Checklist

1. Run `just test` and `just lint`.
2. Update `CHANGELOG.md` and bump `src/pydatatracker/_version.py`.
3. Ensure README/docs reference any new features.
4. Build and publish:
   ```bash
   just publish
   ```
   This runs `uv build` and requires `PYPI_TOKEN` to be set for `uv publish`.
