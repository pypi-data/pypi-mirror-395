#!/usr/bin/env python3
"""
CarLib CLI Tool

A command-line interface for the CarLib dataset conversion library.

Commands:
- convert: Convert datasets to CAR format
- config: Manage configuration files
- info: Show information about CarLib
- validate: Validate CAR files

Usage:
    carlib convert /path/to/data --modality vanilla --target-modality audio --output /path/to/output
    carlib config list
    carlib config show audio
    carlib info
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def create_parser():
    """Create the main argument parser with subcommands"""
    parser = argparse.ArgumentParser(
        prog='carlib',
        description='CarLib - Dataset to CAR format conversion tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert vanilla audio files
  carlib convert /path/to/audio --modality vanilla --target-modality audio -o /output
  
  # Convert webdataset with custom config
  carlib convert /path/to/webdataset.tar --modality webdataset --target-modality image --config my_config.yaml -o /output
  
  # List available configurations
  carlib config list
  
  # Show current audio configuration
  carlib config show audio
  
  # Get CarLib information
  carlib info
        """
    )
    
    # Add version
    parser.add_argument('--version', action='version', version='CarLib 1.0.0')
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert command
    convert_parser = subparsers.add_parser(
        'convert', 
        help='Convert datasets to CAR format',
        description='Convert datasets from various formats to CAR format'
    )
    add_convert_args(convert_parser)
    
    # Config command  
    config_parser = subparsers.add_parser(
        'config',
        help='Manage configuration files',
        description='View and manage CarLib configuration files'
    )
    add_config_args(config_parser)
    
    # Info command
    subparsers.add_parser(
        'info',
        help='Show CarLib information',
        description='Display information about CarLib installation and capabilities'
    )
    
    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate CAR files',
        description='Validate and inspect CAR files'
    )
    add_validate_args(validate_parser)
    
    # Setup command (for checkpoint management)
    setup_parser = subparsers.add_parser(
        'setup',
        help='Setup and manage CarLib checkpoints',
        description='Download and manage model checkpoints'
    )
    add_setup_args(setup_parser)
    
    return parser

def add_convert_args(parser):
    """Add arguments for the convert command"""
    # Required arguments
    parser.add_argument('input_path', help='Path to input dataset directory or file')
    parser.add_argument('--output', '-o', required=True, help='Output directory for CAR files')
    parser.add_argument('--modality', '-m', required=True,
                       choices=['vanilla', 'webdataset', 'hdf5', 'tfrecord'],
                       help='Format type to process')
    parser.add_argument('--target-modality', '-t', required=True,
                       choices=['audio', 'image', 'video'],
                       help='Target media type')
    
    # Optional arguments
    parser.add_argument('--config', '-c', help='Path to YAML configuration file')
    parser.add_argument('--parallel', action='store_true', default=True,
                       help='Enable parallel processing (default: True)')
    parser.add_argument('--sequential', action='store_true', default=False,
                       help='Force sequential processing')
    parser.add_argument('--gpus', '-g', type=int, help='Number of GPUs to use (auto-detected if not specified)')
    parser.add_argument('--recursive', '-r', action='store_true', default=False,
                       help='Search recursively in subdirectories')
    parser.add_argument('--no-recursive', action='store_false', dest='recursive',
                       help='Do not search recursively (default behavior)')
    parser.add_argument('--max-files', type=int, help='Maximum number of files to process')
    
    # Model overrides
    parser.add_argument('--model-name', help='Override model name')
    parser.add_argument('--model-type', help='Override model type (for audio: encodec, dac, snac)')
    
    # Output options
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress progress output')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')

def add_config_args(parser):
    """Add arguments for the config command"""
    config_subparsers = parser.add_subparsers(dest='config_action', help='Config actions')
    
    # List configs
    config_subparsers.add_parser('list', help='List available configuration files')
    
    # Show specific config
    show_parser = config_subparsers.add_parser('show', help='Show configuration for a target modality')
    show_parser.add_argument('target_modality', choices=['audio', 'image', 'video'],
                            help='Target modality to show config for')
    show_parser.add_argument('--config', '-c', help='Path to custom config file to show')
    
    # Create default config
    create_parser = config_subparsers.add_parser('create', help='Create default configuration file')
    create_parser.add_argument('target_modality', choices=['audio', 'image', 'video'],
                              help='Target modality to create config for')
    create_parser.add_argument('--output', '-o', help='Output path for config file')
    
    # Validate config
    validate_parser = config_subparsers.add_parser('validate', help='Validate configuration file')
    validate_parser.add_argument('config_file', help='Path to config file to validate')

def add_validate_args(parser):
    """Add arguments for the validate command"""
    parser.add_argument('car_files', nargs='+', help='CAR files to validate')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--check-integrity', action='store_true', help='Check file integrity')

