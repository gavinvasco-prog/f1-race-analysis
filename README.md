# F1 Race Analysis

## Team Workflow
- Never commit directly to `main`; use your feature branch and open a PR
- `git pull origin main` before starting new work
- Reusable functions go in `src/`, analysis and charts go in `notebooks/`
- Clear commit messages, e.g. `Add tyre degradation regression`

| Member | Branch | Files |
|---|---|---|
| Member 1 | feature/data-pipeline-weather | src/data_pipeline.py, notebooks/01_data_weather.ipynb |
| Member 2 | feature/tyre-degradation-modeling | src/tyre_model.py, notebooks/02_tyre_degradation.ipynb |
| Member 3 | feature/visualizations-readme | src/plots.py, notebooks/03_visualizations.ipynb |
| Member 4 | feature/ml-race-prediction | src/race_model.py, notebooks/04_race_prediction.ipynb |