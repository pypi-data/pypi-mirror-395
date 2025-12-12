"""Transforms (Finish: muuntuu) API for opinionated JSON and YAML rewriting."""

from muuntuu.implementation import json_dump, json_load, yaml_dump, yaml_load
from muuntuu import JSON, Request


def transform(request: Request) -> int:
    """Transform between and within the known formats."""
    debug = request.debug
    _ = debug and print('Debug mode requested.')

    load = json_load if request.source_format == JSON else yaml_load
    dump = json_dump if request.target_format == JSON else yaml_dump

    options = vars(request)
    _ = debug and print(f'Requested transform from {request.source_format}' f' to {request.target_format}')
    data = load(request.source, options)

    dump(data, request.target, options)

    return 0