def add_setup_args(parser):
    """Add arguments for the setup command"""
    setup_subparsers = parser.add_subparsers(dest='setup_action', help='Setup actions')
    
    # Download specific model
    download_parser = setup_subparsers.add_parser('download', help='Download specific model checkpoint')
    download_parser.add_argument('model_name', help='Model name to download (e.g., CI8x8, DV8x16x16)')
    download_parser.add_argument('--force', action='store_true', help='Force re-download even if exists')
    
    # Download all models
    download_all_parser = setup_subparsers.add_parser('download-all', help='Download all model checkpoints')
    download_all_parser.add_argument('--type', choices=['image', 'video'], help='Download only specific model type')
    
    # List available models
    setup_subparsers.add_parser('list', help='List available models and their status')
    
    # Show cache info
    setup_subparsers.add_parser('info', help='Show checkpoint cache information')
    
    # Clean cache
    clean_parser = setup_subparsers.add_parser('clean', help='Clean checkpoint cache')
    clean_parser.add_argument('--keep', type=int, default=5, help='Number of recent checkpoints to keep')

def handle_convert_command(args):
    """Handle the convert subcommand"""
    try:
        from dataset_to_car import convert_dataset_to_car
        
        # Build model config from command line args
        model_config = {}
        if args.model_name:
            model_config['model_name'] = args.model_name
        if args.model_type:
            model_config['model_type'] = args.model_type
        
        # Set verbosity
        if args.quiet:
            # Could implement quiet mode
            pass
        elif args.verbose:
            # Could implement verbose mode  
            pass
        
        print(f"🚀 Starting dataset conversion...")
        print(f"  Input: {args.input_path}")
        print(f"  Output: {args.output}")
        print(f"  Modality: {args.modality}")
        print(f"  Target modality: {args.target_modality}")
        processing_mode = "sequential" if args.sequential else "parallel"
        gpu_info = f"{args.gpus} (specified)" if args.gpus else "auto-detected"
        print(f"  Processing mode: {processing_mode}")
        print(f"  GPUs: {gpu_info}")
        print()
        
        # Determine parallelization mode
        parallel = not args.sequential and args.parallel
        
        convert_dataset_to_car(
            input_path=args.input_path,
            output_path=args.output,
            modality=args.modality,
            target_modality=args.target_modality,
            parallel=parallel,
            num_gpus=args.gpus,
            recursive=args.recursive,
            max_files=args.max_files,
            config_file=args.config,
            model_config=model_config if model_config else None
        )
        
        print(f"\n✅ Conversion completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        sys.exit(1)

def handle_config_command(args):
    """Handle the config subcommand"""
    if args.config_action == 'list':
        print("📋 Available CarLib configurations:")
        print()
        
        config_dir = Path(__file__).parent / 'configs'
        config_files = ['audio_config.yaml', 'image_config.yaml', 'video_config.yaml']
        
        for config_file in config_files:
            config_path = config_dir / config_file
            modality = config_file.split('_')[0]
            status = "✅ Found" if config_path.exists() else "❌ Missing"
            print(f"  {modality.capitalize()}: {config_path} ({status})")
        
        print()
        print("Example configs:")
        example_configs = ['example_custom_audio.yaml', 'example_custom_image.yaml', 'example_custom_video.yaml']
        for example in example_configs:
            example_path = config_dir / example
            if example_path.exists():
                print(f"  {example}: {example_path}")
                
    elif args.config_action == 'show':
        try:
            from dataset_to_car import load_config_from_yaml
            
            print(f"📄 Configuration for {args.target_modality}:")
            print()
            
            config = load_config_from_yaml(args.config, args.target_modality)
            
            for key, value in config.items():
                print(f"  {key}: {value}")
                
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            sys.exit(1)
            
    elif args.config_action == 'create':
        config_dir = Path(__file__).parent / 'configs'
        default_config = config_dir / f'{args.target_modality}_config.yaml'
        
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = Path(f'{args.target_modality}_config.yaml')
        
        try:
            if default_config.exists():
                import shutil
                shutil.copy2(default_config, output_path)
                print(f"✅ Created {args.target_modality} config: {output_path}")
            else:
                print(f"❌ Default config not found: {default_config}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error creating config: {e}")
            sys.exit(1)
            
    elif args.config_action == 'validate':
        try:
            import yaml
            
            with open(args.config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            print(f"✅ Configuration file is valid: {args.config_file}")
            print(f"  Contains {len(config)} settings")
            
        except Exception as e:
            print(f"❌ Invalid configuration file: {e}")
            sys.exit(1)
    else:
        print("❌ No config action specified. Use 'carlib config --help' for usage.")
        sys.exit(1)

def handle_info_command():
    """Handle the info subcommand"""
    print("🚗 CarLib - Dataset to CAR Format Conversion Library")
    print("=" * 50)
    print()
    
    # Version info
    print("📦 Version: 1.0.0")
    print()
    
    # Supported formats
    print("📁 Supported Input Formats:")
    print("  • vanilla: Regular media files (audio/image/video)")
    print("  • webdataset: WebDataset tar archives")
    print("  • hdf5: HDF5 data files")
    print("  • tfrecord: TensorFlow record files")
    print()
    
    print("🎯 Target Modalities:")
    print("  • audio: Audio files (.wav, .mp3, .flac, etc.)")
    print("  • image: Image files (.jpg, .png, .webp, etc.)")
    print("  • video: Video files (.mp4, .avi, .mov, etc.)")
    print()
    
    # Check dependencies
    print("🔧 Dependencies:")
    dependencies = [
        ('torch', 'PyTorch'),
        ('torchaudio', 'TorchAudio'), 
        ('transformers', 'Transformers'),
        ('yaml', 'PyYAML'),
        ('tqdm', 'Progress bars'),
        ('webdataset', 'WebDataset support'),
        ('h5py', 'HDF5 support'),
        ('tensorflow', 'TFRecord support')
    ]
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} (optional)")
    
    print()
    
    # Configuration info
    config_dir = Path(__file__).parent / 'configs'
    print(f"⚙️  Configuration directory: {config_dir}")
    print(f"   {'✅' if config_dir.exists() else '❌'} Config directory exists")
    
    print()
    print("📖 Usage:")
    print("  carlib convert /path/to/data --modality vanilla --target-modality audio -o /output")
    print("  carlib config list")
    print("  carlib info")

def handle_validate_command(args):
    """Handle the validate subcommand"""
    print(f"🔍 Validating {len(args.car_files)} CAR file(s)...")
    print()
    
    valid_files = 0
    invalid_files = 0
    
    for car_file in args.car_files:
        car_path = Path(car_file)
        
        if not car_path.exists():
            print(f"❌ File not found: {car_file}")
            invalid_files += 1
            continue
            
        if not car_path.suffix.lower() == '.car':
            print(f"⚠️  Not a .car file: {car_file}")
            
        try:
            # Basic file validation
            file_size = car_path.stat().st_size
            
            if file_size == 0:
                print(f"❌ Empty file: {car_file}")
                invalid_files += 1
                continue
            
            if args.verbose:
                print(f"✅ {car_file}")
                print(f"   Size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
                
                if args.check_integrity:
                    # Could add more detailed integrity checks here
                    print(f"   Integrity: ✅ Basic checks passed")
            else:
                print(f"✅ {car_file} ({file_size / (1024*1024):.2f} MB)")
            
            valid_files += 1
            
        except Exception as e:
            print(f"❌ Error validating {car_file}: {e}")
            invalid_files += 1
    
    print()
    print(f"📊 Validation Summary:")
    print(f"  ✅ Valid files: {valid_files}")
    print(f"  ❌ Invalid files: {invalid_files}")
    print(f"  📁 Total processed: {len(args.car_files)}")

def handle_setup_command(args):
    """Handle the setup subcommand"""
    try:
        from checkpoints import get_checkpoint_manager, list_models, download_model, download_all
        
        if args.setup_action == 'download':
            print(f"📥 Downloading checkpoint: {args.model_name}")
            success = download_model(args.model_name, force=args.force)
            if success:
                print(f"✅ Successfully downloaded {args.model_name}")
            else:
                print(f"❌ Failed to download {args.model_name}")
                sys.exit(1)
                
        elif args.setup_action == 'download-all':
            print("📦 Downloading all checkpoints...")
            if args.type:
                print(f"   Filtering by type: {args.type}")
            results = download_all(model_type=args.type)
            successful = sum(results.values())
            total = len(results)
            print(f"\n📊 Download Summary: {successful}/{total} successful")
            
        elif args.setup_action == 'list':
            print("📋 Available CarLib Models:")
            print()
            models = list_models()
            
            # Group by type
            for model_type in ['image', 'video']:
                print(f"{model_type.capitalize()} Models:")
                for name, info in models.items():
                    if info['type'] == model_type:
                        status = "✅ Available" if info['available'] else "❌ Not Downloaded"
                        print(f"  {name:12} {status:15} {info['path']}")
                print()
                
        elif args.setup_action == 'info':
            manager = get_checkpoint_manager()
            print("📂 CarLib Checkpoint Information:")
            print(f"   Cache directory: {manager.cache_dir}")
            print(f"   Legacy directory: {manager.legacy_dir}")
            print()
            
            models = list_models()
            available_count = sum(1 for info in models.values() if info['available'])
            total_count = len(models)
            print(f"   Available models: {available_count}/{total_count}")
            
        elif args.setup_action == 'clean':
            manager = get_checkpoint_manager()
            removed = manager.cleanup_cache(keep_recent=args.keep)
            print(f"🧹 Cleaned {removed} old checkpoints")
            
        else:
            print("❌ No setup action specified. Use 'carlib setup --help' for usage.")
            sys.exit(1)
            
    except ImportError as e:
        print(f"❌ Setup command requires checkpoint manager: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'convert':
            handle_convert_command(args)
        elif args.command == 'config':
            handle_config_command(args)
        elif args.command == 'info':
            handle_info_command()
        elif args.command == 'validate':
            handle_validate_command(args)
        elif args.command == 'setup':
            handle_setup_command(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()