# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.9.0] - 2024-11-13

- Added support for Self-Hosted GPU Runners
- Deprecated `matrix` and `preview` fields in place of `advanced_evaluation` in training run creation
- Bug Fixes
  - Fixed main arguments conflicting with flags in CLI
  - Fixed project listing erroring if one project has failed authentication
  - Fixed regex validation errors for asset upload, asset group list, and annotation export
  - Fixed annotation export error handling for single annotated asset and no annotated asset cases
  - Fixed relative pathing issues for asset upload, annotation export, and artifact download
  - Fixed help command failing for some non top-level commands

## [1.8.1] - 2024-09-30

- Bug fixes for Datature CLI

## [1.8.0] - 2024-09-16

- Inference Batch Job Support
  - Webhook & Secret Management
  - Batch Dataset Management
  - Batch Job & Resources Management

## [1.7.2] - 2024-07-29

### Added

- Bug fix for Datature CLI - Added numpy version to requirements.txt

## [1.7.1b1] - 2024-04-23

### Added

- Custom model import (Beta)

## [1.7.0] - 2024-04-16

### Added

- TensorRT conversion utility functions
- TensorRT prediction utility functions

## [1.6.0] - 2024-02-07

### Added

- Annotation Importation
- Artifacts Advanced Exportation
- Ontology Management

### Changed

- Init SDK functions

---

## Unreleased

### [1.6.1] - 2024-02-14

#### Added

- Contributing Guidelines
- Code of Conduct
- Github Actions that Automate the Creation of Releases

#### Changed

- Changed SDK logger name from `nexus` to `datature-nexus`
