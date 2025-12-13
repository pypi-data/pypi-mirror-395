# Changelog

## 0.1.0-alpha.20 (2025-12-09)

Full Changelog: [v0.1.0-alpha.19...v0.1.0-alpha.20](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.19...v0.1.0-alpha.20)

### Bug Fixes

* **types:** allow pyright to infer TypedDict types within SequenceNotStr ([6751a7b](https://github.com/bluehive-health/bluehive-sdk-python/commit/6751a7bedafce25c6c29de3a266baf78ee70da28))


### Chores

* update lockfile ([978ce50](https://github.com/bluehive-health/bluehive-sdk-python/commit/978ce50efcbed885fc4e51f84e99e5bdf4b7122d))

## 0.1.0-alpha.19 (2025-11-28)

Full Changelog: [v0.1.0-alpha.18...v0.1.0-alpha.19](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.18...v0.1.0-alpha.19)

### Bug Fixes

* ensure streams are always closed ([199cb37](https://github.com/bluehive-health/bluehive-sdk-python/commit/199cb37d2f1452bac63db30f1a958c8f8810873f))


### Chores

* add Python 3.14 classifier and testing ([cf2cf5e](https://github.com/bluehive-health/bluehive-sdk-python/commit/cf2cf5eb4f9bf42a039e6d496ec7964b3afca0d1))
* **deps:** mypy 1.18.1 has a regression, pin to 1.17 ([67ddc37](https://github.com/bluehive-health/bluehive-sdk-python/commit/67ddc37871be48e2ca0b59486d3bab5b6786e93b))

## 0.1.0-alpha.18 (2025-11-17)

Full Changelog: [v0.1.0-alpha.17...v0.1.0-alpha.18](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.17...v0.1.0-alpha.18)

### Features

* **api:** api update ([edd7e3f](https://github.com/bluehive-health/bluehive-sdk-python/commit/edd7e3ff03f933c53e0388578b8731366a8a7c76))

## 0.1.0-alpha.17 (2025-11-12)

Full Changelog: [v0.1.0-alpha.16...v0.1.0-alpha.17](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.16...v0.1.0-alpha.17)

### Bug Fixes

* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([e92a55a](https://github.com/bluehive-health/bluehive-sdk-python/commit/e92a55a2f719883ff9ea7f639b4740c5b824e83d))

## 0.1.0-alpha.16 (2025-11-11)

Full Changelog: [v0.1.0-alpha.15...v0.1.0-alpha.16](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.15...v0.1.0-alpha.16)

### Bug Fixes

* compat with Python 3.14 ([c705861](https://github.com/bluehive-health/bluehive-sdk-python/commit/c7058616c0a1a3a1c57acc60afeec14f0ee0c731))


### Chores

* **internal/tests:** avoid race condition with implicit client cleanup ([a192964](https://github.com/bluehive-health/bluehive-sdk-python/commit/a19296467f6b7ccee2eefd1a15982e2360a969c7))
* **internal:** grammar fix (it's -&gt; its) ([1f55feb](https://github.com/bluehive-health/bluehive-sdk-python/commit/1f55feb4f4e96ff030a18511fe1429c3f35272d0))
* **package:** drop Python 3.8 support ([51484a6](https://github.com/bluehive-health/bluehive-sdk-python/commit/51484a6fbc684a6629be881b461e943b6ffd83f1))

## 0.1.0-alpha.15 (2025-10-30)

Full Changelog: [v0.1.0-alpha.14...v0.1.0-alpha.15](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.14...v0.1.0-alpha.15)

### Bug Fixes

* **client:** close streams without requiring full consumption ([25e1e7c](https://github.com/bluehive-health/bluehive-sdk-python/commit/25e1e7ca071fda5025c0999704e48963d08eea1c))


### Chores

* bump `httpx-aiohttp` version to 0.1.9 ([6cf61e6](https://github.com/bluehive-health/bluehive-sdk-python/commit/6cf61e624fdafed663c932e964287c94b870659e))

## 0.1.0-alpha.14 (2025-10-13)

Full Changelog: [v0.1.0-alpha.13...v0.1.0-alpha.14](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.13...v0.1.0-alpha.14)

### Features

* **api:** api update ([9429c0c](https://github.com/bluehive-health/bluehive-sdk-python/commit/9429c0cb38f28ff304b45c53474362fd9d1f5816))


### Chores

* **internal:** detect missing future annotations with ruff ([552be23](https://github.com/bluehive-health/bluehive-sdk-python/commit/552be23072b02ca07ba39de2bcc01b9214eb635c))

## 0.1.0-alpha.13 (2025-10-05)

Full Changelog: [v0.1.0-alpha.12...v0.1.0-alpha.13](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.12...v0.1.0-alpha.13)

### Features

* **api:** api update ([f620ba9](https://github.com/bluehive-health/bluehive-sdk-python/commit/f620ba9397d8b9b9d5880ae0c0610c79f73f5578))

## 0.1.0-alpha.12 (2025-10-05)

Full Changelog: [v0.1.0-alpha.11...v0.1.0-alpha.12](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.11...v0.1.0-alpha.12)

### Features

* **api:** manual updates ([b98edba](https://github.com/bluehive-health/bluehive-sdk-python/commit/b98edba433e0915cd42f46f3f83f33571c2505d2))
* **api:** manual updates ([7787d54](https://github.com/bluehive-health/bluehive-sdk-python/commit/7787d543eb92154ba2365397dfb0d9bf64e13050))

## 0.1.0-alpha.11 (2025-10-05)

Full Changelog: [v0.1.0-alpha.10...v0.1.0-alpha.11](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.10...v0.1.0-alpha.11)

### Features

* **api:** api update ([779bcbd](https://github.com/bluehive-health/bluehive-sdk-python/commit/779bcbda462b257321bd3d0d07a9b2b5cef4cd2e))

## 0.1.0-alpha.10 (2025-10-05)

Full Changelog: [v0.1.0-alpha.9...v0.1.0-alpha.10](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.9...v0.1.0-alpha.10)

### Features

* **api:** api update ([9d744ca](https://github.com/bluehive-health/bluehive-sdk-python/commit/9d744caeab82a0ecedbbc952049c66dd3d17108f))
* improve future compat with pydantic v3 ([6bfbee9](https://github.com/bluehive-health/bluehive-sdk-python/commit/6bfbee94feae482a33366bc32249e0be8fb87a18))
* **types:** replace List[str] with SequenceNotStr in params ([4626a19](https://github.com/bluehive-health/bluehive-sdk-python/commit/4626a19ca1b46dd544b7f404519c30d4c595cd5d))


### Chores

* do not install brew dependencies in ./scripts/bootstrap by default ([4339c62](https://github.com/bluehive-health/bluehive-sdk-python/commit/4339c62ca013f8c1f3039011dc9433c04ee16e8b))
* **internal:** add Sequence related utils ([8cd442c](https://github.com/bluehive-health/bluehive-sdk-python/commit/8cd442cfa017bb5b8907c9e0a1828c8162629c0f))
* **internal:** move mypy configurations to `pyproject.toml` file ([0d4c86c](https://github.com/bluehive-health/bluehive-sdk-python/commit/0d4c86c1da12bf297fac299bbf36b7489d0e1421))
* **internal:** update pydantic dependency ([4d7dd02](https://github.com/bluehive-health/bluehive-sdk-python/commit/4d7dd0265c301da40e4c41761287e9ead841261a))
* **tests:** simplify `get_platform` test ([dcf2239](https://github.com/bluehive-health/bluehive-sdk-python/commit/dcf223975077ef67c796bf1c5eeb9374b8958771))
* **types:** change optional parameter type from NotGiven to Omit ([6ae1819](https://github.com/bluehive-health/bluehive-sdk-python/commit/6ae18194926e69fc615d51add1aadf8808842267))

## 0.1.0-alpha.9 (2025-08-27)

Full Changelog: [v0.1.0-alpha.8...v0.1.0-alpha.9](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.8...v0.1.0-alpha.9)

### Bug Fixes

* avoid newer type syntax ([3eb192a](https://github.com/bluehive-health/bluehive-sdk-python/commit/3eb192a9c2236839c9df644d481f16c9080bd472))


### Chores

* **internal:** change ci workflow machines ([cc6b943](https://github.com/bluehive-health/bluehive-sdk-python/commit/cc6b94314dfe2ff1709d61f1350967e08af858a6))
* **internal:** update pyright exclude list ([ad0c5d7](https://github.com/bluehive-health/bluehive-sdk-python/commit/ad0c5d726b5e71b3def2cdde214f11cd73f84c03))
* update github action ([9ada64d](https://github.com/bluehive-health/bluehive-sdk-python/commit/9ada64d8535118deb501a45cfbea5ea3ed9714dd))

## 0.1.0-alpha.8 (2025-08-13)

Full Changelog: [v0.1.0-alpha.7...v0.1.0-alpha.8](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.7...v0.1.0-alpha.8)

### Chores

* **internal:** codegen related update ([6f04aff](https://github.com/bluehive-health/bluehive-sdk-python/commit/6f04afff1ae3b0d1f7d984c591af132408d433b8))

## 0.1.0-alpha.7 (2025-08-09)

Full Changelog: [v0.1.0-alpha.6...v0.1.0-alpha.7](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.6...v0.1.0-alpha.7)

### Features

* **client:** support file upload requests ([97b5965](https://github.com/bluehive-health/bluehive-sdk-python/commit/97b59652bb608e71d907eac2edf2e31e9971f691))


### Chores

* **internal:** fix ruff target version ([14647cc](https://github.com/bluehive-health/bluehive-sdk-python/commit/14647cc4fffa3f022dded15d158a84f34dc433b9))
* **project:** add settings file for vscode ([c6ce060](https://github.com/bluehive-health/bluehive-sdk-python/commit/c6ce06020743ba8cf316a44f0694e61710b61edb))
* update @stainless-api/prism-cli to v5.15.0 ([85b2246](https://github.com/bluehive-health/bluehive-sdk-python/commit/85b2246ab0b26cc8efb0756893177dafa517b86a))

## 0.1.0-alpha.6 (2025-07-23)

Full Changelog: [v0.1.0-alpha.5...v0.1.0-alpha.6](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.5...v0.1.0-alpha.6)

### Bug Fixes

* **parsing:** parse extra field types ([cbedac0](https://github.com/bluehive-health/bluehive-sdk-python/commit/cbedac003fe3de81d86cf69dfc55badf63a8caa4))

## 0.1.0-alpha.5 (2025-07-22)

Full Changelog: [v0.1.0-alpha.4...v0.1.0-alpha.5](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.4...v0.1.0-alpha.5)

### Features

* clean up environment call outs ([3277aa1](https://github.com/bluehive-health/bluehive-sdk-python/commit/3277aa128c028148a893af9e23ac74ac0349654a))


### Bug Fixes

* **parsing:** ignore empty metadata ([937f49a](https://github.com/bluehive-health/bluehive-sdk-python/commit/937f49a01c0c6e7ac45880c16f1006b74bfb6133))

## 0.1.0-alpha.4 (2025-07-12)

Full Changelog: [v0.1.0-alpha.3...v0.1.0-alpha.4](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.3...v0.1.0-alpha.4)

### Bug Fixes

* **client:** don't send Content-Type header on GET requests ([2c2bbb9](https://github.com/bluehive-health/bluehive-sdk-python/commit/2c2bbb99f7774aeb7eaaf955c188819794376adc))


### Chores

* **readme:** fix version rendering on pypi ([933fd60](https://github.com/bluehive-health/bluehive-sdk-python/commit/933fd60ff623cb82bc3017b5180c73fea804b72a))

## 0.1.0-alpha.3 (2025-07-10)

Full Changelog: [v0.1.0-alpha.2...v0.1.0-alpha.3](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.2...v0.1.0-alpha.3)

### Bug Fixes

* **parsing:** correctly handle nested discriminated unions ([15d178d](https://github.com/bluehive-health/bluehive-sdk-python/commit/15d178d4a1ca566cff253150d6ee4e0ea55d9e2b))

## 0.1.0-alpha.2 (2025-07-09)

Full Changelog: [v0.1.0-alpha.1...v0.1.0-alpha.2](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.1.0-alpha.1...v0.1.0-alpha.2)

### Chores

* **internal:** bump pinned h11 dep ([77b8495](https://github.com/bluehive-health/bluehive-sdk-python/commit/77b84958a99fea04743c4aaf300731dedc61da3a))
* **package:** mark python 3.13 as supported ([e58a361](https://github.com/bluehive-health/bluehive-sdk-python/commit/e58a36108c35a42d3f665ac1972fe20d4afd7c54))

## 0.1.0-alpha.1 (2025-07-06)

Full Changelog: [v0.0.1-alpha.0...v0.1.0-alpha.1](https://github.com/bluehive-health/bluehive-sdk-python/compare/v0.0.1-alpha.0...v0.1.0-alpha.1)

### Features

* **api:** api update ([90448d7](https://github.com/bluehive-health/bluehive-sdk-python/commit/90448d76356b411bb678274c923ebf0d5d904218))


### Chores

* configure new SDK language ([d15c2c6](https://github.com/bluehive-health/bluehive-sdk-python/commit/d15c2c680ba6c46102b5b37fb3d9f31a66e5ba8d))
* update SDK settings ([4e5fa24](https://github.com/bluehive-health/bluehive-sdk-python/commit/4e5fa2407f9fcf01e7c25d040b4656246cb8d492))
* update SDK settings ([a9c06ff](https://github.com/bluehive-health/bluehive-sdk-python/commit/a9c06ff66ca3d06d5c6d1dc35458fbd387a5b7bc))
