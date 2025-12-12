"""
Auto ML Engine - Automatic Machine Learning Pipeline
=====================================================

Core ML automation engine with intelligent model selection.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score, mean_absolute_error, classification_report
)


class AutoMLEngine:
    """
    Automatic Machine Learning Engine.
    
    Automatically selects, trains, and tunes ML models.
    """
    
    def __init__(self, problem_type: str = 'auto'):
        """
        Initialize AutoML engine.
        
        Parameters
        ----------
        problem_type : str
            'auto', 'classification', 'regression'
        """
        self.problem_type = problem_type
        self.best_model = None
        self.best_score = -np.inf
        self.results = {}
        self.scaler = StandardScaler()
        self.label_encoder = None
        
    def fit(self, X: pd.DataFrame, y: pd.Series,
            test_size: float = 0.2,
            cv_folds: int = 5,
            tune_hyperparameters: bool = True,
            verbose: bool = True) -> Dict[str, Any]:
        """
        Automatically train and select best model.
        
        Parameters
        ----------
        X : DataFrame
            Features
        y : Series
            Target
        test_size : float
            Test set proportion
        cv_folds : int
            Cross-validation folds
        tune_hyperparameters : bool
            Enable hyperparameter tuning
        verbose : bool
            Print progress
        
        Returns
        -------
        dict
            Training results and metrics
        """
        # Detect problem type if auto
        if self.problem_type == 'auto':
            self.problem_type = self._detect_problem_type(y)
        
        if verbose:
            print(f"\n🤖 AutoML Engine Starting...")
            print(f"   Problem Type: {self.problem_type}")
            print(f"   Training samples: {len(X)}")
            print(f"   Features: {X.shape[1]}")
        
        # Prepare data
        X_processed, y_processed = self._preprocess(X, y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y_processed, test_size=test_size, random_state=42
        )
        
        # Get candidate models
        models = self._get_candidate_models()
        
        if verbose:
            print(f"\n🔍 Evaluating {len(models)} candidate models...")
        
        # Train and evaluate models
        for name, model in models.items():
            if verbose:
                print(f"   Testing {name}...", end=' ')
            
            try:
                # Train model
                model.fit(X_train, y_train)
                
                # Cross-validation score
                cv_scores = cross_val_score(model, X_train, y_train, cv=cv_folds)
                mean_cv_score = cv_scores.mean()
                
                # Test score
                test_score = model.score(X_test, y_test)
                
                # Store results
                self.results[name] = {
                    'model': model,
                    'cv_score': mean_cv_score,
                    'cv_std': cv_scores.std(),
                    'test_score': test_score,
                }
                
                if verbose:
                    print(f"CV: {mean_cv_score:.4f}, Test: {test_score:.4f}")
                
                # Update best model
                if mean_cv_score > self.best_score:
                    self.best_score = mean_cv_score
                    self.best_model = model
                    self.best_model_name = name
                    
            except Exception as e:
                if verbose:
                    print(f"Failed: {str(e)[:50]}")
                continue
        
        if verbose:
            print(f"\n✓ Best Model: {self.best_model_name} (CV Score: {self.best_score:.4f})")
        
        # Hyperparameter tuning
        if tune_hyperparameters and self.best_model is not None:
            if verbose:
                print(f"\n🔧 Tuning hyperparameters...")
            self._tune_hyperparameters(X_train, y_train, verbose)
        
        # Final evaluation
        final_results = self._final_evaluation(X_test, y_test, verbose)
        
        return final_results
    
    def _detect_problem_type(self, y: pd.Series) -> str:
        """Detect if regression or classification."""
        unique_ratio = y.nunique() / len(y)
        
        if y.dtype in ['int64', 'float64'] and unique_ratio > 0.05:
            return 'regression'
        else:
            return 'classification'
    
    def _preprocess(self, X: pd.DataFrame, y: pd.Series) -> Tuple:
        """Preprocess features and target."""
        X_processed = X.copy()
        y_processed = y.copy()
        
        # Encode categorical features
        for col in X_processed.columns:
            if X_processed[col].dtype == 'object':
                le = LabelEncoder()
                X_processed[col] = le.fit_transform(X_processed[col].astype(str))
        
        # Scale features
        X_processed = pd.DataFrame(
            self.scaler.fit_transform(X_processed),
            columns=X_processed.columns,
            index=X_processed.index
        )
        
        # Encode target if classification
        if self.problem_type == 'classification':
            if y_processed.dtype == 'object':
                self.label_encoder = LabelEncoder()
                y_processed = pd.Series(
                    self.label_encoder.fit_transform(y_processed),
                    index=y_processed.index
                )
        
        return X_processed, y_processed
    
    def _get_candidate_models(self) -> Dict:
        """Get candidate models based on problem type."""
        if self.problem_type == 'classification':
            models = {
                'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
                'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
                'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
                'DecisionTree': DecisionTreeClassifier(random_state=42),
                'KNeighbors': KNeighborsClassifier(n_neighbors=5),
                'NaiveBayes': GaussianNB(),
            }
        else:  # regression
            models = {
                'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
                'GradientBoosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'LinearRegression': LinearRegression(),
                'Ridge': Ridge(random_state=42),
                'Lasso': Lasso(random_state=42),
                'DecisionTree': DecisionTreeRegressor(random_state=42),
                'KNeighbors': KNeighborsRegressor(n_neighbors=5),
            }
        
        return models
    
    def _tune_hyperparameters(self, X_train, y_train, verbose: bool):
        """Tune hyperparameters of best model."""
        param_grids = self._get_param_grids()
        
        if self.best_model_name not in param_grids:
            if verbose:
                print(f"   No hyperparameter grid for {self.best_model_name}")
            return
        
        param_grid = param_grids[self.best_model_name]
        
        try:
            grid_search = GridSearchCV(
                self.best_model,
                param_grid,
                cv=3,
                n_jobs=-1,
                verbose=0
            )
            grid_search.fit(X_train, y_train)
            
            self.best_model = grid_search.best_estimator_
            self.best_score = grid_search.best_score_
            
            if verbose:
                print(f"   Tuned CV Score: {self.best_score:.4f}")
                print(f"   Best params: {grid_search.best_params_}")
                
        except Exception as e:
            if verbose:
                print(f"   Tuning failed: {str(e)[:50]}")
    
    def _get_param_grids(self) -> Dict:
        """Get hyperparameter grids for tuning."""
        if self.problem_type == 'classification':
            return {
                'RandomForest': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [10, 20, None],
                    'min_samples_split': [2, 5],
                },
                'GradientBoosting': {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5],
                },
                'LogisticRegression': {
                    'C': [0.1, 1.0, 10.0],
                    'penalty': ['l2'],
                },
            }
        else:
            return {
                'RandomForest': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [10, 20, None],
                    'min_samples_split': [2, 5],
                },
                'GradientBoosting': {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5],
                },
                'Ridge': {
                    'alpha': [0.1, 1.0, 10.0],
                },
                'Lasso': {
                    'alpha': [0.1, 1.0, 10.0],
                },
            }
    
    def _final_evaluation(self, X_test, y_test, verbose: bool) -> Dict:
        """Final model evaluation."""
        y_pred = self.best_model.predict(X_test)
        
        results = {
            'best_model': self.best_model,
            'best_model_name': self.best_model_name,
            'cv_score': self.best_score,
            'predictions': y_pred,
            'actual': y_test,
        }
        
        if self.problem_type == 'classification':
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            results['metrics'] = {
                'accuracy': float(accuracy),
                'precision': float(precision),
                'recall': float(recall),
                'f1': float(f1),
            }
            
            if verbose:
                print(f"\n📊 Final Evaluation:")
                print(f"   Accuracy: {accuracy:.4f}")
                print(f"   Precision: {precision:.4f}")
                print(f"   Recall: {recall:.4f}")
                print(f"   F1-Score: {f1:.4f}")
        
        else:  # regression
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
                print(f"\n📊 Final Evaluation:")
                print(f"   RMSE: {rmse:.4f}")
                print(f"   MAE: {mae:.4f}")
                print(f"   R²: {r2:.4f}")
        
        return results
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions with best model."""
        if self.best_model is None:
            raise ValueError("No model trained. Use fit() first.")
        
        # Preprocess
        X_processed = X.copy()
        for col in X_processed.columns:
            if X_processed[col].dtype == 'object':
                le = LabelEncoder()
                X_processed[col] = le.fit_transform(X_processed[col].astype(str))
        
        X_processed = self.scaler.transform(X_processed)
        
        # Predict
        predictions = self.best_model.predict(X_processed)
        
        # Decode if classification
        if self.label_encoder is not None:
            predictions = self.label_encoder.inverse_transform(predictions)
        
        return predictions
