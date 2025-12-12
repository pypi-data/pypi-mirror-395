"""
DL Agent - Automatic Deep Learning
===================================

Automatically builds and trains deep learning models.
"""

import pandas as pd
import numpy as np
from typing import Union, Optional, List
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from autodatamind.core.reader import read_data
from autodatamind.core.cleaner import autoclean


def auto_deep(data: Union[str, pd.DataFrame],
              target: str,
              task: str = 'auto',
              epochs: int = 50,
              batch_size: int = 32,
              learning_rate: float = 0.001,
              auto_clean: bool = True,
              save_model: bool = True,
              model_path: Optional[str] = None,
              verbose: bool = True) -> dict:
    """
    Automatically build and train deep learning model.
    
    Parameters
    ----------
    data : str or DataFrame
        Path to file or DataFrame
    target : str
        Target column name
    task : str
        Task type: 'auto', 'classification', 'regression'
    epochs : int
        Number of training epochs
    batch_size : int
        Batch size
    learning_rate : float
        Learning rate
    auto_clean : bool
        Automatically clean data
    save_model : bool
        Save trained model
    model_path : str, optional
        Custom model save path
    verbose : bool
        Print training progress
    
    Returns
    -------
    dict
        Training results with model and metrics
    
    Examples
    --------
    >>> import autodatamind as adm
    >>> result = adm.auto_deep("data.csv", target="price", task="regression")
    >>> result = adm.auto_deep(df, target="category", epochs=100)
    """
    # Load data
    df = read_data(data)
    
    # Auto-clean
    if auto_clean:
        df = autoclean(df, verbose=False)
    
    # Validate target
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found")
    
    # Auto-detect task
    if task == 'auto':
        unique_ratio = df[target].nunique() / len(df)
        task = 'classification' if unique_ratio < 0.05 else 'regression'
    
    if verbose:
        print(f"\n🧠 AutoDeep Starting...")
        print(f"   Task: {task}")
        print(f"   Target: {target}")
        print(f"   Dataset: {len(df)} rows × {len(df.columns)} columns")
        print(f"   Epochs: {epochs}")
    
    # Prepare data
    X_train, X_test, y_train, y_test, preprocessor, num_classes = _prepare_deep_data(
        df, target, task, verbose
    )
    
    # Create model
    input_size = X_train.shape[1]
    model = _create_deep_model(input_size, num_classes, task)
    
    if verbose:
        print(f"   Model architecture: {input_size}→128→64→32→{num_classes if task == 'classification' else 1}")
    
    # Train model
    history = _train_deep_model(
        model, X_train, y_train, X_test, y_test,
        epochs, batch_size, learning_rate, task, verbose
    )
    
    # Evaluate
    results = _evaluate_deep_model(model, X_test, y_test, task, verbose)
    
    # Add info
    results['model'] = model
    results['history'] = history
    results['task'] = task
    results['preprocessor'] = preprocessor
    
    # Save model
    if save_model:
        if model_path is None:
            model_path = f"autodatamind_deep_{target}.pth"
        
        torch.save({
            'model_state': model.state_dict(),
            'preprocessor': preprocessor,
            'task': task,
            'input_size': input_size,
            'num_classes': num_classes,
        }, model_path)
        
        if verbose:
            print(f"\n✓ Model saved: {model_path}")
    
    return results


def _prepare_deep_data(df: pd.DataFrame, target: str, task: str, verbose: bool) -> tuple:
    """Prepare data for deep learning."""
    # Separate features and target
    X = df.drop(columns=[target]).copy()
    y = df[target].copy()
    
    # Encode categorical features
    encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object' or X[col].dtype.name == 'category':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le
    
    # Handle target
    target_encoder = None
    num_classes = 1
    
    if task == 'classification':
        if y.dtype == 'object' or y.dtype.name == 'category':
            target_encoder = LabelEncoder()
            y = target_encoder.fit_transform(y)
        num_classes = len(np.unique(y))
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    
    # Convert to tensors
    X_train = torch.FloatTensor(X_train)
    X_test = torch.FloatTensor(X_test)
    
    if task == 'classification':
        y_train = torch.LongTensor(y_train)
        y_test = torch.LongTensor(y_test)
    else:
        y_train = torch.FloatTensor(y_train.values).reshape(-1, 1)
        y_test = torch.FloatTensor(y_test.values).reshape(-1, 1)
    
    if verbose:
        print(f"   Train set: {len(X_train)} samples")
        print(f"   Test set: {len(X_test)} samples")
        if task == 'classification':
            print(f"   Classes: {num_classes}")
    
    preprocessor = {
        'encoders': encoders,
        'target_encoder': target_encoder,
        'scaler': scaler,
    }
    
    return X_train, X_test, y_train, y_test, preprocessor, num_classes


