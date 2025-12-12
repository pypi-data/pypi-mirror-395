import pytest

import preheat_open as po
from preheat_open.api.conftest import MOCK_LOCATION_ID, mock_adapter


@pytest.fixture(scope="module")
def location(mock_adapter) -> po.Location:
    return mock_adapter.get_location(MOCK_LOCATION_ID)
