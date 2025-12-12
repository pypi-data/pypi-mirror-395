from typing import Dict, Any, List, Tuple, Union
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

# 导入现有的特征工程功能
from .feature_engineering import EnhancedFeatureEngineer, decision_tree_binning, _apply_precomputed_binning
from .feature_engineering import PrintUtils


class FeatureProcessorInterface(ABC):
    """特征处理器接口，定义了所有特征处理器必须实现的方法"""
    
    @abstractmethod
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[pd.DataFrame, Any]:
        """
        处理特征数据
        
        Args:
            X: 特征数据
            y: 目标变量（可选）
            
        Returns:
            处理后的特征数据和额外的信息（如规则、元数据等）
        """
        pass
    
    @abstractmethod
    def apply(self, X: pd.DataFrame, metadata: Any) -> pd.DataFrame:
        """
        将学习到的处理规则应用到新数据
        
        Args:
            X: 特征数据
            metadata: 处理过程中学习到的规则或元数据
            
        Returns:
            处理后的特征数据
        """
        pass


class DecisionTreeBinningProcessor(FeatureProcessorInterface):
    """决策树分箱处理器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.method = config.get("method", "decision_tree")
        self.tune_params = config.get("tune_params", False)
        self.n_trials = config.get("n_trials", 50)
        self.params = config.get("params", {})
    
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[pd.DataFrame, Dict[str, List[float]]]:
        """对训练数据进行分箱"""
        if self.method != "decision_tree":
            return X, {}
            
        print(f"   使用决策树分箱，参数调优: {self.tune_params}")
        X_binned, binning_rules = decision_tree_binning(
            X, y,
            tune_params=self.tune_params,
            n_trials=self.n_trials,
            **self.params
        )
        # 返回空的分箱规则，因为当前decision_tree_binning函数不返回规则
        return X_binned, binning_rules
    
    def apply(self, X: pd.DataFrame, metadata: Dict[str, List[float]]) -> pd.DataFrame:
        """将分箱规则应用到新数据"""
        if not metadata:
            return X
        
        print("   应用决策树分箱规则到新数据...")
        return _apply_precomputed_binning(X, metadata)


class FeatureDeletionProcessor(FeatureProcessorInterface):
    """特征删除处理器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enable", False)
        self.strategy = config.get("strategy", "manual")
        self.features_to_delete = config.get("features_to_delete", [])
        self.threshold = config.get("threshold", 0.01)  # 用于基于重要性或方差的删除
    
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[pd.DataFrame, List[str]]:
        """删除不需要的特征"""
        if not self.enabled:
            return X, []
            
        print(f"   执行特征删除，策略: {self.strategy}")
        features_to_delete = []
        
        if self.strategy == "manual":
            # 手动指定要删除的特征
            features_to_delete = [f for f in self.features_to_delete if f in X.columns]
        elif self.strategy == "low_variance":
            # 删除低方差特征
            variance = X.var()
            features_to_delete = variance[variance < self.threshold].index.tolist()
        elif self.strategy == "high_correlation" and y is not None:
            # 删除高相关特征
            _, features_to_delete = EnhancedFeatureEngineer.remove_multicollinearity(
                X, threshold=self.threshold
            )
        
        if features_to_delete:
            print(f"   删除的特征: {features_to_delete}")
            X = X.drop(columns=features_to_delete)
        
        return X, features_to_delete
    
    def apply(self, X: pd.DataFrame, metadata: List[str]) -> pd.DataFrame:
        """将特征删除规则应用到新数据"""
        if not metadata:
            return X
        
        features_to_delete = [f for f in metadata if f in X.columns]
        if features_to_delete:
            X = X.drop(columns=features_to_delete)
        
        return X


