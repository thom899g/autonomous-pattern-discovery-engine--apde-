"""
APDE Configuration Management
Centralized configuration with type safety and environment variable handling
"""
import os
import json
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class APDEConfig:
    """Configuration dataclass with validation"""
    
    # Data Collection
    data_sources: List[str] = field(default_factory=lambda: ["binance", "kraken"])
    timeframe_minutes: int = 15
    historical_days: int = 365
    
    # Unsupervised Learning
    clustering_algorithm: str = "dbscan"
    autoencoder_latent_dim: int = 32
    min_pattern_samples: int = 10
    pattern_confidence_threshold: float = 0.7
    
    # Reinforcement Learning
    rl_learning_rate: float = 0.001
    rl_discount_factor: float = 0.95
    rl_epsilon_decay: float = 0.995
    max_position_size_usd: float = 10000.0
    
    # Risk Management
    max_daily_loss_percent: float = 5.0
    stop_loss_percent: float = 2.0
    take_profit_percent: float = 4.0
    
    # Firebase Configuration
    firebase_project_id: str = ""
    firestore_collection_prefix: str = "apde_"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "apde_engine.log"
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_config()
        
    def _validate_config(self) -> None:
        """Validate all configuration parameters"""
        valid_algorithms = ["dbscan", "kmeans", "hdbscan"]
        if self.clustering_algorithm not in valid_algorithms:
            raise ValueError(f"Invalid clustering algorithm. Must be one of {valid_algorithms}")
            
        if self.max_position_size_usd <= 0:
            raise ValueError("max_position_size_usd must be positive")
            
        if self.stop_loss_percent >= self.take_profit_percent:
            raise ValueError("stop_loss_percent must be less than take_profit_percent")
    
    @classmethod
    def from_env(cls) -> "APDEConfig":
        """Create config from environment variables"""
        config = cls()
        
        # Override with environment variables if present
        if os.getenv("APDE_FIREBASE_PROJECT_ID"):
            config.firebase_project_id = os.getenv("APDE_FIREBASE_PROJECT_ID")
            
        if os.getenv("APDE_LOG_LEVEL"):
            config.log_level = os.getenv("APDE_LOG_LEVEL")
            
        return config
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary for Firebase storage"""
        return {k: v for k, v in self.__dict__.items() 
                if not k.startswith('_') and not callable(v)}