# CHANGELOG


## v0.1.1 (2025-06-14)

### Bug Fixes

- **release**: Add semantic-release configuration for initial setup
  ([`5fb5c22`](https://github.com/josephbwagner/yendoria/commit/5fb5c224fb4ed18c4663c9bd2807e87a28917f5b))

- Added tag_format configuration - Added major_on_zero and allow_zero_version flags - Enables
  semantic-release to work with initial repository setup

- **release**: Update semantic-release workflow commands
  ([`5aab9ab`](https://github.com/josephbwagner/yendoria/commit/5aab9ab1b86d7025e2dc7c0f5a73b24bc786d72f))

- Updated semantic-release command syntax for newer version - Added baseline tag v0.1.0 for initial
  release setup - Added test script for diagnosing release automation

This should resolve the 'No tags found' error in the release workflow.


## v0.1.0 (2025-06-13)

### Bug Fixes

- **ci**: Add workflow_call trigger to enable reusable workflow
  ([`9a5bf7b`](https://github.com/josephbwagner/yendoria/commit/9a5bf7b14308f54a00e428286bce905eaa806c1b))

- Added workflow_call trigger to CI workflow - Enables release workflow to call CI workflow for
  testing - Resolves GitHub Actions workflow validation error

Fixes release workflow failure that occurred when trying to call CI workflow without proper reusable
  workflow configuration.

### Continuous Integration

- **deps**: Bump codecov/codecov-action from 3 to 5
  ([`9da43c5`](https://github.com/josephbwagner/yendoria/commit/9da43c57abf55cec186ce20cdb118d8a2e2ac6a5))

Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 3 to 5. - [Release
  notes](https://github.com/codecov/codecov-action/releases) -
  [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/codecov/codecov-action/compare/v3...v5)

--- updated-dependencies: - dependency-name: codecov/codecov-action dependency-version: '5'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump codecov/codecov-action from 4 to 5
  ([`cc556c4`](https://github.com/josephbwagner/yendoria/commit/cc556c4ad79076bf35c5adaf4e9410f8a7313708))

### Documentation

- Complete release automation setup
  ([`a904774`](https://github.com/josephbwagner/yendoria/commit/a904774677759e366b6a4c7cf7fbfabe246c0ab0))
