"""
AutoML 数据分析管道包
自动化机器学习管道，包含特征工程、模型调优、集成学习等功能
"""

__version__ = "0.1.0"
__author__ = "name"
__email__ = "your.email@example.com"

# 导入主要模块，方便用户直接使用
from .config import Config
from .feature_engineering import FeatureEngineer
from .feature_processor import FeatureProcessor
from .model_automl import AutoMLPipeline
from .model_tuning import ModelTuner
from .model_ensemble import EnsembleModel
from .model_stacking import StackingModel
from .evaluation import ModelEvaluator

# 定义公开的API
__all__ = [
    'Config',
    'FeatureEngineer', 
    'FeatureProcessor',
    'AutoMLPipeline',
    'ModelTuner',
    'EnsembleModel',
    'StackingModel',
    'ModelEvaluator'
]

# 包初始化信息
print(f"AutoML Pipeline {__version__} 加载成功")