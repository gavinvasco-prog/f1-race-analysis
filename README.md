# 🏎️ Formula 1 Data Analytics & Race Prediction Pipeline

An end-to-end data science and machine learning framework designed to process raw Formula 1 race telemetry, evaluate tire degradation profiles, analyze driver stint performance, and predict final race outcomes across multiple Grands Prix.

---

##  Team Roles & Responsibilities

| Team Member | Role | Feature Branch | Core Responsibilities |
| :--- | :--- | :--- | :--- |
| **Member 1** | Data Pipeline Lead | `feature/data-pipeline-weather` | FastF1 telemetry extraction, weather data integration, CSV data cleaning |
| **Member 2** | Tyre Strategy & Git Co-Lead | `feature/tyre-degradation-modeling` | Compound decay modeling, stint degradation analysis, undercut strategy modeling |
| **Member 3** | Visualizations & Documentation Lead | `feature/visualizations-readme` | Telemetry plots, lap evolution figures, interactive scripts, system documentation |
| **Member 4** | Predictive ML & Git Co-Lead | `feature/ml-race-prediction` | Feature engineering, supervised classification/regression models, evaluation metrics |

---

## Key Insights & Visualizations

### 1. Speed Trap Performance
Analysis of peak velocity measured at the Speed Trap (`SpeedST`) across top constructor teams.

![Top Speed Comparison](reports/figures/top_speed_comparison.png)

### 2. Race Lap Evolution
Tracking driver stint progression, lap time consistency, and pit stop windows during the Bahrain Grand Prix.

![Lap Time Evolution](reports/figures/time_lap_evolution.png)

### 3. Tire Compound Degradation
Comparing compound lap time decay against tire age (`TyreLife`) across `SOFT`, `MEDIUM`, `HARD`, and `INTERMEDIATE` sets.

![Tire Degradation Profile](reports/figures/tire_degradation_profile.png)

---

## Repository Structure

```text
f1-race-analysis/
├── data/
│   ├── raw/                      # Raw telemetry extracted from FastF1
│   └── processed/                # Cleaned CSV datasets (cleaned_laps.csv)
├── notebooks/                    # Interactive Jupyter Notebooks
│   ├── 01_data_pipeline.ipynb
│   ├── 02_tyre_degradation.ipynb
│   ├── 03_visualizations.ipynb   # Member 3 EDA & Visualizations
│   └── 04_ml_prediction.ipynb
├── reports/
│   └── figures/                  # Exported publication-ready charts (.png)
├── src/                          # Modular Python source scripts
│   └── generate_visualizations.py
├── .gitignore
├── PROJECT_DOCUMENTATION.md      # Comprehensive technical documentation
├── README.md                     # Project overview
└── requirements.txt              # Project dependencies
```

---


## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gavinvasco-prog/f1-race-analysis.git
   cd f1-race-analysis
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the visualization pipeline**:
   ```bash
   python src/generate_visualizations.py
   ```
