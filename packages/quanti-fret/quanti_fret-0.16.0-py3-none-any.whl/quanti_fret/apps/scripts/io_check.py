""" Helper to test an io folder using the command line.

It provides 3 commands:
    * sequence:
        check if a folder is a valid triplet sequence or not and display the
        reasons that failed the validation
    * scan:
        Look for all valid triplet sequence inside a given folder and its
        subfolders.
    * config:
        Check if a config is valid or not
"""
from quanti_fret.apps.app_default_path import AppDefaultPath
from quanti_fret.io import (
    CalibrationConfig, FretConfig, TripletScanner, TripletSequenceLoader
)

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments.

    The parser provides 3 subcommands :
        * sequence: Check a folder for a valid triplet sequence
        * scan: look for all valide sequences in subfolders
        * config: validate a config file

    Returns:
        argparse.Namespace: populated namespace
    """
    # Parser
    parser = argparse.ArgumentParser(
        description='Utility tool to check inputs and outputs')
    subs = parser.add_subparsers(dest='command', required=True)

    # Sequence subparser
    sequence = subs.add_parser(
        'sequence',
        description='Check a folder to see if an sequence can be found and '
                    'displays the errors if not')
    sequence.add_argument(
        'folder', type=str, help='Path to the sequence folder'
    )

    # Seeker subparser
    scan = subs.add_parser(
        'scan',
        description='Scan for all the triplet sequences in a folder and it '
                    'subfolders'
    )
    scan.add_argument(
        'root_folder', type=str, help='Path to the root folder to search in'
    )
    scan.add_argument(
        '--list', '-l', action='store_true',
        help='Display the list of all triplet sequences found.'
    )

    # Config subparser
    config = subs.add_parser(
        'config',
        description='Check or fix a config file')
    config.add_argument(
        'phase', type=str, choices=['calibration', 'fret'],
        help='Phase to use for the config'
    )
    config.add_argument(
        '-f', '--fix', action='store_true',
        help='Fix and save the config instead of checking it'
    )
    config.add_argument(
        'config_file', type=str,
        help='Path to the config file, or "active_config" to use the default'
             ' one.'
    )

    # Parse args
    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == 'sequence':
        sequence = TripletSequenceLoader().check_and_load(args.folder,
                                                          verbose=True)
        if sequence is not None:
            print(f'Sequence found with {sequence.size} triplets!')
    elif args.command == 'scan':
        scanner = TripletScanner()
        series = scanner.scan(args.root_folder)
        if series.size == 0:
            print('No triplet sequences found.')
        else:
            if not args.list:
                print(f'Found {series.size} triplet sequences.')
            if args.list:
                print(f'Found {series.size} triplet sequences:')
                for seq in series:
                    print(f' - {seq.folder}: {seq.size} frames')
    elif args.command == 'config':
        if args.config_file == 'active_config':
            active_config_path_file = \
                AppDefaultPath.active_config_path_file(args.phase)
            with open(active_config_path_file, 'r') as f:
                config_path = Path(f.read())
        else:
            config_path = args.config_file

        if args.fix:
            accept_missing_keys = True
        else:
            accept_missing_keys = False

        if args.phase == 'calibration':
            config = CalibrationConfig()
        else:
            config = FretConfig()
        config.load(config_path, accept_missing_keys=accept_missing_keys)

        if args.fix:
            config.save(config_path)
        else:
            print("Your config is valid! :)")
    else:
        print('Invalid command')


if __name__ == '__main__':
    main()
