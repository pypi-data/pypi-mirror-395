from hestia_earth.utils.tools import current_time_ms

from .log import logger
from .aggregate_cycles import aggregate_country, aggregate_global
from .recalculate_cycles import should_recalculate, recalculate
from .utils import distribution
from .utils.quality_score import calculate_score
from .utils.term import is_global as is_global_country


def _mock_nb_distribution(include_distribution: bool):
    original_func = distribution._nb_iterations
    distribution._nb_iterations = lambda *args: (
        original_func(*args) if include_distribution else 0
    )
    not include_distribution and logger.warning("Not generating distribution.")


def _get_aggregate_function(country: dict, filter_by_country: bool = True):
    return (
        aggregate_global
        if is_global_country(country) and filter_by_country
        else aggregate_country
    )


def aggregate(
    country: dict,
    product: dict,
    start_year: int,
    end_year: int,
    source: dict = None,
    include_distribution: bool = True,
    filter_by_country: bool = True,
    include_covariance: bool = True,
):
    """
    Aggregates data from HESTIA.
    Produced data will be aggregated by product, country and year.

    Parameters
    ----------
    country: dict
        The country to group the data.
    product: dict
        The product to group the data.
    start_year: int
        The start year of the data.
    end_year: int
        The end year of the data.
    source: dict
        Optional - the source of the generate data. Will be set to HESTIA if not provided.
    include_distribution : bool
        Include a `distribution` for each aggregated data point. Included by default.
    filter_by_country : bool
        If set to `False`, Cycles from all countries will be used.
        When used with `Worl` or `Continent` aggregation, setting `False` will also use non-aggregated Cycles.
    include_covariance : bool
        Include the `covarianceMatrix`. Included by default.

    Returns
    -------
    list
        A list of aggregated Cycles with nested aggregated Sites.
    """
    # mock nb distributions depending on the parameter
    _mock_nb_distribution(include_distribution)
    aggregate_function = _get_aggregate_function(
        country=country, filter_by_country=filter_by_country
    )

    now = current_time_ms()
    logger.info(
        "Aggregating %s in %s for period %s to %s"
        + (" with distribution" if include_distribution else ""),
        product.get("name"),
        country.get("name"),
        start_year,
        end_year,
    )
    aggregations, countries = aggregate_function(
        country,
        product,
        source,
        start_year,
        end_year,
        include_distribution=include_distribution,
        filter_by_country=filter_by_country,
        include_covariance=include_covariance,
    )
    logger.info("time=%s, unit=ms", current_time_ms() - now)
    aggregations = (
        [recalculate(agg, product) for agg in aggregations]
        if should_recalculate(product)
        else aggregations
    )
    aggregations = [
        calculate_score(cycle=agg, countries=countries) for agg in aggregations
    ]
    return aggregations
