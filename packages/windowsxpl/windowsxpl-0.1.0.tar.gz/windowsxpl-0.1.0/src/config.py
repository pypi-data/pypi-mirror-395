import yaml
import os
from typing import Dict, Any, Optional

class ConfigLoader:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.default_config = self._get_default_config()
        self.config = self._load_config()
    
    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径"""
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "data": {
                "file_path": "/Users/yuguangdeng/code/competition/projects/dataset/lasso_reduce.csv",
                "target_column": None,
                "random_state": 42
            },
            "model_saving": {
                "enable": True,
                "model_dir": "/Users/yuguangdeng/code/competition/projects/models",
                "single_models": True,
                "ensemble_model": True
            },
            "feature_engineering": {
                "enable": True,
                "scaling": {
                    "enable": True,
                    "method": "standard",
                    "params": {}
                },
                "feature_selection": {
                    "enable": False,
                    "method": "lasso",
                    "params": {
                        "threshold": 0.01
                    }
                },
                "missing_value": {
                    "enable": False,
                    "method": "mean",
                    "params": {}
                }
            },
            "models": [
                {
                    "name": "xgboost",
                    "enable": True,
                    "params": {
                        "learning_rate": 0.1,
                        "n_estimators": 100,
                        "max_depth": 6,
                        "subsample": 0.8,
                        "colsample_bytree": 0.8,
                        "random_state": 42
                    },
                    "tuning": {
                        "enable": False,
                        "method": "grid",
                        "param_grid": {
                            "learning_rate": [0.01, 0.1],
                            "n_estimators": [100, 200],
                            "max_depth": [3, 6]
                        }
                    }
                },
                {
                "name": "catboost",
                "enable": True,
                "params": {
                    "learning_rate": 0.1,
                    "n_estimators": 100,
                    "max_depth": 6,
                    "subsample": 0.8,
                    "random_state": 42,
                    "verbose": False
                },
                "tuning": {
                    "enable": False,
                    "method": "grid",
                    "param_grid": {
                        "learning_rate": [0.01, 0.1],
                        "n_estimators": [100, 200],
                        "max_depth": [3, 6]
                    }
                }
            },
            {
                "name": "lightgbm",
                "enable": True,
                "params": {
                    "learning_rate": 0.1,
                    "n_estimators": 100,
                    "max_depth": 6,
                    "subsample": 0.8,
                    "colsample_bytree": 0.8,
                    "random_state": 42,
                    "verbose": -1
                },
                "tuning": {
                    "enable": False,
                    "method": "grid",
                    "param_grid": {
                        "learning_rate": [0.01, 0.1],
                        "n_estimators": [100, 200],
                        "max_depth": [3, 6]
                    }
                }
            }
            ],
            "ensemble": {
                "enable": False,
                "method": "weighted_average",
                "params": {
                    "weights": [0.5, 0.5]
                }
            },
            "evaluation": {
                "cv_folds": 5,
                "metrics": ["auc"],
                "random_state": 42,
                "verbose": True
            }
        }
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """递归合并配置"""
        merged = default.copy()
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            elif key in merged and isinstance(merged[key], list) and isinstance(value, list):
                # 特殊处理models列表，根据name合并
                if key == "models":
                    merged_models = []
                    user_model_dict = {model["name"]: model for model in value}
                    for default_model in merged[key]:
                        if default_model["name"] in user_model_dict:
                            # 合并模型配置
                            merged_model = self._merge_configs(default_model, user_model_dict[default_model["name"]])
                            merged_models.append(merged_model)
                            del user_model_dict[default_model["name"]]
                        else:
                            merged_models.append(default_model)
                    # 添加用户配置中新增的模型
                    merged_models.extend(user_model_dict.values())
                    merged[key] = merged_models
                else:
                    merged[key] = value
            else:
                merged[key] = value
        return merged
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            print(f"配置文件不存在，使用默认配置: {self.config_path}")
            return self.default_config
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f)
            
            if not user_config:
                print("配置文件为空，使用默认配置")
                return self.default_config
            
            # 合并用户配置和默认配置
            merged_config = self._merge_configs(self.default_config, user_config)
            return merged_config
        except Exception as e:
            print(f"加载配置文件失败，使用默认配置: {e}")
            return self.default_config
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        return self.config
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项，支持点号分隔的路径"""
        keys = key.split(".")
        value = self.config
        try:
            for k in keys:
                if isinstance(value, list) and k.isdigit():
                    value = value[int(k)]
                else:
                    value = value[k]
            return value
        except (KeyError, IndexError, TypeError):
            return default
    
    def update(self, key: str, value: Any) -> None:
        """更新配置项，支持点号分隔的路径"""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if isinstance(config, list) and k.isdigit():
                config = config[int(k)]
            else:
                config = config[k]
        
        last_key = keys[-1]
        if isinstance(config, list) and last_key.isdigit():
            config[int(last_key)] = value
        else:
            config[last_key] = value

# 全局配置实例
def get_config(config_path: Optional[str] = None) -> ConfigLoader:
    """获取配置实例"""
    return ConfigLoader(config_path)