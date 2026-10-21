import pandas as pd
import numpy as np
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def load_data(filepath="../data/processed/cleaned_laps.csv"):
    """Loads cleaned race telemetry dataset from local project path."""
    return pd.read_csv(filepath)

def prepare_features(df):
    """Filters dataset to numerical telemetry features and live lap position target."""
    features = ['LapNumber', 'Stint', 'TyreLife', 'LapTime_s', 'AirTemp', 'TrackTemp']
    target = 'Position'
    
    clean_df = df[features + [target, 'EventName']].dropna()
    X = clean_df[features]
    y = clean_df[target]
    groups = clean_df['EventName']
    
    return X, y, groups, features

def train_race_model_group_split(X, y, groups):
    """Trains Random Forest using Group-based split to prevent cross-lap data leakage."""
    logo = LeaveOneGroupOut()
    train_idx, test_idx = next(logo.split(X, y, groups))
    
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    metrics = {
        'MAE': mean_absolute_error(y_test, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
        'R2': r2_score(y_test, y_pred)
    }
    
    return model, metrics
