# Formula 1 Data Analytics & Race Prediction

A data science project analysing Formula 1 timing data from five races of the 2025 season: lap times, tyre degradation, pit stop strategy, weather and race outcome prediction.

Data source: [FastF1](https://github.com/theOehrly/Fast-F1)

---

## Team Roles & Responsibilities

| Team Member | Role | Feature Branch | Core Responsibilities |
| :--- | :--- | :--- | :--- |
| **Member 1** | Data Pipeline Lead | `feature/data-pipeline-weather` | FastF1 data extraction, weather data integration, CSV data cleaning |
| **Member 2** | Tyre Strategy & Git Co-Lead | `feature/tyre-degradation-modeling` | Tyre degradation modelling, lap time prediction, undercut strategy analysis |
| **Member 3** | Visualizations & Documentation Lead | `feature/visualizations-readme` | Speed trap, lap evolution and tyre age charts, project documentation |
| **Member 4** | Predictive ML & Git Co-Lead | `feature/ml-race-prediction` | Feature engineering, race outcome prediction, model evaluation |

---

## Key Visualizations

### 1. Speed Trap Performance
Speed trap (`SpeedST`) values for the six teams with the most valid laps.

![Top Speed Comparison](reports/figures/top_speed_comparison.png)

### 2. Race Lap Evolution
Lap times for five drivers across the Bahrain Grand Prix.

![Lap Time Evolution](reports/figures/lap_time_evolution.png)

### 3. Lap Time vs Tyre Age
All valid laps from the five races, coloured by tyre compound.

![Tire Degradation Profile](reports/figures/tire_degradation_profile.png)

More detail: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gavinvasco-prog/f1-race-analysis.git
   cd f1-race-analysis
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   ```
   - Windows: `.venv\Scripts\Activate.ps1`
   - Mac/Linux: `source .venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the notebooks** in the `notebooks/` folder.
