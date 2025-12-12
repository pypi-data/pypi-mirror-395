import pytest
from unittest.mock import Mock, patch

from hestia_earth.aggregation.utils.term import DEFAULT_COUNTRY_ID
from hestia_earth.aggregation import aggregate

class_path = "hestia_earth.aggregation"

country_id = "GADM-FRA"
product = {}
start_year = 2000
end_year = 2009


@pytest.mark.parametrize(
    "country,filter_by_country,called",
    [
        ({"@id": country_id}, True, True),
        ({"@id": country_id}, False, True),
        ({"@id": DEFAULT_COUNTRY_ID}, True, False),
        ({"@id": DEFAULT_COUNTRY_ID}, False, True),
    ],
)
@patch(f"{class_path}.aggregate_global", return_value=([], []))
@patch(f"{class_path}.aggregate_country", return_value=([], []))
def test_aggregate_country(
    mock_aggregate: Mock,
    mock_1: Mock,
    country: dict,
    filter_by_country: bool,
    called: bool,
):
    aggregate(
        country, product, start_year, end_year, filter_by_country=filter_by_country
    )
    assert mock_aggregate.called == called


@pytest.mark.parametrize(
    "country,filter_by_country,called",
    [
        ({"@id": country_id}, True, False),
        ({"@id": country_id}, False, False),
        ({"@id": DEFAULT_COUNTRY_ID}, True, True),
        ({"@id": DEFAULT_COUNTRY_ID}, False, False),
    ],
)
@patch(f"{class_path}.aggregate_country", return_value=([], []))
@patch(f"{class_path}.aggregate_global", return_value=([], []))
def test_aggregate_global(
    mock_aggregate: Mock,
    mock_1: Mock,
    country: dict,
    filter_by_country: bool,
    called: bool,
):
    aggregate(
        country, product, start_year, end_year, filter_by_country=filter_by_country
    )
    assert mock_aggregate.called == called
