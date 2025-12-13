# Changelog

## 0.1.0-alpha.11 (2025-12-09)

Full Changelog: [v0.1.0-alpha.10...v0.1.0-alpha.11](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.10...v0.1.0-alpha.11)

### Bug Fixes

* **types:** allow pyright to infer TypedDict types within SequenceNotStr ([585abce](https://github.com/dataleonlabs/dataleon-python/commit/585abce89402cc04db3b615e2fe7a4fe326ae050))


### Chores

* **docs:** use environment variables for authentication in code snippets ([1d81c65](https://github.com/dataleonlabs/dataleon-python/commit/1d81c65da902441733d48cb5fe0d7025cdf4c64e))
* update lockfile ([a997c5c](https://github.com/dataleonlabs/dataleon-python/commit/a997c5cb97edd53c92343e375157362eeaa790b6))

## 0.1.0-alpha.10 (2025-11-28)

Full Changelog: [v0.1.0-alpha.9...v0.1.0-alpha.10](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.9...v0.1.0-alpha.10)

### Bug Fixes

* ensure streams are always closed ([0d8605e](https://github.com/dataleonlabs/dataleon-python/commit/0d8605e54f9acc005818c650d64b543b083f33e8))


### Chores

* add Python 3.14 classifier and testing ([0991740](https://github.com/dataleonlabs/dataleon-python/commit/09917407984dd689b1cb7f027ec4737b7f84ff47))
* **deps:** mypy 1.18.1 has a regression, pin to 1.17 ([2b2f28d](https://github.com/dataleonlabs/dataleon-python/commit/2b2f28dafd71092b613593bab16e9902c404ef87))

## 0.1.0-alpha.9 (2025-11-12)

Full Changelog: [v0.1.0-alpha.8...v0.1.0-alpha.9](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.8...v0.1.0-alpha.9)

### Bug Fixes

* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([1d2221f](https://github.com/dataleonlabs/dataleon-python/commit/1d2221f6788945490997f0eea15615905fef86f9))

## 0.1.0-alpha.8 (2025-11-11)

Full Changelog: [v0.1.0-alpha.7...v0.1.0-alpha.8](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.7...v0.1.0-alpha.8)

### Bug Fixes

* compat with Python 3.14 ([87a4a57](https://github.com/dataleonlabs/dataleon-python/commit/87a4a579ec5d3933a87a7d3c4b94ba97191aa5b8))


### Chores

* **internal/tests:** avoid race condition with implicit client cleanup ([16a7270](https://github.com/dataleonlabs/dataleon-python/commit/16a72708bc147c733854ad05e62d5225f79290bd))
* **internal:** grammar fix (it's -&gt; its) ([0d337f6](https://github.com/dataleonlabs/dataleon-python/commit/0d337f6a8784093bf9fde3c7136ad94d55e315d9))
* **package:** drop Python 3.8 support ([8ba1eb6](https://github.com/dataleonlabs/dataleon-python/commit/8ba1eb66b3335afc842a7036cac2116d7b699945))

## 0.1.0-alpha.7 (2025-10-30)

Full Changelog: [v0.1.0-alpha.6...v0.1.0-alpha.7](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.6...v0.1.0-alpha.7)

### Bug Fixes

* **client:** close streams without requiring full consumption ([48f0100](https://github.com/dataleonlabs/dataleon-python/commit/48f01007da66b137cb540a577b77cb99839c0f14))


### Chores

* bump `httpx-aiohttp` version to 0.1.9 ([a2d5e8b](https://github.com/dataleonlabs/dataleon-python/commit/a2d5e8b6e27e5b3f2bf3815ee9dbe0e5b68afc93))

## 0.1.0-alpha.6 (2025-10-14)

Full Changelog: [v0.1.0-alpha.5...v0.1.0-alpha.6](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.5...v0.1.0-alpha.6)

### Features

* **api:** api update ([5e6943f](https://github.com/dataleonlabs/dataleon-python/commit/5e6943fc5724b9bf19cb8958b6d06f4b0abefcaf))


### Chores

* **internal:** detect missing future annotations with ruff ([7ed7019](https://github.com/dataleonlabs/dataleon-python/commit/7ed7019f18938d0b0ac99c18478696bb352dfd63))

## 0.1.0-alpha.5 (2025-09-20)

Full Changelog: [v0.1.0-alpha.4...v0.1.0-alpha.5](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.4...v0.1.0-alpha.5)

### Chores

* do not install brew dependencies in ./scripts/bootstrap by default ([6a205a7](https://github.com/dataleonlabs/dataleon-python/commit/6a205a725a4ab48a90c8b4a54ef68d3d3e85b068))
* **internal:** update pydantic dependency ([59a4c39](https://github.com/dataleonlabs/dataleon-python/commit/59a4c398f569e19bda1dabb3ea4b4e5e5d2a5bc1))
* **types:** change optional parameter type from NotGiven to Omit ([70511ef](https://github.com/dataleonlabs/dataleon-python/commit/70511ef335ba875c0e03677349c44ab7a2609989))

## 0.1.0-alpha.4 (2025-09-10)

Full Changelog: [v0.1.0-alpha.3...v0.1.0-alpha.4](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.3...v0.1.0-alpha.4)

### Features

* **api:** api update ([31746e1](https://github.com/dataleonlabs/dataleon-python/commit/31746e1b0fcbab12448d9b3780e9481c751a4b3b))

## 0.1.0-alpha.3 (2025-09-06)

Full Changelog: [v0.1.0-alpha.2...v0.1.0-alpha.3](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.2...v0.1.0-alpha.3)

### Features

* improve future compat with pydantic v3 ([30807f3](https://github.com/dataleonlabs/dataleon-python/commit/30807f30670da75cef8c342c19e355f15adc165f))
* **types:** replace List[str] with SequenceNotStr in params ([b73bbd4](https://github.com/dataleonlabs/dataleon-python/commit/b73bbd4c876fc07eeb5e0c19db5a7d8bbcded4b4))


### Chores

* **internal:** add Sequence related utils ([6c5b46a](https://github.com/dataleonlabs/dataleon-python/commit/6c5b46a0d05188191626dd2887c52697944715d6))
* **internal:** move mypy configurations to `pyproject.toml` file ([9dd6b45](https://github.com/dataleonlabs/dataleon-python/commit/9dd6b45269b8a5d01ad61bfb73bd492c3c31c75c))
* **tests:** simplify `get_platform` test ([3cfdd7f](https://github.com/dataleonlabs/dataleon-python/commit/3cfdd7f302450237efa48f99d495d3bafc82bbf0))

## 0.1.0-alpha.2 (2025-08-27)

Full Changelog: [v0.1.0-alpha.1...v0.1.0-alpha.2](https://github.com/dataleonlabs/dataleon-python/compare/v0.1.0-alpha.1...v0.1.0-alpha.2)

### Features

* **api:** manual updates ([0b33943](https://github.com/dataleonlabs/dataleon-python/commit/0b339436d2404824f84db4cbb3a1d7dbfce4e648))

## 0.1.0-alpha.1 (2025-08-27)

Full Changelog: [v0.0.1-alpha.0...v0.1.0-alpha.1](https://github.com/dataleonlabs/dataleon-python/compare/v0.0.1-alpha.0...v0.1.0-alpha.1)

### Features

* **api:** api update ([ec2a77c](https://github.com/dataleonlabs/dataleon-python/commit/ec2a77c58ca2f109464ae026f527aaba5b7dbed2))
* **api:** api update ([7ded36e](https://github.com/dataleonlabs/dataleon-python/commit/7ded36ec68b2b2c522ea546049903242642a3c83))
* **api:** api update ([0b0f975](https://github.com/dataleonlabs/dataleon-python/commit/0b0f975bd9db1c7b41bf2654f3bb07ad97376b25))
* **api:** api update ([b865d6b](https://github.com/dataleonlabs/dataleon-python/commit/b865d6b5d9771883b2f5cd5c2fdd9d406b345c8b))
* **api:** api update ([60e3cfa](https://github.com/dataleonlabs/dataleon-python/commit/60e3cfa6959dd5997caba9da5b20701a6b17ce1c))
* **api:** api update ([1a991a6](https://github.com/dataleonlabs/dataleon-python/commit/1a991a605afaecea9533408e3719a98f0c860bbf))
* **api:** api update ([9752cda](https://github.com/dataleonlabs/dataleon-python/commit/9752cda974ff7534c225a0b3c6abaf5abf26664f))
* **api:** api update ([817c5a9](https://github.com/dataleonlabs/dataleon-python/commit/817c5a9a62e8d5596413fbb63332c05ac6a94e36))
* **api:** api update ([0d7cfa1](https://github.com/dataleonlabs/dataleon-python/commit/0d7cfa1f9bf9f4ff95ab4b34d981682bd5c53f68))
* **api:** api update ([b712b46](https://github.com/dataleonlabs/dataleon-python/commit/b712b460b45af0344f8e678620955aab24ae4b1e))
* **api:** api update ([682aa0d](https://github.com/dataleonlabs/dataleon-python/commit/682aa0d71c263dff0a05f99ad643036fdb8c3a2f))
* **api:** manual updates ([4eb679e](https://github.com/dataleonlabs/dataleon-python/commit/4eb679e80eda3416cdbc7f000580bf69f696d224))
* **api:** manual updates ([de826b6](https://github.com/dataleonlabs/dataleon-python/commit/de826b69b93cc0776c8032a9490bef99d073125f))
* **api:** manual updates ([a72956b](https://github.com/dataleonlabs/dataleon-python/commit/a72956bde35f40058e261b24b2c635f3d5a31864))
* **api:** manual updates ([c5ff92d](https://github.com/dataleonlabs/dataleon-python/commit/c5ff92d36e000542bf41b0b1f4c07727f43f0d71))
* **api:** update via SDK Studio ([b5194b9](https://github.com/dataleonlabs/dataleon-python/commit/b5194b93e2deffef6734e6917a82fd1fcc45b1c7))
* **api:** update via SDK Studio ([a300449](https://github.com/dataleonlabs/dataleon-python/commit/a300449dfbf14cd2bd659eba4dd05cd84797522b))
* **api:** update via SDK Studio ([889a514](https://github.com/dataleonlabs/dataleon-python/commit/889a5144f675cae403f426fc894934e464dcb2a9))
* **api:** update via SDK Studio ([2bad5fe](https://github.com/dataleonlabs/dataleon-python/commit/2bad5fe5a06cd13e36685633593f6637437dd0f9))
* **api:** update via SDK Studio ([8530726](https://github.com/dataleonlabs/dataleon-python/commit/85307267a962d22fdecef8395523d4e5a8930f1a))
* **api:** update via SDK Studio ([77c6b67](https://github.com/dataleonlabs/dataleon-python/commit/77c6b679d5b9fedcc443b8030908e24cdef07c49))
* **api:** update via SDK Studio ([a61e1cc](https://github.com/dataleonlabs/dataleon-python/commit/a61e1cc00d6f9bdf466fb4eef1f5858faffd46f6))
* **api:** update via SDK Studio ([83a224d](https://github.com/dataleonlabs/dataleon-python/commit/83a224dafe5bc09eabdd8eac71f8b819667b116d))
* **api:** update via SDK Studio ([aa6d764](https://github.com/dataleonlabs/dataleon-python/commit/aa6d764aa50a0153168c6904962ec5ee2679d736))


### Bug Fixes

* avoid newer type syntax ([2535c11](https://github.com/dataleonlabs/dataleon-python/commit/2535c117430d3679577f469e1352edfd6f573600))


### Chores

* **internal:** change ci workflow machines ([d67b2d3](https://github.com/dataleonlabs/dataleon-python/commit/d67b2d3b7ee3fee369eb6c1fd3862fd88af0d55c))
* **internal:** codegen related update ([f146cbf](https://github.com/dataleonlabs/dataleon-python/commit/f146cbf3c177b2b5d103fb5fae7226e9f7b117d1))
* **internal:** update comment in script ([e720cfd](https://github.com/dataleonlabs/dataleon-python/commit/e720cfdd3e15e2db39c6ed410e554a40d41072aa))
* **internal:** update pyright exclude list ([a5a6c90](https://github.com/dataleonlabs/dataleon-python/commit/a5a6c90735519474c5cb6371bccfab1f631c2577))
* update @stainless-api/prism-cli to v5.15.0 ([24c0124](https://github.com/dataleonlabs/dataleon-python/commit/24c0124e940eb14511a84a2ffed47d92a74b313c))
* update github action ([c6f64fd](https://github.com/dataleonlabs/dataleon-python/commit/c6f64fdf9404988f70e81a481905b1bc8ed9bf51))
* update SDK settings ([0aefed1](https://github.com/dataleonlabs/dataleon-python/commit/0aefed135a6291bf3989ae7119ce427f2bcf1f77))
* update SDK settings ([9d19ee4](https://github.com/dataleonlabs/dataleon-python/commit/9d19ee49d23a9c2f010d095ae88c3d97af8a9066))
