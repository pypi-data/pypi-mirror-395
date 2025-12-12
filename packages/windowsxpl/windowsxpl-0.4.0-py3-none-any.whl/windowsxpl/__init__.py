"""
WindowsXPL - 机器学习管道工具包
"""

__version__ = "0.4.0"
__author__ = "Your Name"

# 导入主要模块，方便用户使用
from .src.config import Config
from .src.feature_engineering import FeatureEngineer
from .src.feature_processor import FeatureProcessor
from .src.model_automl import AutoMLPipeline
from .src.model_tuning import ModelTuner
from .src.model_ensemble import EnsembleModel
from .src.model_stacking import Stackingfrom 

# 导入projects和root中的模块（如果需要）
from .projects import main_stand
from .root import model_automl_with_auto_dt

__all__ = [
    'Config', 'FeatureEngineer', 'FeatureProcessor', 
    'AutoMLPipeline', 'ModelTuner', 'EnsembleModel', 
    'StackingModel', 'ModelEvaluator',
    'main_stand', 'model_automl_with_auto_dt'
]

def main():
    """命令行入口点"""
    print(f"WindowsXPLversion__")
    # 这里可以添加命令行逻辑