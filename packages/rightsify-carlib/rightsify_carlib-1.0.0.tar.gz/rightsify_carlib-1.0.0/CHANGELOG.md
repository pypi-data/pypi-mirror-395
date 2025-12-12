# Changelog

All notable changes to CarLib will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-02

### Added
- Initial release of CarLib
- Support for multiple input formats:
  - vanilla: Regular media files (audio, image, video)
  - webdataset: WebDataset tar archives
  - hdf5: HDF5 data files
  - tfrecord: TensorFlow record files
- Support for multiple target modalities:
  - audio: Audio processing with EnCodec, DAC, SNAC
  - image: Image processing with Cosmos Image models
  - video: Video processing with Cosmos Video models
- CLI tool with subcommands:
  - `convert`: Dataset conversion to CAR format
  - `config`: Configuration management
  - `info`: System information
  - `validate`: CAR file validation
- YAML-based configuration system
- Multi-GPU parallel processing
- Comprehensive error handling and logging
- Progress tracking with tqdm
- Python API for programmatic usage
- Extensive documentation and examples

### Features
- **Multi-format Support**: Convert from various dataset formats
- **Multi-modal Processing**: Handle audio, image, and video data
- **Configurable**: YAML configuration with command-line overrides
- **Scalable**: Multi-GPU processing for large datasets
- **User-friendly**: Simple CLI interface with helpful error messages
- **Extensible**: Clean architecture for adding new formats/modalities

### Dependencies
- torch >= 1.9.0
- torchaudio >= 0.9.0
- transformers >= 4.20.0
- PyYAML >= 5.4.0
- tqdm >= 4.60.0
- numpy >= 1.19.0

### Optional Dependencies
- webdataset >= 0.2.0 (for WebDataset support)
- h5py >= 3.0.0 (for HDF5 support)
- tensorflow >= 2.8.0 (for TFRecord support)

## [Unreleased]

### Planned Features
- Batch processing optimization
- Resume interrupted conversions
- Advanced configuration validation
- Plugin system for custom formats
- Async processing pipeline
- Enhanced logging system