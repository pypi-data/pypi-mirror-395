"""Tests for the oocone.Enocoo.get_area_ids() method."""

import pytest
from syrupy.assertion import SnapshotAssertion

from oocone import Auth, Enocoo
from tests import TIMEZONE
from tests.conftest import MockApiParams


@pytest.mark.parametrize(
    "dataset",
    ["one_area", "two_areas"],
)
async def test_happy_path(
    dataset: str, snapshot: SnapshotAssertion, mock_auth: Auth, mock_api_params: MockApiParams
) -> None:
    """Check that enocoo.get_areas returns the areas as indicated in ownConsumption.php."""
    mock_api_params.dataset_name = dataset
    enocoo = Enocoo(mock_auth, TIMEZONE)

    areas = await enocoo.get_areas()
    assert areas == snapshot
