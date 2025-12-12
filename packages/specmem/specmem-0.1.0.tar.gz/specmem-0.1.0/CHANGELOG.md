# Changelog

All notable changes to SpecMem will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of SpecMem
- Core memory bank with chunking, ranking, and lifecycle management
- SpecIR canonical representation for specifications
- Adapters for Kiro, Cursor, Claude Code, SpecKit, and Tessl
- LanceDB as default vector database backend
- Support for ChromaDB and Qdrant backends
- Local embeddings via SentenceTransformers
- Cloud embedding providers (OpenAI, Anthropic, Google, Together)
- SpecImpact graph for code-to-spec dependency analysis
- SpecDiff for temporal spec intelligence and drift detection
- Test mapping engine with framework-agnostic support
- Streaming context API with token budget optimization
- SpecValidator for specification quality assurance
- CLI with init, scan, build, query, and impact commands
- Python client API for agent integration
- Web UI for browsing and managing specifications

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [0.1.0] - 2025-12-01

### Added
- Initial public release
- Developed as part of the Kiroween Hackathon, December 2025
- IP of Superagentic AI

[Unreleased]: https://github.com/Shashikant86/specmem/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Shashikant86/specmem/releases/tag/v0.1.0