def _create_deep_model(input_size: int, num_classes: int, task: str) -> nn.Module:
    """Create deep neural network."""
    
    class DeepNet(nn.Module):
        def __init__(self, input_size, num_classes, task):
            super(DeepNet, self).__init__()
            self.task = task
            
            # Deep architecture
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
    
    model = DeepNet(input_size, num_classes, task)
    return model


def _train_deep_model(model, X_train, y_train, X_test, y_test,
                      epochs, batch_size, learning_rate, task, verbose):
    """Train deep learning model."""
    # Setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    # Loss and optimizer
    if task == 'classification':
        criterion = nn.CrossEntropyLoss()
    else:
        criterion = nn.MSELoss()
    
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Data loaders
    train_dataset = TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # Training history
    history = {
        'train_loss': [],
        'test_loss': [],
    }
    
    # Training loop
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        history['train_loss'].append(train_loss)
        
        # Validation
        model.eval()
        with torch.no_grad():
            X_test_device = X_test.to(device)
            y_test_device = y_test.to(device)
            test_outputs = model(X_test_device)
            test_loss = criterion(test_outputs, y_test_device).item()
            history['test_loss'].append(test_loss)
        
        # Print progress
        if verbose and (epoch + 1) % 10 == 0:
            print(f"   Epoch {epoch+1}/{epochs} - Loss: {train_loss:.4f} - Val Loss: {test_loss:.4f}")
    
    return history


def _evaluate_deep_model(model, X_test, y_test, task, verbose):
    """Evaluate deep learning model."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()
    
    with torch.no_grad():
        X_test_device = X_test.to(device)
        outputs = model(X_test_device)
        
        if task == 'classification':
            _, predicted = torch.max(outputs, 1)
            accuracy = (predicted == y_test.to(device)).float().mean().item()
            
            results = {
                'metrics': {
                    'accuracy': float(accuracy),
                }
            }
            
            if verbose:
                print(f"\n📊 Evaluation Results:")
                print(f"   Accuracy: {accuracy:.4f}")
        
        else:  # regression
            mse = nn.MSELoss()(outputs, y_test.to(device)).item()
            rmse = np.sqrt(mse)
            
            results = {
                'metrics': {
                    'mse': float(mse),
                    'rmse': float(rmse),
                }
            }
            
            if verbose:
                print(f"\n📊 Evaluation Results:")
                print(f"   RMSE: {rmse:.4f}")
    
    return results


class DLAgent:
    """
    Deep Learning Agent for automatic neural networks.
    """
    
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.task = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def train(self, data: Union[str, pd.DataFrame], target: str, **kwargs) -> dict:
        """Train deep learning model automatically."""
        results = auto_deep(data, target, **kwargs)
        
        self.model = results['model']
        self.preprocessor = results['preprocessor']
        self.task = results['task']
        
        return results
    
    def predict(self, data: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Make predictions."""
        if self.model is None:
            raise ValueError("No model trained. Use train() first.")
        
        self.model.eval()
        
        # Preprocess
        if isinstance(data, pd.DataFrame):
            X = data.copy()
            for col, encoder in self.preprocessor['encoders'].items():
                if col in X.columns:
                    X[col] = encoder.transform(X[col].astype(str))
            
            X = self.preprocessor['scaler'].transform(X)
        else:
            X = data
        
        # Convert to tensor
        X_tensor = torch.FloatTensor(X).to(self.device)
        
        # Predict
        with torch.no_grad():
            outputs = self.model(X_tensor)
            
            if self.task == 'classification':
                _, predictions = torch.max(outputs, 1)
                predictions = predictions.cpu().numpy()
                
                # Decode
                if self.preprocessor['target_encoder'] is not None:
                    predictions = self.preprocessor['target_encoder'].inverse_transform(predictions)
            else:
                predictions = outputs.cpu().numpy().flatten()
        
        return predictions
