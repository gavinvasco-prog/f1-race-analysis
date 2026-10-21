# Technical Project Documentation

## 1. Executive Summary
This project analyses Formula 1 timing data from five races of the 2025 season. It looks at lap times, speed traps, tyre degradation, weather and pit stop strategy, and builds models to predict lap times and race outcomes.

Data is collected with the [FastF1](https://github.com/theOehrly/Fast-F1) Python library ([documentation](https://docs.fastf1.dev)).

---

## 2. Dataset Overview & Data Processing

### 2.1 Dataset Specifications
* **Primary File**: `data/processed/cleaned_laps.csv`
* **Size**: ~2.11 MB
* **Records**: 5,305 laps from the 2025 Bahrain, Monaco, Silverstone, Monza and Suzuka Grands Prix
* **Source**: Official F1 timing data via FastF1, with weather data merged onto each lap (see `src/data_pipeline.py`)

### 2.2 Key Features
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Driver` | String | 3-letter driver identifier (e.g., `VER`, `NOR`, `LEC`) |
| `Team` | String | Constructor team name |
| `Race` | String | Grand Prix name (e.g., `Bahrain`, `Monza`) |
| `LapNumber` | Integer | Lap index within the Grand Prix |
| `LapTime_s` | Float | Total lap duration measured in seconds |
| `Compound` | String | Tyre compound (`SOFT`, `MEDIUM`, `HARD`, `INTERMEDIATE`) |
| `TyreLife` | Integer | Total laps completed on the current tyre set |
| `SpeedST` | Float | Speed recorded at the circuit speed trap (km/h) |
| `TrackTemp` | Float | Track temperature during the lap (°C) |
| `IsAccurate` | Boolean | FastF1 flag: `True` when the lap's timing is reliable |

### 2.3 Data Cleaning & Validation Rules
1. **Visualization notebook (`03_visualizations.ipynb`)**: uses laps where `IsAccurate == True`. This removes pit in/out laps, lap 1 and laps with unreliable timing. It does **not** remove safety car laps or laps deleted for track limits.
2. **Tyre analysis (`Gavin_tyre_degradation.ipynb`)**: uses `clean_laps()` from `src/tyre_model.py`, which removes pit in/out laps, non-green-flag laps (safety car, VSC, yellow flags), laps deleted for track limits, wet tyres, and laps slower than 107% of the fastest lap in each race.

---

## 3. Visualization Pipeline

The visualization notebook exports its charts to `reports/figures/`.

```
              ┌─────────────────────────────────┐
              │ data/processed/cleaned_laps.csv │
              └────────────────┬────────────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │  Filter: IsAccurate == True     │
              └────────────────┬────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Speed Trap      │   │ Lap Time        │   │ Lap Time vs     │
│ Box Plot        │   │ Evolution Plot  │   │ Tyre Age Plot   │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               ▼
              ┌─────────────────────────────────┐
              │ Save PNG figures to             │
              │ reports/figures/                │
              └─────────────────────────────────┘
```

---

## 4. Analytical Insights

### 4.1 Speed Trap Comparison

![Top Speed Comparison](reports/figures/top_speed_comparison.png)

* Median speed trap values are very close across teams, from 300 km/h (Ferrari) to 304 km/h (Williams).
* Most of the spread comes from the track rather than the team: the median is 278 km/h at Monaco and 326 km/h at Monza.

### 4.2 Lap Time Evolution (Bahrain)

![Lap Time Evolution](reports/figures/lap_time_evolution.png)

* Lap times fall over the race as fuel burns off. Piastri's median drops from about 98.4 s (laps 2–10) to about 96.3 s (lap 48 onwards).
* Laps 32–35 are missing for all five drivers, so the plotted lines join across that gap.

### 4.3 Lap Time vs Tyre Age

![Tire Degradation Profile](reports/figures/tire_degradation_profile.png)

* The horizontal bands are different tracks, not a tyre effect: median lap times range from about 77 s (Monaco) to about 103 s (Silverstone).
* Tyre wear is measured properly in `Gavin_tyre_degradation.ipynb`, which separates tyre wear from fuel burn.

---

## 5. How to Run

1. Set up the environment and install dependencies (see the README).
2. Open `notebooks/03_visualizations.ipynb` and run all cells. The charts are saved to `reports/figures/`.

```python
import pandas as pd

# Paths are relative to the notebooks/ folder
df = pd.read_csv("../data/processed/cleaned_laps.csv")
df_valid = df[df["IsAccurate"] == True]
```
