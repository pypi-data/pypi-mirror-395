"""
ML Agent - Automatic Machine Learning
======================================

Automatically trains ML models without any ML knowledge required.
"""

import pandas as pd
import numpy as np
from typing import Union, Optional, Any
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             mean_squared_error, r2_score, mean_absolute_error)
import joblib
from autodatamind.core.reader import read_data
from autodatamind.core.cleaner import autoclean
from autodatamind.core.utils import detect_problem_type, get_numeric_columns, get_categorical_columns


def autotrain(data: Union[str, pd.DataFrame],
              target: str,
              test_size: float = 0.2,
              auto_clean: bool = True,
              save_model: bool = True,
              model_path: Optional[str] = None,
              verbose: bool = True) -> dict:
    """
    Automatically train ML model.
    
    Parameters
    ----------
    data : str or DataFrame
        Path to file or DataFrame
    target : str
        Target column name
    test_size : float
        Test set size (0.0 to 1.0)
    auto_clean : bool
        Automatically clean data
    save_model : bool
        Save trained model to file
    model_path : str, optional
        Custom model save path
    verbose : bool
        Print training progress
    
    Returns
    -------
    dict
        Training results with model, metrics, and predictions
    
    Examples
    --------
    >>> import autodatamind as adm
    >>> result = adm.autotrain("sales.csv", target="revenue")
    >>> result = adm.autotrain(df, target="churn", save_model=True)
    """
    # Load data
    df = read_data(data)
    
    # Auto-clean
    if auto_clean:
        df = autoclean(df, verbose=False)
    
    # Validate target
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in data")
    
    # Detect problem type
    problem_type = detect_problem_type(df, target)
    
    if verbose:
        print(f"\n🤖 AutoTrain Starting...")
        print(f"   Problem Type: {problem_type}")
        print(f"   Target: {target}")
        print(f"   Dataset: {len(df)} rows × {len(df.columns)} columns")
    
    # Prepare data
    X, y, preprocessor = _prepare_data(df, target, problem_type)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    if verbose:
        print(f"   Train set: {len(X_train)} rows")
        print(f"   Test set: {len(X_test)} rows")
    
    # Select and train model
    model = _select_and_train_model(X_train, y_train, problem_type, verbose)
    
    # Evaluate
    results = _evaluate_model(model, X_test, y_test, problem_type, verbose)
    
    # Add additional info
    results['model'] = model
    results['problem_type'] = problem_type
    results['preprocessor'] = preprocessor
    results['feature_names'] = list(X.columns)
    results['target_name'] = target
    
    # Save model
    if save_model:
        if model_path is None:
            model_path = f"autodatamind_model_{target}.joblib"
        
        joblib.dump({
            'model': model,
            'preprocessor': preprocessor,
            'problem_type': problem_type,
            'feature_names': list(X.columns),
        }, model_path)
        
        if verbose:
            print(f"\n✓ Model saved: {model_path}")
    
    return results


def _prepare_data(df: pd.DataFrame, target: str, problem_type: str) -> tuple:
    """Prepare data for training."""
    # Separate features and target
    X = df.drop(columns=[target])
    y = df[target]
    
    # Get column types
    numeric_cols = get_numeric_columns(X)
    categorical_cols = get_categorical_columns(X)
    
    # Encode categorical features
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
    
    # Encode target if classification
    target_encoder = None
    if problem_type in ['binary_classification', 'multiclass_classification']:
        if y.dtype == 'object' or y.dtype.name == 'category':
            target_encoder = LabelEncoder()
            y = target_encoder.fit_transform(y)
    
    # Scale features
    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
    
    # Create preprocessor object
    preprocessor = {
        'encoders': encoders,
        'target_encoder': target_encoder,
        'scaler': scaler,
        'numeric_cols': numeric_cols,
        'categorical_cols': categorical_cols,
    }
    
    return X, y, preprocessor


def _select_and_train_model(X_train, y_train, problem_type: str, verbose: bool):
    """Select best model and train."""
    if verbose:
        print(f"\n🎯 Training model...")
    
    if problem_type == 'regression':
        # Try RandomForest and LinearRegression
        models = {
            'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
            'LinearRegression': LinearRegression(),
        }
    elif problem_type == 'binary_classification':
        models = {
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
        }
    else:  # multiclass_classification
        models = {
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000, multi_class='ovr'),
        }
    
    # Train and select best
    best_model = None
    best_score = -np.inf
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        score = model.score(X_train, y_train)
        
        if score > best_score:
            best_score = score
            best_model = model
            best_name = name
    
    if verbose:
        print(f"   Selected: {best_name} (score: {best_score:.4f})")
    
    return best_model


def _evaluate_model(model, X_test, y_test, problem_type: str, verbose: bool) -> dict:
    """Evaluate trained model."""
    y_pred = model.predict(X_test)
    
    results = {
        'predictions': y_pred,
        'actual': y_test,
    }
    
    if problem_type == 'regression':
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results['metrics'] = {
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2),
        }
        
        if verbose:
            print(f"\n📊 Evaluation Results:")
            print(f"   RMSE: {rmse:.4f}")
            print(f"   MAE: {mae:.4f}")
            print(f"   R²: {r2:.4f}")
    
    else:  # classification
        accuracy = accuracy_score(y_test, y_pred)
        
        # Handle binary vs multiclass
        average = 'binary' if problem_type == 'binary_classification' else 'weighted'
        
        precision = precision_score(y_test, y_pred, average=average, zero_division=0)
        recall = recall_score(y_test, y_pred, average=average, zero_division=0)
        f1 = f1_score(y_test, y_pred, average=average, zero_division=0)
        
        results['metrics'] = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1),
        }
        
        if verbose:
            print(f"\n📊 Evaluation Results:")
            print(f"   Accuracy: {accuracy:.4f}")
            print(f"   Precision: {precision:.4f}")
            print(f"   Recall: {recall:.4f}")
            print(f"   F1-Score: {f1:.4f}")
    
    return results


class MLAgent:
    """
    ML Agent for automatic machine learning.
    """
    
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.problem_type = None
    
    def train(self, data: Union[str, pd.DataFrame], target: str, **kwargs) -> dict:
        """Train model automatically."""
        results = autotrain(data, target, **kwargs)
        
        self.model = results['model']
        self.preprocessor = results['preprocessor']
        self.problem_type = results['problem_type']
        
        return results
    
    def predict(self, data: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Make predictions."""
        if self.model is None:
            raise ValueError("No model trained. Use train() first.")
        
        # Preprocess if needed
        if isinstance(data, pd.DataFrame):
            X = data.copy()
            # Apply preprocessing
            for col, encoder in self.preprocessor['encoders'].items():
                if col in X.columns:
                    X[col] = encoder.transform(X[col].astype(str))
            
            numeric_cols = self.preprocessor['numeric_cols']
            X[numeric_cols] = self.preprocessor['scaler'].transform(X[numeric_cols])
        else:
            X = data
        
        predictions = self.model.predict(X)
        
        # Decode if classification
        if self.preprocessor['target_encoder'] is not None:
            predictions = self.preprocessor['target_encoder'].inverse_transform(predictions)
        
        return predictions
