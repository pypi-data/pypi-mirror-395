#!/usr/bin/env python3
"""
CLI tool for managing vmanage-agent cryptographic keys.

Usage:
    vmanage-keys status              # Show status of all keys
    vmanage-keys rotate <key_type>   # Rotate specific key type
    vmanage-keys export              # Export public keys for registration
    vmanage-keys init                # Initialize all keys
"""

import argparse
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from vmanage_agent.key_manager import KeyManager
from loguru import logger as log


def cmd_status(args):
    """Show status of all keys"""
    km = KeyManager()
    status = km.get_key_status()
    
    print("\n" + "="*60)
    print("VMANAGE-AGENT KEY STATUS")
    print("="*60 + "\n")
    
    for key_type, info in status.items():
        print(f"[{key_type.upper()}]")
        print(f"  Private Key: {'✓ EXISTS' if info['private_key_exists'] else '✗ MISSING'}")
        print(f"  Public Key:  {'✓ EXISTS' if info['public_key_exists'] else '✗ MISSING'}")
        print(f"  Location:    {info['path']}")
        if 'created_at' in info:
            print(f"  Created:     {info['created_at']}")
        print()
    
    # Check if all keys exist
    all_exist = all(
        info['private_key_exists'] and info['public_key_exists']
        for info in status.values()
    )
    
    if all_exist:
        print("✓ All keys present and accounted for!\n")
        return 0
    else:
        print("⚠ Some keys are missing. Run 'vmanage-keys init' to generate them.\n")
        return 1


def cmd_rotate(args):
    """Rotate specific key type"""
    key_type = args.key_type
    
    if key_type not in ['wg_controller', 'wg_tunnel', 'blockchain']:
        print(f"Error: Invalid key_type '{key_type}'")
        print("Valid options: wg_controller, wg_tunnel, blockchain")
        return 1
    
    print(f"\n⚠ WARNING: This will regenerate {key_type} keys!")
    print("Old keys will be overwritten and cannot be recovered.")
    
    if not args.force:
        response = input("\nContinue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Aborted.")
            return 0
    
    km = KeyManager()
    private, public = km.rotate_keys(key_type)
    
    print(f"\n✓ {key_type} keys rotated successfully!")
    print(f"New public key: {public[:40]}...")
    print("\n⚠ IMPORTANT: Register the new public key with backend:")
    print(f"  POST /api/v1/devices/{{id}}/keys/")
    print(f"  {{'key_type': '{key_type}', 'public_key': '{public}'}}\n")
    
    return 0


def cmd_export(args):
    """Export public keys for registration"""
    km = KeyManager()
    public_keys = km.get_public_keys_for_registration()
    
    if args.format == 'json':
        print(json.dumps(public_keys, indent=2))
    else:
        print("\n" + "="*60)
        print("PUBLIC KEYS FOR REGISTRATION")
        print("="*60 + "\n")
        
        for key_name, key_value in public_keys.items():
            print(f"[{key_name}]")
            if key_name == 'blockchain_public_key':
                # For PEM, show first few lines
                lines = key_value.split('\n')
                print('\n'.join(lines[:3]))
                print('...')
                print(lines[-1])
            else:
                print(key_value)
            print()
    
    return 0


def cmd_init(args):
    """Initialize all keys"""
    km = KeyManager()
    
    if args.force:
        print("⚠ Force mode: Will regenerate existing keys!")
    
    print("Initializing all cryptographic keys...")
    keys = km.initialize_all_keys(force=args.force)
    
    print("\n✓ Key initialization complete!\n")
    
    # Show what was done
    for key_type in keys:
        print(f"  ✓ {key_type} keys ready")
    
    print(f"\nKeys stored in: {km.KEY_DIR}")
    print("Run 'vmanage-keys export' to see public keys for registration.\n")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Manage vmanage-agent cryptographic keys',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vmanage-keys status                    # Show all keys
  vmanage-keys init                      # Generate keys
  vmanage-keys rotate wg_controller      # Rotate controller keys
  vmanage-keys export --format json      # Export as JSON
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Status command
    subparsers.add_parser('status', help='Show status of all keys')
    
    # Rotate command
    rotate_parser = subparsers.add_parser('rotate', help='Rotate specific key type')
    rotate_parser.add_argument(
        'key_type',
        choices=['wg_controller', 'wg_tunnel', 'blockchain'],
        help='Type of key to rotate'
    )
    rotate_parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompt'
    )
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export public keys')
    export_parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize all keys')
    init_parser.add_argument(
        '--force',
        action='store_true',
        help='Regenerate existing keys'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to command handler
    commands = {
        'status': cmd_status,
        'rotate': cmd_rotate,
        'export': cmd_export,
        'init': cmd_init
    }
    
    try:
        return commands[args.command](args)
    except Exception as e:
        log.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
