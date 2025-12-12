#!/usr/bin/env python

import argparse
import datetime
import json
import io
import os
import pathlib
import pyclbr
import shutil
import subprocess
import sys
import tarfile

from jinja2 import Environment
from packaging.version import Version
from urllib.request import Request, urlopen

here = pathlib.Path(__file__).parent


FALLIBLE_VERSION = r'''
def fallible_version(func):
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        post_lines = [
            "",
            "",
            "Fallible experimental build {fallible_version}",
            "This build contains the following experimental features:",
            {features}
        ]
        return ret + "\n".join(post_lines)
    return inner


@fallible_version
'''.strip()


def fallible_version(version_str):
    today = datetime.date.today()
    if not version_str:
        # return a dev-tagged default version for today
        return f'{today.year}.{today.month}.{today.day}.dev0'

    parsed_ver = Version(version_str)

    # ensure value is a sane date, raise if not
    parsed_date = datetime.date(parsed_ver.major, parsed_ver.minor, parsed_ver.micro)

    min_ver = today - datetime.timedelta(days=365)
    max_ver = today + datetime.timedelta(days=7)

    # sanity check build year as current or prior year
    if not (min_ver < parsed_date < max_ver):
        raise argparse.ArgumentTypeError('fallible build date out of range (1 year back, 7 days ahead)')

    return parsed_ver.public


parser = argparse.ArgumentParser()
parser.add_argument('ansible_ref')
parser.add_argument('--github-token', default=os.getenv('GITHUB_TOKEN'))
parser.add_argument('--version', type=fallible_version, default=fallible_version(None),
                    help='a PEP440-compliant version string of the form YYYY.M.D')
group = parser.add_mutually_exclusive_group()
group.add_argument('--pr', action='append', type=int)
group.add_argument('--all', action='store_true', default=False)
args = parser.parse_args()


def build_request(url):
    headers = {}
    if args.github_token:
        headers['Authorization'] = f'token {args.github_token}'
    return Request(
        url,
        headers=headers,
    )


def get_fallible_prs():
    print('Fetching all fallible tagged PRs')
    url = (
        'https://api.github.com/repos/ansible/ansible/issues?'
        'labels=fallible&direction=asc&per_page=100'
    )
    for issue in json.load(urlopen(build_request(url))):
        yield issue['number']


def get_prs(prs):
    data = []
    for pr in prs:
        print(f'Fetching details for #{pr}')
        url = f'https://api.github.com/repos/ansible/ansible/pulls/{pr}'
        data.append(json.load(urlopen(build_request(url))))
    return data


def extract_version_tarball(ref, dest):
    print(f'Fetching GitHub tarball for {ref}')
    if ref[0].isdigit():
        ref_type = 'tags'
    else:
        ref_type = 'heads'
    url = (
        'https://github.com/ansible/ansible'
        f'/archive/refs/{ref_type}/{ref}.tar.gz'
    )

    t = tarfile.open(
        mode='r:gz',
        fileobj=io.BytesIO(urlopen(url).read())
    )
    for member in t.getmembers():
        member.name = member.name.partition('/')[2]
        t.extract(member, path=dest, filter='data')


def modify_version(prs):
    print('Patching --version')
    functions = pyclbr.readmodule_ex(
        'ansible.cli.arguments.option_helpers',
        path=[str(here / 'ansible' / 'lib')],
    )
    version = functions['version']
    path = pathlib.Path(version.file)

    newlines = []
    for pr in prs:
        newlines.append(
            f'            "  - {pr["title"]}: {pr["html_url"]}",'
        )

    lines = path.read_text().splitlines()
    start_lineno = version.lineno - 1
    lines[start_lineno:start_lineno] = [
        FALLIBLE_VERSION.format(fallible_version=args.version, features='\n'.join(newlines)),
    ]
    path.write_text('\n'.join(lines))


def get_patches(prs):
    for pr in prs:
        number = pr['number']
        print(f'Fetching patch for #{number}')
        url = f'https://github.com/ansible/ansible/pull/{number}.diff'
        yield number, urlopen(build_request(url)).read()


def apply_patch(pr, patch):
    print(f'Applying patch for #{pr}')
    p = subprocess.Popen(
        [
            'patch',
            '-p1'
        ],
        cwd=here / 'ansible',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    stdout, stderr = p.communicate(input=patch)
    if p.returncode:
        input(
            f'\nFailed to apply patch for {pr}. Resolve the merge conflicts '
            f'and then press ENTER:\n'
            f'\nstdout:\n{stdout.decode()}\nstderr:\n{stderr.decode()}\n'
        )
        print('Continuing')


def generate_fallible_version(fallible_version):
    print(f'Setting fallible version to {fallible_version}')
    version_path = (here / '_fallible_version.py')
    version_path.write_text(f'VERSION = "{fallible_version}"')


def generate_ansible_core_dist_info():
    print('Generating dist_info')
    p = subprocess.Popen(
        [
            sys.executable,
            'setup.py',
            'dist_info'
        ],
        cwd=here / 'ansible',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    p.communicate()


def generate_readme(prs):
    print('Generating FEATURES.md')
    features = (here.parent.parent.parent / 'FEATURES.md.j2').read_text()
    features_out = here.parent.parent.parent / 'FEATURES.md'
    e = Environment()
    t = e.from_string(features)
    features_out.write_text(t.render(prs=prs))


# cleanup
print('Cleaning up _vendor directory')
for path in here.glob('*'):
    if path.name in ('__init__.py', '_build.py'):
        continue
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()

ansible_dir = here / 'ansible'
ansible_dir.mkdir()

if args.all:
    prs = get_prs(get_fallible_prs())
else:
    prs = get_prs(args.pr or [])
patches = list(get_patches(prs))

extract_version_tarball(args.ansible_ref, ansible_dir)

for patch in patches:
    apply_patch(*patch)

modify_version(prs)

generate_ansible_core_dist_info()
generate_fallible_version(args.version)
generate_readme(prs)

# cleanup
print('Cleaning up patch files')
for path in here.glob('**/*.orig'):
    path.unlink()
for path in here.glob('**/*.rej'):
    path.unlink()
