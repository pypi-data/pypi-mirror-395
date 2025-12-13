# Changelog

## 1.21.0 (2025-12-07)

Full Changelog: [v1.20.0...v1.21.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.20.0...v1.21.0)

### Features

* **api:** added context_awareness and context ([ef1a752](https://github.com/deeprails/deeprails-sdk-python/commit/ef1a752f8426ac059c54830d34c98005538959aa))


### Bug Fixes

* ensure streams are always closed ([76fd1df](https://github.com/deeprails/deeprails-sdk-python/commit/76fd1dfa0d8ccfe9fbb2046882cf737b5ca6c865))


### Chores

* add Python 3.14 classifier and testing ([87c660e](https://github.com/deeprails/deeprails-sdk-python/commit/87c660e69f8509666d20a67a8cbabcd63aa67325))
* **deps:** mypy 1.18.1 has a regression, pin to 1.17 ([5d9ceab](https://github.com/deeprails/deeprails-sdk-python/commit/5d9ceabb224e620221a162a0fc56812629f5b2d7))
* **docs:** use environment variables for authentication in code snippets ([05bf7de](https://github.com/deeprails/deeprails-sdk-python/commit/05bf7de49c385433a792058e1d40474840ff3b87))
* update lockfile ([38655f6](https://github.com/deeprails/deeprails-sdk-python/commit/38655f6e1b8f9984e9bc2256a80b7018fa28b295))

## 1.20.0 (2025-11-20)

Full Changelog: [v1.19.0...v1.20.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.19.0...v1.20.0)

### Features

* **api:** fix files upload parameter ([a3e0a11](https://github.com/deeprails/deeprails-sdk-python/commit/a3e0a118e36ae4e4133b42ed57e74692d8052d8f))

## 1.19.0 (2025-11-19)

Full Changelog: [v1.18.0...v1.19.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.18.0...v1.19.0)

### Features

* **api:** Minor changes and updates to examples ([804c8be](https://github.com/deeprails/deeprails-sdk-python/commit/804c8bea03fa1f8cbee47e0858a04ba88cce3d8f))
* **api:** Update pyproject.toml ([4ed51b6](https://github.com/deeprails/deeprails-sdk-python/commit/4ed51b6c313d8a77ec1c9b685b90df8dc1840194))

## 1.18.0 (2025-11-19)

Full Changelog: [v1.17.0...v1.18.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.17.0...v1.18.0)

### Features

* **api:** update package name casing ([0173666](https://github.com/deeprails/deeprails-sdk-python/commit/0173666c5971633c10221bbb0d4962fac233ce48))

## 1.17.0 (2025-11-18)

Full Changelog: [v1.16.0...v1.17.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.16.0...v1.17.0)

### Features

* **api:** revert docs URL ([17ce0e7](https://github.com/deeprails/deeprails-sdk-python/commit/17ce0e774049a9140cb20d6a4994820e70cf5911))

## 1.16.0 (2025-11-18)

Full Changelog: [v1.15.0...v1.16.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.15.0...v1.16.0)

### Features

* **api:** update docs URL ([587d5fb](https://github.com/deeprails/deeprails-sdk-python/commit/587d5fbc58e5bec2f89ee8c48f9815b4cb169caa))

## 1.15.0 (2025-11-12)

Full Changelog: [v1.14.0...v1.15.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.14.0...v1.15.0)

### Features

* **api:** remove dev server ([aee58f7](https://github.com/deeprails/deeprails-sdk-python/commit/aee58f7a369729f5b50030f722a02b6da9abd88c))


### Bug Fixes

* compat with Python 3.14 ([f319169](https://github.com/deeprails/deeprails-sdk-python/commit/f319169022a0fe5992e335dc63a00c9bc47d95d8))
* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([02e642b](https://github.com/deeprails/deeprails-sdk-python/commit/02e642b8fa4f10e49014187ae8887a4dcc1f8a66))


### Chores

* **package:** drop Python 3.8 support ([25663d6](https://github.com/deeprails/deeprails-sdk-python/commit/25663d6698f6b61125f60d5fc0ba8a0ec26a800c))

## 1.14.0 (2025-11-11)

Full Changelog: [v1.13.0...v1.14.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.13.0...v1.14.0)

### Features

* **api:** add retrieve monitor event and examples ([b295221](https://github.com/deeprails/deeprails-sdk-python/commit/b2952212f394e8947c900735a5841b78bf8ec729))

## 1.13.0 (2025-11-10)

Full Changelog: [v1.12.0...v1.13.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.12.0...v1.13.0)

### Features

* **api:** Mass restructuring of API, including response bodies and naming schemes ([c72cf32](https://github.com/deeprails/deeprails-sdk-python/commit/c72cf32b37a41673c895a172dd09dcbe90b6ce40))


### Chores

* **internal:** grammar fix (it's -&gt; its) ([11449b2](https://github.com/deeprails/deeprails-sdk-python/commit/11449b27a513a1c5b5b35ba88778c636582feb0b))

## 1.12.0 (2025-11-02)

Full Changelog: [v1.11.0...v1.12.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.11.0...v1.12.0)

### Features

* **api:** restructure monitor service ([47cac0a](https://github.com/deeprails/deeprails-sdk-python/commit/47cac0a5568f3f73619ccb34e701901468dffbd0))


### Chores

* **internal/tests:** avoid race condition with implicit client cleanup ([0413192](https://github.com/deeprails/deeprails-sdk-python/commit/0413192c31932a21cd34cc4fe63669914a1d1de3))

## 1.11.0 (2025-10-30)

Full Changelog: [v1.10.0...v1.11.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.10.0...v1.11.0)

### Features

* **api:** Add file and web search as extended ai capabilities ([fc2bb8d](https://github.com/deeprails/deeprails-sdk-python/commit/fc2bb8d0ce8f111279583398469ae9bc0d11d474))
* **api:** manual updates ([236c2a9](https://github.com/deeprails/deeprails-sdk-python/commit/236c2a923f7bcaa08f92a799be9ca725a0a3b53b))


### Bug Fixes

* **client:** close streams without requiring full consumption ([db832f6](https://github.com/deeprails/deeprails-sdk-python/commit/db832f6e4067940c762e5d0be9d57cbaf72c7309))

## 1.10.0 (2025-10-29)

Full Changelog: [v1.9.0...v1.10.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.9.0...v1.10.0)

### Features

* **api:** remove evaluate api ([a3ddec1](https://github.com/deeprails/deeprails-sdk-python/commit/a3ddec1696eaa1247eea2a3bffd61e63d6537d30))
* **api:** remove evaluate references ([23519a3](https://github.com/deeprails/deeprails-sdk-python/commit/23519a3349a254fe2fe24a51aeb59545d0820b70))

## 1.9.0 (2025-10-24)

Full Changelog: [v1.8.0...v1.9.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.8.0...v1.9.0)

### Features

* **api:** remove apiresponse from monitor ([4971a99](https://github.com/deeprails/deeprails-sdk-python/commit/4971a99c7357bebbc5e86a2d76d2be55bb34f5ae))

## 1.8.0 (2025-10-22)

Full Changelog: [v1.7.0...v1.8.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.7.0...v1.8.0)

### Features

* **api:** manual updates ([4b46121](https://github.com/deeprails/deeprails-sdk-python/commit/4b461213615578ca0382f044201c8343d4e9f167))

## 1.7.0 (2025-10-22)

Full Changelog: [v1.6.1...v1.7.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.6.1...v1.7.0)

### Features

* **api:** update defend naming and data structures ([ba934de](https://github.com/deeprails/deeprails-sdk-python/commit/ba934de8812d71da159a00fa8283876e682aeb7b))

## 1.6.1 (2025-10-22)

Full Changelog: [v1.6.0...v1.6.1](https://github.com/deeprails/deeprails-sdk-python/compare/v1.6.0...v1.6.1)

### Chores

* bump `httpx-aiohttp` version to 0.1.9 ([fde0f65](https://github.com/deeprails/deeprails-sdk-python/commit/fde0f65f5947336baeee5ae71d7ad49fa8aefc98))

## 1.6.0 (2025-10-20)

Full Changelog: [v1.5.0...v1.6.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.5.0...v1.6.0)

### Features

* **api:** readme example update ([412839e](https://github.com/deeprails/deeprails-sdk-python/commit/412839e484bcc4b216b88ea3f22849dc9355b643))

## 1.5.0 (2025-10-16)

Full Changelog: [v1.4.1...v1.5.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.4.1...v1.5.0)

### Features

* **api:** adding support for system_prompt and ground_truth ([be4cd74](https://github.com/deeprails/deeprails-sdk-python/commit/be4cd74a118dc1e4b1ef90f25f311a0862807176))

## 1.4.1 (2025-10-11)

Full Changelog: [v1.4.0...v1.4.1](https://github.com/deeprails/deeprails-sdk-python/compare/v1.4.0...v1.4.1)

### Chores

* **internal:** detect missing future annotations with ruff ([c0b084c](https://github.com/deeprails/deeprails-sdk-python/commit/c0b084c0f0e71a600274186c30902246aa3816d1))

## 1.4.0 (2025-10-10)

Full Changelog: [v1.3.0...v1.4.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.3.0...v1.4.0)

### Features

* **api:** manual updates ([b6beebc](https://github.com/deeprails/deeprails-sdk-python/commit/b6beebca6323df5ae35ef30d419d96c831bebbb8))

## 1.3.0 (2025-10-08)

Full Changelog: [v1.2.0...v1.3.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.2.0...v1.3.0)

### Features

* **api:** adding code samples ([c7f7565](https://github.com/deeprails/deeprails-sdk-python/commit/c7f7565abd00233d22d9c11a5b2c977414e03439))
* **api:** manual updates ([145946a](https://github.com/deeprails/deeprails-sdk-python/commit/145946a049fb29bff01df6763248330f4d0030ad))

## 1.2.0 (2025-10-07)

Full Changelog: [v1.1.0...v1.2.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.1.0...v1.2.0)

### Features

* **api:** manual updates ([db3e710](https://github.com/deeprails/deeprails-sdk-python/commit/db3e710d267ccf8d99aa214348846e20b6484db6))

## 1.1.0 (2025-10-07)

Full Changelog: [v1.0.0...v1.1.0](https://github.com/deeprails/deeprails-sdk-python/compare/v1.0.0...v1.1.0)

### Features

* **api:** manual updates ([e55683b](https://github.com/deeprails/deeprails-sdk-python/commit/e55683b590ff636e7c876a172c22c52c3208ceda))
* **api:** manual updates ([3309c85](https://github.com/deeprails/deeprails-sdk-python/commit/3309c859f9e67579bcd9d2f2d82ed7d67609dca8))


### Chores

* update SDK settings ([9b65ba6](https://github.com/deeprails/deeprails-sdk-python/commit/9b65ba6e8675011f89f035d608a404d7c1d50453))
* update SDK settings ([957c361](https://github.com/deeprails/deeprails-sdk-python/commit/957c3611f3baf773270a491c66a28b8eeb66d671))
* update SDK settings ([3dcb5cb](https://github.com/deeprails/deeprails-sdk-python/commit/3dcb5cb41ee6c1008f66dace32125fd38626bdca))
* update SDK settings ([b283586](https://github.com/deeprails/deeprails-sdk-python/commit/b28358658ea8cbea0d2cb679343a9cf1c342fbd2))

## 1.0.0 (2025-10-07)

Full Changelog: [v0.0.1...v1.0.0](https://github.com/deeprails/deeprails-python-sdk/compare/v0.0.1...v1.0.0)

### Chores

* update SDK settings ([3dcb5cb](https://github.com/deeprails/deeprails-python-sdk/commit/3dcb5cb41ee6c1008f66dace32125fd38626bdca))
* update SDK settings ([b283586](https://github.com/deeprails/deeprails-python-sdk/commit/b28358658ea8cbea0d2cb679343a9cf1c342fbd2))
