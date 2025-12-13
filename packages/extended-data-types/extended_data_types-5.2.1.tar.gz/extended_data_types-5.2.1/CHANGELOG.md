# CHANGELOG

<!-- version list -->

## v5.2.1 (2025-12-07)

### Bug Fixes

- Restore working Dockerfile with Go 1.25.3 and correct process-compose install
  ([`5bbafb9`](https://github.com/jbcom/extended-data-types/commit/5bbafb9e0473c3dd0423fd024ff5e24f5a3b413d))


## v5.2.0 (2025-12-07)

### Bug Fixes

- Add all mypy error codes for wrapt.ObjectProxy across Python versions
  ([#35](https://github.com/jbcom/extended-data-types/pull/35),
  [`5cf3c04`](https://github.com/jbcom/extended-data-types/commit/5cf3c0432722d482fe4e794008c463c23236f40f))

- Add all mypy error codes for wrapt.ObjectProxy across Python versions
  ([#36](https://github.com/jbcom/extended-data-types/pull/36),
  [`8801df8`](https://github.com/jbcom/extended-data-types/commit/8801df8882261842132bd9451036c25d3b4e00c6))

- Add ruamel.yaml dependency and bump to 5.1.2
  ([`36d88d5`](https://github.com/jbcom/extended-data-types/commit/36d88d5ae260434e2c7feb71fe2a24829244296f))

- Correct mypy type ignore comment for wrapt.ObjectProxy
  ([#34](https://github.com/jbcom/extended-data-types/pull/34),
  [`c3515c8`](https://github.com/jbcom/extended-data-types/commit/c3515c8d3618d0a86ea95f6f275a7398165cadb9))

- Use absolute imports throughout package
  ([#59](https://github.com/jbcom/extended-data-types/pull/59),
  [`fbacc7f`](https://github.com/jbcom/extended-data-types/commit/fbacc7f3bae78123c0609ab30f75e432e972bc58))

- Use mypy override for wrapt.ObjectProxy instead of inline ignores
  ([#36](https://github.com/jbcom/extended-data-types/pull/36),
  [`8801df8`](https://github.com/jbcom/extended-data-types/commit/8801df8882261842132bd9451036c25d3b4e00c6))

- Use TypeAlias for Python 3.9 mypy compatibility and fix ruff linting
  ([#35](https://github.com/jbcom/extended-data-types/pull/35),
  [`5cf3c04`](https://github.com/jbcom/extended-data-types/commit/5cf3c0432722d482fe4e794008c463c23236f40f))

- Use typing_extensions.TypeAlias and string literal for Python 3.9
  ([#35](https://github.com/jbcom/extended-data-types/pull/35),
  [`5cf3c04`](https://github.com/jbcom/extended-data-types/commit/5cf3c0432722d482fe4e794008c463c23236f40f))

### Chores

- Bump version to 5.1.1 ([#37](https://github.com/jbcom/extended-data-types/pull/37),
  [`bb42013`](https://github.com/jbcom/extended-data-types/commit/bb42013b74b77fb6221a3229f577915db429b8b6))

### Code Style

- Apply pre-commit formatting to set_version.py
  ([`74dab09`](https://github.com/jbcom/extended-data-types/commit/74dab0960695d59351724d0e14a109ce02825780))

### Documentation

- Clarify float support and exception handling in number transformations
  ([#45](https://github.com/jbcom/extended-data-types/pull/45),
  [`400c975`](https://github.com/jbcom/extended-data-types/commit/400c9755d16c7887e5c6fda7275dbf0d4140f1ff))

### Features

- Add release workflow and PR creation ([#41](https://github.com/jbcom/extended-data-types/pull/41),
  [`3fd24cb`](https://github.com/jbcom/extended-data-types/commit/3fd24cb0e9ba91924623d7b353b78e3a39a09f28))

- Add string and number transformation utilities
  ([#45](https://github.com/jbcom/extended-data-types/pull/45),
  [`400c975`](https://github.com/jbcom/extended-data-types/commit/400c9755d16c7887e5c6fda7275dbf0d4140f1ff))

- Improve export_utils with better format handling
  ([#45](https://github.com/jbcom/extended-data-types/pull/45),
  [`400c975`](https://github.com/jbcom/extended-data-types/commit/400c9755d16c7887e5c6fda7275dbf0d4140f1ff))

- Migrate from monorepo to standalone package
  ([`c4f24df`](https://github.com/jbcom/extended-data-types/commit/c4f24dfa10729a683390849c8ec83a8ee7d485cb))

- Update docs/conf.py version in sync with CalVer releases
  ([`74dab09`](https://github.com/jbcom/extended-data-types/commit/74dab0960695d59351724d0e14a109ce02825780))

### Refactoring

- Improve string, list, and map utilities
  ([#45](https://github.com/jbcom/extended-data-types/pull/45),
  [`400c975`](https://github.com/jbcom/extended-data-types/commit/400c9755d16c7887e5c6fda7275dbf0d4140f1ff))

- Use absolute imports and add future annotations
  ([`f2568eb`](https://github.com/jbcom/extended-data-types/commit/f2568eb60460ba58faeaa6e9fc02d923452fcd22))

### Testing

- Add comprehensive tests for transformation utilities
  ([#45](https://github.com/jbcom/extended-data-types/pull/45),
  [`400c975`](https://github.com/jbcom/extended-data-types/commit/400c9755d16c7887e5c6fda7275dbf0d4140f1ff))


## v202511.8.0 (2025-12-01)

### Features

- Consolidate control center into unified control surface
  ([#295](https://github.com/jbcom/jbcom-control-center/pull/295),
  [`2c207ca`](https://github.com/jbcom/jbcom-control-center/commit/2c207caf5129184d178bfbff81945eb74988d629))


## v202511.7.1 (2025-12-01)

### Bug Fixes

- Update default model to claude-4-opus for Cursor compatibility
  ([#290](https://github.com/jbcom/jbcom-control-center/pull/290),
  [`9b81310`](https://github.com/jbcom/jbcom-control-center/commit/9b8131073c73107bd07c078801897acc5bbe8370))


## v202511.7.0 (2025-12-01)

### Documentation

- Align instructions with SemVer ([#263](https://github.com/jbcom/jbcom-control-center/pull/263),
  [`1d3d830`](https://github.com/jbcom/jbcom-control-center/commit/1d3d83033aaf2d0b16b7355559dbda208ee20dd7))

- Fix test instructions + repository health audit
  ([#275](https://github.com/jbcom/jbcom-control-center/pull/275),
  [`f9617cb`](https://github.com/jbcom/jbcom-control-center/commit/f9617cb8db0216c0f1fc10310e441ef447373aba))

### Features

- Unified agentic-control package with intelligent multi-org token switching
  ([#285](https://github.com/jbcom/jbcom-control-center/pull/285),
  [`0baced8`](https://github.com/jbcom/jbcom-control-center/commit/0baced883a8ae0c6909e6a631d5de69c7c9d8e21))


## v202511.6.0 (2025-11-29)

### Documentation

- Add FSC Control Center counterparty awareness
  ([#220](https://github.com/jbcom/jbcom-control-center/pull/220),
  [`a0e9ff9`](https://github.com/jbcom/jbcom-control-center/commit/a0e9ff96aefd947266753fb8e8f460463eb8dc8f))

- Update orchestration with completion status
  ([`f0737b5`](https://github.com/jbcom/jbcom-control-center/commit/f0737b52b44300f8ba7d376fc1a32da2ee7035de))

- Update PR_PLAN with agent fleet assignments
  ([`80845b1`](https://github.com/jbcom/jbcom-control-center/commit/80845b1531f900a81786489ce77c030429d4c362))

- Update wiki and orchestration for architectural evolution
  ([`8ad2f99`](https://github.com/jbcom/jbcom-control-center/commit/8ad2f997f41dffb1910c07398a779d1d7c2a9302))

### Features

- Add python-terraform-bridge package
  ([#248](https://github.com/jbcom/jbcom-control-center/pull/248),
  [`2d3cd6f`](https://github.com/jbcom/jbcom-control-center/commit/2d3cd6f05502fe02c0a0178829d871a955ae6b35))


## v202511.5.0 (2025-11-29)

### Features

- Add AWS Secrets Manager create, update, delete operations
  ([#236](https://github.com/jbcom/jbcom-control-center/pull/236),
  [`76b8243`](https://github.com/jbcom/jbcom-control-center/commit/76b82433cc4ff8e2842e0ea2313fba4bfedbc19c))

- Add filtering and transformation to Google user/group listing
  ([#241](https://github.com/jbcom/jbcom-control-center/pull/241),
  [`33feb1c`](https://github.com/jbcom/jbcom-control-center/commit/33feb1ca1ba61df049879eaeb75e46b112542560))

- Add Slack usergroup and conversation listing
  ([#237](https://github.com/jbcom/jbcom-control-center/pull/237),
  [`ef1aea7`](https://github.com/jbcom/jbcom-control-center/commit/ef1aea7eb469df998e9d0fe93722b6af0af8267b))

- Add Vault AWS IAM role helpers ([#239](https://github.com/jbcom/jbcom-control-center/pull/239),
  [`bc7c8aa`](https://github.com/jbcom/jbcom-control-center/commit/bc7c8aa2c9b27dac2748e038ceff34a4b0f5572d))


## v202511.4.0 (2025-11-28)

### Features

- Add FSC fleet coordination support
  ([`7a046b6`](https://github.com/jbcom/jbcom-control-center/commit/7a046b6578cd2216542e893d61ecd501d8305a8c))


## v202511.3.0 (2025-11-28)

- Initial Release
