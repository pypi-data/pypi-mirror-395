"""
Auto DL Engine - Automatic Deep Learning Pipeline
==================================================

Core deep learning automation with PyTorch.
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset
from typing import Dict, Any, Optional, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


class AutoDLEngine:
    """
    Automatic Deep Learning Engine.
    
    Automatically builds and trains deep neural networks.
    """
    
    def __init__(self, task: str = 'auto', architecture: str = 'auto'):
        """
        Initialize AutoDL engine.
        
        Parameters
        ----------
        task : str
            'auto', 'classification', 'regression'
        architecture : str
            'auto', 'mlp', 'deep', 'wide'
        """
        self.task = task
        self.architecture = architecture
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.scaler = StandardScaler()
        self.label_encoder = None
        self.history = {}
        
    def fit(self, X: pd.DataFrame, y: pd.Series,
            epochs: int = 50,
            batch_size: int = 32,
            learning_rate: float = 0.001,
            validation_split: float = 0.2,
            early_stopping_patience: int = 10,
            verbose: bool = True) -> Dict[str, Any]:
        """
        Train deep learning model.
        
        Parameters
        ----------
        X : DataFrame
            Features
        y : Series
            Target
        epochs : int
            Training epochs
        batch_size : int
            Batch size
        learning_rate : float
            Learning rate
        validation_split : float
            Validation set proportion
        early_stopping_patience : int
            Early stopping patience
        verbose : bool
            Print progress
        
        Returns
        -------
        dict
            Training results
        """
        # Detect task if auto
        if self.task == 'auto':
            self.task = self._detect_task(y)
        
        if verbose:
            print(f"\n🧠 AutoDL Engine Starting...")
            print(f"   Task: {self.task}")
            print(f"   Device: {self.device}")
            print(f"   Training samples: {len(X)}")
        
        # Prepare data
        X_train, X_val, y_train, y_val, num_classes = self._prepare_data(
            X, y, validation_split
        )
        
        # Build model
        input_size = X_train.shape[1]
        self.model = self._build_model(input_size, num_classes)
        self.model = self.model.to(self.device)
        
        if verbose:
            total_params = sum(p.numel() for p in self.model.parameters())
            print(f"   Model parameters: {total_params:,}")
            print(f"   Epochs: {epochs}")
        
        # Setup training
        criterion = self._get_criterion()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Data loaders
        train_dataset = TensorDataset(X_train, y_train)
        val_dataset = TensorDataset(X_val, y_val)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size)
        
        # Training loop
        best_val_loss = float('inf')
        patience_counter = 0
        
        self.history = {
            'train_loss': [],
            'val_loss': [],
            'train_metric': [],
            'val_metric': [],
        }
        
        for epoch in range(epochs):
            # Training
            train_loss, train_metric = self._train_epoch(
                train_loader, optimizer, criterion
            )
            
            # Validation
            val_loss, val_metric = self._validate(val_loader, criterion)
            
            # Record history
            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_loss)
            self.history['train_metric'].append(train_metric)
            self.history['val_metric'].append(val_metric)
            
            # Print progress
            if verbose and (epoch + 1) % 10 == 0:
                print(f"   Epoch {epoch+1}/{epochs} - "
                      f"Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f} - "
                      f"Metric: {train_metric:.4f} - Val Metric: {val_metric:.4f}")
            
            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                # Save best model
                self.best_state = self.model.state_dict()
            else:
                patience_counter += 1
                if patience_counter >= early_stopping_patience:
                    if verbose:
                        print(f"   Early stopping at epoch {epoch+1}")
                    break
        
        # Load best model
        self.model.load_state_dict(self.best_state)
        
        # Final evaluation
        results = self._final_evaluation(X_val, y_val, verbose)
        results['history'] = self.history
        results['model'] = self.model
        
        return results
    
    def _detect_task(self, y: pd.Series) -> str:
        """Detect task type."""
        unique_ratio = y.nunique() / len(y)
        
        if y.dtype in ['int64', 'float64'] and unique_ratio > 0.05:
            return 'regression'
        else:
            return 'classification'
    
    def _prepare_data(self, X: pd.DataFrame, y: pd.Series,
                     validation_split: float) -> Tuple:
        """Prepare data for training."""
        X_processed = X.copy()
        y_processed = y.copy()
        
        # Encode categorical features
        for col in X_processed.columns:
            if X_processed[col].dtype == 'object':
                le = LabelEncoder()
                X_processed[col] = le.fit_transform(X_processed[col].astype(str))
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_processed)
        
        # Handle target
        num_classes = 1
        if self.task == 'classification':
            if y_processed.dtype == 'object':
                self.label_encoder = LabelEncoder()
                y_processed = self.label_encoder.fit_transform(y_processed)
            num_classes = len(np.unique(y_processed))
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X_scaled, y_processed, test_size=validation_split, random_state=42
        )
        
        # Convert to tensors
        X_train = torch.FloatTensor(X_train)
        X_val = torch.FloatTensor(X_val)
        
        if self.task == 'classification':
            y_train = torch.LongTensor(y_train)
            y_val = torch.LongTensor(y_val)
        else:
            y_train = torch.FloatTensor(y_train.values if hasattr(y_train, 'values') else y_train).reshape(-1, 1)
            y_val = torch.FloatTensor(y_val.values if hasattr(y_val, 'values') else y_val).reshape(-1, 1)
        
        return X_train, X_val, y_train, y_val, num_classes
    
    def _build_model(self, input_size: int, num_classes: int) -> nn.Module:
        """Build deep neural network."""
        
        if self.architecture == 'auto':
            # Auto-select based on input size
            if input_size < 10:
                self.architecture = 'mlp'
            elif input_size < 50:
                self.architecture = 'deep'
            else:
                self.architecture = 'wide'
        
        if self.architecture == 'mlp':
            # Simple MLP
            model = self._build_mlp(input_size, num_classes)
        elif self.architecture == 'deep':
            # Deep network
            model = self._build_deep(input_size, num_classes)
        else:  # wide
            # Wide network
            model = self._build_wide(input_size, num_classes)
        
        return model
    
    def _build_mlp(self, input_size: int, num_classes: int) -> nn.Module:
        """Build simple MLP."""
        class MLP(nn.Module):
            def __init__(self, input_size, num_classes, task):
                super(MLP, self).__init__()
                self.task = task
                
                self.fc1 = nn.Linear(input_size, 64)
                self.bn1 = nn.BatchNorm1d(64)
                self.dropout1 = nn.Dropout(0.3)
                
                self.fc2 = nn.Linear(64, 32)
                self.bn2 = nn.BatchNorm1d(32)
                
                if task == 'classification':
                    self.output = nn.Linear(32, num_classes)
                else:
                    self.output = nn.Linear(32, 1)
                
                self.relu = nn.ReLU()
            
            def forward(self, x):
                x = self.relu(self.bn1(self.fc1(x)))
                x = self.dropout1(x)
                x = self.relu(self.bn2(self.fc2(x)))
                x = self.output(x)
                return x
        
        return MLP(input_size, num_classes, self.task)
    
    def _build_deep(self, input_size: int, num_classes: int) -> nn.Module:
        """Build deep network."""
        class DeepNet(nn.Module):
            def __init__(self, input_size, num_classes, task):
                super(DeepNet, self).__init__()
                self.task = task
                
                self.fc1 = nn.Linear(input_size, 128)
                self.bn1 = nn.BatchNorm1d(128)
                self.dropout1 = nn.Dropout(0.3)
                
                self.fc2 = nn.Linear(128, 64)
                self.bn2 = nn.BatchNorm1d(64)
                self.dropout2 = nn.Dropout(0.2)
                
                self.fc3 = nn.Linear(64, 32)
                self.bn3 = nn.BatchNorm1d(32)
                
                if task == 'classification':
                    self.output = nn.Linear(32, num_classes)
                else:
                    self.output = nn.Linear(32, 1)
                
                self.relu = nn.ReLU()
            
            def forward(self, x):
                x = self.relu(self.bn1(self.fc1(x)))
                x = self.dropout1(x)
                x = self.relu(self.bn2(self.fc2(x)))
                x = self.dropout2(x)
                x = self.relu(self.bn3(self.fc3(x)))
                x = self.output(x)
                return x
        
        return DeepNet(input_size, num_classes, self.task)
    
    def _build_wide(self, input_size: int, num_classes: int) -> nn.Module:
        """Build wide network."""
        class WideNet(nn.Module):
            def __init__(self, input_size, num_classes, task):
                super(WideNet, self).__init__()
                self.task = task
                
                self.fc1 = nn.Linear(input_size, 256)
                self.bn1 = nn.BatchNorm1d(256)
                self.dropout1 = nn.Dropout(0.4)
                
                self.fc2 = nn.Linear(256, 128)
                self.bn2 = nn.BatchNorm1d(128)
                self.dropout2 = nn.Dropout(0.3)
                
                self.fc3 = nn.Linear(128, 64)
                self.bn3 = nn.BatchNorm1d(64)
                
                if task == 'classification':
                    self.output = nn.Linear(64, num_classes)
                else:
                    self.output = nn.Linear(64, 1)
                
                self.relu = nn.ReLU()
            
            def forward(self, x):
                x = self.relu(self.bn1(self.fc1(x)))
                x = self.dropout1(x)
                x = self.relu(self.bn2(self.fc2(x)))
                x = self.dropout2(x)
                x = self.relu(self.bn3(self.fc3(x)))
                x = self.output(x)
                return x
        
        return WideNet(input_size, num_classes, self.task)
    
    def _get_criterion(self):
        """Get loss function."""
        if self.task == 'classification':
            return nn.CrossEntropyLoss()
        else:
            return nn.MSELoss()
    
    def _train_epoch(self, train_loader, optimizer, criterion):
        """Train one epoch."""
        self.model.train()
        total_loss = 0.0
        total_metric = 0.0
        
        for batch_X, batch_y in train_loader:
            batch_X = batch_X.to(self.device)
            batch_y = batch_y.to(self.device)
            
            optimizer.zero_grad()
            outputs = self.model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            # Calculate metric
            if self.task == 'classification':
                _, predicted = torch.max(outputs, 1)
                total_metric += (predicted == batch_y).float().mean().item()
            else:
                total_metric += loss.item()  # Use loss as metric for regression
        
        avg_loss = total_loss / len(train_loader)
        avg_metric = total_metric / len(train_loader)
        
        return avg_loss, avg_metric
    
    def _validate(self, val_loader, criterion):
        """Validate model."""
        self.model.eval()
        total_loss = 0.0
        total_metric = 0.0
        
        with torch.no_grad():
            for batch_X, batch_y in val_loader:
                batch_X = batch_X.to(self.device)
                batch_y = batch_y.to(self.device)
                
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                
                total_loss += loss.item()
                
                if self.task == 'classification':
                    _, predicted = torch.max(outputs, 1)
                    total_metric += (predicted == batch_y).float().mean().item()
                else:
                    total_metric += loss.item()
        
        avg_loss = total_loss / len(val_loader)
        avg_metric = total_metric / len(val_loader)
        
        return avg_loss, avg_metric
    
    def _final_evaluation(self, X_val, y_val, verbose: bool) -> Dict:
        """Final evaluation."""
        self.model.eval()
        
        with torch.no_grad():
            X_val_device = X_val.to(self.device)
            outputs = self.model(X_val_device)
            
            if self.task == 'classification':
                _, predicted = torch.max(outputs, 1)
                accuracy = (predicted == y_val.to(self.device)).float().mean().item()
                
                results = {
                    'metrics': {
                        'accuracy': float(accuracy),
                    }
                }
                
                if verbose:
                    print(f"\n📊 Final Evaluation:")
                    print(f"   Accuracy: {accuracy:.4f}")
            
            else:  # regression
                mse = nn.MSELoss()(outputs, y_val.to(self.device)).item()
                rmse = np.sqrt(mse)
                
                results = {
                    'metrics': {
                        'mse': float(mse),
                        'rmse': float(rmse),
                    }
                }
                
                if verbose:
                    print(f"\n📊 Final Evaluation:")
                    print(f"   RMSE: {rmse:.4f}")
        
        return results
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        if self.model is None:
            raise ValueError("No model trained. Use fit() first.")
        
        self.model.eval()
        
        # Preprocess
        X_processed = X.copy()
        for col in X_processed.columns:
            if X_processed[col].dtype == 'object':
                le = LabelEncoder()
                X_processed[col] = le.fit_transform(X_processed[col].astype(str))
        
        X_scaled = self.scaler.transform(X_processed)
        X_tensor = torch.FloatTensor(X_scaled).to(self.device)
        
        # Predict
        with torch.no_grad():
            outputs = self.model(X_tensor)
            
            if self.task == 'classification':
                _, predictions = torch.max(outputs, 1)
                predictions = predictions.cpu().numpy()
                
                if self.label_encoder is not None:
                    predictions = self.label_encoder.inverse_transform(predictions)
            else:
                predictions = outputs.cpu().numpy().flatten()
        
        return predictions
