# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## Unreleased

## 1.0.1 - 2014-06-08
### Added
- Test module
- Added pytest to the requirements.txt list.
- .travis.yml
- Adds _credentials.py file in .gitignore for the test module.
- Testing Section under README.md
- Encrypted file for travis service.

## 1.0.0 - 2014-06-08

### Added

- This CHANGELOG file.
- decorators.py file
- Exceptions: AuthorizationHeaderNotSet, AttributeIsNotResponseType
in nova_exceptions.py
 
### Changed
- Most get methods in api.py use decorators for validation.
- Defined missing attributes in \_\_init\_\_ method.







