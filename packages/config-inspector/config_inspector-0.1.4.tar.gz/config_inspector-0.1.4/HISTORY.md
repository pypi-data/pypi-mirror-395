# History

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## 0.1.4 (2025-12-04)
- ADDED: tox and 100% test coverage
- ADDED: `updater_factory` to get the correspinding file updater by looking at the file extension.

## 0.1.3 (2025-12-01)
- ADDED: When writing a file with `FileContentService.write_text()` we set utf-8 errors to `replace`.

## 0.1.2 (2025-11-11)

- ADDED: When reading a file with `FileContentService.get_payload` we set utf-8 errors to `replace`.

## 0.1.1 (2025-11-05)

- ADDED: Added `.js` and `.ps1` extensions that simply use `PlainTextUpdater` and do not try to validate/format on save.

## 0.1.0 (2025-10-06)

- First release
