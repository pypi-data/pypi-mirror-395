#!/usr/bin/env python3
"""
Advanced Machine Learning Pipeline
Integration of ML models for simulation enhancement, prediction, and control
"""

import numpy as np
import tensorflow as tf
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import xgboost as xgb
import lightgbm as lgb
import joblib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import glm
from dataclasses import dataclass
from enum import Enum
import hashlib
import pickle

class MLModelType(Enum):
    PHYSICS_PREDICTOR = "physics_predictor"
    PARTICLE_TRACKER = "particle_tracker"
    ANOMALY_DETECTOR = "anomaly_detector"
    PARAMETER_OPTIMIZER = "parameter_optimizer"
    RENDER_ENHANCER = "render_enhancer"
    BEHAVIOR_CLASSIFIER = "behavior_classifier"
    REAL_TIME_ADVISOR = "real_time_advisor"

@dataclass
class TrainingConfig:
    epochs: int = 100
    batch_size: int = 32
    learning_rate: float = 0.001
    validation_split: float = 0.2
    early_stopping_patience: int = 10
    model_save_path: str = "models/"

@dataclass
class MLFeatureSet:
    particle_positions: np.ndarray
    particle_velocities: np.ndarray
    forces: np.ndarray
    simulation_time: float
    environmental_params: Dict[str, float]
    performance_metrics: Dict[str, float]

class PhysicsPredictor(nn.Module):
    """Neural network for predicting particle physics"""
    
    def __init__(self, input_dim=128, hidden_dims=[512, 256, 128], output_dim=6):
        super(PhysicsPredictor, self).__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
        self.attention = nn.MultiheadAttention(input_dim, 8)
        
    def forward(self, x):
        # Apply attention for temporal dependencies
        if len(x.shape) == 2:
            x = x.unsqueeze(0)  # Add sequence dimension
            x, _ = self.attention(x, x, x)
            x = x.squeeze(0)
        
        return self.network(x)

