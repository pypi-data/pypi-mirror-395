# Changelog

## [0.2.1](https://github.com/nikoheikkila/ghanon/compare/v0.2.0...v0.2.1) (2025-12-04)


### 🐛 Bug Fixes

* **ci:** remove --locked from uv sync ([a78b6a1](https://github.com/nikoheikkila/ghanon/commit/a78b6a18f63d5eb252671f55e77a430a78cc92ec))

## [0.2.0](https://github.com/nikoheikkila/ghanon/compare/v0.1.0...v0.2.0) (2025-12-04)


### ✨ Features

* add initial business logic ([ced4253](https://github.com/nikoheikkila/ghanon/commit/ced42537302bed0cc54101227a7614ab7dc352cc))
* add publishing workflow ([#1](https://github.com/nikoheikkila/ghanon/issues/1)) ([67a15fc](https://github.com/nikoheikkila/ghanon/commit/67a15fce1817c0b61f8dad624815f030228f9e16))
* colorize CLI output ([41e1f4b](https://github.com/nikoheikkila/ghanon/commit/41e1f4b992cceb51c681a2daddafa37de57107f9))
* ensure `contents` permissions are specified when changing permissions ([05854dd](https://github.com/nikoheikkila/ghanon/commit/05854ddd590356a0593b34aecf36d5931817b403))
* ensure all jobs have permissions set ([8677828](https://github.com/nikoheikkila/ghanon/commit/8677828e1c8377beb273a233b7416cc9e3efc4b0))
* ensure all reusable workflow jobs have permissions set ([8a5c646](https://github.com/nikoheikkila/ghanon/commit/8a5c64644bdc70ce12a71ec91f80158404b828e9))
* handle passing multiple workflows ([27298e0](https://github.com/nikoheikkila/ghanon/commit/27298e07990c2cc810632f18524ef0a553c266ee))
* raise error when using push.branches trigger instead of pull_request ([bfd69f6](https://github.com/nikoheikkila/ghanon/commit/bfd69f6c32975056f973eed3953d2b863cf93c9b))
* remove a feature requiring branch triggers ([1b2cf17](https://github.com/nikoheikkila/ghanon/commit/1b2cf171194a88bde70bf4ddf57ba6258c07d101))
* validate all workflows when ran without arguments ([738d54e](https://github.com/nikoheikkila/ghanon/commit/738d54edbb2655016e0dd8ea60a3e90f9983ab5d))


### 🐛 Bug Fixes

* add release manifest ([6bff518](https://github.com/nikoheikkila/ghanon/commit/6bff5182463662f54bb092cc7c3634252066a987))
* improve error logging and test matching ([4f20ca5](https://github.com/nikoheikkila/ghanon/commit/4f20ca5fb6b979f11de8c02df00ac233469d385b))
* install all packages ([badaf0a](https://github.com/nikoheikkila/ghanon/commit/badaf0abee225ef336955afb6b626888ee486d05))
* log only workflow filename when parsing is successful ([5a4e584](https://github.com/nikoheikkila/ghanon/commit/5a4e5849add97ffec48abe11997c1c1043a93cdf))
* parse line information for error messages more accurately ([452ea2d](https://github.com/nikoheikkila/ghanon/commit/452ea2d8c13f9ea5bd44caf3212108041da86207))
* properly handle ANSI codes in CLI output ([bd5cbb9](https://github.com/nikoheikkila/ghanon/commit/bd5cbb96969b2b6133f751fc7c4ed055ed70fec3))
* remove fancy checkmark from install script ([f603c35](https://github.com/nikoheikkila/ghanon/commit/f603c35d659b4e344357906a3da5a23dfa4db6ed))
* use pyrefly for better Python typing experience ([db5962b](https://github.com/nikoheikkila/ghanon/commit/db5962bfac5ccdcb44e97a545ff73987b7683d8e))


### 📚 Documentation

* add Copilot instructions ([a67bd98](https://github.com/nikoheikkila/ghanon/commit/a67bd98dc83f6a51b020154a4a227b5a33508053))
* add new agents ([e7d5818](https://github.com/nikoheikkila/ghanon/commit/e7d5818a6042cbdea43ec4ea38283848726d1b0d))
* add open source community files ([9f29515](https://github.com/nikoheikkila/ghanon/commit/9f29515ca1532247771f2c11ac1d73f1895292ae))


### ♻️ Code Refactoring

* add better linting with Ruff ([8bc95cc](https://github.com/nikoheikkila/ghanon/commit/8bc95cc49029d05c273ae69558896d79286bb258))
* add missing unit tests for 100% coverage ([937150a](https://github.com/nikoheikkila/ghanon/commit/937150aad7a2a325dd4125cdf0d2e38ef3a52dd4))
* align tests between spec and Pytest ([469e2b9](https://github.com/nikoheikkila/ghanon/commit/469e2b9b2d0919bc7e9c787a9727a399cc8a1f33))
* clean up spec files ([d4d5419](https://github.com/nikoheikkila/ghanon/commit/d4d5419408ff93bc9541c7d96c18ef07b1759462))
* concurrency module ([258bd80](https://github.com/nikoheikkila/ghanon/commit/258bd80cc1fcce989215554f01311fa7ca375127))
* container module ([ad11a60](https://github.com/nikoheikkila/ghanon/commit/ad11a60c42d294570edd8a98f54a87f9a525af95))
* defaults module ([f5cab1c](https://github.com/nikoheikkila/ghanon/commit/f5cab1cf15919a4b9323546834603ecbbeb6f9a9))
* environment module ([3cc4125](https://github.com/nikoheikkila/ghanon/commit/3cc412570ea4c4e8ff633b9e1d48c614645f9999))
* events module ([3eb280e](https://github.com/nikoheikkila/ghanon/commit/3eb280e542b6f31330d3284ac54e98283a73f59a))
* events module ([cd8174e](https://github.com/nikoheikkila/ghanon/commit/cd8174e8ee0cd27f683e7040d7411e468560ec7b))
* extract base and flexible models ([1a3bb2b](https://github.com/nikoheikkila/ghanon/commit/1a3bb2bcb4fbd303d7fec10636450081eead5b6d))
* extract CLI to own module with tests ([8cb9717](https://github.com/nikoheikkila/ghanon/commit/8cb9717cd0f518cf4b567b193e3e736daae58fb1))
* extract workflow triggers to module ([9c40188](https://github.com/nikoheikkila/ghanon/commit/9c40188de4c2162dec88fe7c0be3fe697f147e40))
* improve enum usage ([8693bd0](https://github.com/nikoheikkila/ghanon/commit/8693bd0e58112886c7e09f6be2f16962c39e06a2))
* improve error messages and YAML parsing ([581ace5](https://github.com/nikoheikkila/ghanon/commit/581ace527569f4fdf961b7c0bcf5edbc814699ad))
* improve feature-to-test mapping ([ebe623b](https://github.com/nikoheikkila/ghanon/commit/ebe623be6fdf022200539190842b850a9bc50524))
* improve parsing logic and remove redundant tests ([c543386](https://github.com/nikoheikkila/ghanon/commit/c543386cf96a50d0eb0214de6e2cc1b6610b811b))
* improve YAML parsing tests ([247beb8](https://github.com/nikoheikkila/ghanon/commit/247beb8ebdf0812366fb33c17707fdc5d8823072))
* jobs module ([2bd321d](https://github.com/nikoheikkila/ghanon/commit/2bd321d1d5c87de14690e34472ee4b3612e0c7a5))
* jobs module ([1e60d8c](https://github.com/nikoheikkila/ghanon/commit/1e60d8cff8c2be7ae770372c0a92e645850cfbd3))
* matrix module ([33031e7](https://github.com/nikoheikkila/ghanon/commit/33031e7598c72fe5a87dda9add8795aed4f9f6d1))
* move activity type enums ([71d6483](https://github.com/nikoheikkila/ghanon/commit/71d64830c8f70b3b1906b09d7581f7f501e26581))
* move enums ([3bcd196](https://github.com/nikoheikkila/ghanon/commit/3bcd196b250dc9542c71c4a0fff791c7f9a213fa))
* move enums ([8d6377c](https://github.com/nikoheikkila/ghanon/commit/8d6377c5cddf6e17f455b081b9dca4bc0a943654))
* move parser to module ([777d6da](https://github.com/nikoheikkila/ghanon/commit/777d6da40fd76b3fe8b87f4ccfc774079615b43a))
* move runner logic ([d66fdc9](https://github.com/nikoheikkila/ghanon/commit/d66fdc93177cff40bb739721cfe80685446273dc))
* move ShellType enum ([8225046](https://github.com/nikoheikkila/ghanon/commit/8225046861790dc86408de24498521cbd7d0692f))
* move type aliases ([88903a5](https://github.com/nikoheikkila/ghanon/commit/88903a5798b817d7bf047fc7c5f25e384618bd85))
* move type aliases ([7289382](https://github.com/nikoheikkila/ghanon/commit/7289382926beae4c911c6f972f1a07877790c4c7))
* move type aliases ([fecb038](https://github.com/nikoheikkila/ghanon/commit/fecb038760dd98d9c21f9b6a4191e0eba6be8cab))
* move type aliases ([dcb6859](https://github.com/nikoheikkila/ghanon/commit/dcb6859316ff7e0735d29484cb624d5b1cbbccd3))
* move type aliases ([776d24c](https://github.com/nikoheikkila/ghanon/commit/776d24c0c54af87616c7ddc911f55a430b8b5f30))
* organise tests around CLI usage ([bd10b99](https://github.com/nikoheikkila/ghanon/commit/bd10b99c6cf30fcd88a653f0e816fa037482fff9))
* permissions module ([3065feb](https://github.com/nikoheikkila/ghanon/commit/3065feb219fd0598ce44ce57d3729209b12edbff))
* reduce duplication ([3b208bc](https://github.com/nikoheikkila/ghanon/commit/3b208bc2b9c24fed5277e6033d306d332a19150d))
* remove redundant imports ([1793f9f](https://github.com/nikoheikkila/ghanon/commit/1793f9fe95a07a2c50d74262a242f27a1f3b1415))
* rename models to domain ([0f72ebd](https://github.com/nikoheikkila/ghanon/commit/0f72ebd43094ef2cca51efbcacf28e673df5ceed))
* rename test class ([aa75edb](https://github.com/nikoheikkila/ghanon/commit/aa75edbbb1ffb4b9ef3371bb38bd6cfcc23d6d03))
* reorganise activity type event tests ([3e8578e](https://github.com/nikoheikkila/ghanon/commit/3e8578e0aa75d720f13052dc5a75fea163947fe2))
* reorganise pull request events tests ([f670bfe](https://github.com/nikoheikkila/ghanon/commit/f670bfebad31c69214299ac677e50cd159fc0bf7))
* reorganise pull request target event tests ([9a877fc](https://github.com/nikoheikkila/ghanon/commit/9a877fc486199c479851100e683ee3f96fa784e8))
* reorganise push events test ([d35403f](https://github.com/nikoheikkila/ghanon/commit/d35403f2eff25f7c529a5bf672de8a4b39b0f35a))
* reorganise schedule event tests ([962ab7f](https://github.com/nikoheikkila/ghanon/commit/962ab7f78f1d9f196d66c3e8dc7c1288820ce22e))
* reorganise workflow call event tests ([77be231](https://github.com/nikoheikkila/ghanon/commit/77be2315714ca1559485beeddfcaeeafeddb716e))
* reorganise workflow dispatch event tests ([e0881f5](https://github.com/nikoheikkila/ghanon/commit/e0881f5ce7dc6fcebd2fbdf1debb506d52c6828d))
* reorganise workflow model tests ([af0e708](https://github.com/nikoheikkila/ghanon/commit/af0e708361e9d0f047e7688efe153eb51edb5273))
* reorganise workflow run event tests ([a14f512](https://github.com/nikoheikkila/ghanon/commit/a14f512dce4361e15783d2efd718b7b0012d9f16))
* reorganise YAML parsing tests ([4d501c2](https://github.com/nikoheikkila/ghanon/commit/4d501c25e3dc3ec252c77539a2716161617b4c3c))
* reorganize tests ([064ddf2](https://github.com/nikoheikkila/ghanon/commit/064ddf2144c6cdc4d831d7f3f4a804d77bf674f1))
* round trip tests ([8c4dbed](https://github.com/nikoheikkila/ghanon/commit/8c4dbed184c7de465ef89cc620fa48fdcc658a7e))
* simplify condition ([3345a6a](https://github.com/nikoheikkila/ghanon/commit/3345a6ab66e31106325b7905e45548be8a0b35ac))
* split edge cases tests to relevant modules ([f4c7dbd](https://github.com/nikoheikkila/ghanon/commit/f4c7dbd44f225ae6f6b417231e165394d27d7516))
* step module ([aaddbf1](https://github.com/nikoheikkila/ghanon/commit/aaddbf16ed88351b6f76ce9c21c44f16c6a6f75b))


### 💚 Continuous Integration

* add build workflow ([f45dbc8](https://github.com/nikoheikkila/ghanon/commit/f45dbc828ceef1e92f72b23798d9d11a3033b09c))
* add dog-fooding test ([6a4660e](https://github.com/nikoheikkila/ghanon/commit/6a4660ea3f47a6dde5d8c3baba20c259e1126a6a))
* add local test installation script ([8636892](https://github.com/nikoheikkila/ghanon/commit/86368924188b58dfccee8b95ca157baa0403a83d))
* add step for testing package installation ([d48f526](https://github.com/nikoheikkila/ghanon/commit/d48f526168467752c962fa1ed66250f311216702))
* upload coverage report to Coveralls ([6ce4764](https://github.com/nikoheikkila/ghanon/commit/6ce4764dfd9ebbcfd1a0ab3a09cd3adc06da8521))
