"""Talk to the OpenF1 API. Every pull is saved to data/ so we only download once."""
import os
import time
import requests
import pandas as pd

BASE_URL = "https://api.openf1.org/v1/"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def get(endpoint, **params):
    """Ask OpenF1 for `endpoint` (e.g. 'sessions') and return a DataFrame."""
    r = requests.get(BASE_URL + endpoint, params=params)
    if r.status_code == 429:           # too many requests: wait, then retry
        time.sleep(1)
        return get(endpoint, **params)
    r.raise_for_status()               # stop with an error on any other failure
    return pd.DataFrame(r.json())


def get_cached(name, endpoint, **params):
    """Same as get(), but reads data/<name>.csv if it exists, else downloads and saves it."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, name + ".csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    df = get(endpoint, **params)
    df.to_csv(path, index=False)
    return df


# One row per OpenF1 endpoint: what it covers, how often rows show up, and the
# columns worth knowing about. Kept as a list of dicts (like a little spreadsheet)
# so endpoint_reference() can turn it into a DataFrame.
ENDPOINTS = [
    {"endpoint": "sessions",             "granularity": "1 row per session (practice/quali/race)",
     "key_fields": "session_name, session_type, date_start/end, circuit_short_name, year"},
    {"endpoint": "meetings",             "granularity": "1 row per Grand Prix weekend",
     "key_fields": "meeting_name, country_name, circuit_key, year"},
    {"endpoint": "drivers",              "granularity": "1 row per driver per session",
     "key_fields": "full_name, name_acronym, team_name, team_colour, headshot_url"},
    {"endpoint": "laps",                 "granularity": "1 row per driver per lap",
     "key_fields": "lap_number, lap_duration, duration_sector_1/2/3, i1_speed, i2_speed, st_speed, is_pit_out_lap"},
    {"endpoint": "car_data",             "granularity": "~3.7 Hz telemetry samples",
     "key_fields": "speed, throttle, brake, n_gear, rpm, drs"},
    {"endpoint": "location",             "granularity": "~3.7 Hz",
     "key_fields": "x, y, z (track-position coordinates)"},
    {"endpoint": "position",             "granularity": "1 row per position change",
     "key_fields": "position, date"},
    {"endpoint": "intervals",            "granularity": "~every 4s, race only",
     "key_fields": "gap_to_leader, interval (gap to car ahead)"},
    {"endpoint": "stints",               "granularity": "1 row per tyre stint",
     "key_fields": "compound, lap_start, lap_end, tyre_age_at_start"},
    {"endpoint": "pit",                  "granularity": "1 row per pit stop",
     "key_fields": "lap_number, lane_duration, stop_duration"},
    {"endpoint": "weather",              "granularity": "~every 1 min",
     "key_fields": "air_temperature, track_temperature, humidity, rainfall, wind_speed"},
    {"endpoint": "race_control",         "granularity": "1 row per event",
     "key_fields": "category, flag, message, scope, lap_number"},
    {"endpoint": "team_radio",           "granularity": "1 row per radio clip",
     "key_fields": "recording_url (mp3)"},
    {"endpoint": "starting_grid",        "granularity": "1 row per driver, pre-race",
     "key_fields": "position (grid slot), lap_duration (quali time that set it)"},
    {"endpoint": "session_result",       "granularity": "1 row per driver, post-session",
     "key_fields": "position, duration, gap_to_leader, dnf/dns/dsq"},
    {"endpoint": "overtakes",            "granularity": "1 row per pass, race only (may be incomplete)",
     "key_fields": "overtaking_driver_number, overtaken_driver_number, position"},
    {"endpoint": "championship_drivers", "granularity": "1 row per driver, race sessions only (beta)",
     "key_fields": "points_start/current, position_start/current"},
    {"endpoint": "championship_teams",   "granularity": "1 row per team, race sessions only (beta)",
     "key_fields": "team_name, points_start/current, position_start/current"},
]


def endpoint_reference():
    """A table of every OpenF1 endpoint with what it returns, for quick lookup."""
    return pd.DataFrame(ENDPOINTS)


def top_drivers(year, n=5):
    """The n drivers highest in the final championship standings of `year`."""
    races = get("sessions", year=year, session_name="Race")
    last = races["session_key"].iloc[-1]                       # final race of the season
    standings = get("championship_drivers", session_key=last)
    drivers = get("drivers", session_key=last)
    top = standings.sort_values("position_current").head(n)
    top = top.merge(drivers[["driver_number", "full_name", "team_name"]], on="driver_number")
    return top[["position_current", "driver_number", "full_name", "team_name", "points_current"]]
