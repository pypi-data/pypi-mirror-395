#!/usr/bin/env python3
"""
NeuroSound CLI - Command-line interface for audio compression.
"""

import argparse
import sys
import os
from pathlib import Path

from .core import NeuroSound


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='🧠 NeuroSound - Ultra-efficient audio compression (12.52x ratio)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic compression
  neurosound input.wav output.mp3
  
  # Aggressive mode (fastest)
  neurosound input.wav output.mp3 -m aggressive
  
  # Safe mode (highest quality)
  neurosound input.wav output.mp3 -m safe
  
  # Quiet mode
  neurosound input.wav output.mp3 -q

Modes:
  balanced    12.52x ratio, 0.105s, 29mJ (RECOMMENDED)
  aggressive  12.40x ratio, 0.095s, 27mJ (fastest)
  safe        11.80x ratio, 0.115s, 32mJ (highest quality)

GitHub: https://github.com/bhanquier/neuroSound
        """
    )
    
    parser.add_argument('input', type=str, help='Input WAV file (16-bit PCM)')
    parser.add_argument('output', type=str, help='Output MP3 file')
    parser.add_argument(
        '-m', '--mode',
        choices=['balanced', 'aggressive', 'safe'],
        default='balanced',
        help='Compression mode (default: balanced)'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress output'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='NeuroSound 3.1.0'
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    if not args.input.lower().endswith('.wav'):
        print(f"❌ Error: Input must be WAV file, got: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Compress
    try:
        codec = NeuroSound(mode=args.mode)
        size, ratio, energy = codec.compress(args.input, args.output, verbose=not args.quiet)
        
        if args.quiet:
            # Print machine-readable output
            print(f"{size},{ratio:.2f},{energy:.0f}")
        
        sys.exit(0)
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
