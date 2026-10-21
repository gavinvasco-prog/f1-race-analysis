import pandas as pd
import numpy as np
from sklearn.model_selection import LeaveOneGroupOut, cross_val_predict
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def load_data(filepath="../data/processed/cleaned_laps.csv"):
    """Loads cleaned race telemetry dataset from local project path."""
    return pd.read_csv(filepath)

def prepare_features(df):
    """Filters dataset to numerical telemetry features and live lap position target."""
    features = ['LapNumber', 'Stint', 'TyreLife', 'LapTime_s', 'AirTemp', 'TrackTemp']
    target = 'Position'
    
    # Using 'Race' column instead of 'EventName' to match processed CSV schema
    clean_df = df[features + [target, 'Race']].dropna()
    X = clean_df[features]
    y = clean_df[target]
    groups = clean_df['Race']
    
    return X, y, groups, features

def train_race_model_group_split(X, y, groups):
    """Evaluates Random Forest across all races using LeaveOneGroupOut cross-validation to prevent leakage."""
    logo = LeaveOneGroupOut()
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Generate predictions across all race groups via cross-validation
    y_pred = cross_val_predict(model, X, y, groups=groups, cv=logo)
    
    # Fit final model on full dataset for downstream feature analysis
    model.fit(X, y)
    
    metrics = {
        'MAE': mean_absolute_error(y, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y, y_pred)),
        'R2': r2_score(y, y_pred)
    }
    
    return model, metrics
