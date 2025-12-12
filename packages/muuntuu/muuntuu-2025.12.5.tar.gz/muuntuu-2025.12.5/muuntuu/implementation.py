"""Format specific load and dump implementations for the transforms (Finish: muuntuu) tool."""

import json
import pathlib
from typing import Union

from ruamel.yaml import YAML  # type: ignore

from muuntuu import ENCODING, ENC_ERRS, NL, Options, PathLike


def json_dump(data: object, path: PathLike, options: Union[Options, None] = None) -> None:
    """doc"""
    if options is None:
        options = {}
    debug = options.get('debug', False)
    ensure_ascii = options.get('ensure_ascii', False)
    indent = options.get('gen_offset', 2)
    _ = debug and print(f'json_dump(data, path={path}, options={options}) called ...')
    with open(path, 'wt', encoding=ENCODING, errors=ENC_ERRS) as target:
        json.dump(data, target, ensure_ascii=ensure_ascii, indent=indent)
        target.write(NL)


def json_load(path: PathLike, options: Union[Options, None] = None) -> object:
    """doc"""
    if options is None:
        options = {}
    debug = options.get('debug', False)
    _ = debug and print(f'json_load(path={path}, options={options}) called ...')
    with open(path, 'rt', encoding=ENCODING, errors=ENC_ERRS) as source:
        return json.load(source)


def yaml_configured(
    typ: Union[str, None] = 'safe',
    sort_base_map: bool = False,
    gen_offset: int = 2,
    map_offset: int = 2,
    seq_offset: int = 2,
    width: int = 150,
    default_flow_style: bool = False,
) -> YAML:
    """Return configured YAML processor."""
    yaml = YAML() if typ is None else YAML(typ=typ)

    yaml.sort_base_mapping_type_on_output = sort_base_map
    yaml.indent(mapping=map_offset, sequence=seq_offset, offset=gen_offset)
    yaml.width = width
    yaml.default_flow_style = default_flow_style

    return yaml


def yaml_load(path: PathLike, options: Union[Options, None] = None) -> object:
    """doc"""
    if options is None:
        options = {}
    debug = options.get('debug', False)
    _ = debug and print(f'yaml_load(path={path}, options={options}) called ...')
    yaml = yaml_configured()
    with open(path, 'rt', encoding=ENCODING, errors=ENC_ERRS) as source:
        return yaml.load(source)


def yaml_dump(data: object, path: PathLike, options: Union[Options, None] = None) -> None:
    """doc"""
    if options is None:
        options = {}
    debug = options.get('debug', False)
    policy_writer = options.get('policy_writer', 'safe')
    sort_base_map = options.get('sort_base_map', False)
    gen_offset = options.get('gen_offset', 2)
    map_offset = options.get('map_offset', 2)
    seq_offset = options.get('seq_offset', 2)
    width = options.get('width', 150)
    default_flow_style = options.get('default_flow_style', False)
    _ = debug and print(f'yaml_dump(data, path={path}, options={options}) called ...')
    yaml = yaml_configured(
        typ=policy_writer,
        sort_base_map=sort_base_map,
        gen_offset=gen_offset,
        map_offset=map_offset,
        seq_offset=seq_offset,
        width=width,
        default_flow_style=default_flow_style,
    )
    yaml.dump(data, pathlib.Path(path))  # upstream requires a target with a write method
