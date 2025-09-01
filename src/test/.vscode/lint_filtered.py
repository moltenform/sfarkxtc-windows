import sys
import json
from shinerainsevenlib.standard import *


def mainPylint():
    args = [
        '-m', 'pylint', '--rcfile', 'pyproject.toml', '--ignore-paths=.*OUTSIDE.*',
        '--output-format=json2', '.'
    ]
    pyExe = sys.executable
    args.insert(0, pyExe)
    print(args)
    retcode, stdout, stderr = files.run(args, throwOnFailure=False)
    stdout = stdout.decode('utf-8')
    events = json.loads(stdout)
    events = events['messages']
    for event in events:
        line = formatOneLinePylint(event)
        if 'nocpy_' in line:
            continue
        if "E1101: Instance of 'Bucket' has no" in line:
            # skip this - we don't care about it for Bucket
            continue
        if "W0621: Redefining name 'fixture_" in line:
            # skip this - we don't care about it for fixtures
            continue
        if "Access to a protected member _get of" in line:
            # skip this - we don't care about it for fixtures
            continue
        if "Access to a protected member _get_id of" in line:
            # skip this - we don't care about it for fixtures
            continue

        print(line)


def mainRuff():
    args = [
        '-m', 'ruff', 'check', '--config=pyproject.toml', '--output-format=json',
        '--exclude=.*OUTSIDE.*'
    ]
    if '--fix' in sys.argv:
        args.append('--fix')

    args.append('.')
    pyExe = sys.executable
    args.insert(0, pyExe)
    print(args)
    retcode, stdout, stderr = files.run(args, throwOnFailure=False)
    stdout = stdout.decode('utf-8')
    events = json.loads(stdout)
    for event in events:
        line = formatOneLineRuff(event)
        if 'nocpy_' in line:
            continue

        if "Access to a protected member _get_id of" in line:
            # skip this - we don't care about it for fixtures
            continue

        print(line)


def formatOneLineRuff(msg):
    # example.py:32:67: W0640: An example message (the-warning-type)
    return f"{msg['filename']}:{msg['location'].get('row')}:{msg['location'].get('column')}: {msg['code']} {msg['message']} ({msg.get('url', '').split('/')[-1]})"


def formatOneLinePylint(msg):
    # example.py:32:67: W0640: An example message (the-warning-type)
    return f"{msg['path']}:{msg['line']}:{msg['column']}: {msg['messageId']}: {msg['message']} ({msg['symbol']})"


if __name__ == '__main__':
    try:
        files.delete('__init__.py')
        if '--ruff' in sys.argv:
            mainRuff()
        else:
            mainPylint()
    finally:
        files.writeAll('__init__.py', '')
