"""
Reusable functions for the tyre degradation and strategy analysis.

Used by notebooks/Gavin_tyre_degradation.ipynb. All functions take the
combined laps + weather data from data/processed/cleaned_laps.csv.
"""
import pandas as pd
from sklearn.linear_model import LinearRegression

DRY_COMPOUNDS = ["SOFT", "MEDIUM", "HARD"]


def clean_laps(df, slow_lap_threshold=1.07):
    """Keep only representative racing laps.

    Removes pit in/out laps, laps not under green flag, laps deleted for
    track limits, wet-weather tyres, and laps slower than 107% of the
    fastest lap in that race.
    """
    clean = df[
        df["PitInTime"].isna()                                      # not a pit-in lap
        & df["PitOutTime"].isna()                                   # not a pit-out lap
        & (pd.to_numeric(df["TrackStatus"], errors="coerce") == 1)  # green flag only
        & (df["Deleted"] != True)                                   # not deleted for track limits
        & df["Compound"].isin(DRY_COMPOUNDS)                        # dry tyres only
    ].copy()

    fastest = clean.groupby("Race")["LapTime_s"].transform("min")
    return clean[clean["LapTime_s"] <= fastest * slow_lap_threshold].copy()


def add_lap_delta(clean):
    """Drop lap 1 and add LapDelta: each lap's time minus that driver's
    median lap time in that race. This removes car speed differences."""
    data = clean[clean["LapNumber"] > 1].copy()   # drop standing-start laps
    driver_median = data.groupby(["Race", "Driver"])["LapTime_s"].transform("median")
    data["LapDelta"] = data["LapTime_s"] - driver_median
    return data


def fit_degradation(model_data):
    """Fit LapDelta ~ TyreLife + LapNumber separately for each compound.

    The TyreLife coefficient is tyre wear (seconds per lap of tyre age);
    the LapNumber coefficient is the fuel effect (seconds per lap).
    """
    results = []
    for compound, group in model_data.groupby("Compound"):
        X = group[["TyreLife", "LapNumber"]]
        y = group["LapDelta"]
        model = LinearRegression().fit(X, y)
        results.append({
            "Compound": compound,
            "Tyre wear (s per lap of age)": model.coef_[0],
            "Fuel effect (s per lap)": model.coef_[1],
            "R²": model.score(X, y),
            "Laps": len(group),
        })
    return pd.DataFrame(results)


def find_pit_battles(df, max_gap=3, max_stop_diff=5):
    """Find undercut/overcut battles between cars running next to each other.

    A battle is two drivers adjacent on track (within max_gap seconds) whose
    first pit stops are 1 to max_stop_diff laps apart. The attacker is the car
    that was behind before the stops; success means the attacker is ahead
    a lap after both have pitted. Uses the uncleaned data, since pit laps are needed.
    """
    raw = df.copy()
    raw["LapEndTime"] = pd.to_timedelta(raw["Time_x"]).dt.total_seconds()
    raw["TrackStatusNum"] = pd.to_numeric(raw["TrackStatus"], errors="coerce")

    events = []
    for race, r in raw.groupby("Race"):
        pos = r.pivot_table(index="LapNumber", columns="Driver", values="Position")
        end = r.pivot_table(index="LapNumber", columns="Driver", values="LapEndTime")
        status = r.pivot_table(index="LapNumber", columns="Driver", values="TrackStatusNum")
        first_stop = r[r["PitInTime"].notna()].groupby("Driver")["LapNumber"].min()

        for x, px in first_stop.items():                # x = driver who pitted first
            before = px - 1
            if before not in pos.index or pd.isna(pos.at[before, x]):
                continue
            for y, py in first_stop.items():            # y = rival who pitted later
                if y == x or not (1 <= py - px <= max_stop_diff):
                    continue
                if pd.isna(pos.at[before, y]) or abs(pos.at[before, x] - pos.at[before, y]) != 1:
                    continue                            # must be running next to each other
                gap = abs(end.at[before, x] - end.at[before, y])
                if pd.isna(gap) or gap > max_gap:
                    continue                            # must be close on track
                after = py + 2                          # a lap after the rival's out-lap
                if after not in pos.index or pd.isna(pos.at[after, x]) or pd.isna(pos.at[after, y]):
                    continue

                x_behind_before = pos.at[before, x] > pos.at[before, y]
                attacker, defender = (x, y) if x_behind_before else (y, x)
                events.append({
                    "Race": race,
                    "Attacker": attacker,
                    "Defender": defender,
                    "Strategy": "Undercut" if attacker == x else "Overcut",
                    "Gap before (s)": round(gap, 2),
                    "Success": pos.at[after, attacker] < pos.at[after, defender],
                    "Green flag stops": status.at[px, x] == 1 and status.at[py, y] == 1,
                })

    return pd.DataFrame(events)
