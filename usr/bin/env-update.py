#!/usr/bin/env python
"""
Refresh an environment yaml file to current versions.

This script reads an existing `environment.yml` file (for Conda/Mamba
environments) and writes out a new file listing the same packages, but listing
all currently available versions of the listed packages.

For an alternate approach, that queries PyPI/Conda-Forge to gather the most
recent versions of all packages, see @yuvipanda's similar script at
https://github.com/berkeley-dsep-infra/datahub/issues/3630#issuecomment-1226684419
which inspired this one.  That script will ensure newest versions of all
packages, but with the risk that the resulting environment file has version
incompatibilities amongst packages.

Since this one relies on querying the existing environment instead of upstream
package repositories, it will not guarantee that the updated file has the most
recent version of everything. Instead ensures that it lists versions that can
be installed together.

Notes and caveats:
- the pip section is left as-is, and versions in it are NOT updated.
"""

# Stdlib imports
import argparse
import json
import re
import shutil
import tempfile

from pathlib import Path
from subprocess import check_output

# Third-party imports
from ruyaml import YAML


# Utility functions
def parse_dep(dep):
    """Parse a dependency into (package, version) tuple.

    If the given dependency can't be parsed, returns None.
    """
    if not isinstance(dep, str):
        return None

    match = re.match(r'([a-zA-Z0-9_-]+)==?([0-9.]+)', dep)
    if match:
        package = match.group(1)
        version = match.group(2)
        return package, version
    else:
        return None


def parse_deps(deps):
    return [ d for d in map(parse_dep, deps) if d is not None]


# Tests
def test_parse_deps():
    deps = ['abseil-cpp=20211102.0=hdf3f5d2_2',
            'affine=2.3.1=pyhd8ed1ab_0',
            'aiohttp=3.8.1=py39hb18efdd_1',
            'aiosignal=1.2.0=pyhd8ed1ab_0',
            'alabaster=0.7.12=py_0',
            'foo=BADVER-nostring']

    parsed = [('abseil-cpp', '20211102.0'),
              ('affine', '2.3.1'),
              ('aiohttp', '3.8.1'),
              ('aiosignal', '1.2.0'),
              ('alabaster', '0.7.12')]

    assert parsed == parse_deps(deps)


# Main script entry point
def main():
    argparser = argparse.ArgumentParser(description=__doc__,
                                       formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument('filename',
                           help='Environment filename to update')
    argparser.add_argument('--inplace', action='store_true',
                          help='Update the env file in-place')
    args = argparser.parse_args()

    # Load the environment definition from disk
    yaml = YAML(typ="rt")

    envfile = Path(args.filename)
    with envfile.open() as f:
        env = yaml.load(f)

    # Read the _actual_ current package versions from conda
    newenv = json.loads(check_output(['conda', 'env', 'export', '--json']))
    # Process the dependencies section - we'll have current versions only
    # for things we can parse
    newenv_deps = dict(parse_deps(newenv['dependencies']))

    # Now, create a new dependencies section to replace the old one
    new_deps = []

    # The logic is: go through the originals one by one, and only update
    # deps for which we found one in the real environment from conda
    for ori_dep in env['dependencies']:
        ori_parsed = parse_dep(ori_dep)
        if ori_parsed is None:
            # If we can't parse the definition as pkg/version, keep
            # the original
            new_dep = ori_dep
        else:
            pkg, ver = ori_parsed
            new_ver = newenv_deps.get(pkg)
            if new_ver is None:
                # If there's nothing in the current env for that original
                # package, keep the original dep declaration untouched
                new_dep = ori_dep
            else:
                # Only if we have a proper replacement, use it
                new_dep = f'{pkg}=={new_ver}'
        new_deps.append(new_dep)

    # Now, we can replace the deps section with ours
    env['dependencies'] = new_deps

    # Write output to disk, either to a separate file for easy comparison
    # by the user or in-place if requested
    if args.inplace:
        print(f'Overwriting {args.filename} in-place.')
        with tempfile.NamedTemporaryFile('w') as f:
            yaml.dump(env, f)
            f.flush()
            shutil.copyfile(f.name, args.filename)
    else:
        newfile = envfile.parent/(envfile.stem+'-updated' + envfile.suffix)
        print(f'Output left in file: {newfile.name}')
        with newfile.open('w') as f:
            yaml.dump(env, f)


# Script execution
if __name__ == '__main__':
    main()
