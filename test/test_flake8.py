import subprocess


def test_call_flake8(tmpdir):
    tmp = tmpdir.join('tmp.py')
    tmp.write('')
    output = subprocess.check_output(
        ['flake8', str(tmp)],
        stderr=subprocess.STDOUT,
    )
    assert output == b''


def test_call_flake8_version():
    output = subprocess.check_output(
        ['flake8', '--version'],
        stderr=subprocess.STDOUT,
    )
    assert b'flake8-commas-x: ' in output
