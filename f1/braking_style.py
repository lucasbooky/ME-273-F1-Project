"""Braking-style metrics: how often, how long, and how hard a driver brakes.

Complements the racing-line curvature work (which looks at the *shape* of the
path a driver takes through corners, using x/y location data) by looking at a
*control input* instead: the brake pedal and how fast speed drops while it's
pressed. Uses car_data, not location.
"""
import pandas as pd
from f1.fetch import get_cached


def get_car_data(session_key, driver_number, name):
    """Fetch (and cache) brake/speed telemetry for one driver, sorted by time."""
    car = get_cached(name, "car_data", session_key=session_key, driver_number=driver_number)
    car["date"] = pd.to_datetime(car["date"], format="ISO8601")
    car = car.sort_values("date").reset_index(drop=True)
    return car


def find_braking_zones(car_data):
    """Find each stretch of consecutive rows where the brake is pressed.

    `brake` is 100 while the pedal is pressed, 0 while it isn't. Returns a
    list of (start_index, end_index) pairs, one per braking zone, as indices
    into car_data.

    This is written as an explicit loop so the logic is easy to follow: walk
    through the rows and note where a braking zone starts and ends. (A
    vectorized version is possible too — np.diff on a boolean "is braking"
    array finds the same start/end points without the loop — but the loop
    version reads closer to the plain description above.)
    """
    is_braking = car_data["brake"].to_numpy() > 0
    zones = []
    start = None
    for i, braking in enumerate(is_braking):
        if braking and start is None:
            start = i                      # zone begins here
        elif not braking and start is not None:
            zones.append((start, i - 1))   # zone just ended at the previous row
            start = None
    if start is not None:                  # still braking on the last sample
        zones.append((start, len(is_braking) - 1))
    return zones


def zone_metrics(car_data, zones):
    """One row per braking zone: how long it lasted and how hard they braked.

    - duration: seconds spent on the brake
    - speed_drop: km/h lost from the start to the end of the zone
    - decel_rate: average km/h lost per second (bigger = harder braking)
    """
    rows = []
    for start, end in zones:
        duration = (car_data.loc[end, "date"] - car_data.loc[start, "date"]).total_seconds()
        if duration <= 0:
            continue                       # single-sample zone, nothing to measure

        speed_drop = car_data.loc[start, "speed"] - car_data.loc[end, "speed"]
        rows.append({
            "start_index": start,
            "end_index": end,
            "duration": duration,
            "speed_drop": speed_drop,
            "decel_rate": speed_drop / duration,
        })
    return pd.DataFrame(rows)


def braking_style(session_key, driver_number, name):
    """Summarize one driver's braking style in a session as a single dict.

    n_brake_zones    -- how many separate times they got on the brake (frequency)
    avg_duration     -- typical length of a braking zone, in seconds
    avg_decel_rate   -- typical braking intensity, in km/h lost per second
    decel_consistency-- std dev of decel_rate across zones (low = brakes the
                         same way every time, high = erratic/inconsistent)

    Returns None if the driver never braked (shouldn't happen for a full race).
    """
    car = get_car_data(session_key, driver_number, name)
    zones = find_braking_zones(car)
    metrics = zone_metrics(car, zones)

    if metrics.empty:
        return None

    return {
        "driver_number": driver_number,
        "n_brake_zones": len(metrics),
        "avg_duration": metrics["duration"].mean(),
        "avg_decel_rate": metrics["decel_rate"].mean(),
        "decel_consistency": metrics["decel_rate"].std(),
    }


def braking_style_table(session_key, driver_numbers, name_fn):
    """braking_style() for several drivers at once, as one DataFrame.

    `name_fn` turns a driver number into the cache name used for that
    driver's car_data, e.g. `lambda num: f"aus2025_car_{num}"`, matching how
    the notebook already caches each driver's telemetry.
    """
    rows = []
    for num in driver_numbers:
        row = braking_style(session_key, num, name_fn(num))
        if row is not None:
            rows.append(row)
    return pd.DataFrame(rows)
