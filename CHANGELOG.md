# CHANGELOG


## v0.4.0 (2025-06-15)

### Features

- Implement AI foundations
  ([`bc8ec42`](https://github.com/josephbwagner/yendoria/commit/bc8ec42f9e234c4f06dc1376b8c142f5d5aa8b44))


## v0.3.1 (2025-06-14)

### Bug Fixes

- Address bandit warnings
  ([`52196b6`](https://github.com/josephbwagner/yendoria/commit/52196b6907a4eb06b6992c2c4133105299a81a7a))


## v0.3.0 (2025-06-14)

### Features

- Modding support
  ([`2447aca`](https://github.com/josephbwagner/yendoria/commit/2447acaa173233c40e209a53b8c4f117b906f1be))


## v0.2.1 (2025-06-14)

### Bug Fixes

- **deprecations**: Modernize event handling and update security tools
  ([`e1f51e0`](https://github.com/josephbwagner/yendoria/commit/e1f51e0a0c50a51bdb7e6beaab82c9e0a450132f))

- Replace deprecated tcod.event.EventDispatch with Protocol-based approach - Update from deprecated
  'safety check' to 'safety scan' command - Upgrade pip from vulnerable 24.3.1 to secure 25.1.1 -
  Fix import formatting and remove unused imports - All CI checks now pass without deprecation
  warnings

Resolves all deprecation warnings and security vulnerabilities.


## v0.2.0 (2025-06-14)

### Features

- Enable publishing
  ([`5a6da54`](https://github.com/josephbwagner/yendoria/commit/5a6da547e00423e06f95098d44ffb4d05d7718a7))


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
