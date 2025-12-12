from __future__ import annotations


def group_series(acquisition, list_of_series: list) -> list:
    """
    :param ZSeriesBaseAcquisition acquisition:
    z-series version 2 and 3 are all defined in a separate sequence.
    So we need to aggregate for post processing based on their names.
    post-processing can be dark / flat copy to others NXtomo
    """
    for series in list_of_series:
        if series[0].is_part_of_same_series(acquisition):
            series.append(acquisition)
            return list_of_series
    list_of_series.append(
        [
            acquisition,
        ]
    )
    return list_of_series
