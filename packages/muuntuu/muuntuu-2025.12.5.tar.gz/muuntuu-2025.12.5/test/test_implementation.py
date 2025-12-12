import pathlib
import tempfile


import muuntuu.implementation as impl
from muuntuu import ENCODING, ENC_ERRS

FIXTURE = pathlib.Path('test/fixtures/')

MISSING_TARGET_MESSAGE = (
    'error: target path must be given - either as second positional argument or as value to the --target option'
)

with open(FIXTURE / 'offsets-width.yaml', 'rt', encoding=ENCODING, errors=ENC_ERRS) as handle:
    WEIRD = handle.read()


def test_impl_ok_json_to_yaml_non_default(capsys):
    source = FIXTURE / 'offsets-width.json'
    with tempfile.TemporaryDirectory() as temp_dir:
        target = pathlib.Path(temp_dir) / 'weird.yaml'
        options = {
            'source_pos': None,
            'target_pos': None,
            'source': str(source),
            'target': str(target),
            'debug': True,
            'gen_offset': 3,
            'map_offset': 1,
            'seq_offset': 2,
            'width': 20,
            'default_flow_style': False,
            'policy_writer': 'rt',
            'sort_base_map': False,
            'force': None,
            'quiet': None,
            'version': None,
            'source_format': 'json',
            'target_format': 'yaml',
        }
        data = impl.json_load(source, options=options)
        impl.yaml_dump(data, target, options=options)
        assert target.is_file()
        with open(target, 'rt', encoding=ENCODING, errors=ENC_ERRS) as handle:
            result = handle.read()
        with open(FIXTURE / 'offsets-width.yml', 'rt', encoding=ENCODING, errors=ENC_ERRS) as handle:
            expected = handle.read()
        assert result == expected
    out, err = capsys.readouterr()
    assert not err
    assert 'json_load(path=test/fixtures/offsets-width.json, options={' in out
    assert 'weird.yaml' in out


def test_impl_ok_json_to_yaml_with_defaults(capsys):
    source = FIXTURE / 'some-object.json'
    with tempfile.TemporaryDirectory() as temp_dir:
        target = pathlib.Path(temp_dir) / 'default.yaml'
        options = None
        data = impl.json_load(source, options=options)
        impl.yaml_dump(data, target, options=options)
        assert target.is_file()
        with open(target, 'rt', encoding=ENCODING, errors=ENC_ERRS) as handle:
            result = handle.read()
        with open(FIXTURE / 'some-object.yml', 'rt', encoding=ENCODING, errors=ENC_ERRS) as handle:
            expected = handle.read()
        assert result == expected
    out, err = capsys.readouterr()
    assert not err
    assert not out


def test_impl_ok_yaml_to_json_with_defaults(capsys):
    source = FIXTURE / 'some-object.yml'
    with tempfile.TemporaryDirectory() as temp_dir:
        target = pathlib.Path(temp_dir) / 'default.json'
        options = None
        data = impl.yaml_load(source, options=options)
        impl.json_dump(data, target, options=options)
        assert target.is_file()
        with open(target, 'rt', encoding=ENCODING, errors=ENC_ERRS) as handle:
            result = handle.read()
        with open(FIXTURE / 'some-object.json', 'rt', encoding=ENCODING, errors=ENC_ERRS) as handle:
            expected = handle.read()
        assert result == expected
    out, err = capsys.readouterr()
    assert not err
    assert not out
