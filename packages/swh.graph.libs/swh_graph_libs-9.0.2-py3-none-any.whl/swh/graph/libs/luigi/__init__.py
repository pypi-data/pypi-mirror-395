# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""
Luigi tasks
===========

This package contains `Luigi <https://luigi.readthedocs.io/>`_ tasks.
These come in two kinds:
"""

# WARNING: do not import unnecessary things here to keep cli startup time under
# control

from .topology import *  # noqa
