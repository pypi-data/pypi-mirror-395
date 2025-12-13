# Copyright 2025 Georges Racinet <georges.racinet@cloudcrane.io>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later

from pathlib import Path
from .. import identification


def test_incarnation_id():
    assert identification.INCARNATION_ID


def test_ensure_client_id(tmpdir):
    path = Path(tmpdir / 'client-id')
    identification.CLIENT_ID = None  # can have been set by another test

    identification.ensure_client_id(path)
    client_id = identification.CLIENT_ID

    assert len(client_id.split('-')) == 5

    identification.CLIENT_ID = None
    identification.ensure_client_id(path)

    assert identification.CLIENT_ID == client_id