class EnhancedFeatureProcessor(FeatureProcessorInterface):
    """增强特征处理器 - 整合多重共线性处理和特征重要性筛选"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enable", False)
        self.corr_threshold = config.get("corr_threshold", 0.95)
        self.selection_threshold = config.get("selection_threshold", 25)
        self.remove_collinearity = config.get("remove_collinearity", True)
        self.use_feature_selection = config.get("use_feature_selection", True)
    
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """执行增强特征处理：多重共线性处理 + 特征重要性筛选"""
        if not self.enabled:
            return X, {"selected_features": X.columns.tolist()}
            
        print(f"   执行增强特征处理")
        
        # 保存原始特征列表
        original_features = X.columns.tolist()
        
        # 1. 处理多重共线性
        removed_collinear_features = []
        if self.remove_collinearity:
            X, removed_collinear_features = EnhancedFeatureEngineer.remove_multicollinearity(
                X, threshold=self.corr_threshold
            )
        
        # 2. 特征重要性筛选
        selected_features = X.columns.tolist()
        feature_importance_df = None
        
        if self.use_feature_selection and y is not None:
            X, selected_features, feature_importance_df = EnhancedFeatureEngineer.select_by_importance(
                X, y, threshold_percentile=self.selection_threshold, method="xgboost"
            )
        
        # 保存元数据
        metadata = {
            "selected_features": selected_features,
            "removed_collinear_features": removed_collinear_features,
            "original_features": original_features
        }
        
        return X, metadata
    
    def apply(self, X: pd.DataFrame, metadata: Dict[str, Any]) -> pd.DataFrame:
        """应用增强特征处理规则到新数据"""
        if not metadata or "selected_features" not in metadata:
            return X
        
        selected_features = metadata["selected_features"]
        # 只保留处理过程中选择的特征
        features_to_keep = [f for f in selected_features if f in X.columns]
        
        return X[features_to_keep]


class FeatureProcessor:
    """特征处理器，统一管理和应用各种特征加工策略"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化特征处理器
        
        Args:
            config: 配置文件，包含各种特征处理器的配置
        """
        self.config = config
        self.processors: Dict[str, FeatureProcessorInterface] = {}
        self.processor_metadata: Dict[str, Any] = {}
        
        # 初始化默认处理器
        self._initialize_processors()
    
    def _initialize_processors(self):
        """初始化特征处理器"""
        # 获取特征工程配置
        feature_engineering_config = self.config.get("feature_engineering", {})
        
        # 初始化分箱处理器
        binning_config = feature_engineering_config.get("binning", {})
        if binning_config.get("enable", False):
            self.add_processor("binning", DecisionTreeBinningProcessor(binning_config))
        
        # 初始化增强特征处理器（替换原有的特征删除处理器）
        enhanced_fe_config = feature_engineering_config.get("enhanced_feature_engineering", {})
        if enhanced_fe_config.get("enable", False):
            self.add_processor("enhanced_feature", EnhancedFeatureProcessor(enhanced_fe_config))
    
    def add_processor(self, name: str, processor: FeatureProcessorInterface):
        """
        添加新的特征处理器（扩展点）
        
        Args:
            name: 处理器名称
            processor: 特征处理器实例
        """
        self.processors[name] = processor
    
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> pd.DataFrame:
        """
        处理训练数据，应用所有启用的特征处理器
        
        Args:
            X: 特征数据
            y: 目标变量（可选）
            
        Returns:
            处理后的特征数据
        """
        X_processed = X.copy()
        
        if not self.processors:
            print("没有启用任何特征处理器")
            return X_processed
        
        PrintUtils.print_section("执行特征处理")
        
        for name, processor in self.processors.items():
            print(f"\n处理步骤: {name}")
            X_processed, metadata = processor.process(X_processed, y)
            self.processor_metadata[name] = metadata
            print(f"   处理后特征数量: {X_processed.shape[1]}")
        
        PrintUtils.print_section("特征处理完成")
        print(f"最终特征数量: {X_processed.shape[1]}")
        
        return X_processed
    
    def apply(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        将训练好的特征处理规则应用到新数据
        
        Args:
            X: 特征数据
            
        Returns:
            处理后的特征数据
        """
        X_processed = X.copy()
        
        for name, processor in self.processors.items():
            metadata = self.processor_metadata.get(name)
            if metadata is not None:
                X_processed = processor.apply(X_processed, metadata)
        
        return X_processed
    
    def get_processor_metadata(self, processor_name: str) -> Any:
        """
        获取特定处理器的元数据
        
        Args:
            processor_name: 处理器名称
            
        Returns:
            处理器的元数据
        """
        return self.processor_metadata.get(processor_name)
    
    def list_processors(self) -> List[str]:
        """
        列出所有启用的处理器
        
        Returns:
            启用的处理器名称列表
        """
        return list(self.processors.keys())
