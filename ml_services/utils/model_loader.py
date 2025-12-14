"""
Model Loader Utility
Handles loading and caching of ML models
"""

import os
import joblib
from typing import Any, Optional
from pathlib import Path

# Cache for loaded models
_model_cache: dict[str, Any] = {}


class ModelLoader:
    """
    Utility class for loading ML models, scalers, and encoders
    """
    
    MODELS_DIR = Path(__file__).parent.parent / "models"
    
    @staticmethod
    def load_model(model_name: str) -> Any:
        """
        Load a trained model from disk (with caching)
        """
        if model_name in _model_cache:
            return _model_cache[model_name]
        
        model_path = ModelLoader.MODELS_DIR / model_name / "model.pkl"
        
        if not model_path.exists():
            # Return a dummy model for development
            # In production, this should raise an error or load a default model
            print(f"Warning: Model {model_name} not found. Using dummy model.")
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            # Train with dummy data
            import numpy as np
            X = np.random.rand(10, 2)
            y = np.random.rand(10) * 100000
            model.fit(X, y)
            _model_cache[model_name] = model
            return model
        
        model = joblib.load(model_path)
        _model_cache[model_name] = model
        return model
    
    @staticmethod
    def load_scaler(model_name: str) -> Any:
        """
        Load a scaler/preprocessor for a model
        """
        cache_key = f"{model_name}_scaler"
        if cache_key in _model_cache:
            return _model_cache[cache_key]
        
        scaler_path = ModelLoader.MODELS_DIR / model_name / "scaler.pkl"
        
        if not scaler_path.exists():
            # Return a dummy scaler for development
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            import numpy as np
            scaler.fit(np.random.rand(10, 2))
            _model_cache[cache_key] = scaler
            return scaler
        
        scaler = joblib.load(scaler_path)
        _model_cache[cache_key] = scaler
        return scaler
    
    @staticmethod
    def load_encoder(model_name: str) -> Any:
        """
        Load a feature encoder for a model
        """
        cache_key = f"{model_name}_encoder"
        if cache_key in _model_cache:
            return _model_cache[cache_key]
        
        encoder_path = ModelLoader.MODELS_DIR / model_name / "encoder.pkl"
        
        if not encoder_path.exists():
            # Return None if encoder doesn't exist
            return None
        
        encoder = joblib.load(encoder_path)
        _model_cache[cache_key] = encoder
        return encoder
    
    @staticmethod
    def load_encoders(model_name: str) -> dict:
        """
        Load multiple encoders for a model (e.g., label encoders)
        """
        cache_key = f"{model_name}_encoders"
        if cache_key in _model_cache:
            return _model_cache[cache_key]
        
        encoders_dir = ModelLoader.MODELS_DIR / model_name / "encoders"
        
        if not encoders_dir.exists():
            # Return empty dict if encoders don't exist
            return {}
        
        encoders = {}
        for encoder_file in encoders_dir.glob("*.pkl"):
            encoder_name = encoder_file.stem
            encoders[encoder_name] = joblib.load(encoder_file)
        
        _model_cache[cache_key] = encoders
        return encoders

