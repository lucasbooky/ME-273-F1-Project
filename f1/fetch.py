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


def top_drivers(year, n=5):
    """The n drivers highest in the final championship standings of `year`."""
    races = get("sessions", year=year, session_name="Race")
    last = races["session_key"].iloc[-1]                       # final race of the season
    standings = get("championship_drivers", session_key=last)
    drivers = get("drivers", session_key=last)
    top = standings.sort_values("position_current").head(n)
    top = top.merge(drivers[["driver_number", "full_name", "team_name"]], on="driver_number")
    return top[["position_current", "driver_number", "full_name", "team_name", "points_current"]]
