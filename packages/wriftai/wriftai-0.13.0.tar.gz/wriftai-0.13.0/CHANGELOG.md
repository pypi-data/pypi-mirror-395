# Changelog

## [0.13.0](https://github.com/wriftai/wriftai-python/compare/v0.12.0...v0.13.0) (2025-12-05)


### Features

* Combined model owner and name into one parameter. ([#147](https://github.com/wriftai/wriftai-python/issues/147)) ([2bc7d6a](https://github.com/wriftai/wriftai-python/commit/2bc7d6ac77825ea78499e843e7d98900db2e420f))

## [0.12.0](https://github.com/wriftai/wriftai-python/compare/v0.11.0...v0.12.0) (2025-12-02)


### Features

* Added sorting direction for listing models and users. ([#145](https://github.com/wriftai/wriftai-python/issues/145)) ([5d214f6](https://github.com/wriftai/wriftai-python/commit/5d214f6e4b1f1bb3127de29c2c938ffd102bdc55))

## [0.11.0](https://github.com/wriftai/wriftai-python/compare/v0.10.0...v0.11.0) (2025-11-25)


### Features

* Update README.md, fix integration test imports and change init module frontmatter in docs. ([#141](https://github.com/wriftai/wriftai-python/issues/141)) ([14899c0](https://github.com/wriftai/wriftai-python/commit/14899c0bb50809ef8ff7b849ab49b04c85c6baa3))

## [0.10.0](https://github.com/wriftai/wriftai-python/compare/v0.9.0...v0.10.0) (2025-11-21)


### Features

* Added on_poll callback in WaitOptions. ([#129](https://github.com/wriftai/wriftai-python/issues/129)) ([314aad3](https://github.com/wriftai/wriftai-python/commit/314aad38dca99743e4464f98303e7c787f5e5f18))

## [0.9.0](https://github.com/wriftai/wriftai-python/compare/v0.8.0...v0.9.0) (2025-11-21)


### Features

* Added slug in hardware resource. ([#134](https://github.com/wriftai/wriftai-python/issues/134)) ([1ddb577](https://github.com/wriftai/wriftai-python/commit/1ddb5770e479f1dedcd2dce27dcdaf401d246f30))
* Replaced hardware name with identifier for models. ([#136](https://github.com/wriftai/wriftai-python/issues/136)) ([837f1f8](https://github.com/wriftai/wriftai-python/commit/837f1f8f980e80a3ba8ed5c4fd65ebca2d72f18a))

## [0.8.0](https://github.com/wriftai/wriftai-python/compare/v0.7.0...v0.8.0) (2025-11-13)


### Features

* Added more sorting options for listing models and users. ([#124](https://github.com/wriftai/wriftai-python/issues/124)) ([47a6455](https://github.com/wriftai/wriftai-python/commit/47a6455dee8b57f9257d89906c71af4c42e43095))

## [0.7.0](https://github.com/wriftai/wriftai-python/compare/v0.6.1...v0.7.0) (2025-11-12)


### Features

* Add automated documentation ([#110](https://github.com/wriftai/wriftai-python/issues/110)) ([51012cf](https://github.com/wriftai/wriftai-python/commit/51012cf6e8b30851a6672327dad3716f4f4d4f2f))

## [0.6.1](https://github.com/wriftai/wriftai-python/compare/v0.6.0...v0.6.1) (2025-11-07)


### Bug Fixes

* Updated metadata in pyproject.toml ([#114](https://github.com/wriftai/wriftai-python/issues/114)) ([3c79429](https://github.com/wriftai/wriftai-python/commit/3c79429697d8346d40bc870eb2b9d6bcc5da19bd))

## [0.6.0](https://github.com/wriftai/wriftai-python/compare/v0.5.0...v0.6.0) (2025-11-07)


### Features

* Updated wait method to take prediction id. ([#120](https://github.com/wriftai/wriftai-python/issues/120)) ([1b1461a](https://github.com/wriftai/wriftai-python/commit/1b1461a35beb9403c7abc85951aa5674005d8207))

## [0.5.0](https://github.com/wriftai/wriftai-python/compare/v0.4.0...v0.5.0) (2025-10-17)


### Features

* Updated Prediction's create method to support waiting. ([#100](https://github.com/wriftai/wriftai-python/issues/100)) ([b862837](https://github.com/wriftai/wriftai-python/commit/b862837fde8aa59783725047a93a8df6f043ccbd))

## [0.4.0](https://github.com/wriftai/wriftai-python/compare/v0.3.0...v0.4.0) (2025-10-16)


### Features

* renamed APIRequestor to API and made it public ([#101](https://github.com/wriftai/wriftai-python/issues/101)) ([a75167a](https://github.com/wriftai/wriftai-python/commit/a75167a9e88545d43e5711533fa7e8de814a2eea))

## [0.3.0](https://github.com/wriftai/wriftai-python/compare/v0.2.0...v0.3.0) (2025-10-15)


### Features

* Removed Unpack and update version create method ([#105](https://github.com/wriftai/wriftai-python/issues/105)) ([356bc31](https://github.com/wriftai/wriftai-python/commit/356bc315f0688eefa5d4bdb98cb9fb03bc988a73))

## [0.2.0](https://github.com/wriftai/wriftai-python/compare/v0.1.0...v0.2.0) (2025-10-09)


### Features

* Updated model's create method ([#98](https://github.com/wriftai/wriftai-python/issues/98)) ([c4c2a01](https://github.com/wriftai/wriftai-python/commit/c4c2a01a8ebc96ab32f4667c28f10ee32d8cc088))

## 0.1.0 (2025-10-03)


### Features

* Add release step in CI and code hygiene. ([#80](https://github.com/wriftai/wriftai-python/issues/80)) ([adb5caf](https://github.com/wriftai/wriftai-python/commit/adb5caf5316d094257b792b2156327f7272f2df5))
* Add support for listing models by username ([#61](https://github.com/wriftai/wriftai-python/issues/61)) ([bbde584](https://github.com/wriftai/wriftai-python/commit/bbde584983792155db64891def0534e5c11acb82))
* Added Async client with lazy initialization ([#16](https://github.com/wriftai/wriftai-python/issues/16)) ([b8b6711](https://github.com/wriftai/wriftai-python/commit/b8b67112fa4cefe938960c4d39af99fcacfbb367))
* Added Authenticated User resource ([#26](https://github.com/wriftai/wriftai-python/issues/26)) ([297ed6c](https://github.com/wriftai/wriftai-python/commit/297ed6c7ed284b9151ebe5e4e2fd0fdc0e41cb4a))
* Added get model version using sync and async function ([#31](https://github.com/wriftai/wriftai-python/issues/31)) ([9169faf](https://github.com/wriftai/wriftai-python/commit/9169faff78019fd446a464f4f2f95493b5a4cb0e))
* Added hardware resource with unit and integration tests ([#21](https://github.com/wriftai/wriftai-python/issues/21)) ([c71a0e0](https://github.com/wriftai/wriftai-python/commit/c71a0e0d8ca201db3b4d6db275d5b6dd7185b39d))
* Added issue and PR templates ([#74](https://github.com/wriftai/wriftai-python/issues/74)) ([89c7581](https://github.com/wriftai/wriftai-python/commit/89c7581e0a0ff79848472648d14e4e79c928ff6f))
* Added Model resource ([#48](https://github.com/wriftai/wriftai-python/issues/48)) ([a414d75](https://github.com/wriftai/wriftai-python/commit/a414d75de8ed0891ad345dbd75906b3eecfdf977))
* Added model update functionality ([#68](https://github.com/wriftai/wriftai-python/issues/68)) ([8f147ba](https://github.com/wriftai/wriftai-python/commit/8f147ba63a1998a5328bc0a08c6cae8ba6259103))
* Added support for creating model. ([#54](https://github.com/wriftai/wriftai-python/issues/54)) ([8571723](https://github.com/wriftai/wriftai-python/commit/8571723640a0eb2c4e963a83a8f8e5bd29aa2bfb))
* Added support for deleting a model. ([#51](https://github.com/wriftai/wriftai-python/issues/51)) ([158f76a](https://github.com/wriftai/wriftai-python/commit/158f76a52ce153b71af20fa5e0c655ab06165891))
* Added support for get prediction and integration tests ([#20](https://github.com/wriftai/wriftai-python/issues/20)) ([339f8b7](https://github.com/wriftai/wriftai-python/commit/339f8b79dad3454ccadedff07b775e866c62ae5e))
* Added support for getting a model. ([#53](https://github.com/wriftai/wriftai-python/issues/53)) ([1b53664](https://github.com/wriftai/wriftai-python/commit/1b536642b207b720b85eb68958e3fd5ce9a00226))
* Added support for listing model versions ([ba72342](https://github.com/wriftai/wriftai-python/commit/ba72342a66aef4d3b547443cca1d22e29d7cee27))
* Added support for listing models of authenticated user ([#58](https://github.com/wriftai/wriftai-python/issues/58)) ([13e97ae](https://github.com/wriftai/wriftai-python/commit/13e97aef810a3c8c570823f64d92cfcf48351e4a))
* Added support for listing models. ([#49](https://github.com/wriftai/wriftai-python/issues/49)) ([b3cb941](https://github.com/wriftai/wriftai-python/commit/b3cb94127cc12efecba997b5d06f641b8ef3ceb0))
* Added support for listing predictions ([#35](https://github.com/wriftai/wriftai-python/issues/35)) ([89839fb](https://github.com/wriftai/wriftai-python/commit/89839fbea376219ff5755984587754d8239c44ec))
* Added support for listing users ([#32](https://github.com/wriftai/wriftai-python/issues/32)) ([3fc836b](https://github.com/wriftai/wriftai-python/commit/3fc836bee1b92e7c2ba266c5d5f5804d82a50ae3))
* Added support for searching models based on query. ([#63](https://github.com/wriftai/wriftai-python/issues/63)) ([5d15dfe](https://github.com/wriftai/wriftai-python/commit/5d15dfe6ddba1fee365449820d65dd2031e41111))
* Added support for searching users based on query. ([#62](https://github.com/wriftai/wriftai-python/issues/62)) ([1a854d1](https://github.com/wriftai/wriftai-python/commit/1a854d1b99d67da50729980f0b43c34931d34ea5))
* Added support to create prediction against latest and specific version. ([#60](https://github.com/wriftai/wriftai-python/issues/60)) ([c7eebb7](https://github.com/wriftai/wriftai-python/commit/c7eebb74038765d7afc5a79e21b40f5d36e9fbb5))
* Added support to make pagination fields optional. ([5a8a061](https://github.com/wriftai/wriftai-python/commit/5a8a061c9c1c0846c52c6e3fe72883292f88fc99))
* Added sync client with lazy initialization ([#8](https://github.com/wriftai/wriftai-python/issues/8)) ([3bf396c](https://github.com/wriftai/wriftai-python/commit/3bf396ce4f62301c078e86e057510230cc83af47))
* Added User resource ([#22](https://github.com/wriftai/wriftai-python/issues/22)) ([76eded4](https://github.com/wriftai/wriftai-python/commit/76eded46a91f118cc8ad4fe51369478097c4d3aa))
* Added wait and async_wait methods to Predictions resource ([#73](https://github.com/wriftai/wriftai-python/issues/73)) ([73468a0](https://github.com/wriftai/wriftai-python/commit/73468a0db34c95cc49fec4041cbd91a073846782))
* Update authenticated users ([#69](https://github.com/wriftai/wriftai-python/issues/69)) ([649d1b7](https://github.com/wriftai/wriftai-python/commit/649d1b7144d90072790efb3a86a01f5f92148858))
