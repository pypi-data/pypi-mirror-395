# Changelog

## 1.21.0-beta.22 (2025-12-08)

Full Changelog: [v1.21.0-beta.21...v1.21.0-beta.22](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.21...v1.21.0-beta.22)

### Bug Fixes

* **types:** allow pyright to infer TypedDict types within SequenceNotStr ([797f2cd](https://github.com/stainless-sdks/sink-python-public/commit/797f2cd2b832ed79205a9a11739c55652ed89e2b))


### Chores

* add missing docstrings ([6583f5d](https://github.com/stainless-sdks/sink-python-public/commit/6583f5d3685eab3979e5fe055ac365ac8f779f08))
* **docs:** use environment variables for authentication in code snippets ([376ceaf](https://github.com/stainless-sdks/sink-python-public/commit/376ceaf74289fe98e3a90fd3ae19b4097193b1ff))
* update lockfile ([5452578](https://github.com/stainless-sdks/sink-python-public/commit/5452578b07e2195d3b4a41a716d26c6fef4ba0c8))

## 1.21.0-beta.21 (2025-11-28)

Full Changelog: [v1.21.0-beta.20...v1.21.0-beta.21](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.20...v1.21.0-beta.21)

### Bug Fixes

* ensure streams are always closed ([be96fb7](https://github.com/stainless-sdks/sink-python-public/commit/be96fb72f759209844955879f0fc0b636ec42816))


### Chores

* add Python 3.14 classifier and testing ([98c1483](https://github.com/stainless-sdks/sink-python-public/commit/98c1483c69e12a764e919ec8939ef08f919df951))
* **deps:** mypy 1.18.1 has a regression, pin to 1.17 ([961a039](https://github.com/stainless-sdks/sink-python-public/commit/961a03962460dd8da8e45441734c4665c2142446))

## 1.21.0-beta.20 (2025-11-12)

Full Changelog: [v1.21.0-beta.19...v1.21.0-beta.20](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.19...v1.21.0-beta.20)

### Bug Fixes

* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([e1c05d9](https://github.com/stainless-sdks/sink-python-public/commit/e1c05d96c275be188a39fe2fc2cc7a02a2b5b619))

## 1.21.0-beta.19 (2025-11-11)

Full Changelog: [v1.21.0-beta.18...v1.21.0-beta.19](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.18...v1.21.0-beta.19)

### Bug Fixes

* compat with Python 3.14 ([1ccb5e1](https://github.com/stainless-sdks/sink-python-public/commit/1ccb5e120ba6b07b3c878f3230c4bbbf08a8437a))


### Chores

* **internal/tests:** avoid race condition with implicit client cleanup ([1bd3c5c](https://github.com/stainless-sdks/sink-python-public/commit/1bd3c5c5da27831dfbfc7fd4b884d764a753406f))
* **internal:** grammar fix (it's -&gt; its) ([f1c65f6](https://github.com/stainless-sdks/sink-python-public/commit/f1c65f67a4347e7a36b82f9da0d799d5ab86bbaf))
* **package:** drop Python 3.8 support ([1d95d36](https://github.com/stainless-sdks/sink-python-public/commit/1d95d369a0a2bb63a62c0b1f6565ed6892cf4caa))

## 1.21.0-beta.18 (2025-10-30)

Full Changelog: [v1.21.0-beta.17...v1.21.0-beta.18](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.17...v1.21.0-beta.18)

### Bug Fixes

* **client:** close streams without requiring full consumption ([047f1bc](https://github.com/stainless-sdks/sink-python-public/commit/047f1bcfc2cb1603e25da272b98f7c4648bf8a99))


### Chores

* bump `httpx-aiohttp` version to 0.1.9 ([211d0c6](https://github.com/stainless-sdks/sink-python-public/commit/211d0c6fe60ae2542195963b7b50478c7b64965f))
* **internal:** detect missing future annotations with ruff ([bee4ded](https://github.com/stainless-sdks/sink-python-public/commit/bee4dedba3c79ffd32239374acf2f4fa04290020))

## 1.21.0-beta.17 (2025-09-30)

Full Changelog: [v1.21.0-beta.16...v1.21.0-beta.17](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.16...v1.21.0-beta.17)

### Bug Fixes

* do not set headers with default to omit ([e7bbefc](https://github.com/stainless-sdks/sink-python-public/commit/e7bbefc3e6e935f033a0b00307e5348a4ca02c5c))

## 1.21.0-beta.16 (2025-09-25)

Full Changelog: [v1.21.0-beta.15...v1.21.0-beta.16](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.15...v1.21.0-beta.16)

### Features

* **api:** manual updates ([8dec50d](https://github.com/stainless-sdks/sink-python-public/commit/8dec50d265dcefa840d356423219bdd8983e8093))
* **client:** add support for verifying signatures on incoming webhooks ([1a2bcf5](https://github.com/stainless-sdks/sink-python-public/commit/1a2bcf5cff9fdf71981b0b5c66b2db3f4fc1a9e3))
* **client:** support file upload requests ([a1388bd](https://github.com/stainless-sdks/sink-python-public/commit/a1388bd61dec4b362228621a64c321e6569042fa))
* improve future compat with pydantic v3 ([0c4f194](https://github.com/stainless-sdks/sink-python-public/commit/0c4f19445cdc6899693e27217643244ef3b08414))
* **types:** replace List[str] with SequenceNotStr in params ([e3d87a1](https://github.com/stainless-sdks/sink-python-public/commit/e3d87a1f3e2890bb2b6db4ac96be000b064b0296))


### Bug Fixes

* avoid newer type syntax ([60d3f4e](https://github.com/stainless-sdks/sink-python-public/commit/60d3f4e800d1d9053e25eba9e56bd18fbee75327))
* **compat:** compat with `pydantic&lt;2.8.0` when using additional fields ([eefc324](https://github.com/stainless-sdks/sink-python-public/commit/eefc3245d101feefb291b9f430b0380b15f4e6e5))
* **project:** make webhooks dependency optional ([37315bf](https://github.com/stainless-sdks/sink-python-public/commit/37315bf9ceeba01ae6071e719f332771e36edb47))


### Chores

* do not install brew dependencies in ./scripts/bootstrap by default ([163a825](https://github.com/stainless-sdks/sink-python-public/commit/163a825fa0c8d57169309ce5dbf606755facc562))
* improve example values ([cafa651](https://github.com/stainless-sdks/sink-python-public/commit/cafa65110de56267ce2ac12a22b2d6701c1ad06a))
* **internal:** add Sequence related utils ([c12467f](https://github.com/stainless-sdks/sink-python-public/commit/c12467f556566116e2a5c69d7ba67bc0f9485034))
* **internal:** change ci workflow machines ([c486c3f](https://github.com/stainless-sdks/sink-python-public/commit/c486c3fe5b8ca886df483532b926416ba0e244a1))
* **internal:** fix ruff target version ([1f06944](https://github.com/stainless-sdks/sink-python-public/commit/1f069445f71773b865cbab76ebc014180aa00bd6))
* **internal:** minor formatting change ([b21c7c4](https://github.com/stainless-sdks/sink-python-public/commit/b21c7c40c2ca6118867842709e6e0103d3d632f7))
* **internal:** move mypy configurations to `pyproject.toml` file ([bae3739](https://github.com/stainless-sdks/sink-python-public/commit/bae373914185bb547328814e45fb359563315d24))
* **internal:** update comment in script ([a6d1506](https://github.com/stainless-sdks/sink-python-public/commit/a6d1506089615c6828ec2e2ecf9b537ed6001dd7))
* **internal:** update pydantic dependency ([cdd62ac](https://github.com/stainless-sdks/sink-python-public/commit/cdd62aca3128b7579117297b25ee67e5c566fda6))
* **internal:** update pyright exclude list ([74e2185](https://github.com/stainless-sdks/sink-python-public/commit/74e218598b92439d33fabf7d41c483aeca7bce19))
* remove accidental webhooks changes ([e45f53d](https://github.com/stainless-sdks/sink-python-public/commit/e45f53d031c93471dd2e6a17ff881ee103014221))
* **tests:** simplify `get_platform` test ([121d46b](https://github.com/stainless-sdks/sink-python-public/commit/121d46bd9120ef385debde40d6221efc368f0b29))
* **types:** change optional parameter type from NotGiven to Omit ([f004717](https://github.com/stainless-sdks/sink-python-public/commit/f0047172e4a962aa5f7f380843294122f3ef7405))
* update @stainless-api/prism-cli to v5.15.0 ([670fda8](https://github.com/stainless-sdks/sink-python-public/commit/670fda8e135b3a66badf5efb5d73a761b39244d2))
* update github action ([8313cf4](https://github.com/stainless-sdks/sink-python-public/commit/8313cf45367b332889aba20177a133cd3c10475f))

## 1.21.0-beta.15 (2025-07-30)

Full Changelog: [v1.21.0-beta.14...v1.21.0-beta.15](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.14...v1.21.0-beta.15)

### Features

* **api:** manual updates ([744f988](https://github.com/stainless-sdks/sink-python-public/commit/744f9880e1ca3d2b74db783d63f64cf4449fc9ee))


### Chores

* **project:** add settings file for vscode ([68c0de9](https://github.com/stainless-sdks/sink-python-public/commit/68c0de9fbe85a9b3b302db3217520e75a2e7fed5))

## 1.21.0-beta.14 (2025-07-23)

Full Changelog: [v1.21.0-beta.13...v1.21.0-beta.14](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.13...v1.21.0-beta.14)

### Bug Fixes

* **parsing:** parse extra field types ([fbcb486](https://github.com/stainless-sdks/sink-python-public/commit/fbcb48675eac12fe6c1f0a045963803fd700a307))


### Chores

* **types:** rebuild Pydantic models after all types are defined ([1a9e55e](https://github.com/stainless-sdks/sink-python-public/commit/1a9e55ee32ad85c4a7e9fa2af3562ebb9d6446f3))

## 1.21.0-beta.13 (2025-07-22)

Full Changelog: [v1.21.0-beta.12...v1.21.0-beta.13](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.12...v1.21.0-beta.13)

### Features

* clean up environment call outs ([1c51771](https://github.com/stainless-sdks/sink-python-public/commit/1c51771b877ea07d6c8016a6ae67069a37531519))


### Bug Fixes

* **parsing:** ignore empty metadata ([f5da772](https://github.com/stainless-sdks/sink-python-public/commit/f5da7725245288e8c4a16b472f0d4b103bcf63f7))

## 1.21.0-beta.12 (2025-07-12)

Full Changelog: [v1.21.0-beta.11...v1.21.0-beta.12](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.11...v1.21.0-beta.12)

### Bug Fixes

* **client:** don't send Content-Type header on GET requests ([5a2a2ea](https://github.com/stainless-sdks/sink-python-public/commit/5a2a2eaeafcb7a7c6a13f91bab3a6bd82e29b5d3))


### Chores

* **readme:** fix version rendering on pypi ([ea0ac09](https://github.com/stainless-sdks/sink-python-public/commit/ea0ac09eb0cd2e0ffa75ca3ed2fe29a4bd0c1274))

## 1.21.0-beta.11 (2025-07-10)

Full Changelog: [v1.21.0-beta.10...v1.21.0-beta.11](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.10...v1.21.0-beta.11)

### Bug Fixes

* **parsing:** correctly handle nested discriminated unions ([de1f36a](https://github.com/stainless-sdks/sink-python-public/commit/de1f36a652a217e45573abd187678d5eb5b75f7c))


### Chores

* **package:** mark python 3.13 as supported ([5e9a27b](https://github.com/stainless-sdks/sink-python-public/commit/5e9a27be213237701641c3d700c34a77bd6f2f6c))

## 1.21.0-beta.10 (2025-07-09)

Full Changelog: [v1.21.0-beta.9...v1.21.0-beta.10](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.9...v1.21.0-beta.10)

### Features

* **api:** manual updates ([69050ab](https://github.com/stainless-sdks/sink-python-public/commit/69050ab7fc872700e0659e270ef3034687910386))


### Chores

* **internal:** bump pinned h11 dep ([b23a35c](https://github.com/stainless-sdks/sink-python-public/commit/b23a35ccb92af871a45f3f59c41b05bbd30be5c9))

## 1.21.0-beta.9 (2025-07-08)

Full Changelog: [v1.21.0-beta.8...v1.21.0-beta.9](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.8...v1.21.0-beta.9)

### Chores

* **ci:** change upload type ([1993f42](https://github.com/stainless-sdks/sink-python-public/commit/1993f4235b192da3df5da4685d6d7182a8446666))
* **internal:** codegen related update ([bf54338](https://github.com/stainless-sdks/sink-python-public/commit/bf543387e5b0341c006de1df239e0176d190db28))
* **types:** use string-based forward references for cyclic types ([bbee9dd](https://github.com/stainless-sdks/sink-python-public/commit/bbee9dd939c7e1e01d6bfd77c5ffdd28cf624b4f))

## 1.21.0-beta.8 (2025-06-30)

Full Changelog: [v1.21.0-beta.7...v1.21.0-beta.8](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.7...v1.21.0-beta.8)

### Bug Fixes

* **ci:** correct conditional ([9d6648c](https://github.com/stainless-sdks/sink-python-public/commit/9d6648c3795756b976b54049845823789eecfd09))
* **ci:** release-doctor — report correct token name ([975f1d2](https://github.com/stainless-sdks/sink-python-public/commit/975f1d25c4bc2e52eb6a996fddef078342297927))


### Chores

* **ci:** only run for pushes and fork pull requests ([496f412](https://github.com/stainless-sdks/sink-python-public/commit/496f4124e6ca1ad2bce7e4e12b9554ad317cd7ae))

## 1.21.0-beta.7 (2025-06-26)

Full Changelog: [v1.21.0-beta.6...v1.21.0-beta.7](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.6...v1.21.0-beta.7)

### Features

* **client:** add follow_redirects request option ([1bae0fd](https://github.com/stainless-sdks/sink-python-public/commit/1bae0fd0ca0521166e6546640a738cf062b96dcf))
* **client:** add support for aiohttp ([fad22dc](https://github.com/stainless-sdks/sink-python-public/commit/fad22dcedaf943d5fb49427bd1a48071df4d2ee4))


### Bug Fixes

* **client:** correctly parse binary response | stream ([56d65f5](https://github.com/stainless-sdks/sink-python-public/commit/56d65f5d12c14f4383ffaca8fc90de045c521144))
* **docs/api:** remove references to nonexistent types ([653ca78](https://github.com/stainless-sdks/sink-python-public/commit/653ca7867ad8b2fe1b380f769ebf77b57a241225))
* **pagination:** correct next page check ([6bd25c4](https://github.com/stainless-sdks/sink-python-public/commit/6bd25c4ac00b0f529f7c8338bf213fbc07a54e0b))
* **tests:** fix: tests which call HTTP endpoints directly with the example parameters ([a6dce0a](https://github.com/stainless-sdks/sink-python-public/commit/a6dce0a009931e68b93051e7ff2ec69df2149efd))
* **types:** fix type aliases for request params ([1cd790c](https://github.com/stainless-sdks/sink-python-public/commit/1cd790cf798022dfb14096bbbb80d70001b3a672))


### Chores

* **ci:** enable for pull requests ([b9b567f](https://github.com/stainless-sdks/sink-python-public/commit/b9b567f09fbb1aa0b746b83abf1ae403955f4b37))
* **ci:** fix installation instructions ([e6f70a9](https://github.com/stainless-sdks/sink-python-public/commit/e6f70a9bef85143c571846316b2e8182251e6a5b))
* **ci:** upload sdks to package manager ([6d79603](https://github.com/stainless-sdks/sink-python-public/commit/6d79603ecf081430041bd8752f9743a080575462))
* **docs:** grammar improvements ([4be872f](https://github.com/stainless-sdks/sink-python-public/commit/4be872f8bdcfabc459c2fed242cc1a3e257afc07))
* **docs:** remove reference to rye shell ([195f274](https://github.com/stainless-sdks/sink-python-public/commit/195f274a9b6a899bbe181db33999fe6c18f834bc))
* **internal:** codegen related update ([7703e74](https://github.com/stainless-sdks/sink-python-public/commit/7703e746f5fdba93220a5783717050df516a3239))
* **internal:** minor formatting ([b03ecd1](https://github.com/stainless-sdks/sink-python-public/commit/b03ecd1ba82bb7538b11ccd79f5d8c11ec2bf7d0))
* **internal:** update conftest.py ([ee3ff69](https://github.com/stainless-sdks/sink-python-public/commit/ee3ff6999e3356ea4fda620ead6406f52321ed08))
* **readme:** update badges ([6a82e8d](https://github.com/stainless-sdks/sink-python-public/commit/6a82e8d9a5351d08373e47e4f245d25d3a69275b))
* **tests:** add tests for httpx client instantiation & proxies ([9907ab1](https://github.com/stainless-sdks/sink-python-public/commit/9907ab1f1f42097c73295501f0c2cfac109ee86d))
* **tests:** run tests in parallel ([0d7ecaa](https://github.com/stainless-sdks/sink-python-public/commit/0d7ecaae6358e2fdf7babc7587c0ec9125ca4a87))
* **tests:** skip some failing tests on the latest python versions ([c688f22](https://github.com/stainless-sdks/sink-python-public/commit/c688f22c9dde9dc5e369bd0c0c29cd7852f128c1))


### Documentation

* **client:** fix httpx.Timeout documentation reference ([5206615](https://github.com/stainless-sdks/sink-python-public/commit/5206615a41b0adb818319a4a447b4df69f27db11))

## 1.21.0-beta.6 (2025-05-10)

Full Changelog: [v1.21.0-beta.5...v1.21.0-beta.6](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.5...v1.21.0-beta.6)

### Bug Fixes

* **package:** support direct resource imports ([bcba7e2](https://github.com/stainless-sdks/sink-python-public/commit/bcba7e2e78cf560226a46cde5946654f2e5350c0))


### Chores

* **internal:** avoid lint errors in pagination expressions ([3f17b93](https://github.com/stainless-sdks/sink-python-public/commit/3f17b938e80cfe0529bb7f7bf8fe744c61e0e6eb))


### Documentation

* remove or fix invalid readme examples ([ff40b0d](https://github.com/stainless-sdks/sink-python-public/commit/ff40b0d1c67772d15e7ffca9c8061f4dcdc59b83))

## 1.21.0-beta.5 (2025-05-09)

Full Changelog: [v1.21.0-beta.4...v1.21.0-beta.5](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.4...v1.21.0-beta.5)

### Bug Fixes

* **perf:** optimize some hot paths ([43fcaae](https://github.com/stainless-sdks/sink-python-public/commit/43fcaaea0391db1162ad7934ffe74719de3100b0))
* **perf:** skip traversing types for NotGiven values ([fa91b24](https://github.com/stainless-sdks/sink-python-public/commit/fa91b24622f46450f781cb69733ca2c3ccbb24b4))
* **pydantic v1:** more robust ModelField.annotation check ([6f2df6f](https://github.com/stainless-sdks/sink-python-public/commit/6f2df6f0961a73bd5fafad074d4c98d6239c0deb))


### Chores

* broadly detect json family of content-type headers ([b941b73](https://github.com/stainless-sdks/sink-python-public/commit/b941b73e22053172bafef2d92e67d07fb8bdb34b))
* **ci:** add timeout thresholds for CI jobs ([fcf441b](https://github.com/stainless-sdks/sink-python-public/commit/fcf441b57b236ba362de418a8a6cfb31710374ef))
* **ci:** only use depot for staging repos ([1105960](https://github.com/stainless-sdks/sink-python-public/commit/1105960b194c110dcec241cc850b67556f1f020a))
* **client:** minor internal fixes ([75072db](https://github.com/stainless-sdks/sink-python-public/commit/75072db49ea24e973b89998f6d667cfee4e6890d))
* **internal:** avoid errors for isinstance checks on proxies ([9fd46f0](https://github.com/stainless-sdks/sink-python-public/commit/9fd46f07bed006632f0855c268ecb876e536fa11))
* **internal:** base client updates ([6a0f355](https://github.com/stainless-sdks/sink-python-public/commit/6a0f355fb4db66363784857fe1b9c5172428a2d2))
* **internal:** bump pyright version ([9785042](https://github.com/stainless-sdks/sink-python-public/commit/978504230ef120efac606c80bcb676494760f9bc))
* **internal:** codegen related update ([8ac9cc4](https://github.com/stainless-sdks/sink-python-public/commit/8ac9cc43b01b46b9594a542c593b353eaf522258))
* **internal:** codegen related update ([24c366b](https://github.com/stainless-sdks/sink-python-public/commit/24c366b15d64271aa2b01943cd49f4417405bffb))
* **internal:** codegen related update ([705145d](https://github.com/stainless-sdks/sink-python-public/commit/705145dd8312eec0aaafa37678394ed977c6f9c3))
* **internal:** expand CI branch coverage ([4799e7d](https://github.com/stainless-sdks/sink-python-public/commit/4799e7d47b57e36310a9aa0bba6b8ac2126e73ca))
* **internal:** fix list file params ([36ede19](https://github.com/stainless-sdks/sink-python-public/commit/36ede1972710ddafaa9f24e663937083568a8122))
* **internal:** import reformatting ([34b3220](https://github.com/stainless-sdks/sink-python-public/commit/34b3220bbe1fa938bf8632ebaba6336eccbd4145))
* **internal:** minor formatting changes ([fb9511d](https://github.com/stainless-sdks/sink-python-public/commit/fb9511de3e1fcc19c84d6a09813dc283c1f19351))
* **internal:** only run examples workflow in main repo ([#787](https://github.com/stainless-sdks/sink-python-public/issues/787)) ([bcc43e8](https://github.com/stainless-sdks/sink-python-public/commit/bcc43e8b09624cd5796c4dd02d6d14743f5fd98b))
* **internal:** reduce CI branch coverage ([15a2bb6](https://github.com/stainless-sdks/sink-python-public/commit/15a2bb64b21c1be72f9d3eada34223107f52b968))
* **internal:** refactor retries to not use recursion ([083bb77](https://github.com/stainless-sdks/sink-python-public/commit/083bb773fee542ef7c3c84c9b3212cdeb7204b77))
* **internal:** slight transform perf improvement ([#789](https://github.com/stainless-sdks/sink-python-public/issues/789)) ([8260912](https://github.com/stainless-sdks/sink-python-public/commit/82609123da0be0a5c8ba9c5f59ddb4b84fe8f221))
* **internal:** update models test ([500f27a](https://github.com/stainless-sdks/sink-python-public/commit/500f27a3bd9ce6535014f4d75db9adf52fe8c0e8))
* **internal:** update pyright settings ([25c4872](https://github.com/stainless-sdks/sink-python-public/commit/25c4872774b15b1ff524b2a0b955af3544727570))
* slight wording improvement in README ([#791](https://github.com/stainless-sdks/sink-python-public/issues/791)) ([21331dd](https://github.com/stainless-sdks/sink-python-public/commit/21331dd13b3723d3c8a0694e163b1d4e8db85257))
* **tests:** improve enum examples ([#790](https://github.com/stainless-sdks/sink-python-public/issues/790)) ([253adff](https://github.com/stainless-sdks/sink-python-public/commit/253adffbcc0e1628662eb2f9e050a200a4704373))

## 1.21.0-beta.4 (2025-04-08)

Full Changelog: [v1.21.0-beta.3...v1.21.0-beta.4](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.3...v1.21.0-beta.4)

### Bug Fixes

* **client:** send all configured auth headers ([#784](https://github.com/stainless-sdks/sink-python-public/issues/784)) ([d9a7171](https://github.com/stainless-sdks/sink-python-public/commit/d9a7171da4e6d33361862ef83dc8bc06673fb8ea))

## 1.21.0-beta.3 (2025-04-04)

Full Changelog: [v1.21.0-beta.2...v1.21.0-beta.3](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.2...v1.21.0-beta.3)

### Bug Fixes

* **client:** add missing `None` default ([#782](https://github.com/stainless-sdks/sink-python-public/issues/782)) ([1b0d7db](https://github.com/stainless-sdks/sink-python-public/commit/1b0d7db59a4df19b929b56ffffbb24564bbdfa04))


### Chores

* add hash of OpenAPI spec/config inputs to .stats.yml ([#777](https://github.com/stainless-sdks/sink-python-public/issues/777)) ([58e2b72](https://github.com/stainless-sdks/sink-python-public/commit/58e2b726a31b61a683ed32bb2a5b764847ac3cc3))
* fix typos ([#775](https://github.com/stainless-sdks/sink-python-public/issues/775)) ([5ea75a7](https://github.com/stainless-sdks/sink-python-public/commit/5ea75a76b98054b81765e8ad1970d3349dd490b2))
* internal codegen changes ([#779](https://github.com/stainless-sdks/sink-python-public/issues/779)) ([64e019f](https://github.com/stainless-sdks/sink-python-public/commit/64e019fa5f5a5e1756337b588bf7a9b0dc4db198))
* **internal:** minor test fixes ([#780](https://github.com/stainless-sdks/sink-python-public/issues/780)) ([37ffeb2](https://github.com/stainless-sdks/sink-python-public/commit/37ffeb202b0d6e43a8856f99cbcb62b749aa9e9c))
* **internal:** remove trailing character ([#781](https://github.com/stainless-sdks/sink-python-public/issues/781)) ([9c35916](https://github.com/stainless-sdks/sink-python-public/commit/9c35916950b8a7cad1dc3845fab2cea6a9a24d82))
* **internal:** update config ([#778](https://github.com/stainless-sdks/sink-python-public/issues/778)) ([e84e779](https://github.com/stainless-sdks/sink-python-public/commit/e84e779ece78a236fc44f83d3367d2a1bfcb2ecc))
* remove custom code ([fae98ce](https://github.com/stainless-sdks/sink-python-public/commit/fae98cee874ac7f0cca63fc3395a835bed683455))

## 1.21.0-alpha.8 (2025-03-17)

Full Changelog: [v1.21.0-alpha.7...v1.21.0-alpha.8](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-alpha.7...v1.21.0-alpha.8)

### Bug Fixes

* publishing ([d4eb87a](https://github.com/stainless-sdks/sink-python-public/commit/d4eb87a51b9bfaf144c43e98f69218059521f85e))

## 1.21.0-alpha.7 (2025-03-17)

Full Changelog: [v1.21.0-alpha.6...v1.21.0-alpha.7](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-alpha.6...v1.21.0-alpha.7)

### Bug Fixes

* publishing ([735376f](https://github.com/stainless-sdks/sink-python-public/commit/735376fb8f4b8e4c0d7da9a6862aae738c91b882))

## 1.21.0-alpha.6 (2025-03-17)

Full Changelog: [v1.21.0-alpha.5...v1.21.0-alpha.6](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-alpha.5...v1.21.0-alpha.6)

### Chores

* switch back to rye ([#770](https://github.com/stainless-sdks/sink-python-public/issues/770)) ([cd1ca46](https://github.com/stainless-sdks/sink-python-public/commit/cd1ca46394e2eaff3f2c8f9d9d90e3bbafca0445))

## 1.21.0-alpha.5 (2025-03-14)

Full Changelog: [v1.21.0-alpha.4...v1.21.0-alpha.5](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-alpha.4...v1.21.0-alpha.5)

### Features

* add SKIP_BREW env var to ./scripts/bootstrap ([#764](https://github.com/stainless-sdks/sink-python-public/issues/764)) ([42ba7a3](https://github.com/stainless-sdks/sink-python-public/commit/42ba7a3911c4887978e49a6a5e95ee79f2c2edb5))
* **client:** allow passing `NotGiven` for body ([#754](https://github.com/stainless-sdks/sink-python-public/issues/754)) ([04d64d3](https://github.com/stainless-sdks/sink-python-public/commit/04d64d3efc11902602b3c8bd2d1b8b0ad626fcd7))
* **client:** send `X-Stainless-Read-Timeout` header ([#749](https://github.com/stainless-sdks/sink-python-public/issues/749)) ([eee8255](https://github.com/stainless-sdks/sink-python-public/commit/eee82556a0ec719a7ab2426b2c31c73f01685b8e))
* **pagination:** tests for has_more pagination ([#751](https://github.com/stainless-sdks/sink-python-public/issues/751)) ([1508e02](https://github.com/stainless-sdks/sink-python-public/commit/1508e0214aef4a8f2d5091b0b6823114adaafe17))


### Bug Fixes

* asyncify on non-asyncio runtimes ([#753](https://github.com/stainless-sdks/sink-python-public/issues/753)) ([3b2d912](https://github.com/stainless-sdks/sink-python-public/commit/3b2d91294041314b5eef8f68cc5af0ea1dff603e))
* **client:** mark some request bodies as optional ([04d64d3](https://github.com/stainless-sdks/sink-python-public/commit/04d64d3efc11902602b3c8bd2d1b8b0ad626fcd7))
* **types:** correct naming ([#767](https://github.com/stainless-sdks/sink-python-public/issues/767)) ([941ab0d](https://github.com/stainless-sdks/sink-python-public/commit/941ab0db8f0f9e411ddb3b5e4113f50b89040798))
* **types:** handle more discriminated union shapes ([#769](https://github.com/stainless-sdks/sink-python-public/issues/769)) ([94aebf4](https://github.com/stainless-sdks/sink-python-public/commit/94aebf44edfda8e6288b016a1fc73a642bcc0a79))


### Chores

* add test case for `~n` refs ([#762](https://github.com/stainless-sdks/sink-python-public/issues/762)) ([f426e6e](https://github.com/stainless-sdks/sink-python-public/commit/f426e6ecf6319fe7f999dbb6d252af9ff5b20b08))
* **docs:** update client docstring ([#759](https://github.com/stainless-sdks/sink-python-public/issues/759)) ([6a74e81](https://github.com/stainless-sdks/sink-python-public/commit/6a74e81d289efa3ffcfbfee3b4c5dfbeb7c2f23e))
* **email:** change email domain ([#756](https://github.com/stainless-sdks/sink-python-public/issues/756)) ([03ad525](https://github.com/stainless-sdks/sink-python-public/commit/03ad525fb3c99ff6f36107012e4586d46e1d7279))
* export more types ([#766](https://github.com/stainless-sdks/sink-python-public/issues/766)) ([4b362b4](https://github.com/stainless-sdks/sink-python-public/commit/4b362b4c3e1f998eecb0add469bcce822d2a3651))
* **internal:** fix devcontainers setup ([#755](https://github.com/stainless-sdks/sink-python-public/issues/755)) ([bf988ce](https://github.com/stainless-sdks/sink-python-public/commit/bf988ce93028cb21979d98ee1e1eea5c6213b11a))
* **internal:** fix type traversing dictionary params ([#750](https://github.com/stainless-sdks/sink-python-public/issues/750)) ([90ef2c0](https://github.com/stainless-sdks/sink-python-public/commit/90ef2c090790501fe8959b685315f2d7f54ce931))
* **internal:** import ordering changes ([#763](https://github.com/stainless-sdks/sink-python-public/issues/763)) ([52a73b6](https://github.com/stainless-sdks/sink-python-public/commit/52a73b66e14e1debb10f20612534c18f3e617343))
* **internal:** minor type handling changes ([#752](https://github.com/stainless-sdks/sink-python-public/issues/752)) ([89c3158](https://github.com/stainless-sdks/sink-python-public/commit/89c3158582d30da172b44fb9d3491c6b3edb2977))
* **internal:** properly set __pydantic_private__ ([#757](https://github.com/stainless-sdks/sink-python-public/issues/757)) ([a8b679f](https://github.com/stainless-sdks/sink-python-public/commit/a8b679f700b14347823e702fef90d83cf97c5ebf))
* **internal:** remove extra empty newlines ([#768](https://github.com/stainless-sdks/sink-python-public/issues/768)) ([b30e93c](https://github.com/stainless-sdks/sink-python-public/commit/b30e93c5e75cc0ff120ca5cec3888da278a6ae59))
* **internal:** remove unused http client options forwarding ([#761](https://github.com/stainless-sdks/sink-python-public/issues/761)) ([726a048](https://github.com/stainless-sdks/sink-python-public/commit/726a0484edc6fc198a26b4daa97523df224b7d42))
* **internal:** style changes ([#760](https://github.com/stainless-sdks/sink-python-public/issues/760)) ([77eef56](https://github.com/stainless-sdks/sink-python-public/commit/77eef564231ca4ec440b6138ea5af252a1b32ac7))
* test custom env ([#747](https://github.com/stainless-sdks/sink-python-public/issues/747)) ([6dc57b2](https://github.com/stainless-sdks/sink-python-public/commit/6dc57b23065d5b29b6195717d781765ab73ae99c))


### Documentation

* update URLs from stainlessapi.com to stainless.com ([#758](https://github.com/stainless-sdks/sink-python-public/issues/758)) ([3f1e8d5](https://github.com/stainless-sdks/sink-python-public/commit/3f1e8d57bea1fa34d827cae3808638cfc0887172))

## 1.21.0-alpha.4 (2025-02-04)

Full Changelog: [v1.21.0-alpha.3...v1.21.0-alpha.4](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-alpha.3...v1.21.0-alpha.4)

### Bug Fixes

* improve names for conflicting params ([#746](https://github.com/stainless-sdks/sink-python-public/issues/746)) ([0c8131a](https://github.com/stainless-sdks/sink-python-public/commit/0c8131ae132941264a3bc21b51ad5391727c1850))


### Chores

* better bootstrap script logging ([#740](https://github.com/stainless-sdks/sink-python-public/issues/740)) ([1408091](https://github.com/stainless-sdks/sink-python-public/commit/140809134576c6ef40ce176d02669acca6b8f396))
* **bootstrap:** setup python ([#741](https://github.com/stainless-sdks/sink-python-public/issues/741)) ([e4e1697](https://github.com/stainless-sdks/sink-python-public/commit/e4e1697bb4d5d806c23478c6d1acd947acf5cbcd))
* **internal:** bummp ruff dependency ([#745](https://github.com/stainless-sdks/sink-python-public/issues/745)) ([e9ceea8](https://github.com/stainless-sdks/sink-python-public/commit/e9ceea8e9e6d95ac41a2a5ab8795de42e28777f9))
* **internal:** change default timeout to an int ([#744](https://github.com/stainless-sdks/sink-python-public/issues/744)) ([e51c70d](https://github.com/stainless-sdks/sink-python-public/commit/e51c70ddd8cd9854c829dafa41eacf7dccae95e0))
* **internal:** remove unnecessary type quotations ([#743](https://github.com/stainless-sdks/sink-python-public/issues/743)) ([30dfaa1](https://github.com/stainless-sdks/sink-python-public/commit/30dfaa1627578c5f5cd23d21d635f21f830bde6d))
* simplify types ([#742](https://github.com/stainless-sdks/sink-python-public/issues/742)) ([5c2d258](https://github.com/stainless-sdks/sink-python-public/commit/5c2d2584ab77ebd1d67f0b8cc8ac25d3d64a597b))
* update bootstrap script ([#738](https://github.com/stainless-sdks/sink-python-public/issues/738)) ([dc0c60b](https://github.com/stainless-sdks/sink-python-public/commit/dc0c60b5585c9da8290e8cb2864b57fe097989a7))

## 1.21.0-alpha.3 (2025-01-23)

Full Changelog: [v1.21.0-alpha.2...v1.21.0-alpha.3](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-alpha.2...v1.21.0-alpha.3)

### Features

* **project:** switch from rye to uv ([#736](https://github.com/stainless-sdks/sink-python-public/issues/736)) ([db87129](https://github.com/stainless-sdks/sink-python-public/commit/db87129fd8af49f717e45d10e8ff9c0e2f872ecb))

## 1.21.0-alpha.2 (2025-01-21)

Full Changelog: [v1.21.0-alpha.1...v1.21.0-alpha.2](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-alpha.1...v1.21.0-alpha.2)

### Features

* add duplicate subproperty test ([#670](https://github.com/stainless-sdks/sink-python-public/issues/670)) ([f5fb22d](https://github.com/stainless-sdks/sink-python-public/commit/f5fb22d1d0cf02110424eeded27775e1a99043ae))
* add test case for path param with queries ([#659](https://github.com/stainless-sdks/sink-python-public/issues/659)) ([592e4d3](https://github.com/stainless-sdks/sink-python-public/commit/592e4d3e08f292d768acce11b69d4c32db7c0bf5))
* **client:** add `retries_taken` to raw response class ([#623](https://github.com/stainless-sdks/sink-python-public/issues/623)) ([5735b42](https://github.com/stainless-sdks/sink-python-public/commit/5735b425c55f2f00f77090d2fbeef0fc0c7a4e12))
* **client:** allow overriding retry count header ([#658](https://github.com/stainless-sdks/sink-python-public/issues/658)) ([7c2fc3c](https://github.com/stainless-sdks/sink-python-public/commit/7c2fc3c6a6356a57bb1ac8caa358b89d36af4efa))
* **client:** send retry count header ([#652](https://github.com/stainless-sdks/sink-python-public/issues/652)) ([b3d9237](https://github.com/stainless-sdks/sink-python-public/commit/b3d9237c0088a90c649fa26511ba550927e1373b))
* discriminator property should be considered required ([#635](https://github.com/stainless-sdks/sink-python-public/issues/635)) ([d749330](https://github.com/stainless-sdks/sink-python-public/commit/d749330ea266f8f16663bf93272ef5409a54da56))
* **perf:** lazily instantiate resource classes ([#649](https://github.com/stainless-sdks/sink-python-public/issues/649)) ([757f706](https://github.com/stainless-sdks/sink-python-public/commit/757f7062956c77779f40670759087964681fc0c7))
* **project:** drop support for Python 3.7 ([#681](https://github.com/stainless-sdks/sink-python-public/issues/681)) ([21e02a0](https://github.com/stainless-sdks/sink-python-public/commit/21e02a0ba1e29390ed721c1601e098c039b2853f))
* support custom configurability ([#657](https://github.com/stainless-sdks/sink-python-public/issues/657)) ([d7224d9](https://github.com/stainless-sdks/sink-python-public/commit/d7224d93c61f1d32d0068356f8693eac5a9be7a2))
* **tests:** add tests for page number pagination ([#650](https://github.com/stainless-sdks/sink-python-public/issues/650)) ([4d45cc9](https://github.com/stainless-sdks/sink-python-public/commit/4d45cc9f571c4f7470241725f8991f114c9e81cc))


### Bug Fixes

* allow header params to override default headers ([#671](https://github.com/stainless-sdks/sink-python-public/issues/671)) ([6a8b7d3](https://github.com/stainless-sdks/sink-python-public/commit/6a8b7d3a55e9856831c83673a17a43f1388c68a1))
* **asyncify:** avoid hanging process under certain conditions ([#690](https://github.com/stainless-sdks/sink-python-public/issues/690)) ([b884984](https://github.com/stainless-sdks/sink-python-public/commit/b8849847a9a58b0fa589ae3e67190ec023a21994))
* **client/async:** correctly retry in all cases ([#674](https://github.com/stainless-sdks/sink-python-public/issues/674)) ([3abd469](https://github.com/stainless-sdks/sink-python-public/commit/3abd469010749b8b797deff50b8ff7c8b3e26cba))
* **client:** avoid OverflowError with very large retry counts ([#668](https://github.com/stainless-sdks/sink-python-public/issues/668)) ([cff2b21](https://github.com/stainless-sdks/sink-python-public/commit/cff2b21589a5e20baf9fcdf957c962c3929eb518))
* **client:** compat with new httpx 0.28.0 release ([#701](https://github.com/stainless-sdks/sink-python-public/issues/701)) ([885bf75](https://github.com/stainless-sdks/sink-python-public/commit/885bf75539d0ac0b256b9558a3ad0aa289b6c1a6))
* **client:** correctly apply client level timeouts ([#620](https://github.com/stainless-sdks/sink-python-public/issues/620)) ([b666f69](https://github.com/stainless-sdks/sink-python-public/commit/b666f69196d680d730e44ff010a3913533312f1d))
* **client:** correctly serialise array body params ([#628](https://github.com/stainless-sdks/sink-python-public/issues/628)) ([c19cbc5](https://github.com/stainless-sdks/sink-python-public/commit/c19cbc5c4dfacaed607d57139c5d719b60df69b5))
* **client:** disallow optional path params ([#714](https://github.com/stainless-sdks/sink-python-public/issues/714)) ([d606a69](https://github.com/stainless-sdks/sink-python-public/commit/d606a69186d9cd5a5f1f59f43c5f22b316a19353))
* **client:** handle domains with underscores ([#651](https://github.com/stainless-sdks/sink-python-public/issues/651)) ([bf829b0](https://github.com/stainless-sdks/sink-python-public/commit/bf829b01d10a00736649e58e44f2bb89a1c58817))
* **client:** only call .close() when needed ([#721](https://github.com/stainless-sdks/sink-python-public/issues/721)) ([6017f7e](https://github.com/stainless-sdks/sink-python-public/commit/6017f7ecca4ca051973a5802c7bf18246a3187e4))
* **client:** rename duplicate param names ([#731](https://github.com/stainless-sdks/sink-python-public/issues/731)) ([368aabd](https://github.com/stainless-sdks/sink-python-public/commit/368aabd05adead7d92bdf24dfbb19d8c2278bbba))
* correct positional arguments ([#727](https://github.com/stainless-sdks/sink-python-public/issues/727)) ([b0c0061](https://github.com/stainless-sdks/sink-python-public/commit/b0c00610c167cf6bb2c1e4601192af2df144eda5))
* correctly handle deserialising `cls` fields ([#725](https://github.com/stainless-sdks/sink-python-public/issues/725)) ([4b4afb2](https://github.com/stainless-sdks/sink-python-public/commit/4b4afb297988a16a550acf780fe88551c3b76da7))
* do not pass through `\` when escaping string literals ([#640](https://github.com/stainless-sdks/sink-python-public/issues/640)) ([98bef20](https://github.com/stainless-sdks/sink-python-public/commit/98bef207f188e55b0476e9e08c0628ae220c2029))
* don't use dicts as iterables in transform ([#679](https://github.com/stainless-sdks/sink-python-public/issues/679)) ([6fd3bee](https://github.com/stainless-sdks/sink-python-public/commit/6fd3bee3b51fdf999349050ce15bc2443251c7c7))
* don't use dicts as iterables in transform ([#688](https://github.com/stainless-sdks/sink-python-public/issues/688)) ([87b6a55](https://github.com/stainless-sdks/sink-python-public/commit/87b6a559fb6b24edfdf27994779f7f11241db3c1))
* escape invalid param names ([#676](https://github.com/stainless-sdks/sink-python-public/issues/676)) ([d288a15](https://github.com/stainless-sdks/sink-python-public/commit/d288a15c77060dd471bacdd4f34cd6435a597793))
* support json safe serialization for basemodel subclasses ([#680](https://github.com/stainless-sdks/sink-python-public/issues/680)) ([04c184c](https://github.com/stainless-sdks/sink-python-public/commit/04c184c9c5452c84c76cc3b3ac60a6774263e240))
* **tests:** make test_get_platform less flaky ([#733](https://github.com/stainless-sdks/sink-python-public/issues/733)) ([b9cb10a](https://github.com/stainless-sdks/sink-python-public/commit/b9cb10aa43890973f69dcef8f3c7521dc601dd88))
* **types:** correctly mark stream discriminator as optional ([#645](https://github.com/stainless-sdks/sink-python-public/issues/645)) ([bcd9043](https://github.com/stainless-sdks/sink-python-public/commit/bcd90435c7b2ccde36451bb03bfc44fe4d253fc6))
* use object for map items ([#693](https://github.com/stainless-sdks/sink-python-public/issues/693)) ([a4211b5](https://github.com/stainless-sdks/sink-python-public/commit/a4211b596a098f112c9297d4cb7fea55056bce1f))


### Chores

* add comment to test skip reason ([#692](https://github.com/stainless-sdks/sink-python-public/issues/692)) ([63589c5](https://github.com/stainless-sdks/sink-python-public/commit/63589c5ae563a6d1e740eacf46d4a3bd8520a5a0))
* add docstrings to raw response properties ([#643](https://github.com/stainless-sdks/sink-python-public/issues/643)) ([116b73e](https://github.com/stainless-sdks/sink-python-public/commit/116b73ecea18c1f2d099040bba15ac607e3c6a6d))
* add example for error configurations ([#704](https://github.com/stainless-sdks/sink-python-public/issues/704)) ([b79f9e0](https://github.com/stainless-sdks/sink-python-public/commit/b79f9e07d009fffea9f7ba34d83d26c52dc56245))
* add missing isclass check ([#719](https://github.com/stainless-sdks/sink-python-public/issues/719)) ([e321fdd](https://github.com/stainless-sdks/sink-python-public/commit/e321fdd65d35cbebc3352627e1536dcc60ceb43b))
* add repr to PageInfo class ([#669](https://github.com/stainless-sdks/sink-python-public/issues/669)) ([91bedee](https://github.com/stainless-sdks/sink-python-public/commit/91bedeecbf1dd6d1cc8871001f06c536ce445d8b))
* add test for duplicate params with different casing ([#686](https://github.com/stainless-sdks/sink-python-public/issues/686)) ([82095c9](https://github.com/stainless-sdks/sink-python-public/commit/82095c96032d792d9763e6e114173a5451c093f1))
* add tests for nullable header params ([#617](https://github.com/stainless-sdks/sink-python-public/issues/617)) ([6887962](https://github.com/stainless-sdks/sink-python-public/commit/68879622294cb938f65bbf18f846276a50516bc0))
* bump license year ([#718](https://github.com/stainless-sdks/sink-python-public/issues/718)) ([f79f7ef](https://github.com/stainless-sdks/sink-python-public/commit/f79f7eff968dc3a07b32341cc8476205555645d5))
* **ci:** also run pydantic v1 tests ([#638](https://github.com/stainless-sdks/sink-python-public/issues/638)) ([3ebdf93](https://github.com/stainless-sdks/sink-python-public/commit/3ebdf93b4011a4a8a0fff38342c643a3f8ce6561))
* **ci:** bump prism mock server version ([#630](https://github.com/stainless-sdks/sink-python-public/issues/630)) ([e231e24](https://github.com/stainless-sdks/sink-python-public/commit/e231e24f7340eb53fdb739bb3fa6d76ec3c863a0))
* **client:** fix parsing union responses when non-json is returned ([#637](https://github.com/stainless-sdks/sink-python-public/issues/637)) ([ce47730](https://github.com/stainless-sdks/sink-python-public/commit/ce47730a86e6a2ccbbe0ac722334c45b538c42ca))
* disable falling test for now with a TODO ([#691](https://github.com/stainless-sdks/sink-python-public/issues/691)) ([9b25b31](https://github.com/stainless-sdks/sink-python-public/commit/9b25b31c18c7367e34b289309580319d337d9668))
* **docs:** add documentation for $shared & $client resources ([#634](https://github.com/stainless-sdks/sink-python-public/issues/634)) ([510c595](https://github.com/stainless-sdks/sink-python-public/commit/510c5956c9b5f46d8b9df61f3307790cc3223374))
* **examples:** minor formatting changes ([#633](https://github.com/stainless-sdks/sink-python-public/issues/633)) ([4512d5c](https://github.com/stainless-sdks/sink-python-public/commit/4512d5ce13b5b53ac6498ff8eef97b599222905b))
* fix error message import example ([#615](https://github.com/stainless-sdks/sink-python-public/issues/615)) ([141ba8f](https://github.com/stainless-sdks/sink-python-public/commit/141ba8f650f013c69c286807d645f9888a6d8bc3))
* fix model used in pagination ([#716](https://github.com/stainless-sdks/sink-python-public/issues/716)) ([22a2126](https://github.com/stainless-sdks/sink-python-public/commit/22a2126eac10eaa98ecacc89fc1c4878b3a5612b))
* **internal:** add support for parsing bool response content ([#663](https://github.com/stainless-sdks/sink-python-public/issues/663)) ([2e5b910](https://github.com/stainless-sdks/sink-python-public/commit/2e5b91040d4e339fbb42909b657e881e0a329793))
* **internal:** add support for TypeAliasType ([#710](https://github.com/stainless-sdks/sink-python-public/issues/710)) ([2cb4fdf](https://github.com/stainless-sdks/sink-python-public/commit/2cb4fdfa13c2ab85c1f0d9ecb2d5bc1b3e0e371d))
* **internal:** add type construction helper ([#618](https://github.com/stainless-sdks/sink-python-public/issues/618)) ([6f28db9](https://github.com/stainless-sdks/sink-python-public/commit/6f28db9b336ff361389c056bf9623aa803b974b8))
* **internal:** avoid pytest-asyncio deprecation warning ([#734](https://github.com/stainless-sdks/sink-python-public/issues/734)) ([f779644](https://github.com/stainless-sdks/sink-python-public/commit/f7796443ac10506384f7744c8929a23eceee2de7))
* **internal:** bump httpx dependency ([#720](https://github.com/stainless-sdks/sink-python-public/issues/720)) ([898b21c](https://github.com/stainless-sdks/sink-python-public/commit/898b21c6e7e162d44f60aaec121bd3828c08e443))
* **internal:** bump mypy ([#678](https://github.com/stainless-sdks/sink-python-public/issues/678)) ([30251c5](https://github.com/stainless-sdks/sink-python-public/commit/30251c5d13625afbef8dc0964236d35a0bf949a4))
* **internal:** bump pydantic dependency ([#707](https://github.com/stainless-sdks/sink-python-public/issues/707)) ([3e152e1](https://github.com/stainless-sdks/sink-python-public/commit/3e152e1ff92a616947184adccd54b29aed7c05c3))
* **internal:** bump pyright ([#622](https://github.com/stainless-sdks/sink-python-public/issues/622)) ([74ebdd8](https://github.com/stainless-sdks/sink-python-public/commit/74ebdd8494a891a8de7c0f8a048bcd51d8fb8ee2))
* **internal:** bump pyright ([#703](https://github.com/stainless-sdks/sink-python-public/issues/703)) ([6e28f06](https://github.com/stainless-sdks/sink-python-public/commit/6e28f0692191f341e393f448ff886f67158aac37))
* **internal:** bump pyright ([#709](https://github.com/stainless-sdks/sink-python-public/issues/709)) ([c301047](https://github.com/stainless-sdks/sink-python-public/commit/c3010473551a477536941becbbe1bf70d6456d9e))
* **internal:** bump pyright / mypy version ([#648](https://github.com/stainless-sdks/sink-python-public/issues/648)) ([55f0292](https://github.com/stainless-sdks/sink-python-public/commit/55f0292039d9df9854130311f0493df26ad96c47))
* **internal:** bump pyright dependency ([#729](https://github.com/stainless-sdks/sink-python-public/issues/729)) ([3121471](https://github.com/stainless-sdks/sink-python-public/commit/312147152ff156f3423f10c28d611d140c17bb6a))
* **internal:** bump pytest to v8 & pydantic ([#677](https://github.com/stainless-sdks/sink-python-public/issues/677)) ([0fa30a8](https://github.com/stainless-sdks/sink-python-public/commit/0fa30a8906dc89110f58c0aca2770ed7a28072a3))
* **internal:** bump ruff ([#647](https://github.com/stainless-sdks/sink-python-public/issues/647)) ([028bbc7](https://github.com/stainless-sdks/sink-python-public/commit/028bbc7f8b79fb0365cb6e96d98887035ffe095e))
* **internal:** bump ruff dependency ([#673](https://github.com/stainless-sdks/sink-python-public/issues/673)) ([4df3727](https://github.com/stainless-sdks/sink-python-public/commit/4df372735faccbe7af3d7f7bd22fa235e6379114))
* **internal:** bump ruff version ([#625](https://github.com/stainless-sdks/sink-python-public/issues/625)) ([ecd647b](https://github.com/stainless-sdks/sink-python-public/commit/ecd647b32a9af26b29850ca6d59e12ae56210151))
* **internal:** ensure package is importable in lint cmd ([#631](https://github.com/stainless-sdks/sink-python-public/issues/631)) ([5120a1f](https://github.com/stainless-sdks/sink-python-public/commit/5120a1f2805952298f2de91c92769f913ada2f02))
* **internal:** exclude mypy from running on tests ([#700](https://github.com/stainless-sdks/sink-python-public/issues/700)) ([42fb86c](https://github.com/stainless-sdks/sink-python-public/commit/42fb86c660e79622ae9ad1beadf7822eb8e689ba))
* **internal:** fix compat model_dump method when warnings are passed ([#694](https://github.com/stainless-sdks/sink-python-public/issues/694)) ([63278cd](https://github.com/stainless-sdks/sink-python-public/commit/63278cd81cf43e1a6621c8d40ab4d7922002c6a5))
* **internal:** fix some typos ([#717](https://github.com/stainless-sdks/sink-python-public/issues/717)) ([eb41ce2](https://github.com/stainless-sdks/sink-python-public/commit/eb41ce2781c87a9d3f19a4fa93847683348e2cd6))
* **internal:** minor style changes ([#735](https://github.com/stainless-sdks/sink-python-public/issues/735)) ([48cf9b0](https://github.com/stainless-sdks/sink-python-public/commit/48cf9b0a82935bcb0b80eb82aea49a17ffecd8de))
* **internal:** more robust attribute generation ([#655](https://github.com/stainless-sdks/sink-python-public/issues/655)) ([959fc05](https://github.com/stainless-sdks/sink-python-public/commit/959fc050eca84fac14dfa35c202a472239b11912))
* **internal:** quote more types ([#684](https://github.com/stainless-sdks/sink-python-public/issues/684)) ([327a1d4](https://github.com/stainless-sdks/sink-python-public/commit/327a1d4751e5f2e0ef6a6a03b4a6c3abf556ce56))
* **internal:** remove some duplicated imports ([#712](https://github.com/stainless-sdks/sink-python-public/issues/712)) ([92d17df](https://github.com/stainless-sdks/sink-python-public/commit/92d17dfd6aef2add339d185890c4a0ef4086cd64))
* **internal:** remove unused black config ([#675](https://github.com/stainless-sdks/sink-python-public/issues/675)) ([9854f39](https://github.com/stainless-sdks/sink-python-public/commit/9854f392ff57370092e6707a5f07ae05d05a562e))
* **internal:** test updates ([#624](https://github.com/stainless-sdks/sink-python-public/issues/624)) ([789d15f](https://github.com/stainless-sdks/sink-python-public/commit/789d15ff2bd53e28677febe05f556f64a43c7806))
* **internal:** update deps ([#726](https://github.com/stainless-sdks/sink-python-public/issues/726)) ([2a83ee4](https://github.com/stainless-sdks/sink-python-public/commit/2a83ee4c5968288bd3ea2d0d516640d1f34910b8))
* **internal:** update pydantic compat helper function ([#626](https://github.com/stainless-sdks/sink-python-public/issues/626)) ([eb65dda](https://github.com/stainless-sdks/sink-python-public/commit/eb65ddad78e31a4769c2e008506e728d3bd893c2))
* **internal:** update pydantic v1 compat helpers ([#654](https://github.com/stainless-sdks/sink-python-public/issues/654)) ([17f4d28](https://github.com/stainless-sdks/sink-python-public/commit/17f4d28d46a7f0103374338f47a0b6afe931db6a))
* **internal:** update some imports ([#632](https://github.com/stainless-sdks/sink-python-public/issues/632)) ([f84f386](https://github.com/stainless-sdks/sink-python-public/commit/f84f38691c251b494c44506a38f108c7743f41d0))
* **internal:** update test syntax ([#672](https://github.com/stainless-sdks/sink-python-public/issues/672)) ([8cd30d7](https://github.com/stainless-sdks/sink-python-public/commit/8cd30d744583b95c0a08e9d5b2b915a94a8f0ecf))
* **internal:** updated imports ([#713](https://github.com/stainless-sdks/sink-python-public/issues/713)) ([11cc644](https://github.com/stainless-sdks/sink-python-public/commit/11cc644692cd38f9a86d8dd26f900c464422bdeb))
* **internal:** updates ([#629](https://github.com/stainless-sdks/sink-python-public/issues/629)) ([7c1218e](https://github.com/stainless-sdks/sink-python-public/commit/7c1218e9371995d7febe6fef3241c798aad7ca55))
* **internal:** use `TypeAlias` marker for type assignments ([#621](https://github.com/stainless-sdks/sink-python-public/issues/621)) ([c438ed3](https://github.com/stainless-sdks/sink-python-public/commit/c438ed36279edb0970f73815d17fead3fd653f98))
* **internal:** use `typing_extensions.overload` instead of `typing` ([#656](https://github.com/stainless-sdks/sink-python-public/issues/656)) ([792f1d2](https://github.com/stainless-sdks/sink-python-public/commit/792f1d2651fcf4a5769acd72926742ff329124ec))
* **internal:** use different 32bit detection method ([#636](https://github.com/stainless-sdks/sink-python-public/issues/636)) ([fdb5e59](https://github.com/stainless-sdks/sink-python-public/commit/fdb5e590d06de26d3024430f9b51f2bd8c071bc7))
* make the `Omit` type public ([#705](https://github.com/stainless-sdks/sink-python-public/issues/705)) ([f08ab37](https://github.com/stainless-sdks/sink-python-public/commit/f08ab373d6267509c0e0f8d12c4dbbfe8fc80412))
* minor change to test values ([#728](https://github.com/stainless-sdks/sink-python-public/issues/728)) ([b2937bd](https://github.com/stainless-sdks/sink-python-public/commit/b2937bdf9d21568061d12afa706a69ad8d1a54d2))
* minor dependency version bump ([#639](https://github.com/stainless-sdks/sink-python-public/issues/639)) ([94fedb1](https://github.com/stainless-sdks/sink-python-public/commit/94fedb1e977f514ec4c631d0ae392b65bc6bbf08))
* minor refactors ([#702](https://github.com/stainless-sdks/sink-python-public/issues/702)) ([ef7798b](https://github.com/stainless-sdks/sink-python-public/commit/ef7798b0bf79c3a6aa081c42ddbeb2c896ce842a))
* pyproject.toml formatting changes ([#641](https://github.com/stainless-sdks/sink-python-public/issues/641)) ([2174247](https://github.com/stainless-sdks/sink-python-public/commit/21742472a34ae95768bba2a0f73d4f6765e66592))
* re-enable disabled tests ([#711](https://github.com/stainless-sdks/sink-python-public/issues/711)) ([d3c2608](https://github.com/stainless-sdks/sink-python-public/commit/d3c2608d8c83ae3bd6dc2b3455fab2486185dfb3))
* remove custom methods ([#619](https://github.com/stainless-sdks/sink-python-public/issues/619)) ([5002084](https://github.com/stainless-sdks/sink-python-public/commit/5002084a1be8f5c5305d83681ca152c7c82cee1f))
* remove ill-formatted parameter ([#706](https://github.com/stainless-sdks/sink-python-public/issues/706)) ([11ce472](https://github.com/stainless-sdks/sink-python-public/commit/11ce4729f49fa03a7d3baaf4a6c26f3b236e0326))
* remove now unused `cached-property` dep ([#696](https://github.com/stainless-sdks/sink-python-public/issues/696)) ([911414c](https://github.com/stainless-sdks/sink-python-public/commit/911414cc9b117e6061ac0e32301604aaa072be66))
* remove old tests ([#730](https://github.com/stainless-sdks/sink-python-public/issues/730)) ([2ae3f33](https://github.com/stainless-sdks/sink-python-public/commit/2ae3f330cffac7ba1295ae0b904af436966a5d5d))
* spec update ([#682](https://github.com/stainless-sdks/sink-python-public/issues/682)) ([4ad1dbb](https://github.com/stainless-sdks/sink-python-public/commit/4ad1dbbfa4337db93e6955c86059b942e82a1419))
* test case for default header overriding ([#666](https://github.com/stainless-sdks/sink-python-public/issues/666)) ([ad5791d](https://github.com/stainless-sdks/sink-python-public/commit/ad5791d73b357a94756d70c1ebfd1232d115fbed))
* test case for reverse cursor pagination ([#665](https://github.com/stainless-sdks/sink-python-public/issues/665)) ([29b7785](https://github.com/stainless-sdks/sink-python-public/commit/29b77854765153699220104d42d0fa34cb613157))
* test for missing param name ([#685](https://github.com/stainless-sdks/sink-python-public/issues/685)) ([a3c63f1](https://github.com/stainless-sdks/sink-python-public/commit/a3c63f1dbb9321e8ce4943dc65b2d810867f6a5c))
* test legacy responses ([#662](https://github.com/stainless-sdks/sink-python-public/issues/662)) ([ada50df](https://github.com/stainless-sdks/sink-python-public/commit/ada50df36579923198f11a6116099de6ca6e5f40))
* test legacy responses ([#664](https://github.com/stainless-sdks/sink-python-public/issues/664)) ([79885a7](https://github.com/stainless-sdks/sink-python-public/commit/79885a7c80536a8f966c02e7d6c79610fe45b93c))
* test overriding default headers ([#698](https://github.com/stainless-sdks/sink-python-public/issues/698)) ([f435b54](https://github.com/stainless-sdks/sink-python-public/commit/f435b54c6285655cc903138a626f33bac1e9eb17))
* test request param clashes with `self` ([#697](https://github.com/stainless-sdks/sink-python-public/issues/697)) ([eebbfb9](https://github.com/stainless-sdks/sink-python-public/commit/eebbfb9200bca1d3c94611d0e9d0db1b3f364004))
* **test:** change test name ([#642](https://github.com/stainless-sdks/sink-python-public/issues/642)) ([a82aaa1](https://github.com/stainless-sdks/sink-python-public/commit/a82aaa166706f9894f6ece111be219acac136c21))
* tests for array headers ([#667](https://github.com/stainless-sdks/sink-python-public/issues/667)) ([82fc43d](https://github.com/stainless-sdks/sink-python-public/commit/82fc43d0807ed117802628a9d9c57b325b376b17))
* **tests:** adjust retry timeout values ([#683](https://github.com/stainless-sdks/sink-python-public/issues/683)) ([15c204d](https://github.com/stainless-sdks/sink-python-public/commit/15c204d96e88bc5a93731b2e2c360b0ba4f4e2ee))
* **tests:** limit array example length ([#689](https://github.com/stainless-sdks/sink-python-public/issues/689)) ([af3889c](https://github.com/stainless-sdks/sink-python-public/commit/af3889c4eee66c6a88936880515d2fa279add1b3))
* update schema to test x-stainless-skip for terraform ([#627](https://github.com/stainless-sdks/sink-python-public/issues/627)) ([1191c83](https://github.com/stainless-sdks/sink-python-public/commit/1191c8349f0db927405f6c234752e69f950387d8))


### Documentation

* add info log level to readme ([#695](https://github.com/stainless-sdks/sink-python-public/issues/695)) ([51d1ed4](https://github.com/stainless-sdks/sink-python-public/commit/51d1ed49bb68381fd7be307ff49da03c24c8a113))
* **api.md:** fix return type annotations ([#699](https://github.com/stainless-sdks/sink-python-public/issues/699)) ([2a91b20](https://github.com/stainless-sdks/sink-python-public/commit/2a91b202cd61f00dbdc565db523762f7445b1ec4))
* fix typo in fenced code block language ([#661](https://github.com/stainless-sdks/sink-python-public/issues/661)) ([0afc0e1](https://github.com/stainless-sdks/sink-python-public/commit/0afc0e139545145ed3da45cd3a7394802ad3939a))
* fix typos ([#722](https://github.com/stainless-sdks/sink-python-public/issues/722)) ([7dba689](https://github.com/stainless-sdks/sink-python-public/commit/7dba6896b048e541e0cd029dcf3589c872900a91))
* improve and reference contributing documentation ([#660](https://github.com/stainless-sdks/sink-python-public/issues/660)) ([540bee7](https://github.com/stainless-sdks/sink-python-public/commit/540bee7f087ece9715df84ec5e68e798d3854c4c))
* more typo fixes ([#723](https://github.com/stainless-sdks/sink-python-public/issues/723)) ([75ab443](https://github.com/stainless-sdks/sink-python-public/commit/75ab443df53cbf4d2cbd38f4106a7941b2eb0828))
* move comments in example snippets ([#687](https://github.com/stainless-sdks/sink-python-public/issues/687)) ([ef67399](https://github.com/stainless-sdks/sink-python-public/commit/ef67399ed86e99fd39165ea6652f2373f407448c))
* **raw responses:** fix duplicate `the` ([#732](https://github.com/stainless-sdks/sink-python-public/issues/732)) ([72c5806](https://github.com/stainless-sdks/sink-python-public/commit/72c5806478163ef97a76aa228c60f0e9fed92e1d))
* **readme:** add section on determining installed version ([#644](https://github.com/stainless-sdks/sink-python-public/issues/644)) ([8cf0670](https://github.com/stainless-sdks/sink-python-public/commit/8cf0670a1c9218d936e1cb7da7b69e2e9df5a671))
* **readme:** example snippet for client context manager ([#715](https://github.com/stainless-sdks/sink-python-public/issues/715)) ([484652e](https://github.com/stainless-sdks/sink-python-public/commit/484652eb1d1118f1ac616b2a167d22f21d884ffd))
* **readme:** fix http client proxies example ([#708](https://github.com/stainless-sdks/sink-python-public/issues/708)) ([cd984cf](https://github.com/stainless-sdks/sink-python-public/commit/cd984cf71df1cc98e9b4bfd00a179cc4a5c39727))
* **readme:** fix misplaced period ([#724](https://github.com/stainless-sdks/sink-python-public/issues/724)) ([da89c5e](https://github.com/stainless-sdks/sink-python-public/commit/da89c5e4a1850bdbf972ad57a3187349de3366b2))
* update CONTRIBUTING.md ([#646](https://github.com/stainless-sdks/sink-python-public/issues/646)) ([3bc46e5](https://github.com/stainless-sdks/sink-python-public/commit/3bc46e50675c10ec61e83040cc237ada508b9eab))

## 1.21.0-alpha.1 (2024-07-23)

Full Changelog: [v1.21.0-beta.3...v1.21.0-alpha.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.3...v1.21.0-alpha.1)

### Bug Fixes

* nullable parameters ([#613](https://github.com/stainless-sdks/sink-python-public/issues/613)) ([5e3dd9e](https://github.com/stainless-sdks/sink-python-public/commit/5e3dd9ed338766bd63947730e87f1031568c3786))


### Chores

* **tests:** update prism version ([#614](https://github.com/stainless-sdks/sink-python-public/issues/614)) ([62c2047](https://github.com/stainless-sdks/sink-python-public/commit/62c2047aae4b0cf785cf2e996be4dfef3ef8a871))


### Documentation

* **readme:** fix example snippet imports ([#611](https://github.com/stainless-sdks/sink-python-public/issues/611)) ([a646011](https://github.com/stainless-sdks/sink-python-public/commit/a646011f11d2dac1018e56c48d13c86544e4ba6f))

## 1.21.0-beta.3 (2024-07-20)

Full Changelog: [v1.21.0-beta.2...v1.21.0-beta.3](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.2...v1.21.0-beta.3)

### Chores

* remove custom code ([1698716](https://github.com/stainless-sdks/sink-python-public/commit/1698716521a9adaa998d214e9ddb8002bc252319))

## 1.21.0-beta.2 (2024-03-11)

Full Changelog: [v1.21.0-beta.1...v1.21.0-beta.2](https://github.com/stainless-sdks/sink-python-public/compare/v1.21.0-beta.1...v1.21.0-beta.2)

### Features

* add body param root with extra params ([#456](https://github.com/stainless-sdks/sink-python-public/issues/456)) ([dfe6b67](https://github.com/stainless-sdks/sink-python-public/commit/dfe6b67eff62ebe6f76506c76aa0be3139ee8179))
* add more pagination tests ([#447](https://github.com/stainless-sdks/sink-python-public/issues/447)) ([ccc4467](https://github.com/stainless-sdks/sink-python-public/commit/ccc44679a1e81473dc7aafa8b3def811965da9e8))
* add nested pagination array case ([#458](https://github.com/stainless-sdks/sink-python-public/issues/458)) ([c8a6229](https://github.com/stainless-sdks/sink-python-public/commit/c8a62295069bd7b5c292a852b37edf361ea93982))
* **api:** omit platform headers ([#461](https://github.com/stainless-sdks/sink-python-public/issues/461)) ([76f41a8](https://github.com/stainless-sdks/sink-python-public/commit/76f41a8e91e7907a79ca01dbfa6ee4bc772030c6))
* **api:** reduce unnecessary union ([#474](https://github.com/stainless-sdks/sink-python-public/issues/474)) ([4652b32](https://github.com/stainless-sdks/sink-python-public/commit/4652b3232b40d6c07f57a5f93d0d428d2dec32d5))


### Bug Fixes

* **docs:** better comment escape code handling ([#460](https://github.com/stainless-sdks/sink-python-public/issues/460)) ([bcb0ea8](https://github.com/stainless-sdks/sink-python-public/commit/bcb0ea8534b1501e29f6f3e659d04163a4d8a2e0))
* **types:** loosen most List params types to Iterable ([#446](https://github.com/stainless-sdks/sink-python-public/issues/446)) ([7d2b777](https://github.com/stainless-sdks/sink-python-public/commit/7d2b77797b86cda9851f40c143b0f7f80390c717))
* use qs.stringify for complex query parameters ([#473](https://github.com/stainless-sdks/sink-python-public/issues/473)) ([61b1dce](https://github.com/stainless-sdks/sink-python-public/commit/61b1dcef9677902f2bddca985e43542608178001))


### Chores

* add test for base64 params ([#470](https://github.com/stainless-sdks/sink-python-public/issues/470)) ([d3d49a3](https://github.com/stainless-sdks/sink-python-public/commit/d3d49a34d580657b211cb4e04be6e63796c12004))
* **client:** improve error message for invalid http_client argument ([#471](https://github.com/stainless-sdks/sink-python-public/issues/471)) ([a9e4c82](https://github.com/stainless-sdks/sink-python-public/commit/a9e4c8289993b80aff7213733d5f2273b3d4a116))
* **client:** use correct accept headers for binary data ([#454](https://github.com/stainless-sdks/sink-python-public/issues/454)) ([6d4b21c](https://github.com/stainless-sdks/sink-python-public/commit/6d4b21c87c675644e2e99bf02c5162d9738d9855))
* docs changes ([#451](https://github.com/stainless-sdks/sink-python-public/issues/451)) ([2aa0a8b](https://github.com/stainless-sdks/sink-python-public/commit/2aa0a8b216338b85a1f24a4c3f475f9fcb1c1470))
* **docs:** mention install from git repo ([#465](https://github.com/stainless-sdks/sink-python-public/issues/465)) ([3df7b1a](https://github.com/stainless-sdks/sink-python-public/commit/3df7b1a89cc461ab83584d71f4608282c5a8aeb0))
* export NOT_GIVEN sentinel value ([#477](https://github.com/stainless-sdks/sink-python-public/issues/477)) ([4de7ad4](https://github.com/stainless-sdks/sink-python-public/commit/4de7ad4f7d4ddf9843f96315bd3ca24703369e29))
* **internal:** add lint command ([#445](https://github.com/stainless-sdks/sink-python-public/issues/445)) ([905b43c](https://github.com/stainless-sdks/sink-python-public/commit/905b43c1ff7d9dccceeb930594affa06137a2b70))
* **internal:** bump pyright ([#459](https://github.com/stainless-sdks/sink-python-public/issues/459)) ([0a27fb9](https://github.com/stainless-sdks/sink-python-public/commit/0a27fb997342d576a04d67dccc38c3df9d08a25f))
* **internal:** bump pyright ([#475](https://github.com/stainless-sdks/sink-python-public/issues/475)) ([2618ec4](https://github.com/stainless-sdks/sink-python-public/commit/2618ec43adafe1ed3df23832e90e46fbe7e38216))
* **internal:** bump rye to v0.24.0 ([#455](https://github.com/stainless-sdks/sink-python-public/issues/455)) ([2f03d7c](https://github.com/stainless-sdks/sink-python-public/commit/2f03d7cb110478e3c686c7b4c2f2ada359a5873c))
* **internal:** improve deserialisation of discriminated unions ([#478](https://github.com/stainless-sdks/sink-python-public/issues/478)) ([114208d](https://github.com/stainless-sdks/sink-python-public/commit/114208d2683eca84efc675f1066539d997294d40))
* **internal:** minor core client restructuring ([#462](https://github.com/stainless-sdks/sink-python-public/issues/462)) ([ead517f](https://github.com/stainless-sdks/sink-python-public/commit/ead517f3cccaba81938f2755db270e4f64e617b1))
* **internal:** refactor release environment script ([#452](https://github.com/stainless-sdks/sink-python-public/issues/452)) ([ab423a2](https://github.com/stainless-sdks/sink-python-public/commit/ab423a2ea523422acf4173b2b770efd51a55e485))
* **internal:** split up transforms into sync / async ([#468](https://github.com/stainless-sdks/sink-python-public/issues/468)) ([8fe4b21](https://github.com/stainless-sdks/sink-python-public/commit/8fe4b215a83cf41760e7a0b81ef1efde48996845))
* **internal:** support more input types ([#469](https://github.com/stainless-sdks/sink-python-public/issues/469)) ([27a19e3](https://github.com/stainless-sdks/sink-python-public/commit/27a19e35ef2f02a09b5efb376e94f05325298c6f))
* **internal:** support parsing Annotated types ([#476](https://github.com/stainless-sdks/sink-python-public/issues/476)) ([1b0ac21](https://github.com/stainless-sdks/sink-python-public/commit/1b0ac21fdec3d7afdf8db7f8bb38af343a27ef05))
* **internal:** support serialising iterable types ([#443](https://github.com/stainless-sdks/sink-python-public/issues/443)) ([539ea65](https://github.com/stainless-sdks/sink-python-public/commit/539ea65ffde7f564ef539cd65f5d28105361a025))
* **internal:** update deps ([#457](https://github.com/stainless-sdks/sink-python-public/issues/457)) ([63cb52f](https://github.com/stainless-sdks/sink-python-public/commit/63cb52f0fddd5f5b36a7b0d5f6ee79c39f8e5700))
* move to sink_sdk import for testing config ([#463](https://github.com/stainless-sdks/sink-python-public/issues/463)) ([c20e59a](https://github.com/stainless-sdks/sink-python-public/commit/c20e59a3d72887617395c745842b90d16e00ea97))
* test methods not included in api.md ([#467](https://github.com/stainless-sdks/sink-python-public/issues/467)) ([ceed48c](https://github.com/stainless-sdks/sink-python-public/commit/ceed48cbe5f0679ef160ebb472a7f933c2160ac5))
* test resources not included in api.md ([#466](https://github.com/stainless-sdks/sink-python-public/issues/466)) ([3543f90](https://github.com/stainless-sdks/sink-python-public/commit/3543f906675eca2445eebb6bca3262b1a7a639c4))
* updates ([#449](https://github.com/stainless-sdks/sink-python-public/issues/449)) ([20b76c5](https://github.com/stainless-sdks/sink-python-public/commit/20b76c54e23758f246135d996d16ebf63e76837b))


### Documentation

* add CONTRIBUTING.md ([#448](https://github.com/stainless-sdks/sink-python-public/issues/448)) ([65063e5](https://github.com/stainless-sdks/sink-python-public/commit/65063e5666a5063b15a1417c911501d006dd29f3))
* **contributing:** improve wording ([#464](https://github.com/stainless-sdks/sink-python-public/issues/464)) ([9924c49](https://github.com/stainless-sdks/sink-python-public/commit/9924c49fa88f0dfb60ec75de68f22ed262f4a578))
* **readme:** fix async streaming snippet ([#472](https://github.com/stainless-sdks/sink-python-public/issues/472)) ([0939172](https://github.com/stainless-sdks/sink-python-public/commit/0939172eedbfdfbb0f357866de99424f0179b80a))

## 1.21.0-beta.1 (2024-02-04)

Full Changelog: [v1.20.1-beta.1...v1.21.0-beta.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.20.1-beta.1...v1.21.0-beta.1)

### Features

* **client:** enable follow redirects by default ([#435](https://github.com/stainless-sdks/sink-python-public/issues/435)) ([0467f7e](https://github.com/stainless-sdks/sink-python-public/commit/0467f7e503a10d3a11d35f059e89b355953bcad4))
* **client:** support parsing custom response types ([#438](https://github.com/stainless-sdks/sink-python-public/issues/438)) ([77b7c9b](https://github.com/stainless-sdks/sink-python-public/commit/77b7c9b2d59179feca69a79ab59107238be9fa81))


### Bug Fixes

* prevent crash when platform.architecture() is not allowed ([#442](https://github.com/stainless-sdks/sink-python-public/issues/442)) ([6883a9e](https://github.com/stainless-sdks/sink-python-public/commit/6883a9e769422e534beb23f1010073b842d2b368))


### Chores

* add more test cases for leading _ props ([#432](https://github.com/stainless-sdks/sink-python-public/issues/432)) ([29bf695](https://github.com/stainless-sdks/sink-python-public/commit/29bf6958eb6b10ca42a889b5056fb71380cf971e))
* add test for const enums ([#440](https://github.com/stainless-sdks/sink-python-public/issues/440)) ([5f04391](https://github.com/stainless-sdks/sink-python-public/commit/5f04391fd297cc61fcac4abcaca1551ea9a906fb))
* **internal:** cast type in mocked test ([#439](https://github.com/stainless-sdks/sink-python-public/issues/439)) ([53a178e](https://github.com/stainless-sdks/sink-python-public/commit/53a178e6e16625795cf90a8e14cda643dfc85790))
* **internal:** enable ruff type checking misuse lint rule ([#437](https://github.com/stainless-sdks/sink-python-public/issues/437)) ([8414d33](https://github.com/stainless-sdks/sink-python-public/commit/8414d33b1c47362e99576f02d029a3d32a29c349))
* **internal:** support multipart data with overlapping keys ([#436](https://github.com/stainless-sdks/sink-python-public/issues/436)) ([2ad11aa](https://github.com/stainless-sdks/sink-python-public/commit/2ad11aa13badc1eec2372294a5ec74dbe7c17dec))
* **internal:** support pre-release versioning ([#441](https://github.com/stainless-sdks/sink-python-public/issues/441)) ([dd4841c](https://github.com/stainless-sdks/sink-python-public/commit/dd4841c863752c1869b02e1bc570bce34dc905b0))


### Refactors

* remove unnecessary builtin import ([#434](https://github.com/stainless-sdks/sink-python-public/issues/434)) ([c378c65](https://github.com/stainless-sdks/sink-python-public/commit/c378c65a3a1c0e6da81807ed8cf18feeaa814d53))

## 1.20.1-beta.1 (2024-01-18)

Full Changelog: [v1.20.0-beta.1...v1.20.1-beta.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.20.0-beta.1...v1.20.1-beta.1)

### Bug Fixes

* add test for case when every param in a body is read-only ([#430](https://github.com/stainless-sdks/sink-python-public/issues/430)) ([5c0ac10](https://github.com/stainless-sdks/sink-python-public/commit/5c0ac1013d40e220d78a068c1559a0255204f4b2))

## 1.20.0-beta.1 (2024-01-18)

Full Changelog: [v1.19.0...v1.20.0-beta.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.19.0...v1.20.0-beta.1)

### Features

* add and test `send_as_query_param` and `send_as_path_param` ([#422](https://github.com/stainless-sdks/sink-python-public/issues/422)) ([fcb88e9](https://github.com/stainless-sdks/sink-python-public/commit/fcb88e9461e8f55d7e8da778a553f5983bd7d959))
* add path param enum test ([#423](https://github.com/stainless-sdks/sink-python-public/issues/423)) ([bc8b8e7](https://github.com/stainless-sdks/sink-python-public/commit/bc8b8e7ef702f53a269870d75de6111198701e69))
* add test for resource with only custom methods ([#421](https://github.com/stainless-sdks/sink-python-public/issues/421)) ([261334f](https://github.com/stainless-sdks/sink-python-public/commit/261334f1c47a6944deea5a947f2cc1fe9d9a342c))
* **client:** add support for streaming raw responses ([#420](https://github.com/stainless-sdks/sink-python-public/issues/420)) ([22aa937](https://github.com/stainless-sdks/sink-python-public/commit/22aa937735b242f2fbeb430a5fc61f92602691f6))


### Chores

* **internal:** fix typing util function ([#425](https://github.com/stainless-sdks/sink-python-public/issues/425)) ([f2a332a](https://github.com/stainless-sdks/sink-python-public/commit/f2a332a0d64f8b4d88bc0f9ed3489c969d04adef))
* **internal:** remove redundant client test ([#426](https://github.com/stainless-sdks/sink-python-public/issues/426)) ([1c6389c](https://github.com/stainless-sdks/sink-python-public/commit/1c6389c1b0441a460528fb19e40a716e0a4f5149))
* **internal:** share client instances between all tests ([#429](https://github.com/stainless-sdks/sink-python-public/issues/429)) ([c87da80](https://github.com/stainless-sdks/sink-python-public/commit/c87da806b47de6b7f57a22bf7c031e75eda48a13))
* **internal:** speculative retry-after-ms support ([#427](https://github.com/stainless-sdks/sink-python-public/issues/427)) ([622c5c0](https://github.com/stainless-sdks/sink-python-public/commit/622c5c0fac4aae21ddbe3ecfb22cfdcdda3b3099))
* **internal:** updates to proxy helper ([#424](https://github.com/stainless-sdks/sink-python-public/issues/424)) ([41a41ef](https://github.com/stainless-sdks/sink-python-public/commit/41a41ef5e5cb244183d0087f3f4f565f7d00f939))
* lazy load raw resource class properties ([#428](https://github.com/stainless-sdks/sink-python-public/issues/428)) ([b782293](https://github.com/stainless-sdks/sink-python-public/commit/b782293af7ccd33c4e7bb02ab7334e5e1a60a57e))


### Documentation

* **readme:** improve api reference ([#418](https://github.com/stainless-sdks/sink-python-public/issues/418)) ([7484d19](https://github.com/stainless-sdks/sink-python-public/commit/7484d1934f1a0835e966523f067334bcaceb4a58))

## 1.19.0 (2024-01-10)

Full Changelog: [v1.18.0...v1.19.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.18.0...v1.19.0)

### Features

* **types:** add test for unknown paginated items ([#414](https://github.com/stainless-sdks/sink-python-public/issues/414)) ([afaec95](https://github.com/stainless-sdks/sink-python-public/commit/afaec95169f9a2cf9d0f8badf91bf30afdde05f2))


### Chores

* add .keep files for examples and custom code directories ([#416](https://github.com/stainless-sdks/sink-python-public/issues/416)) ([e675a0c](https://github.com/stainless-sdks/sink-python-public/commit/e675a0c33e4867149b534c741b57fd366a235fbf))
* **client:** improve debug logging for failed requests ([#417](https://github.com/stainless-sdks/sink-python-public/issues/417)) ([690a83d](https://github.com/stainless-sdks/sink-python-public/commit/690a83d3d114b320f21a03aa0af5a6ef31b50cb5))

## 1.18.0 (2024-01-05)

Full Changelog: [v1.17.0...v1.18.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.17.0...v1.18.0)

### Features

* add test case for models using $ref syntax ([#411](https://github.com/stainless-sdks/sink-python-public/issues/411)) ([bf1cb91](https://github.com/stainless-sdks/sink-python-public/commit/bf1cb91997190eac6b3f245e7095aca89aaa11f1))


### Bug Fixes

* escape interface names, fix pagination types ([#413](https://github.com/stainless-sdks/sink-python-public/issues/413)) ([e0ada8d](https://github.com/stainless-sdks/sink-python-public/commit/e0ada8dfb49ba2148e6182423fca5df1c6c047e1))


### Chores

* **internal:** bump license ([#408](https://github.com/stainless-sdks/sink-python-public/issues/408)) ([ef91d8c](https://github.com/stainless-sdks/sink-python-public/commit/ef91d8c29655a009ad7225bcfff4e6a2211e4b98))
* **internal:** replace isort with ruff ([#410](https://github.com/stainless-sdks/sink-python-public/issues/410)) ([0a7cfc7](https://github.com/stainless-sdks/sink-python-public/commit/0a7cfc78468d74262366f5eb284fe8298a8e1ef2))
* use property declarations for resource members ([#412](https://github.com/stainless-sdks/sink-python-public/issues/412)) ([8e4cd34](https://github.com/stainless-sdks/sink-python-public/commit/8e4cd349d5673426b9856150aca4306d84e18a08))

## 1.17.0 (2023-12-28)

Full Changelog: [v1.16.0...v1.17.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.16.0...v1.17.0)

### Features

* add test for fake pages ([#402](https://github.com/stainless-sdks/sink-python-public/issues/402)) ([cb8e7e6](https://github.com/stainless-sdks/sink-python-public/commit/cb8e7e61e41fc6b6f94b156ff8f48ef1500aa86f))


### Bug Fixes

* better typing for parameters when `x-stainless-empty-object: true` ([#403](https://github.com/stainless-sdks/sink-python-public/issues/403)) ([d69eb4a](https://github.com/stainless-sdks/sink-python-public/commit/d69eb4a09cfc2c6bd5bb0f7b716c24befd33ce44))
* **client:** correctly use custom http client auth ([#407](https://github.com/stainless-sdks/sink-python-public/issues/407)) ([adabba5](https://github.com/stainless-sdks/sink-python-public/commit/adabba57b3b1ba6ea8b673b43402e7e40a4a26e0))


### Chores

* **internal:** add bin script ([#404](https://github.com/stainless-sdks/sink-python-public/issues/404)) ([9b4f1c0](https://github.com/stainless-sdks/sink-python-public/commit/9b4f1c09f8da7bbd05c7fa0003ddb073a33aef9d))
* **internal:** bump typing-extensions ([#401](https://github.com/stainless-sdks/sink-python-public/issues/401)) ([6b541d5](https://github.com/stainless-sdks/sink-python-public/commit/6b541d594a1338fdd6dabe115e2e970fffd2a2f7))
* **internal:** fix typos ([#400](https://github.com/stainless-sdks/sink-python-public/issues/400)) ([b2ccc5f](https://github.com/stainless-sdks/sink-python-public/commit/b2ccc5fa7cfa5267d2e3c1b8fc855d9568dff042))
* **internal:** minor utils restructuring ([#399](https://github.com/stainless-sdks/sink-python-public/issues/399)) ([36229d2](https://github.com/stainless-sdks/sink-python-public/commit/36229d27148c45f0ec889fbbbefafd6b2170f7a3))
* **internal:** updates to base client ([#397](https://github.com/stainless-sdks/sink-python-public/issues/397)) ([c849f2e](https://github.com/stainless-sdks/sink-python-public/commit/c849f2e9381977c50d8fcd993ec9d4cb8666d209))
* **internal:** use ruff instead of black for formatting ([#406](https://github.com/stainless-sdks/sink-python-public/issues/406)) ([e3d12c7](https://github.com/stainless-sdks/sink-python-public/commit/e3d12c71c68f1fe94bf30a7fcd16a6a2eff35f31))

## 1.16.0 (2023-12-18)

Full Changelog: [v1.15.2...v1.16.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.15.2...v1.16.0)

### Features

* add test case for reserved params names ([#396](https://github.com/stainless-sdks/sink-python-public/issues/396)) ([63ef425](https://github.com/stainless-sdks/sink-python-public/commit/63ef425e0103cfd98e735b06c758eb7e2e2a778c))
* add test for binary endpoint with a path param ([#395](https://github.com/stainless-sdks/sink-python-public/issues/395)) ([af6c68b](https://github.com/stainless-sdks/sink-python-public/commit/af6c68b9f43bb3588beb6ea83363e69be9c67a2a))


### Bug Fixes

* better typing for parameters when request body is defined as empty ([#394](https://github.com/stainless-sdks/sink-python-public/issues/394)) ([63ee967](https://github.com/stainless-sdks/sink-python-public/commit/63ee967b8a202c4923fcaf8a155b57fddcf20ff9))


### Chores

* uses Stainless GitHub App for codeflow ([#388](https://github.com/stainless-sdks/sink-python-public/issues/388)) ([89718eb](https://github.com/stainless-sdks/sink-python-public/commit/89718eb69cde6486c10b58f003d5869afb68c145))


### Documentation

* improve README timeout comment ([#390](https://github.com/stainless-sdks/sink-python-public/issues/390)) ([d44cb4f](https://github.com/stainless-sdks/sink-python-public/commit/d44cb4f29f5ec9e87ec66a667dde4d40b915342a))


### Refactors

* **client:** simplify cleanup ([#391](https://github.com/stainless-sdks/sink-python-public/issues/391)) ([eee21b2](https://github.com/stainless-sdks/sink-python-public/commit/eee21b2d4cc1f64ea1621dc00a14f9a961122446))
* remove unused model types used in params ([#393](https://github.com/stainless-sdks/sink-python-public/issues/393)) ([2f9d6ab](https://github.com/stainless-sdks/sink-python-public/commit/2f9d6abe303d061767336c40fce6b852958ea59c))
* simplify internal error handling ([#392](https://github.com/stainless-sdks/sink-python-public/issues/392)) ([927e01b](https://github.com/stainless-sdks/sink-python-public/commit/927e01b1c4b6a6dfee084d78723afbd20f1c9af4))

## 1.15.2 (2023-12-08)

Full Changelog: [v1.15.1...v1.15.2](https://github.com/stainless-sdks/sink-python-public/compare/v1.15.1...v1.15.2)

### Bug Fixes

* avoid leaking memory when Client.with_options is used ([#386](https://github.com/stainless-sdks/sink-python-public/issues/386)) ([44bf594](https://github.com/stainless-sdks/sink-python-public/commit/44bf594f4e3b0080d57d36fedacfb041310e7887))

## 1.15.1 (2023-12-08)

Full Changelog: [v1.15.0...v1.15.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.15.0...v1.15.1)

### Bug Fixes

* **errors:** properly assign APIError.body ([#384](https://github.com/stainless-sdks/sink-python-public/issues/384)) ([c239fe9](https://github.com/stainless-sdks/sink-python-public/commit/c239fe9c4658e3b977506868c3b003f0f85b7ff9))

## 1.15.0 (2023-12-07)

Full Changelog: [v1.14.0...v1.15.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.14.0...v1.15.0)

### Features

* add support for pagination refs ([#379](https://github.com/stainless-sdks/sink-python-public/issues/379)) ([7e7d15c](https://github.com/stainless-sdks/sink-python-public/commit/7e7d15cfdfae4bc95d736cb34f836b172b88f8f7))
* **pagination:** add test for cursor_id without previous cursor param ([#377](https://github.com/stainless-sdks/sink-python-public/issues/377)) ([5772bd5](https://github.com/stainless-sdks/sink-python-public/commit/5772bd5d1234e1ec56172f0d5a6c2a0b959b9a59))


### Chores

* **internal:** enable more lint rules ([#383](https://github.com/stainless-sdks/sink-python-public/issues/383)) ([9024110](https://github.com/stainless-sdks/sink-python-public/commit/902411068fcbfddd44c0a46d8e688026cb960f1f))
* **internal:** reformat imports ([#381](https://github.com/stainless-sdks/sink-python-public/issues/381)) ([6a07586](https://github.com/stainless-sdks/sink-python-public/commit/6a075862cd6e4f152534d44a1fdbde5990002f44))
* **internal:** reformat imports ([#382](https://github.com/stainless-sdks/sink-python-public/issues/382)) ([a2205fa](https://github.com/stainless-sdks/sink-python-public/commit/a2205fa95c1f27f0a7df4caea3415d5313b88534))

## 1.14.0 (2023-12-04)

Full Changelog: [v1.13.0...v1.14.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.13.0...v1.14.0)

### Features

* **pagination:** add support for top-level arrays ([#375](https://github.com/stainless-sdks/sink-python-public/issues/375)) ([22ac11b](https://github.com/stainless-sdks/sink-python-public/commit/22ac11b6b3414afcb8dcddff537b306c1acc5c88))
* **pagination:** support response headers ([#371](https://github.com/stainless-sdks/sink-python-public/issues/371)) ([21081ac](https://github.com/stainless-sdks/sink-python-public/commit/21081ac3886ae19d3e49c986bb18db07e07ba397))


### Chores

* **package:** lift anyio v4 restriction ([#373](https://github.com/stainless-sdks/sink-python-public/issues/373)) ([3c62f7c](https://github.com/stainless-sdks/sink-python-public/commit/3c62f7c261f7df43011eb4d4d661846140dd0390))

## 1.13.0 (2023-12-01)

Full Changelog: [v1.12.1...v1.13.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.12.1...v1.13.0)

### Features

* **pagination:** add offset support ([#368](https://github.com/stainless-sdks/sink-python-public/issues/368)) ([b6f3d34](https://github.com/stainless-sdks/sink-python-public/commit/b6f3d340a606b2c439fb6551b3981283c9be6160))
* **pagination:** add support for cursor_url ([#369](https://github.com/stainless-sdks/sink-python-public/issues/369)) ([87f393f](https://github.com/stainless-sdks/sink-python-public/commit/87f393fd0934b2810cc79573ed7ed577f3f34ee4))


### Bug Fixes

* **client:** correct base_url setter implementation ([#370](https://github.com/stainless-sdks/sink-python-public/issues/370)) ([b62c111](https://github.com/stainless-sdks/sink-python-public/commit/b62c1118b64e7b22e6a00e1511d243db3f03795c))


### Chores

* **internal:** replace string concatenation with f-strings ([#366](https://github.com/stainless-sdks/sink-python-public/issues/366)) ([2e80f83](https://github.com/stainless-sdks/sink-python-public/commit/2e80f83191582daa796dcdb8a54c29980b6cbd80))
* remove pagination tests for now ([#367](https://github.com/stainless-sdks/sink-python-public/issues/367)) ([640303c](https://github.com/stainless-sdks/sink-python-public/commit/640303c992784a16b99e5911fda7875c4bebfd23))


### Documentation

* **readme:** update example snippets ([#364](https://github.com/stainless-sdks/sink-python-public/issues/364)) ([5d26ea1](https://github.com/stainless-sdks/sink-python-public/commit/5d26ea12b473bed69f0c177997093a264bca3825))

## 1.12.1 (2023-11-30)

Full Changelog: [v1.12.0...v1.12.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.12.0...v1.12.1)

### Bug Fixes

* **client:** ensure retried requests are closed ([#363](https://github.com/stainless-sdks/sink-python-public/issues/363)) ([4383f52](https://github.com/stainless-sdks/sink-python-public/commit/4383f524f7961b5cc1549ef84cf721bba070bd0e))


### Chores

* **client:** improve copy method ([#354](https://github.com/stainless-sdks/sink-python-public/issues/354)) ([dcee1bd](https://github.com/stainless-sdks/sink-python-public/commit/dcee1bdfeb822ea8346154574db8b454331818fa))
* **deps:** bump mypy to v1.7.1 ([#359](https://github.com/stainless-sdks/sink-python-public/issues/359)) ([c1ada65](https://github.com/stainless-sdks/sink-python-public/commit/c1ada65a9c433cd02c6f7ffd6b6f04b92f86a292))
* **docs:** fix argument names in docstrings ([#352](https://github.com/stainless-sdks/sink-python-public/issues/352)) ([43e86b0](https://github.com/stainless-sdks/sink-python-public/commit/43e86b0c8647c1aba73998da50597757f93b3a0e))
* **internal:** add tests for proxy change ([#362](https://github.com/stainless-sdks/sink-python-public/issues/362)) ([6069582](https://github.com/stainless-sdks/sink-python-public/commit/606958228c32b2bd04b2e24ba0b1bafbdc057511))
* **internal:** options updates ([#356](https://github.com/stainless-sdks/sink-python-public/issues/356)) ([d06046b](https://github.com/stainless-sdks/sink-python-public/commit/d06046beb69b42f391d2e0484fd00e520fd33b24))
* **internal:** revert recent options change ([#357](https://github.com/stainless-sdks/sink-python-public/issues/357)) ([62f9c7e](https://github.com/stainless-sdks/sink-python-public/commit/62f9c7e0adb8f1bf40c30d311c6885001330ebd2))
* **internal:** send more detailed x-stainless headers ([#358](https://github.com/stainless-sdks/sink-python-public/issues/358)) ([2437a93](https://github.com/stainless-sdks/sink-python-public/commit/2437a9342514d67e23ae694635db8d67d332f6b1))
* **internal:** updates to proxy helper ([#361](https://github.com/stainless-sdks/sink-python-public/issues/361)) ([4e4402b](https://github.com/stainless-sdks/sink-python-public/commit/4e4402bb93496bbabb69650e6664609ba44f165f))
* **package:** add license classifier metadata ([#355](https://github.com/stainless-sdks/sink-python-public/issues/355)) ([c18227f](https://github.com/stainless-sdks/sink-python-public/commit/c18227fe388fc802ba3cfc38f4fcf8a5f67d1b9c))

## 1.12.0 (2023-11-21)

Full Changelog: [v1.11.3...v1.12.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.11.3...v1.12.0)

### Features

* add string type test ([#347](https://github.com/stainless-sdks/sink-python-public/issues/347)) ([7b16a91](https://github.com/stainless-sdks/sink-python-public/commit/7b16a919f92288beb517c44b11cbcacdd868de4c))
* add tests for union with unknown variant ([#348](https://github.com/stainless-sdks/sink-python-public/issues/348)) ([c9684b5](https://github.com/stainless-sdks/sink-python-public/commit/c9684b5bd8b47d01f0a63d53dca4a5623194f333))
* **client:** support reading the base url from an env variable ([#343](https://github.com/stainless-sdks/sink-python-public/issues/343)) ([c0b050e](https://github.com/stainless-sdks/sink-python-public/commit/c0b050e4ca7f8ae099ebc8ad01fcf76af36cae8c))
* idk ([#341](https://github.com/stainless-sdks/sink-python-public/issues/341)) ([745ad7e](https://github.com/stainless-sdks/sink-python-public/commit/745ad7e29e6f81b3ac0207ded753e9a51d967887))


### Bug Fixes

* **client:** attempt to parse unknown json content types ([#351](https://github.com/stainless-sdks/sink-python-public/issues/351)) ([227c50d](https://github.com/stainless-sdks/sink-python-public/commit/227c50db49eaf4022e8702a32afe0f1b68d7499d))


### Chores

* **internal:** fix devcontainer interpeter path ([#340](https://github.com/stainless-sdks/sink-python-public/issues/340)) ([83271cf](https://github.com/stainless-sdks/sink-python-public/commit/83271cfe1532d9cb71dd1540599a9c97bae3d714))
* **internal:** fix some docstring argument names ([#349](https://github.com/stainless-sdks/sink-python-public/issues/349)) ([375fa99](https://github.com/stainless-sdks/sink-python-public/commit/375fa993e8dbe4e3f11e476bd5b06884a8b9e9e3))
* **internal:** fix typo in NotGiven docstring ([#338](https://github.com/stainless-sdks/sink-python-public/issues/338)) ([a758078](https://github.com/stainless-sdks/sink-python-public/commit/a758078ea54979f8ef4e4c234b46c2611be678f2))
* **internal:** update stats file ([#345](https://github.com/stainless-sdks/sink-python-public/issues/345)) ([5de6a32](https://github.com/stainless-sdks/sink-python-public/commit/5de6a326b182a697b9265e64457ae3b7be6c5d45))
* **internal:** update type hint for helper function ([#350](https://github.com/stainless-sdks/sink-python-public/issues/350)) ([fb3c127](https://github.com/stainless-sdks/sink-python-public/commit/fb3c127dc32c03967ab1c5eb80af64c73cf07b95))
* update enum tests ([#346](https://github.com/stainless-sdks/sink-python-public/issues/346)) ([0780884](https://github.com/stainless-sdks/sink-python-public/commit/07808844b0b143c7647f63114c39a02d36f0d70b))


### Documentation

* fix code comment typo ([#342](https://github.com/stainless-sdks/sink-python-public/issues/342)) ([2b24c3c](https://github.com/stainless-sdks/sink-python-public/commit/2b24c3c416396cd14c7873e6896ef517ddb13657))
* **readme:** minor updates ([#344](https://github.com/stainless-sdks/sink-python-public/issues/344)) ([9034162](https://github.com/stainless-sdks/sink-python-public/commit/9034162dc3267ebb4d31bb6f0c1f6b951424cb76))

## 1.11.3 (2023-11-13)

Full Changelog: [v1.11.2...v1.11.3](https://github.com/stainless-sdks/sink-python-public/compare/v1.11.2...v1.11.3)

### Bug Fixes

* **client:** retry if SSLWantReadError occurs in the async client ([#336](https://github.com/stainless-sdks/sink-python-public/issues/336)) ([7065e26](https://github.com/stainless-sdks/sink-python-public/commit/7065e26ca8ccce082634f59acf56f7f91768fcc5))

## 1.11.2 (2023-11-10)

Full Changelog: [v1.11.1...v1.11.2](https://github.com/stainless-sdks/sink-python-public/compare/v1.11.1...v1.11.2)

### Bug Fixes

* **client:** serialise pydantic v1 default fields correctly in params ([#334](https://github.com/stainless-sdks/sink-python-public/issues/334)) ([91a5093](https://github.com/stainless-sdks/sink-python-public/commit/91a50931dfc78f16b8eee4cfbf6f948b1af98bae))

## 1.11.1 (2023-11-10)

Full Changelog: [v1.11.0...v1.11.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.11.0...v1.11.1)

### Bug Fixes

* **models:** mark unknown fields as set in pydantic v1 ([#332](https://github.com/stainless-sdks/sink-python-public/issues/332)) ([d82b7d8](https://github.com/stainless-sdks/sink-python-public/commit/d82b7d8ef2085be4b6c1418d2d9d07f4d41401e7))

## 1.11.0 (2023-11-10)

Full Changelog: [v1.10.0...v1.11.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.10.0...v1.11.0)

### Features

* **client:** support passing chunk size for binary responses ([#329](https://github.com/stainless-sdks/sink-python-public/issues/329)) ([21adeb9](https://github.com/stainless-sdks/sink-python-public/commit/21adeb9803b524a046148ef62478c12988562f74))
* **client:** support passing httpx.Timeout to method timeout argument ([#323](https://github.com/stainless-sdks/sink-python-public/issues/323)) ([d798c7f](https://github.com/stainless-sdks/sink-python-public/commit/d798c7fc6cd9ba9262d53a82f0558b2b47d3b54a))


### Bug Fixes

* **client:** correctly flush the stream response body ([#331](https://github.com/stainless-sdks/sink-python-public/issues/331)) ([c5391af](https://github.com/stainless-sdks/sink-python-public/commit/c5391af8f62a72f4074c5e74c92eae494557884e))


### Chores

* **docs:** fix github links ([#326](https://github.com/stainless-sdks/sink-python-public/issues/326)) ([00bcc79](https://github.com/stainless-sdks/sink-python-public/commit/00bcc794a9453f2916e4cb8e446555bd386370ff))
* **internal:** fix some typos ([#325](https://github.com/stainless-sdks/sink-python-public/issues/325)) ([455cda5](https://github.com/stainless-sdks/sink-python-public/commit/455cda58ce6433315e16588a8de23bf855f45a6e))
* **internal:** improve github devcontainer setup ([#328](https://github.com/stainless-sdks/sink-python-public/issues/328)) ([168adf7](https://github.com/stainless-sdks/sink-python-public/commit/168adf799c7214971b892a6ca2c843221dd5fb6e))
* **types:** add more array types tests ([#327](https://github.com/stainless-sdks/sink-python-public/issues/327)) ([6666614](https://github.com/stainless-sdks/sink-python-public/commit/66666143949965164f0a55842e7a5b6a11af513e))


### Documentation

* reword package description ([#330](https://github.com/stainless-sdks/sink-python-public/issues/330)) ([d64aa3d](https://github.com/stainless-sdks/sink-python-public/commit/d64aa3dab4f54c460e2b9a87520a60d24e3e0237))

## 1.10.0 (2023-11-06)

Full Changelog: [v1.9.0...v1.10.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.9.0...v1.10.0)

### Features

* temporarily skip mutual recursion cases ([#319](https://github.com/stainless-sdks/sink-python-public/issues/319)) ([fc0444b](https://github.com/stainless-sdks/sink-python-public/commit/fc0444ba0bed913c50442307753338ae053e8801))


### Bug Fixes

* prevent TypeError in Python 3.8 (ABC is not subscriptable) ([#322](https://github.com/stainless-sdks/sink-python-public/issues/322)) ([64770ff](https://github.com/stainless-sdks/sink-python-public/commit/64770ffe936cc73d7c680de52298cff4b2e2bdb6))


### Chores

* **internal:** remove unused int/float conversion ([#320](https://github.com/stainless-sdks/sink-python-public/issues/320)) ([8489d07](https://github.com/stainless-sdks/sink-python-public/commit/8489d07c9408a3d3f4265d0fcea1131f9b956cfd))


### Documentation

* **api:** improve method signatures for named path params ([#317](https://github.com/stainless-sdks/sink-python-public/issues/317)) ([67d81e9](https://github.com/stainless-sdks/sink-python-public/commit/67d81e98b65edb1a876456984d456c7331a7b70c))
* **readme:** improve example snippets ([#321](https://github.com/stainless-sdks/sink-python-public/issues/321)) ([615ae3d](https://github.com/stainless-sdks/sink-python-public/commit/615ae3d087fbf9a0efd5477ab80e61c1737ec29c))

## 1.9.0 (2023-11-03)

Full Changelog: [v1.8.1...v1.9.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.8.1...v1.9.0)

### Features

* add support for default headers per-resource ([#311](https://github.com/stainless-sdks/sink-python-public/issues/311)) ([83e671c](https://github.com/stainless-sdks/sink-python-public/commit/83e671ccd1c792acad0c78711be48c3732c72c00))
* add union type name tests ([#313](https://github.com/stainless-sdks/sink-python-public/issues/313)) ([9b2ef1d](https://github.com/stainless-sdks/sink-python-public/commit/9b2ef1defbf26615fabd9df910892038844e8c8e))
* **client:** allow binary returns ([#314](https://github.com/stainless-sdks/sink-python-public/issues/314)) ([b3b610e](https://github.com/stainless-sdks/sink-python-public/commit/b3b610e180722d968caed4e38acb0a3997a14ae8))
* **client:** support accessing raw response objects ([#306](https://github.com/stainless-sdks/sink-python-public/issues/306)) ([aa1b0a3](https://github.com/stainless-sdks/sink-python-public/commit/aa1b0a3c82017440b6696905ecce436dde7e9e11))
* **client:** support passing BaseModels to request params at runtime ([#315](https://github.com/stainless-sdks/sink-python-public/issues/315)) ([1512d45](https://github.com/stainless-sdks/sink-python-public/commit/1512d45e35654496d77564d27734b996b7b52f69))
* **github:** include a devcontainer setup ([#312](https://github.com/stainless-sdks/sink-python-public/issues/312)) ([205d58d](https://github.com/stainless-sdks/sink-python-public/commit/205d58d7d2262a4c36b9fde1c09efa5d0d9b5501))
* **package:** add classifiers ([#310](https://github.com/stainless-sdks/sink-python-public/issues/310)) ([cc0502a](https://github.com/stainless-sdks/sink-python-public/commit/cc0502ab4fb789cba4c4ab35e80bf6e8081e2c23))


### Bug Fixes

* **binaries:** don't synchronously block in astream_to_file ([#316](https://github.com/stainless-sdks/sink-python-public/issues/316)) ([b9d2d6b](https://github.com/stainless-sdks/sink-python-public/commit/b9d2d6be0260e23d86f8bbea139a76655c3a0ceb))


### Chores

* **internal:** minor restructuring of base client ([#309](https://github.com/stainless-sdks/sink-python-public/issues/309)) ([8629df3](https://github.com/stainless-sdks/sink-python-public/commit/8629df381102fbfb11dfe232820a82c2ea5345c2))

## 1.8.1 (2023-10-26)

Full Changelog: [v1.8.0...v1.8.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.8.0...v1.8.1)

### Chores

* **internal:** require explicit overrides ([#304](https://github.com/stainless-sdks/sink-python-public/issues/304)) ([9842624](https://github.com/stainless-sdks/sink-python-public/commit/9842624f098b3c9e28612a9f9f1b2cc5d48b2fd1))

## 1.8.0 (2023-10-26)

Full Changelog: [v1.7.0...v1.8.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.7.0...v1.8.0)

### Features

* more unions tests ([#302](https://github.com/stainless-sdks/sink-python-public/issues/302)) ([46d2282](https://github.com/stainless-sdks/sink-python-public/commit/46d228258feab2014edd2ae1e51e1483e24096bf))


### Documentation

* improve to dictionary example ([#300](https://github.com/stainless-sdks/sink-python-public/issues/300)) ([2b3ec08](https://github.com/stainless-sdks/sink-python-public/commit/2b3ec08e431766660ecb80110f4878f5e05bb4ba))

## 1.7.0 (2023-10-24)

Full Changelog: [v1.6.3...v1.7.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.6.3...v1.7.0)

### Features

* **client:** improve file upload types ([#297](https://github.com/stainless-sdks/sink-python-public/issues/297)) ([97ef7fd](https://github.com/stainless-sdks/sink-python-public/commit/97ef7fdd3f6969c194e78e4af6477ffb30fe7cf2))

## 1.6.3 (2023-10-20)

Full Changelog: [v1.6.2...v1.6.3](https://github.com/stainless-sdks/sink-python-public/compare/v1.6.2...v1.6.3)

### Chores

* **internal:** bump mypy ([#295](https://github.com/stainless-sdks/sink-python-public/issues/295)) ([59ad33a](https://github.com/stainless-sdks/sink-python-public/commit/59ad33aedf39efd77b2125338947d51854dd9375))

## 1.6.2 (2023-10-20)

Full Changelog: [v1.6.1...v1.6.2](https://github.com/stainless-sdks/sink-python-public/compare/v1.6.1...v1.6.2)

### Chores

* **internal:** bump pyright ([#293](https://github.com/stainless-sdks/sink-python-public/issues/293)) ([a9c7182](https://github.com/stainless-sdks/sink-python-public/commit/a9c7182112bdb7695000d161d1546e7ca3300353))

## 1.6.1 (2023-10-19)

Full Changelog: [v1.5.2...v1.6.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.5.2...v1.6.1)

### Features

* **client:** support passing httpx.URL instances to base_url ([#288](https://github.com/stainless-sdks/sink-python-public/issues/288)) ([fda1ded](https://github.com/stainless-sdks/sink-python-public/commit/fda1ded935d98301e1da4c41c88779c2318259f6))


### Chores

* **internal:** update gitignore ([#290](https://github.com/stainless-sdks/sink-python-public/issues/290)) ([c71382a](https://github.com/stainless-sdks/sink-python-public/commit/c71382abc6d71b7dba81f9d3e8dcdc1b28f9c5e8))
* **internal:** update gitignore ([#291](https://github.com/stainless-sdks/sink-python-public/issues/291)) ([01f5d89](https://github.com/stainless-sdks/sink-python-public/commit/01f5d89b5e9a4f59fc114a5fa338f80b226f6113))

## 1.5.2 (2023-10-17)

Full Changelog: [v1.5.1...v1.5.2](https://github.com/stainless-sdks/sink-python-public/compare/v1.5.1...v1.5.2)

### Chores

* **internal:** improve publish script ([#286](https://github.com/stainless-sdks/sink-python-public/issues/286)) ([296fe57](https://github.com/stainless-sdks/sink-python-public/commit/296fe577ab42b9756695e89af321d76ce888496d))

## 1.5.1 (2023-10-17)

Full Changelog: [v1.5.0...v1.5.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.5.0...v1.5.1)

### Chores

* **internal:** migrate from Poetry to Rye ([#284](https://github.com/stainless-sdks/sink-python-public/issues/284)) ([ed3b9fb](https://github.com/stainless-sdks/sink-python-public/commit/ed3b9fbed913c2e7c3ccef6a5bd85ac17d7ce563))

## 1.5.0 (2023-10-17)

Full Changelog: [v1.4.1...v1.5.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.4.1...v1.5.0)

### Features

* use Rye instead of Poetry!!! ([acb9d00](https://github.com/stainless-sdks/sink-python-public/commit/acb9d00d65bb3f1cb38f420eb7002454dae0e841))

## 1.4.1 (2023-10-17)

Full Changelog: [v1.4.0...v1.4.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.4.0...v1.4.1)

### Chores

* test change ([e126521](https://github.com/stainless-sdks/sink-python-public/commit/e12652107613089e0340f28135fbc818a8fcf8aa))

## 1.4.0 (2023-10-17)

Full Changelog: [v1.3.1...v1.4.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.3.1...v1.4.0)

### Features

* add case for nullable unions ([#277](https://github.com/stainless-sdks/sink-python-public/issues/277)) ([906363a](https://github.com/stainless-sdks/sink-python-public/commit/906363aef298e245ce80ecba63a67b693acc91e4))
* add tests for date path params ([#281](https://github.com/stainless-sdks/sink-python-public/issues/281)) ([c62fff8](https://github.com/stainless-sdks/sink-python-public/commit/c62fff862d20c432654a3f1eac6507e68a34e041))
* partially add extra_params_and_fields case ([#275](https://github.com/stainless-sdks/sink-python-public/issues/275)) ([0211b94](https://github.com/stainless-sdks/sink-python-public/commit/0211b94b8d0139ce483f03b607be77e5fc369452))


### Bug Fixes

* **client:** accept io.IOBase instances in file params ([#278](https://github.com/stainless-sdks/sink-python-public/issues/278)) ([44ef9eb](https://github.com/stainless-sdks/sink-python-public/commit/44ef9eb9722cd46816b8d529aefaad64800937cd))


### Documentation

* improve error message for invalid file param type ([#280](https://github.com/stainless-sdks/sink-python-public/issues/280)) ([4f8005a](https://github.com/stainless-sdks/sink-python-public/commit/4f8005a0f527c62a54ab5684975f4acec4f51823))
* organisation -&gt; organization (UK to US English) ([#279](https://github.com/stainless-sdks/sink-python-public/issues/279)) ([2773f0e](https://github.com/stainless-sdks/sink-python-public/commit/2773f0ecdf95e455c5de4a016ce73da9dc483a77))

## 1.3.1 (2023-10-16)

Full Changelog: [v1.3.0...v1.3.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.3.0...v1.3.1)

### Chores

* bump ([#273](https://github.com/stainless-sdks/sink-python-public/issues/273)) ([0643508](https://github.com/stainless-sdks/sink-python-public/commit/06435080a22d6b9d0f5ab11055ce77f2e661da73))

## 1.3.0 (2023-10-14)

Full Changelog: [v1.2.5...v1.3.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.2.5...v1.3.0)

### Features

* added Ruby ([#270](https://github.com/stainless-sdks/sink-python-public/issues/270)) ([58e22c9](https://github.com/stainless-sdks/sink-python-public/commit/58e22c9a0d34531a52bebd42732a5415dad360ec))


### Chores

* **internal:** enable lint rule ([#272](https://github.com/stainless-sdks/sink-python-public/issues/272)) ([a88f5ce](https://github.com/stainless-sdks/sink-python-public/commit/a88f5cefcfc331af4fda4c0b101bc6d0f64af964))

## 1.2.5 (2023-10-13)

Full Changelog: [v1.2.4...v1.2.5](https://github.com/stainless-sdks/sink-python-public/compare/v1.2.4...v1.2.5)

### Chores

* **internal:** cleanup some redundant code ([#268](https://github.com/stainless-sdks/sink-python-public/issues/268)) ([e1e921c](https://github.com/stainless-sdks/sink-python-public/commit/e1e921c3890ead873fae9f476e76620b1b0a8dde))

## 1.2.4 (2023-10-13)

Full Changelog: [v1.2.3...v1.2.4](https://github.com/stainless-sdks/sink-python-public/compare/v1.2.3...v1.2.4)

### Bug Fixes

* **streaming:** add additional overload for ambiguous stream param ([#266](https://github.com/stainless-sdks/sink-python-public/issues/266)) ([11ef175](https://github.com/stainless-sdks/sink-python-public/commit/11ef175fb8935fec17c7bcafeeaa427247d5fb63))

## 1.2.3 (2023-10-13)

Full Changelog: [v1.2.2...v1.2.3](https://github.com/stainless-sdks/sink-python-public/compare/v1.2.2...v1.2.3)

### Chores

* update comment ([#264](https://github.com/stainless-sdks/sink-python-public/issues/264)) ([d2abb24](https://github.com/stainless-sdks/sink-python-public/commit/d2abb2420639d9e2af776c4e773e3ac1fbe7db3d))

## 1.2.2 (2023-10-12)

Full Changelog: [v1.2.1...v1.2.2](https://github.com/stainless-sdks/sink-python-public/compare/v1.2.1...v1.2.2)

### Chores

* add case insensitive get header function ([#262](https://github.com/stainless-sdks/sink-python-public/issues/262)) ([506e7ad](https://github.com/stainless-sdks/sink-python-public/commit/506e7ad683f6ff9c53b14647801e5f0030f7bc57))

## 1.2.1 (2023-10-12)

Full Changelog: [v1.2.0...v1.2.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.2.0...v1.2.1)

## 1.2.0 (2023-10-12)

Full Changelog: [v1.1.0...v1.2.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.1.0...v1.2.0)

### Features

* add more streaming tests ([#250](https://github.com/stainless-sdks/sink-python-public/issues/250)) ([5061d3c](https://github.com/stainless-sdks/sink-python-public/commit/5061d3cc8027cd5aa4c7063d793e965d9d0fd7c5))
* add nested request model test case ([#252](https://github.com/stainless-sdks/sink-python-public/issues/252)) ([37ef646](https://github.com/stainless-sdks/sink-python-public/commit/37ef6461babaa916599f75b4945cd6c9b6d1ae8f))
* add tests for property array of objects in params ([#258](https://github.com/stainless-sdks/sink-python-public/issues/258)) ([8715c0d](https://github.com/stainless-sdks/sink-python-public/commit/8715c0dee43f66b261d7fa1e14170f7e67d58e7a))
* **client:** add client argument test ([#259](https://github.com/stainless-sdks/sink-python-public/issues/259)) ([f163e51](https://github.com/stainless-sdks/sink-python-public/commit/f163e512e6477c702a574ee5543179d71f9bef20))
* **client:** add forwards-compatible pydantic methods ([#253](https://github.com/stainless-sdks/sink-python-public/issues/253)) ([3ca03c0](https://github.com/stainless-sdks/sink-python-public/commit/3ca03c0a477168d22727608f6f19ad113b136710))
* **client:** add logging setup ([#257](https://github.com/stainless-sdks/sink-python-public/issues/257)) ([2d03fa5](https://github.com/stainless-sdks/sink-python-public/commit/2d03fa51c35f2fcccd81de0bd6823a5c22c43422))
* **client:** add support for passing in a httpx client ([#254](https://github.com/stainless-sdks/sink-python-public/issues/254)) ([c7c9971](https://github.com/stainless-sdks/sink-python-public/commit/c7c997195870c8fdaba4501c91566a08fdf126e1))


### Chores

* restructuring ([#251](https://github.com/stainless-sdks/sink-python-public/issues/251)) ([d39c0b4](https://github.com/stainless-sdks/sink-python-public/commit/d39c0b46e47405c8cf637558028d319d0158e4c1))
* **tests:** update test examples ([#248](https://github.com/stainless-sdks/sink-python-public/issues/248)) ([788d4ac](https://github.com/stainless-sdks/sink-python-public/commit/788d4ac5eafd9e199183df5a137775217baec3f7))
* update README ([#255](https://github.com/stainless-sdks/sink-python-public/issues/255)) ([2fb6819](https://github.com/stainless-sdks/sink-python-public/commit/2fb68191ac15d7dbe7ec2d02d8f14d2a86d7c134))


### Refactors

* **test:** refactor authentication tests ([#256](https://github.com/stainless-sdks/sink-python-public/issues/256)) ([72349a8](https://github.com/stainless-sdks/sink-python-public/commit/72349a89c79c9a69dddb81e9a41e731d8184f993))

## 1.1.0 (2023-10-03)

Full Changelog: [v1.0.1...v1.1.0](https://github.com/stainless-sdks/sink-python-public/compare/v1.0.1...v1.1.0)

### Features

* add super_mixed_union endpoint ([#245](https://github.com/stainless-sdks/sink-python-public/issues/245)) ([00e3a83](https://github.com/stainless-sdks/sink-python-public/commit/00e3a83828270a6631429cc2e1b6bf47d573aab9))
* **client:** handle retry-after header with a date format ([#243](https://github.com/stainless-sdks/sink-python-public/issues/243)) ([0c2e15d](https://github.com/stainless-sdks/sink-python-public/commit/0c2e15d6291a8bf82c4db02c1e9258d18f982308))
* **types:** add test for primitive 2d arrays ([#246](https://github.com/stainless-sdks/sink-python-public/issues/246)) ([dfca65e](https://github.com/stainless-sdks/sink-python-public/commit/dfca65ead2fe36fe0dfb0868c84aa9172ee12220))

## 1.0.1 (2023-10-02)

Full Changelog: [v1.0.0...v1.0.1](https://github.com/stainless-sdks/sink-python-public/compare/v1.0.0...v1.0.1)

## 1.0.0 (2023-09-27)

Full Changelog: [v0.4.4...v1.0.0](https://github.com/stainless-sdks/sink-python-public/compare/v0.4.4...v1.0.0)

### Chores

* **tests:** improve raw response test ([#239](https://github.com/stainless-sdks/sink-python-public/issues/239)) ([638f543](https://github.com/stainless-sdks/sink-python-public/commit/638f54388e5d567332b263aabb90c05cc7ea2954))

## 0.4.4 (2023-09-26)

Full Changelog: [v0.4.2...v0.4.4](https://github.com/stainless-sdks/sink-python-public/compare/v0.4.2...v0.4.4)

### Features

* **package:** export a root error type ([#237](https://github.com/stainless-sdks/sink-python-public/issues/237)) ([6048b1f](https://github.com/stainless-sdks/sink-python-public/commit/6048b1f36c86983e59d1da17e32d88d25dd59a44))

## 0.4.2 (2023-09-22)

Full Changelog: [v0.4.1...v0.4.2](https://github.com/stainless-sdks/sink-python-public/compare/v0.4.1...v0.4.2)

### Chores

* **internal:** move error classes from _base_exceptions to _exceptions (⚠️ breaking) ([#235](https://github.com/stainless-sdks/sink-python-public/issues/235)) ([4f4413f](https://github.com/stainless-sdks/sink-python-public/commit/4f4413fe81e5507e1c17483ba7daf8d7e95a0ea5))

## 0.4.1 (2023-09-22)

Full Changelog: [v0.4.0...v0.4.1](https://github.com/stainless-sdks/sink-python-public/compare/v0.4.0...v0.4.1)

### Bug Fixes

* **client:** don't error by default for unexpected content types ([#233](https://github.com/stainless-sdks/sink-python-public/issues/233)) ([afacad6](https://github.com/stainless-sdks/sink-python-public/commit/afacad6d27c0a88893af0644e7924acba0c96403))

## 0.4.0 (2023-09-21)

Full Changelog: [v0.3.2...v0.4.0](https://github.com/stainless-sdks/sink-python-public/compare/v0.3.2...v0.4.0)

### ⚠ BREAKING CHANGES

* fix capitalization of `Github` to `GitHub` in some places ([#232](https://github.com/stainless-sdks/sink-python-public/issues/232))

### Features

* **api:** add more reserved word testcases ([#230](https://github.com/stainless-sdks/sink-python-public/issues/230)) ([4ef6f43](https://github.com/stainless-sdks/sink-python-public/commit/4ef6f437606f3d0d221507bbaea202b37f9b0328))


### Refactors

* fix capitalization of `Github` to `GitHub` in some places ([#232](https://github.com/stainless-sdks/sink-python-public/issues/232)) ([c7720a0](https://github.com/stainless-sdks/sink-python-public/commit/c7720a04f64ec343f3ed83092f3eeb6a32f02160))

## 0.3.2 (2023-09-20)

Full Changelog: [v0.3.1...v0.3.2](https://github.com/stainless-sdks/sink-python-public/compare/v0.3.1...v0.3.2)

### Bug Fixes

* allow deprecated method aliases ([#228](https://github.com/stainless-sdks/sink-python-public/issues/228)) ([3e8278d](https://github.com/stainless-sdks/sink-python-public/commit/3e8278de2470521c682be969245f4802fc749122))

## 0.3.1 (2023-09-19)

Full Changelog: [v0.3.0...v0.3.1](https://github.com/stainless-sdks/sink-python-public/compare/v0.3.0...v0.3.1)

### Features

* **types:** improve params type names ([#226](https://github.com/stainless-sdks/sink-python-public/issues/226)) ([bace972](https://github.com/stainless-sdks/sink-python-public/commit/bace97269945710a34a8c00cdd6d13169e749a30))

## 0.3.0 (2023-09-15)

Full Changelog: [v0.2.11...v0.3.0](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.11...v0.3.0)

### ⚠ BREAKING CHANGES

* add an enum value ([#225](https://github.com/stainless-sdks/sink-python-public/issues/225))

### Features

* add an enum value ([#225](https://github.com/stainless-sdks/sink-python-public/issues/225)) ([5b321a5](https://github.com/stainless-sdks/sink-python-public/commit/5b321a5bb7f42b9501a4c04835e92c0d3c8e7bf7))

## 0.2.11 (2023-09-15)

Full Changelog: [v0.2.10...v0.2.11](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.10...v0.2.11)

### Chores

* **internal:** add helpers ([#220](https://github.com/stainless-sdks/sink-python-public/issues/220)) ([2072fbc](https://github.com/stainless-sdks/sink-python-public/commit/2072fbc0aedf9120243a75bf4e3d368fd47f8560))

## 0.2.10 (2023-09-14)

Full Changelog: [v0.2.9...v0.2.10](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.9...v0.2.10)

### Bug Fixes

* **client:** properly configure model set fields ([#219](https://github.com/stainless-sdks/sink-python-public/issues/219)) ([05ffa62](https://github.com/stainless-sdks/sink-python-public/commit/05ffa620986d37e7fd5349c696ee343f1d753e8c))
* **config:** use correct positional params name in tests ([#216](https://github.com/stainless-sdks/sink-python-public/issues/216)) ([da0b2ca](https://github.com/stainless-sdks/sink-python-public/commit/da0b2cafb150bfcd42278d9091a21c89b74aa159))


### Chores

* **internal:** cleaner references to complex union types ([#218](https://github.com/stainless-sdks/sink-python-public/issues/218)) ([ade3a1d](https://github.com/stainless-sdks/sink-python-public/commit/ade3a1dd7b2d22a0fe2dd5a366f2f4c0408443d5))
* **internal:** remove unused aliases ([#214](https://github.com/stainless-sdks/sink-python-public/issues/214)) ([6f17266](https://github.com/stainless-sdks/sink-python-public/commit/6f1726645397cb8460f55ca1d2dea515dff5412e))
* **internal:** update pyright ([#213](https://github.com/stainless-sdks/sink-python-public/issues/213)) ([892b26d](https://github.com/stainless-sdks/sink-python-public/commit/892b26d2a50e5f5c0a62133fcd344f2cee6e63c2))


### Documentation

* add some missing inline documentation ([#215](https://github.com/stainless-sdks/sink-python-public/issues/215)) ([749f51e](https://github.com/stainless-sdks/sink-python-public/commit/749f51e6efac03f2549f92a1efb34b89275beed9))

## 0.2.9 (2023-09-08)

Full Changelog: [v0.2.8...v0.2.9](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.8...v0.2.9)

### Features

* add tests for renaming properties ([#210](https://github.com/stainless-sdks/sink-python-public/issues/210)) ([e278ee6](https://github.com/stainless-sdks/sink-python-public/commit/e278ee60e91acf8e98b389599ed852004a4087fd))


### Chores

* **internal:** cleanup test params ([#209](https://github.com/stainless-sdks/sink-python-public/issues/209)) ([d132678](https://github.com/stainless-sdks/sink-python-public/commit/d1326784a149a4565a22a177cf2fa36dd2116ab1))
* **internal:** minor update ([#204](https://github.com/stainless-sdks/sink-python-public/issues/204)) ([3a733e3](https://github.com/stainless-sdks/sink-python-public/commit/3a733e3ceca1c467f1f58607ce70f6ab6e7c9509))
* **internal:** update lock file ([#208](https://github.com/stainless-sdks/sink-python-public/issues/208)) ([74f501f](https://github.com/stainless-sdks/sink-python-public/commit/74f501f869b44f168cf6cd28acd1354a8d00252a))
* **internal:** updates ([#211](https://github.com/stainless-sdks/sink-python-public/issues/211)) ([8016d0b](https://github.com/stainless-sdks/sink-python-public/commit/8016d0bf5141807f659af292421140cf70c3958e))


### Documentation

* **readme:** add link to api.md ([#206](https://github.com/stainless-sdks/sink-python-public/issues/206)) ([1aa2eeb](https://github.com/stainless-sdks/sink-python-public/commit/1aa2eeba5c9aa8580d60be0a41a34f769d9be643))

## 0.2.8 (2023-09-06)

Full Changelog: [v0.2.7...v0.2.8](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.7...v0.2.8)

### Features

* add `x-stainless-useDefault` testcase ([#197](https://github.com/stainless-sdks/sink-python-public/issues/197)) ([8965e9a](https://github.com/stainless-sdks/sink-python-public/commit/8965e9a7feccb82d0f16f6e8e948c1688763552d))
* add nested pagination property test ([#194](https://github.com/stainless-sdks/sink-python-public/issues/194)) ([c8b7aff](https://github.com/stainless-sdks/sink-python-public/commit/c8b7aff40575382c4f822df780f258abab16a9fb))
* add test for doc escaping ([#199](https://github.com/stainless-sdks/sink-python-public/issues/199)) ([3f962bb](https://github.com/stainless-sdks/sink-python-public/commit/3f962bb63e205f76a4244c1cbb3054d4dab43c5a))
* add test for params model with param in name ([#200](https://github.com/stainless-sdks/sink-python-public/issues/200)) ([27b3ad4](https://github.com/stainless-sdks/sink-python-public/commit/27b3ad4e8f705e4b57e562396824a70793a14061))
* add test for union of numbers ([#196](https://github.com/stainless-sdks/sink-python-public/issues/196)) ([9df50e4](https://github.com/stainless-sdks/sink-python-public/commit/9df50e4da9780ce64c9fe6f944df48d1e9fe3569))
* add tests for child model references ([#188](https://github.com/stainless-sdks/sink-python-public/issues/188)) ([0a124e7](https://github.com/stainless-sdks/sink-python-public/commit/0a124e75fdf231ec760e426d4ff67ece9e8de916))
* add tests for optional file params ([#201](https://github.com/stainless-sdks/sink-python-public/issues/201)) ([7330886](https://github.com/stainless-sdks/sink-python-public/commit/733088659c90a4b38be1a60013df97e21fbc53d1))
* add tests for union items in arrays ([#191](https://github.com/stainless-sdks/sink-python-public/issues/191)) ([2b6b3a2](https://github.com/stainless-sdks/sink-python-public/commit/2b6b3a277abed142434dedd40431926df89e3aee))
* fixes tests where an array has to have unique enum values ([#202](https://github.com/stainless-sdks/sink-python-public/issues/202)) ([c88d621](https://github.com/stainless-sdks/sink-python-public/commit/c88d621ac317dcac885d0895b63b2c56a4264adc))
* more params types tests ([#190](https://github.com/stainless-sdks/sink-python-public/issues/190)) ([631d7ec](https://github.com/stainless-sdks/sink-python-public/commit/631d7ece377fd997196e2645447ecc48e0d57c90))
* **types:** de-duplicate nested streaming params types ([#198](https://github.com/stainless-sdks/sink-python-public/issues/198)) ([8632c46](https://github.com/stainless-sdks/sink-python-public/commit/8632c46d4d297f7e1043ab01581c6e27d72da4c1))
* updates ([#192](https://github.com/stainless-sdks/sink-python-public/issues/192)) ([d52fdf1](https://github.com/stainless-sdks/sink-python-public/commit/d52fdf1ca2fe5d0055d76b0d461c54c5e6b6b9fa))


### Chores

* **internal:** minor formatting changes ([#195](https://github.com/stainless-sdks/sink-python-public/issues/195)) ([08998fc](https://github.com/stainless-sdks/sink-python-public/commit/08998fcacffed9cc4e4fb18f4fccbceaba6b18a3))
* **internal:** update base client ([#203](https://github.com/stainless-sdks/sink-python-public/issues/203)) ([b87ac5e](https://github.com/stainless-sdks/sink-python-public/commit/b87ac5ed2a9abf41d19787fa4e9c3444de582518))


### Documentation

* **readme:** reference pydantic helpers ([#193](https://github.com/stainless-sdks/sink-python-public/issues/193)) ([78ae5e5](https://github.com/stainless-sdks/sink-python-public/commit/78ae5e5934e8786bf878da45e61758459239072f))

## 0.2.7 (2023-08-31)

Full Changelog: [v0.2.6...v0.2.7](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.6...v0.2.7)

### Features

* add test case for null property ([#184](https://github.com/stainless-sdks/sink-python-public/issues/184)) ([e439f7a](https://github.com/stainless-sdks/sink-python-public/commit/e439f7a64611ba0d9510ddf9467b80db5f5c4678))
* add test for method named get ([#185](https://github.com/stainless-sdks/sink-python-public/issues/185)) ([075b177](https://github.com/stainless-sdks/sink-python-public/commit/075b1774f0d3c07350057acd525663fffcec00be))
* add tests for complex union types in params ([#182](https://github.com/stainless-sdks/sink-python-public/issues/182)) ([8bf1b33](https://github.com/stainless-sdks/sink-python-public/commit/8bf1b33d1b00b5b236a0f0a109f88dc945e52ed6))
* sync ([#180](https://github.com/stainless-sdks/sink-python-public/issues/180)) ([a4fc313](https://github.com/stainless-sdks/sink-python-public/commit/a4fc313a98573edb3d5be500532160b61c4dc5df))


### Chores

* **internal:** add `pydantic.generics` import for compatibility ([#186](https://github.com/stainless-sdks/sink-python-public/issues/186)) ([c7c7b27](https://github.com/stainless-sdks/sink-python-public/commit/c7c7b277bdee6ba86a91760cff1449660960cd4c))
* **internal:** update lock file ([#183](https://github.com/stainless-sdks/sink-python-public/issues/183)) ([bf3fb96](https://github.com/stainless-sdks/sink-python-public/commit/bf3fb96b7a2afdc3b018e1875ced44d9580e9cd8))

## 0.2.6 (2023-08-28)

Full Changelog: [v0.2.5...v0.2.6](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.5...v0.2.6)

### Features

* add ambiguous schemas and transforms on them ([#80](https://github.com/stainless-sdks/sink-python-public/issues/80)) ([ac8c921](https://github.com/stainless-sdks/sink-python-public/commit/ac8c92171d30db9891f38cadba59e267067b58b2))
* add test cases for duplicate param names ([#175](https://github.com/stainless-sdks/sink-python-public/issues/175)) ([2bda4c7](https://github.com/stainless-sdks/sink-python-public/commit/2bda4c774b1023e3368f14b6d6a63ee9c2f0753b))
* add tests for envelope unwrapping arrays ([#164](https://github.com/stainless-sdks/sink-python-public/issues/164)) ([ce16297](https://github.com/stainless-sdks/sink-python-public/commit/ce1629758591a47f7301fc18eee5f6f24146f1cb))
* add tests for model import clashing ([#176](https://github.com/stainless-sdks/sink-python-public/issues/176)) ([26e8375](https://github.com/stainless-sdks/sink-python-public/commit/26e83751d5a628ee8bda8ce9e98a709020dd8d89))
* add tests for reserved names ([#174](https://github.com/stainless-sdks/sink-python-public/issues/174)) ([e2753ea](https://github.com/stainless-sdks/sink-python-public/commit/e2753eab62dcf33a0736d56551a669d9a6c236e4))
* tests for skipping object properties ([#169](https://github.com/stainless-sdks/sink-python-public/issues/169)) ([6516103](https://github.com/stainless-sdks/sink-python-public/commit/6516103c97ceedad53d94e25d2602dae14d3cd77))


### Bug Fixes

* **ci:** correct branch check ([#172](https://github.com/stainless-sdks/sink-python-public/issues/172)) ([3ac5309](https://github.com/stainless-sdks/sink-python-public/commit/3ac5309041e055e341ab090424b12ece621b8a16))
* **internal:** fixes internal naming issue ([#177](https://github.com/stainless-sdks/sink-python-public/issues/177)) ([13d6b14](https://github.com/stainless-sdks/sink-python-public/commit/13d6b14d1d89c245256854c48a75771e41e5af03))


### Chores

* **ci:** setup workflows to create releases and release PRs ([#178](https://github.com/stainless-sdks/sink-python-public/issues/178)) ([e30edb6](https://github.com/stainless-sdks/sink-python-public/commit/e30edb6f7c77314d4b7b3f7dabd982dc3ec3fb3d))
* **deps:** bump lock file ([#171](https://github.com/stainless-sdks/sink-python-public/issues/171)) ([873349d](https://github.com/stainless-sdks/sink-python-public/commit/873349dd1fa654319b1c5cf1785e005be4cf51c7))
* **deps:** update lock file ([#170](https://github.com/stainless-sdks/sink-python-public/issues/170)) ([cbac2d2](https://github.com/stainless-sdks/sink-python-public/commit/cbac2d236818fe5587c69bc03554a130228b0812))
* **internal:** improve support for streaming responses ([#85](https://github.com/stainless-sdks/sink-python-public/issues/85)) ([658ae3a](https://github.com/stainless-sdks/sink-python-public/commit/658ae3a250f691ab0d295d926c3521a9e7d43f15))
* **internal:** minor reformatting ([#78](https://github.com/stainless-sdks/sink-python-public/issues/78)) ([e8b14d6](https://github.com/stainless-sdks/sink-python-public/commit/e8b14d6d689f52e2c41364840832b17508a1c4cd))
* **internal:** run Release Doctor in Next PR too ([#83](https://github.com/stainless-sdks/sink-python-public/issues/83)) ([5de7a23](https://github.com/stainless-sdks/sink-python-public/commit/5de7a2339fdf6633bb47073cd5d916597cc70936))
* **internal:** update anyio ([#167](https://github.com/stainless-sdks/sink-python-public/issues/167)) ([dc848dc](https://github.com/stainless-sdks/sink-python-public/commit/dc848dcbd19576f673d1387adeecc6893cabb6fb))
* **internal:** use different release PR header ([#82](https://github.com/stainless-sdks/sink-python-public/issues/82)) ([ac4e5a0](https://github.com/stainless-sdks/sink-python-public/commit/ac4e5a0e660a0a4b10c4ec0508903566982765af))
* test change ([#163](https://github.com/stainless-sdks/sink-python-public/issues/163)) ([5c4eb1e](https://github.com/stainless-sdks/sink-python-public/commit/5c4eb1e38c9580f5f6392564babe5904df28c820))
* test change 2 ([#165](https://github.com/stainless-sdks/sink-python-public/issues/165)) ([8fb1636](https://github.com/stainless-sdks/sink-python-public/commit/8fb163647393d1cea563026ecdcec8d50d6c1327))

## [0.2.5](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.4...v0.2.5) (2023-04-27)


### Features

* add tests for concrete page types ([#73](https://github.com/stainless-sdks/sink-python-public/issues/73)) ([4d69fe5](https://github.com/stainless-sdks/sink-python-public/commit/4d69fe5aadee8bfce34af16608a14ddb1e2efb34))


### Bug Fixes

* **ci:** correct version for release-please action ([#75](https://github.com/stainless-sdks/sink-python-public/issues/75)) ([8ee5a27](https://github.com/stainless-sdks/sink-python-public/commit/8ee5a2714f59e4eb9f1359af40d08d27d3366854))

## [0.2.4](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.3...v0.2.4) (2023-04-26)


### Features

* add test cases for allOf ([#68](https://github.com/stainless-sdks/sink-python-public/issues/68)) ([a20eacc](https://github.com/stainless-sdks/sink-python-public/commit/a20eacc0cd6bf57a89aa1ad987cf469342f430e3))
* header params tests ([#66](https://github.com/stainless-sdks/sink-python-public/issues/66)) ([8ac2279](https://github.com/stainless-sdks/sink-python-public/commit/8ac22790db4331e73943a3918c766e8ddb3d704d))

## [0.2.3](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.2...v0.2.3) (2023-04-18)


### Features

* **ci:** add workflow for running PyPI publishing manually ([#63](https://github.com/stainless-sdks/sink-python-public/issues/63)) ([be7a1c6](https://github.com/stainless-sdks/sink-python-public/commit/be7a1c6a9a1ae96b2119ed0bd645af54dffe472c))

## [0.2.2](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.1...v0.2.2) (2023-04-18)


### Features

* **api:** update docs ([#60](https://github.com/stainless-sdks/sink-python-public/issues/60)) ([d0ea156](https://github.com/stainless-sdks/sink-python-public/commit/d0ea156140b36a9d0fe705d4ad0b07799d7fe20f))

## [0.2.1](https://github.com/stainless-sdks/sink-python-public/compare/v0.2.0...v0.2.1) (2023-04-18)


### Features

* add timeout option to methods ([#29](https://github.com/stainless-sdks/sink-python-public/issues/29)) ([3d68204](https://github.com/stainless-sdks/sink-python-public/commit/3d68204c945d33492d6dda459fb4e4b09276c2af))
* **ci:** add script to publish to PyPi ([#49](https://github.com/stainless-sdks/sink-python-public/issues/49)) ([518cd7e](https://github.com/stainless-sdks/sink-python-public/commit/518cd7e8238f36737a4df3943e5c2e530169d6c0))
* test change ([#42](https://github.com/stainless-sdks/sink-python-public/issues/42)) ([7b653da](https://github.com/stainless-sdks/sink-python-public/commit/7b653da06aba2b85fcf3f2b60fa5f63fec4566d2))
* use foo ([#44](https://github.com/stainless-sdks/sink-python-public/issues/44)) ([020d77d](https://github.com/stainless-sdks/sink-python-public/commit/020d77d73c9c56aeba7af615be35cb2cb4a4c70f))
* use foo ([#45](https://github.com/stainless-sdks/sink-python-public/issues/45)) ([4b08a66](https://github.com/stainless-sdks/sink-python-public/commit/4b08a66da9f200db63d2183a14db8002988b9228))


### Bug Fixes

* **ci:** release doctor workflow + improvements ([#53](https://github.com/stainless-sdks/sink-python-public/issues/53)) ([6b506a9](https://github.com/stainless-sdks/sink-python-public/commit/6b506a993bee182e3cddbb0307ff778192d47550))
* **ci:** release file options syntax ([#47](https://github.com/stainless-sdks/sink-python-public/issues/47)) ([793bb08](https://github.com/stainless-sdks/sink-python-public/commit/793bb08d8a54caf76f3e40f3d62a84be1fd43180))
