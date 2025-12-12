## Checklist for a new release

1. [ ] Review that `AUTHORS.md` has been updated.
2. [ ] Review `@deprecated` and `FutureWarnings` that can be cleaned up now.

3. [ ] Add compatibility info to `README.md`, extract the correct versions from `pyproject.toml`. e.g.:
      ```
      ### Compatibility info

      - Python: `python>=x.x.x`
      -
      ```

4. CI pipeline:
    - [ ] Ensure Changelog has been updated to reflect changes that are included in the release.
    - [ ] Automated pipeline passes.
    - [ ] All tests pass.


5. [ ] Create tag for bumped version:
    - Merge this MR into `main`.
    - Switch to `main` branch.
    - Create and push an **annotated** tag `vX.Y.Z` pointing to the merge commit:

      ```bash
      echo $NEW_VERSION

      git tag -a "v${NEW_VERSION}"  # Note: should be vX.Y.Z, not X.Y.Z
      # You will be prompted for a tag description: `Release vX.Y.Z`
      git push origin "v${NEW_VERSION}"
      ```

6. [ ] Push an empty commit to `main` with message `Start development of vX.Y.Z+1.dev`.
7. [ ] **Create** and **push** (see steps above) an **annotated** tag `vX.Y.Z+1.dev` pointing to the commit above.  Commit annotation: `Start development of vX.Y.Z+1`.

8. When `Release to test.pypi.org` job of the tag pipeline succeeds:
    - [ ] Install package in (test) env and validate (e.g., run a quick notebook).
       ```bash
       pip install quantify-core==x.x.x --extra-index-url=https://test.pypi.org/simple/
       ```
       - _(For creating test env)_
         ```bash
         ENV_NAME=qtest # Adjust
         PY_VER=3.8
         DISPLAY_NAME="Python $PY_VER Quantify Test Env" && echo $DISPLAY_NAME # Adjust

         conda create --name $ENV_NAME python=$PY_VER
         conda activate $ENV_NAME
         conda install -c conda-forge jupyterlab
         python -m ipykernel install --user --name=$ENV_NAME --display-name="$DISPLAY_NAME"
         ```

9. [ ] Release on PyPi by triggering manual `Release to pypi.org` job and wait till it succeeds.
10. [ ] Post the new release in Slack (`#software-for-users` and `#software-for-developers`).
    - PS Rockets are a must! 🚀🚀🚀
11. [ ] Inform the Quantify Marketing Team.
