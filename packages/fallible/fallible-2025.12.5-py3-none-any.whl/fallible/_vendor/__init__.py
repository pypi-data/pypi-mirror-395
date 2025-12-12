# Copyright: (c) 2022, Matt Martz <matt@sivel.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import pathlib
import sys

here = pathlib.Path(__file__).parent


def _infect():
    os.environ['ANSIBLE_DEVEL_WARNING'] = '0'
    ansible = here / 'ansible' / 'lib'
    ansible_test = here / 'ansible' / 'test' / 'lib'
    sys.path[0:0] = [str(ansible), str(ansible_test)]


_infect()
