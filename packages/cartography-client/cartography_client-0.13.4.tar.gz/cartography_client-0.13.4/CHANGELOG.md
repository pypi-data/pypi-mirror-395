# Changelog

## 0.13.4 (2025-12-03)

Full Changelog: [v0.13.3...v0.13.4](https://github.com/evrimai/cartography-client/compare/v0.13.3...v0.13.4)

### Chores

* **docs:** use environment variables for authentication in code snippets ([0cbae06](https://github.com/evrimai/cartography-client/commit/0cbae06d8a84d35ae46e65275a2570b9d18bef40))
* update lockfile ([28befbd](https://github.com/evrimai/cartography-client/commit/28befbdd3dc004ce05616f278a5b3c13dc1446a4))

## 0.13.3 (2025-11-28)

Full Changelog: [v0.13.2...v0.13.3](https://github.com/evrimai/cartography-client/compare/v0.13.2...v0.13.3)

### Bug Fixes

* ensure streams are always closed ([eb5cac1](https://github.com/evrimai/cartography-client/commit/eb5cac16b7b61a0f5ae6c057e5f290844847afb6))


### Chores

* add Python 3.14 classifier and testing ([2c7e427](https://github.com/evrimai/cartography-client/commit/2c7e427e13059156331b63b205ca2c94830015b7))
* **deps:** mypy 1.18.1 has a regression, pin to 1.17 ([dd77c91](https://github.com/evrimai/cartography-client/commit/dd77c9100aae7ad60e5156a6404b943b1ae7aec6))

## 0.13.2 (2025-11-12)

Full Changelog: [v0.13.1...v0.13.2](https://github.com/evrimai/cartography-client/compare/v0.13.1...v0.13.2)

### Bug Fixes

* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([5c7c85b](https://github.com/evrimai/cartography-client/commit/5c7c85bd67bec17395433157518546fc41a7dbcc))

## 0.13.1 (2025-11-11)

Full Changelog: [v0.13.0...v0.13.1](https://github.com/evrimai/cartography-client/compare/v0.13.0...v0.13.1)

### Bug Fixes

* compat with Python 3.14 ([842352e](https://github.com/evrimai/cartography-client/commit/842352e0f102800845f27729e59e96c59bcf5451))


### Chores

* **package:** drop Python 3.8 support ([1663b47](https://github.com/evrimai/cartography-client/commit/1663b47f067b2046756b47c6fbac366a1aa78304))

## 0.13.0 (2025-11-07)

Full Changelog: [v0.12.0...v0.13.0](https://github.com/evrimai/cartography-client/compare/v0.12.0...v0.13.0)

### Features

* **api:** api update ([b932946](https://github.com/evrimai/cartography-client/commit/b932946ac65d06d0e5e9102cdcabc3ccb981d662))

## 0.12.0 (2025-11-07)

Full Changelog: [v0.11.0...v0.12.0](https://github.com/evrimai/cartography-client/compare/v0.11.0...v0.12.0)

### Features

* **api:** api update ([2926915](https://github.com/evrimai/cartography-client/commit/292691521510fcb3d6d03972ad49c6cd6b2a4591))

## 0.11.0 (2025-11-06)

Full Changelog: [v0.10.0...v0.11.0](https://github.com/evrimai/cartography-client/compare/v0.10.0...v0.11.0)

### Features

* **api:** manual updates ([6905493](https://github.com/evrimai/cartography-client/commit/6905493dc40ac0bcc6e9b3897a18c7b7f39db339))

## 0.10.0 (2025-11-06)

Full Changelog: [v0.9.3...v0.10.0](https://github.com/evrimai/cartography-client/compare/v0.9.3...v0.10.0)

### Features

* **api:** api update ([3dd4766](https://github.com/evrimai/cartography-client/commit/3dd47667ab2266c2eabcef5faec21729edb10f5d))


### Chores

* **internal/tests:** avoid race condition with implicit client cleanup ([891e5db](https://github.com/evrimai/cartography-client/commit/891e5db5e6aeed20693df048a1ff000482647358))
* **internal:** grammar fix (it's -&gt; its) ([b16d21b](https://github.com/evrimai/cartography-client/commit/b16d21be4c881991c759fe43825f1f6532553c8a))

## 0.9.3 (2025-10-30)

Full Changelog: [v0.9.2...v0.9.3](https://github.com/evrimai/cartography-client/compare/v0.9.2...v0.9.3)

### Bug Fixes

* **client:** close streams without requiring full consumption ([e7d426f](https://github.com/evrimai/cartography-client/commit/e7d426f7d254b257bc6ba8adbf848686f3d29b08))


### Chores

* bump `httpx-aiohttp` version to 0.1.9 ([6036d15](https://github.com/evrimai/cartography-client/commit/6036d1522e018c7d67c86de7b23111f590201358))

## 0.9.2 (2025-10-12)

Full Changelog: [v0.9.1...v0.9.2](https://github.com/evrimai/cartography-client/compare/v0.9.1...v0.9.2)

### Chores

* **internal:** detect missing future annotations with ruff ([88fced5](https://github.com/evrimai/cartography-client/commit/88fced51bb6c69c6ade5a7c36efb29897b8e0239))

## 0.9.1 (2025-09-20)

Full Changelog: [v0.9.0...v0.9.1](https://github.com/evrimai/cartography-client/compare/v0.9.0...v0.9.1)

### Chores

* do not install brew dependencies in ./scripts/bootstrap by default ([95b877d](https://github.com/evrimai/cartography-client/commit/95b877d88330c2e1d04cb4c65c4b694ccfba710e))

## 0.9.0 (2025-09-19)

Full Changelog: [v0.8.1...v0.9.0](https://github.com/evrimai/cartography-client/compare/v0.8.1...v0.9.0)

### Features

* **api:** api update ([9a480f9](https://github.com/evrimai/cartography-client/commit/9a480f9ae3e1740836587c43321ab86e37102b69))
* improve future compat with pydantic v3 ([c85338d](https://github.com/evrimai/cartography-client/commit/c85338d505acb8984563bd8211097ffd85fbfaad))
* **types:** replace List[str] with SequenceNotStr in params ([8a84b9c](https://github.com/evrimai/cartography-client/commit/8a84b9ca21a7e04cd703d72b67b0b4361ee43474))


### Chores

* **internal:** add Sequence related utils ([f8bc56f](https://github.com/evrimai/cartography-client/commit/f8bc56f11eee087e94fa809619d1ed99686376f6))
* **internal:** move mypy configurations to `pyproject.toml` file ([8316eef](https://github.com/evrimai/cartography-client/commit/8316eef3600753d76d18ba9901aef5db73c9e318))
* **internal:** update pydantic dependency ([7e7996b](https://github.com/evrimai/cartography-client/commit/7e7996be107571e0b6f73c7adda69bb69011bdfe))
* **internal:** update pyright exclude list ([7c58f1b](https://github.com/evrimai/cartography-client/commit/7c58f1b8a9657a72b66d1d44a7de96deb333a132))
* **tests:** simplify `get_platform` test ([37a131e](https://github.com/evrimai/cartography-client/commit/37a131ec48cc3a08e024789bb68e4ad0d829c690))
* **types:** change optional parameter type from NotGiven to Omit ([a3fe03d](https://github.com/evrimai/cartography-client/commit/a3fe03da7fd242b930beeb2d41f0b34bc19c7749))

## 0.8.1 (2025-08-27)

Full Changelog: [v0.8.0...v0.8.1](https://github.com/evrimai/cartography-client/compare/v0.8.0...v0.8.1)

### Bug Fixes

* avoid newer type syntax ([2b4c710](https://github.com/evrimai/cartography-client/commit/2b4c710297b5d4b7f233c7e868933d508f47afa2))


### Chores

* **internal:** change ci workflow machines ([b1b2d68](https://github.com/evrimai/cartography-client/commit/b1b2d68da44ce55d83cf66a32c01cbc141d5c5fd))

## 0.8.0 (2025-08-25)

Full Changelog: [v0.7.0...v0.8.0](https://github.com/evrimai/cartography-client/compare/v0.7.0...v0.8.0)

### Features

* **api:** api update ([1a41dce](https://github.com/evrimai/cartography-client/commit/1a41dce5f3515b85d5e12fa3be3ae24331fb49a3))

## 0.7.0 (2025-08-23)

Full Changelog: [v0.6.0...v0.7.0](https://github.com/evrimai/cartography-client/compare/v0.6.0...v0.7.0)

### Features

* **api:** api update ([4991942](https://github.com/evrimai/cartography-client/commit/4991942007689cf9ce15a562b7b7346c7c6d4554))


### Chores

* update github action ([5a20e0d](https://github.com/evrimai/cartography-client/commit/5a20e0d72f059a5375b023aa099ad42712ad6468))

## 0.6.0 (2025-08-20)

Full Changelog: [v0.5.0...v0.6.0](https://github.com/evrimai/cartography-client/compare/v0.5.0...v0.6.0)

### Features

* **api:** api update ([463f7cf](https://github.com/evrimai/cartography-client/commit/463f7cf4912d177044712520fb2310c13367912e))

## 0.5.0 (2025-08-12)

Full Changelog: [v0.4.0...v0.5.0](https://github.com/evrimai/cartography-client/compare/v0.4.0...v0.5.0)

### Features

* **api:** api update ([2ec757e](https://github.com/evrimai/cartography-client/commit/2ec757e00ad59797ba75e34be63bb185471a32c2))

## 0.4.0 (2025-08-12)

Full Changelog: [v0.3.1...v0.4.0](https://github.com/evrimai/cartography-client/compare/v0.3.1...v0.4.0)

### Features

* **api:** api update ([153bc19](https://github.com/evrimai/cartography-client/commit/153bc192d14eb79fdfa4f145993aebbf15e5c36d))


### Chores

* **internal:** codegen related update ([b85c126](https://github.com/evrimai/cartography-client/commit/b85c12659f0b39c6199de08fe7056c7e99b1f02c))
* **internal:** update comment in script ([a07f9a0](https://github.com/evrimai/cartography-client/commit/a07f9a0d031cd204b36c9809aa836a41141e1f75))

## 0.3.1 (2025-08-09)

Full Changelog: [v0.3.0...v0.3.1](https://github.com/evrimai/cartography-client/compare/v0.3.0...v0.3.1)

### Chores

* update @stainless-api/prism-cli to v5.15.0 ([5cd60ac](https://github.com/evrimai/cartography-client/commit/5cd60acb8f0654f9b86003f311aaeab26c0a63aa))

## 0.3.0 (2025-08-05)

Full Changelog: [v0.2.0...v0.3.0](https://github.com/evrimai/cartography-client/compare/v0.2.0...v0.3.0)

### Features

* **api:** api update ([54ce37e](https://github.com/evrimai/cartography-client/commit/54ce37edecc328ec401a24e9ef4c8631086a2e23))

## 0.2.0 (2025-08-05)

Full Changelog: [v0.1.0...v0.2.0](https://github.com/evrimai/cartography-client/compare/v0.1.0...v0.2.0)

### Features

* **api:** manual updates ([99f1a13](https://github.com/evrimai/cartography-client/commit/99f1a133c89c4ed7d5fba0836aad152c775d8274))

## 0.1.0 (2025-08-05)

Full Changelog: [v0.0.1...v0.1.0](https://github.com/evrimai/cartography-client/compare/v0.0.1...v0.1.0)

### Features

* **api:** manual updates ([d76ab2e](https://github.com/evrimai/cartography-client/commit/d76ab2e066b6aeda4e772d8d56bd06bb934bba20))

## 0.0.1 (2025-08-05)

Full Changelog: [v0.0.1-alpha.0...v0.0.1](https://github.com/evrimai/cartography-client/compare/v0.0.1-alpha.0...v0.0.1)

### Chores

* update SDK settings ([6f6f16f](https://github.com/evrimai/cartography-client/commit/6f6f16ff247068a3c7a634f0846bb8efc7fec0e9))
* update SDK settings ([f1ee3e6](https://github.com/evrimai/cartography-client/commit/f1ee3e6f47aaade030da77c1864e42054adee06c))