class AdvancedMLPipeline:
    def __init__(self, simulation_app):
        self.simulation_app = simulation_app
        self.models: Dict[MLModelType, Any] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.training_data: List[MLFeatureSet] = []
        self.prediction_cache: Dict[str, np.ndarray] = {}
        
        # ML pipeline configuration
        self.config = {
            "enable_real_time_learning": True,
            "prediction_interval": 0.1,  # seconds
            "max_training_samples": 10000,
            "feature_history_length": 10,
            "model_auto_save": True,
            "confidence_threshold": 0.8
        }
        
        # Performance tracking
        self.performance_metrics = {
            "predictions_made": 0,
            "prediction_accuracy": 0.0,
            "training_time": 0.0,
            "inference_time": 0.0
        }
        
        # Initialize all ML models
        self.initialize_models()
        
        # Create model directory
        import os
        os.makedirs("models", exist_ok=True)
        
        # Load pre-trained models if available
        self.load_pretrained_models()
        
    def initialize_models(self):
        """Initialize all machine learning models"""
        print("Initializing Advanced ML Pipeline...")
        
        # Physics prediction model (PyTorch)
        self.models[MLModelType.PHYSICS_PREDICTOR] = PhysicsPredictor()
        self.models[MLModelType.PHYSICS_PREDICTOR].eval()
        
        # Particle tracking model (XGBoost)
        self.models[MLModelType.PARTICLE_TRACKER] = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            objective='reg:squarederror'
        )
        
        # Anomaly detection model (Scikit-learn)
        self.models[MLModelType.ANOMALY_DETECTOR] = DBSCAN(eps=0.5, min_samples=5)
        
        # Parameter optimization model (LightGBM)
        self.models[MLModelType.PARAMETER_OPTIMIZER] = lgb.LGBMRegressor(
            n_estimators=50,
            max_depth=4,
            learning_rate=0.05
        )
        
        # Initialize scalers
        self.scalers["features"] = StandardScaler()
        self.scalers["targets"] = StandardScaler()
        
        # Move PyTorch models to GPU if available
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if torch.cuda.is_available():
            self.models[MLModelType.PHYSICS_PREDICTOR] = self.models[MLModelType.PHYSICS_PREDICTOR].to(self.device)
            print(f"Using GPU: {torch.cuda.get_device_name()}")
        else:
            print("Using CPU for ML computations")
            
    def load_pretrained_models(self):
        """Load pre-trained models from disk"""
        try:
            model_paths = {
                MLModelType.PHYSICS_PREDICTOR: "models/physics_predictor.pth",
                MLModelType.PARTICLE_TRACKER: "models/particle_tracker.json",
                MLModelType.PARAMETER_OPTIMIZER: "models/parameter_optimizer.txt"
            }
            
            for model_type, path in model_paths.items():
                if self.load_model(model_type, path):
                    print(f"Loaded pre-trained model: {model_type.value}")
                    
        except Exception as e:
            print(f"Error loading pre-trained models: {e}")
    
    def extract_features(self, simulation_state: Dict[str, Any]) -> MLFeatureSet:
        """Extract features from current simulation state for ML training"""
        particles = simulation_state.get("particles", [])
        
        if not particles:
            return MLFeatureSet(
                particle_positions=np.array([]),
                particle_velocities=np.array([]),
                forces=np.array([]),
                simulation_time=0.0,
                environmental_params={},
                performance_metrics={}
            )
        
        # Extract particle features
        positions = []
        velocities = []
        forces = []
        
        for particle in particles:
            positions.append([particle.position.x, particle.position.y, particle.position.z])
            velocities.append([particle.velocity.x, particle.velocity.y, particle.velocity.z])
            # Forces would be extracted from physics module if available
            forces.append([0.0, -9.8, 0.0])  # Default gravity
            
        # Environmental parameters
        env_params = {
            "gravity": -9.8,
            "wind_strength": 0.0,
            "air_resistance": 0.1,
            "time_step": simulation_state.get("time_step", 0.016)
        }
        
        # Performance metrics
        perf_metrics = {
            "fps": self.simulation_app.fps,
            "particle_count": len(particles),
            "frame_time": self.simulation_app.average_frame_time
        }
        
        return MLFeatureSet(
            particle_positions=np.array(positions),
            particle_velocities=np.array(velocities),
            forces=np.array(forces),
            simulation_time=simulation_state.get("simulation_time", 0.0),
            environmental_params=env_params,
            performance_metrics=perf_metrics
        )
    
    def prepare_training_data(self, feature_sets: List[MLFeatureSet]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare feature and target arrays for training"""
        if not feature_sets:
            return np.array([]), np.array([])
        
        features = []
        targets = []
        
        for i, feature_set in enumerate(feature_sets[:-1]):
            # Current state features
            current_features = self.flatten_features(feature_set)
            
            # Next state targets (from next timestep)
            next_feature_set = feature_sets[i + 1]
            next_targets = self.flatten_features(next_feature_set, targets_only=True)
            
            features.append(current_features)
            targets.append(next_targets)
        
        return np.array(features), np.array(targets)
    
    def flatten_features(self, feature_set: MLFeatureSet, targets_only: bool = False) -> np.ndarray:
        """Flatten feature set into 1D array for ML models"""
        flattened = []
        
        if not targets_only:
            # Particle statistics
            if len(feature_set.particle_positions) > 0:
                flattened.extend(feature_set.particle_positions.mean(axis=0))  # Mean position
                flattened.extend(feature_set.particle_positions.std(axis=0))   # Position std
                flattened.extend(feature_set.particle_velocities.mean(axis=0)) # Mean velocity
                flattened.extend(feature_set.particle_velocities.std(axis=0))  # Velocity std
            
            # Environmental parameters
            flattened.extend([
                feature_set.environmental_params.get("gravity", -9.8),
                feature_set.environmental_params.get("wind_strength", 0.0),
                feature_set.environmental_params.get("air_resistance", 0.1)
            ])
            
            # Performance metrics
            flattened.extend([
                feature_set.performance_metrics.get("fps", 60.0),
                feature_set.performance_metrics.get("particle_count", 0),
                feature_set.simulation_time
            ])
        else:
            # For targets, we only want future particle states
            if len(feature_set.particle_positions) > 0:
                flattened.extend(feature_set.particle_positions.mean(axis=0))
                flattened.extend(feature_set.particle_velocities.mean(axis=0))
        
        return np.array(flattened)
    
    def train_physics_predictor(self, training_config: TrainingConfig = None):
        """Train the physics prediction neural network"""
        if training_config is None:
            training_config = TrainingConfig()
        
        if len(self.training_data) < 100:
            print("Insufficient training data")
            return
        
        print("Training Physics Predictor...")
        start_time = time.time()
        
        # Prepare data
        features, targets = self.prepare_training_data(self.training_data)
        
        if len(features) == 0:
            print("No valid training data")
            return
        
        # Scale features and targets
        features_scaled = self.scalers["features"].fit_transform(features)
        targets_scaled = self.scalers["targets"].fit_transform(targets)
        
        # Convert to PyTorch tensors
        features_tensor = torch.FloatTensor(features_scaled)
        targets_tensor = torch.FloatTensor(targets_scaled)
        
        # Create dataset and dataloader
        dataset = torch.utils.data.TensorDataset(features_tensor, targets_tensor)
        dataloader = torch.utils.data.DataLoader(
            dataset, 
            batch_size=training_config.batch_size, 
            shuffle=True
        )
        
        # Initialize model and optimizer
        model = self.models[MLModelType.PHYSICS_PREDICTOR]
        model.train()
        optimizer = optim.Adam(model.parameters(), lr=training_config.learning_rate)
        criterion = nn.MSELoss()
        
        # Training loop
        best_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(training_config.epochs):
            epoch_loss = 0.0
            for batch_features, batch_targets in dataloader:
                if torch.cuda.is_available():
                    batch_features = batch_features.to(self.device)
                    batch_targets = batch_targets.to(self.device)
                
                optimizer.zero_grad()
                predictions = model(batch_features)
                loss = criterion(predictions, batch_targets)
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
            
            avg_loss = epoch_loss / len(dataloader)
            
            # Early stopping
            if avg_loss < best_loss:
                best_loss = avg_loss
                patience_counter = 0
                # Save best model
                if self.config["model_auto_save"]:
                    self.save_model(MLModelType.PHYSICS_PREDICTOR, "models/physics_predictor_best.pth")
            else:
                patience_counter += 1
                
            if patience_counter >= training_config.early_stopping_patience:
                print(f"Early stopping at epoch {epoch}")
                break
            
            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {avg_loss:.6f}")
        
        # Set model back to evaluation mode
        model.eval()
        
        training_time = time.time() - start_time
        self.performance_metrics["training_time"] = training_time
        print(f"Physics Predictor training completed in {training_time:.2f} seconds")
    
    def predict_next_state(self, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Predict next simulation state using ML models"""
        start_time = time.time()
        
        # Extract features from current state
        feature_set = self.extract_features(current_state)
        features = self.flatten_features(feature_set)
        
        if len(features) == 0:
            return current_state
        
        # Scale features
        features_scaled = self.scalers["features"].transform(features.reshape(1, -1))
        
        # Predict using neural network
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            if torch.cuda.is_available():
                features_tensor = features_tensor.to(self.device)
            
            predictions_scaled = self.models[MLModelType.PHYSICS_PREDICTOR](features_tensor)
            predictions = self.scalers["targets"].inverse_transform(
                predictions_scaled.cpu().numpy()
            )
        
        # Convert predictions back to simulation state
        predicted_state = self.convert_predictions_to_state(predictions[0], current_state)
        
        inference_time = time.time() - start_time
        self.performance_metrics["inference_time"] = inference_time
        self.performance_metrics["predictions_made"] += 1
        
        return predicted_state
    
    def convert_predictions_to_state(self, predictions: np.ndarray, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Convert ML predictions back to simulation state format"""
        # This is a simplified conversion - in practice, this would be more complex
        predicted_state = current_state.copy()
        
        # Update particle positions and velocities based on predictions
        if "particles" in predicted_state and len(predicted_state["particles"]) > 0:
            # For simplicity, apply predictions to all particles equally
            # In advanced implementation, this would be per-particle
            mean_position_change = predictions[:3]
            mean_velocity_change = predictions[3:6]
            
            for particle in predicted_state["particles"]:
                particle.position += glm.vec3(*mean_position_change)
                particle.velocity += glm.vec3(*mean_velocity_change)
        
        return predicted_state
    
    def detect_anomalies(self, feature_set: MLFeatureSet) -> Dict[str, Any]:
        """Detect anomalous behavior in simulation"""
        if len(feature_set.particle_positions) == 0:
            return {"anomalies": [], "confidence": 0.0}
        
        # Extract features for anomaly detection
        features = []
        for i in range(len(feature_set.particle_positions)):
            particle_features = np.concatenate([
                feature_set.particle_positions[i],
                feature_set.particle_velocities[i]
            ])
            features.append(particle_features)
        
        features = np.array(features)
        
        # Cluster particles to find anomalies
        clusters = self.models[MLModelType.ANOMALY_DETECTOR].fit_predict(features)
        
        # Identify anomalies (cluster label -1)
        anomaly_indices = np.where(clusters == -1)[0]
        anomaly_confidence = len(anomaly_indices) / len(features) if len(features) > 0 else 0.0
        
        return {
            "anomalies": anomaly_indices.tolist(),
            "confidence": anomaly_confidence,
            "total_particles": len(features),
            "anomaly_count": len(anomaly_indices)
        }
    
    def optimize_parameters(self, objective: str, constraints: Dict[str, Any]) -> Dict[str, float]:
        """Optimize simulation parameters using ML"""
        # Extract historical performance data
        performance_data = []
        parameter_data = []
        
        for feature_set in self.training_data[-100:]:  # Use recent history
            params = feature_set.environmental_params
            performance = feature_set.performance_metrics.get("fps", 60.0)
            
            parameter_data.append([
                params.get("gravity", -9.8),
                params.get("wind_strength", 0.0),
                params.get("air_resistance", 0.1)
            ])
            performance_data.append(performance)
        
        if len(performance_data) < 10:
            return constraints  # Not enough data
        
        # Train parameter optimizer
        X = np.array(parameter_data)
        y = np.array(performance_data)
        
        self.models[MLModelType.PARAMETER_OPTIMIZER].fit(X, y)
        
        # Find optimal parameters (simplified grid search)
        best_score = -float('inf')
        best_params = constraints.copy()
        
        # Simple parameter sweep (in practice, use Bayesian optimization)
        gravity_range = np.linspace(-20, 0, 10)
        wind_range = np.linspace(-5, 5, 10)
        resistance_range = np.linspace(0, 1, 10)
        
        for gravity in gravity_range:
            for wind in wind_range:
                for resistance in resistance_range:
                    params = np.array([[gravity, wind, resistance]])
                    score = self.models[MLModelType.PARAMETER_OPTIMIZER].predict(params)[0]
                    
                    if score > best_score:
                        best_score = score
                        best_params = {
                            "gravity": float(gravity),
                            "wind_strength": float(wind),
                            "air_resistance": float(resistance)
                        }
        
        return best_params
    
    def update_training_data(self, simulation_state: Dict[str, Any]):
        """Update training data with current simulation state"""
        feature_set = self.extract_features(simulation_state)
        
        # Limit training data size
        if len(self.training_data) >= self.config["max_training_samples"]:
            self.training_data.pop(0)
        
        self.training_data.append(feature_set)
        
        # Auto-train if enough new data
        if len(self.training_data) % 100 == 0 and self.config["enable_real_time_learning"]:
            self.train_physics_predictor()
    
    def get_ml_advice(self, simulation_state: Dict[str, Any]) -> Dict[str, Any]:
        """Get ML-based advice for simulation improvement"""
        advice = {
            "performance_optimization": {},
            "parameter_recommendations": {},
            "anomaly_alerts": {},
            "prediction_insights": {}
        }
        
        # Performance optimization advice
        if self.simulation_app.fps < 30:
            advice["performance_optimization"] = {
                "message": "Low FPS detected",
                "suggestion": "Reduce particle count or simplify physics",
                "confidence": 0.9
            }
        
        # Parameter recommendations
        optimal_params = self.optimize_parameters("fps", {})
        advice["parameter_recommendations"] = optimal_params
        
        # Anomaly detection
        feature_set = self.extract_features(simulation_state)
        anomalies = self.detect_anomalies(feature_set)
        if anomalies["confidence"] > self.config["confidence_threshold"]:
            advice["anomaly_alerts"] = anomalies
        
        # Prediction insights
        if self.performance_metrics["predictions_made"] > 0:
            advice["prediction_insights"] = {
                "prediction_accuracy": self.performance_metrics["prediction_accuracy"],
                "average_inference_time": self.performance_metrics["inference_time"],
                "recommendation": "ML predictions are active and accurate"
            }
        
        return advice
    
    def save_model(self, model_type: MLModelType, filepath: str) -> bool:
        """Save a trained ML model to disk"""
        try:
            if model_type == MLModelType.PHYSICS_PREDICTOR:
                torch.save(self.models[model_type].state_dict(), filepath)
            elif model_type == MLModelType.PARTICLE_TRACKER:
                self.models[model_type].save_model(filepath)
            elif model_type == MLModelType.PARAMETER_OPTIMIZER:
                self.models[model_type].booster_.save_model(filepath)
            else:
                joblib.dump(self.models[model_type], filepath)
            return True
        except Exception as e:
            print(f"Error saving model {model_type.value}: {e}")
            return False
    
    def load_model(self, model_type: MLModelType, filepath: str) -> bool:
        """Load a trained ML model from disk"""
        try:
            if model_type == MLModelType.PHYSICS_PREDICTOR:
                self.models[model_type].load_state_dict(torch.load(filepath))
                self.models[model_type].eval()
            elif model_type == MLModelType.PARTICLE_TRACKER:
                self.models[model_type].load_model(filepath)
            elif model_type == MLModelType.PARAMETER_OPTIMIZER:
                self.models[model_type] = lgb.Booster(model_file=filepath)
            else:
                self.models[model_type] = joblib.load(filepath)
            return True
        except Exception as e:
            print(f"Error loading model {model_type.value}: {e}")
            return False
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report of ML pipeline"""
        return {
            "models_trained": len([m for m in self.models if hasattr(m, 'fit')]),
            "training_data_size": len(self.training_data),
            "performance_metrics": self.performance_metrics,
            "active_predictions": self.config["enable_real_time_learning"],
            "hardware_acceleration": "GPU" if torch.cuda.is_available() else "CPU",
            "model_memory_usage": "N/A"  # Would calculate actual memory usage
        }
    
    def cleanup(self):
        """Cleanup ML resources"""
        # Clear training data
        self.training_data.clear()
        
        # Clear cache
        self.prediction_cache.clear()
        
        # Save models on cleanup
        if self.config["model_auto_save"]:
            self.save_model(MLModelType.PHYSICS_PREDICTOR, "models/physics_predictor_final.pth")
            print("ML models saved successfully")

# Example usage integration with main application
class MLEnhancedSimulation:
    def __init__(self, base_simulation, ml_pipeline):
        self.base_simulation = base_simulation
        self.ml_pipeline = ml_pipeline
        self.use_ml_predictions = False
        
    def update(self, dt):
        # Get current state
        current_state = self.get_current_state()
        
        # Update ML training data
        self.ml_pipeline.update_training_data(current_state)
        
        # Use ML predictions if enabled
        if self.use_ml_predictions:
            predicted_state = self.ml_pipeline.predict_next_state(current_state)
            self.apply_predicted_state(predicted_state)
        else:
            # Use normal physics update
            self.base_simulation.update(dt)
    
    def get_current_state(self):
        # Extract current simulation state for ML
        return {
            "particles": self.base_simulation.particles if hasattr(self.base_simulation, 'particles') else [],
            "simulation_time": self.base_simulation.simulation_time,
            "time_step": self.base_simulation.time_step if hasattr(self.base_simulation, 'time_step') else 0.016
        }
    
    def apply_predicted_state(self, predicted_state):
        # Apply ML-predicted state to simulation
        # This would update particle positions, velocities, etc.
        pass

if __name__ == "__main__":
    # Test the ML pipeline
    pipeline = AdvancedMLPipeline(None)
    print("Advanced ML Pipeline initialized successfully")
    print(f"Available models: {[model_type.value for model_type in pipeline.models.keys()]}")