import numpy


def deduce_machine_current(timestamps: tuple, known_machine_current: dict) -> tuple:
    """
    :param known_machine_current: keys are timestamp. Value is machine current
    :param timestamps: timestamp for which we want to get machine current
    """
    if not isinstance(known_machine_current, dict):
        raise TypeError("known_machine_current is expected to be a dict")
    for elmt in timestamps:
        if not isinstance(elmt, numpy.datetime64):
            raise TypeError(
                f"Elements of timestamps are expected to be {numpy.datetime64} and not {type(elmt)}"
            )
    if len(known_machine_current) == 0:
        raise ValueError("known_machine_current should contain at least one element")
    for key, value in known_machine_current.items():
        if not isinstance(key, numpy.datetime64):
            raise TypeError(
                f"known_machine_current keys are expected to be instances of {numpy.datetime64} and not {type(key)}"
            )
        if not isinstance(value, (float, numpy.number)):
            raise TypeError(
                "known_machine_current values are expected to be instances of float"
            )

    # 1. Order **known** machine current by time stamps (key)
    known_machine_current = dict(sorted(known_machine_current.items()))
    known_timestamps = numpy.fromiter(
        known_machine_current.keys(),
        dtype="datetime64[ns]",
        count=len(known_machine_current),
    )
    known_machine_current_values = numpy.fromiter(
        known_machine_current.values(),
        dtype="float64",
        count=len(known_machine_current),
    )

    # 2. Sort the supplied timestamps
    timestamps = numpy.array(timestamps, dtype="datetime64[ns]")
    timestamp_input_ordering = numpy.argsort(timestamps)
    timestamps_sorted = numpy.take_along_axis(
        timestamps, indices=timestamp_input_ordering, axis=0
    )

    # 3. Convert to float for numpy.interp
    known_timestamps_float = known_timestamps.astype("float64")
    timestamps_float = timestamps_sorted.astype("float64")

    # 4. Interpolate the values
    interpolated_values = numpy.interp(
        timestamps_float, known_timestamps_float, known_machine_current_values
    )

    # 5. Reorder interpolated values to match the order of original timestamps
    ordered_interpolated_values = numpy.zeros_like(interpolated_values)
    for i, o_pos in enumerate(timestamp_input_ordering):
        ordered_interpolated_values[o_pos] = interpolated_values[i]
    return tuple(ordered_interpolated_values)
