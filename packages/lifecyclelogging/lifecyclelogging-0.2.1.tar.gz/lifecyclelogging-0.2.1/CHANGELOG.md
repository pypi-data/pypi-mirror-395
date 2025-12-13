# CHANGELOG

<!-- version list -->

## v0.2.1 (2025-12-07)

### Bug Fixes

- Restore working Dockerfile with Go 1.25.3 and correct process-compose install
  ([`eef6fda`](https://github.com/jbcom/lifecyclelogging/commit/eef6fdaadd8f5ec7073b05d53933a511ee4fbb02))


## v0.2.0 (2025-12-07)

### Bug Fixes

- Properly sanitize only filename, not directory path
  ([#28](https://github.com/jbcom/lifecyclelogging/pull/28),
  [`0707a30`](https://github.com/jbcom/lifecyclelogging/commit/0707a30f528578adda7c562c7a9aa926464110ac))

- Resolve CI failures from linting and test issues
  ([#28](https://github.com/jbcom/lifecyclelogging/pull/28),
  [`0707a30`](https://github.com/jbcom/lifecyclelogging/commit/0707a30f528578adda7c562c7a9aa926464110ac))

- Use absolute imports and fix lint issues
  ([#46](https://github.com/jbcom/lifecyclelogging/pull/46),
  [`3ce738d`](https://github.com/jbcom/lifecyclelogging/commit/3ce738d0ecb133c8ed52283209cc25aced10e2c4))

### Chores

- Remove .DS_Store files and add to .gitignore
  ([#28](https://github.com/jbcom/lifecyclelogging/pull/28),
  [`0707a30`](https://github.com/jbcom/lifecyclelogging/commit/0707a30f528578adda7c562c7a9aa926464110ac))

- **config**: Migrate config renovate.json
  ([#27](https://github.com/jbcom/lifecyclelogging/pull/27),
  [`14618ed`](https://github.com/jbcom/lifecyclelogging/commit/14618edcc060b17fcdb91b5deb6c8a8b901309e9))

- **deps**: Update actions/checkout action to v6
  ([#31](https://github.com/jbcom/lifecyclelogging/pull/31),
  [`9e497d6`](https://github.com/jbcom/lifecyclelogging/commit/9e497d62b7ceb795df2314e75c3cca026676be9a))

- **deps**: Update actions/checkout action to v6
  ([#25](https://github.com/jbcom/lifecyclelogging/pull/25),
  [`d837604`](https://github.com/jbcom/lifecyclelogging/commit/d8376047f1382f7365b142dbdf972e1ddb83d7c4))

- **deps**: Update actions/checkout action to v6
  ([#26](https://github.com/jbcom/lifecyclelogging/pull/26),
  [`e11bddd`](https://github.com/jbcom/lifecyclelogging/commit/e11bdddfa73e78ba8cb43cbd2f405269750e559f))

- **deps**: Update actions/checkout to v6 ([#25](https://github.com/jbcom/lifecyclelogging/pull/25),
  [`d837604`](https://github.com/jbcom/lifecyclelogging/commit/d8376047f1382f7365b142dbdf972e1ddb83d7c4))

- **deps**: Update actions/download-artifact action to v6
  ([#32](https://github.com/jbcom/lifecyclelogging/pull/32),
  [`07246e3`](https://github.com/jbcom/lifecyclelogging/commit/07246e3e2c6fbb4415e358ae1997a6d7044cafa8))

### Code Style

- Format handlers.py with black ([#28](https://github.com/jbcom/lifecyclelogging/pull/28),
  [`0707a30`](https://github.com/jbcom/lifecyclelogging/commit/0707a30f528578adda7c562c7a9aa926464110ac))

### Documentation

- Add AI agent guidelines and fix workflow conflicts
  ([#28](https://github.com/jbcom/lifecyclelogging/pull/28),
  [`0707a30`](https://github.com/jbcom/lifecyclelogging/commit/0707a30f528578adda7c562c7a9aa926464110ac))

### Features

- Leverage extended-data-types 5.2.0 for improved data handling
  ([#28](https://github.com/jbcom/lifecyclelogging/pull/28),
  [`0707a30`](https://github.com/jbcom/lifecyclelogging/commit/0707a30f528578adda7c562c7a9aa926464110ac))

- Migrate from monorepo to standalone package
  ([`92645c9`](https://github.com/jbcom/lifecyclelogging/commit/92645c93d84c4169c853e0f0bf5fe8fddc564cac))

- Upgrade to extended-data-types 5.2.0 and unified CI workflow
  ([#28](https://github.com/jbcom/lifecyclelogging/pull/28),
  [`0707a30`](https://github.com/jbcom/lifecyclelogging/commit/0707a30f528578adda7c562c7a9aa926464110ac))

### Refactoring

- Use absolute imports and add future annotations
  ([`e413f71`](https://github.com/jbcom/lifecyclelogging/commit/e413f7190dd97adc24eda75f4634d414d863791b))


## v202511.8.0 (2025-12-01)

### Documentation

- Create handoff for documentation overhaul
  ([#298](https://github.com/jbcom/jbcom-control-center/pull/298),
  [`4481bd2`](https://github.com/jbcom/jbcom-control-center/commit/4481bd27d6cd665cecc678acf784395c9986d930))

### Features

- Consolidate control center into unified control surface
  ([#295](https://github.com/jbcom/jbcom-control-center/pull/295),
  [`2c207ca`](https://github.com/jbcom/jbcom-control-center/commit/2c207caf5129184d178bfbff81945eb74988d629))


## v202511.7.0 (2025-12-01)

### Bug Fixes

- Update default model to claude-4-opus for Cursor compatibility
  ([#290](https://github.com/jbcom/jbcom-control-center/pull/290),
  [`9b81310`](https://github.com/jbcom/jbcom-control-center/commit/9b8131073c73107bd07c078801897acc5bbe8370))

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


## v202511.4.0 (2025-11-29)

### Features

- Add FSC fleet coordination support
  ([`7a046b6`](https://github.com/jbcom/jbcom-control-center/commit/7a046b6578cd2216542e893d61ecd501d8305a8c))


## v202511.3.0 (2025-11-28)

- Initial Release
