# Copyright (c) 2021-2024 Datalayer, Inc.
#
# Datalayer License

import json

from .._version import __version__


async def test_config(jp_fetch):
    # When
    response = await jp_fetch("datalayer_ui", "config")

    # Then
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {
        "extension": "datalayer_ui",
        "version": __version__,
    }
