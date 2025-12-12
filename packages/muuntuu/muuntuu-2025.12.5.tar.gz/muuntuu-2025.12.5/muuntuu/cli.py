"""Command line interface for transforms (Finish: muuntuu) helper tool."""

import argparse
import pathlib
import sys

from typing import Union  # py39 does not handle |

from muuntuu.api import transform
from muuntuu import (
    APP_ALIAS,
    APP_ENV,
    APP_NAME,
    DEBUG,
    JSON,
    Request,
    VERSION,
    YML,
)


JSON_SUFFIXES = set(['.json'])
YAML_SUFFIXES = set(['.yaml', '.yml'])
KNOWN_SUFFIXES = JSON_SUFFIXES | YAML_SUFFIXES


def parser_configured() -> argparse.ArgumentParser:
    """Return the configured argument parser."""
    parser = argparse.ArgumentParser(
        prog=APP_ALIAS,
        description=APP_NAME,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'source_pos',
        nargs='?',
        metavar='SOURCE_FILE',
        help='JSON or YAML source as positional argument',
    )
    parser.add_argument(
        'target_pos',
        nargs='?',
        metavar='TARGET_FILE',
        help='JSON or YAML target as positional argument',
    )
    parser.add_argument(
        '--source',
        '-s',
        dest='source',
        metavar='FILE',
        help='JSON or YAML source',
    )
    parser.add_argument(
        '--target',
        '-t',
        dest='target',
        metavar='FILE',
        help='JSON or YAML target',
    )
    parser.add_argument(
        '--debug',
        '-d',
        dest='debug',
        default=None,
        action='store_true',
        help=f'work in debug mode (default: False), overwrites any environment variable {APP_ENV}_DEBUG value',
    )
    parser.add_argument(
        '--policy-writer',
        dest='policy_writer',
        type=str,
        default='safe',
        help='[YAML only] select writer policy from (safe, r[ound-]t[rip], or "empty") (default: safe)',
    )
    parser.add_argument(
        '--general-offset',
        dest='gen_offset',
        type=int,
        default=2,
        help='general offset (indent) on output (default: 2) - verify the amount yourself, please',
    )
    parser.add_argument(
        '--mapping-offset',
        dest='map_offset',
        type=int,
        default=2,
        help='[YAML only] mapping offset (indent) on output (default: 2) - verify the amount yourself, please',
    )
    parser.add_argument(
        '--sequence-offset',
        dest='seq_offset',
        type=int,
        default=2,
        help='[YAML only] sequence offset (indent) on output (default: 2) - verify the amount yourself, please',
    )
    parser.add_argument(
        '--width',
        dest='width',
        type=int,
        default=150,
        help='[YAML only] constrain width on output (default: 150) - verify the amount yourself, please',
    )
    parser.add_argument(
        '--default-flow-style',
        dest='default_flow_style',
        default=False,
        action='store_true',
        help='[YAML only] select default flow style on output (default: False)',
    )
    parser.add_argument(
        '--sort-base',
        dest='sort_base_map',
        default=False,
        action='store_true',
        help='[YAML only] sort base mapping type on output (default: False)',
    )
    parser.add_argument(
        '--force',
        '-f',
        dest='force',
        default=None,
        action='store_true',
        help='overwrite existing targets (default: False)',
    )
    parser.add_argument(
        '--quiet',
        '-q',
        dest='quiet',
        default=None,
        action='store_true',
        help='work in quiet mode (default: False)',
    )
    parser.add_argument(
        '--version',
        '-V',
        dest='version',
        default=None,
        action='store_true',
        help='display version and exit',
    )

    return parser


def validate_source(options: Request, engine: argparse.ArgumentParser) -> str:
    """Validate the source given."""
    if not (options.source_pos or options.source):
        engine.error(
            'source path must be given - either as first positional argument or as value to the --source option'
        )

    if options.source_pos and options.source:
        engine.error(
            'source path given both as first positional argument and as value to the --source option - pick one'
        )

    if not options.source:
        options.source = options.source_pos

    if not pathlib.Path(options.source).is_file():
        engine.error(f'requested source ({options.source}) is not a file')

    source_suffix = pathlib.Path(options.source).suffix.lower()
    if source_suffix not in KNOWN_SUFFIXES:
        engine.error(
            f'requested source suffix ({source_suffix})'
            f' is not in known suffixes ({", ".join(sorted(KNOWN_SUFFIXES))})'
        )

    return source_suffix


def validate_target(options: Request, engine: argparse.ArgumentParser) -> str:
    """Validate the target given."""
    if not (options.target_pos or options.target):
        engine.error(
            'target path must be given - either as second positional argument or as value to the --target option'
        )

    if options.target_pos and options.target:
        engine.error(
            'target path given both as second positional argument and as value to the --target option - pick one'
        )

    if not options.target:
        options.target = options.target_pos

    if pathlib.Path(options.target).exists() and not options.force:
        engine.error(f'requested target ({options.target}) already exist - remove or request other target')

    target_suffix = pathlib.Path(options.target).suffix.lower()
    if target_suffix not in KNOWN_SUFFIXES:
        engine.error(
            f'requested target suffix ({target_suffix})'
            f' is not in known suffixes ({", ".join(sorted(KNOWN_SUFFIXES))})'
        )

    return target_suffix


def parse_request(argv: list[str]) -> Union[int, Request]:
    """Parse the request vector into validated options."""
    parser = parser_configured()
    if not argv:
        parser.print_help()
        return 0

    options = parser.parse_args(argv)

    if options.version:
        print(VERSION)
        return 0

    # Ensure consistent request for verbosity
    if options.debug and options.quiet:
        parser.error('Cannot be quiet and debug - pick one')

    # Ensure hierarchical setting of debug: command line overwrites environment variable value
    if options.debug is None:
        options.debug = DEBUG

    # Quiet overwrites any debug requests
    if options.quiet:
        options.debug = False

    # validate and map the writer policy for YAML into ('safe', 'rt', None)
    known_policies = ('safe', 'rt', None)
    if not options.policy_writer:
        options.policy_writer = None
    else:
        options.policy_writer = options.policy_writer.lower()
    if options.policy_writer and options.policy_writer not in known_policies:
        options.policy_writer = known_policies[0]

    # Validate and derive the DSL values for source and target formats
    options.source_format = JSON if validate_source(options, engine=parser) in JSON_SUFFIXES else YML
    options.target_format = JSON if validate_target(options, engine=parser) in JSON_SUFFIXES else YML

    return options


def main(argv: Union[list[str], None] = None) -> int:
    """Delegate processing to functional module."""
    argv = sys.argv[1:] if argv is None else argv
    options = parse_request(argv)
    if isinstance(options, int):
        return 0
    return transform(request=options)
