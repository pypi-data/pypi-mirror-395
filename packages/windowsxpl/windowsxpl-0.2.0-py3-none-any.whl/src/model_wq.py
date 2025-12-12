"""
模型优化版本 - 模块化重构
相比基础版本(model.py)的优化点：
1. ✅ 多重共线性处理 - 移除高度相关特征
2. ✅ 特征重要性筛选 - 基于XGBoost重要性的特征选择
3. ✅ 多模型集成 - XGBoost + LightGBM + CatBoost
4. ✅ 差异化特征策略 - 不同模型使用不同特征集
5. ✅ 超参数优化 - 针对性的参数调优
6. ✅ 早停机制 - XGBoost的早停训练
7. ✅ 多融合策略 - 简单平均/加权平均/排名平均/Stacking
8. ✅ 模块化架构 - 清晰的代码组织结构
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

# ==================== 配置管理模块 ====================

class ModelConfig:
    """模型配置类 - 集中管理所有配置参数"""
    
    # 数据配置
    DATA_FILE = "lasso_reduce.csv"
    RANDOM_STATE = 42
    N_SPLITS = 5
    
    # 特征工程配置
    MULTICOLLINEARITY_THRESHOLD = 0.95
    FEATURE_SELECTION_PERCENTILE = 25  # 保留前75%特征
    
    # XGBoost配置（激进优化）
    XGBOOST_PARAMS = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'learning_rate': 0.03,
        'max_depth': 6,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 10,
        'reg_alpha': 15,
        'reg_lambda': 15,
        'gamma': 0.2,
        'random_state': RANDOM_STATE,
        'tree_method': 'hist'
    }
    XGBOOST_ROUNDS = 2000
    XGBOOST_EARLY_STOPPING = 100
    
    # LightGBM配置（保守优化）
    LIGHTGBM_PARAMS = {
        'random_state': RANDOM_STATE,
        'learning_rate': 0.04,
        'n_estimators': 300,
        'max_depth': 6,
        'num_leaves': 40,
        'min_child_samples': 30,
        'subsample': 0.85,
        'subsample_freq': 1,
        'colsample_bytree': 0.85,
        'reg_alpha': 5,
        'reg_lambda': 5,
        'min_split_gain': 0.1,
        'verbose': -1
    }
    
    # CatBoost配置（原版稳定）
    CATBOOST_PARAMS = {
        'random_state': RANDOM_STATE,
        'learning_rate': 0.05,
        'iterations': 200,
        'depth': 6,
        'verbose': 0
    }

# ==================== 数据加载模块 ====================

def load_data(file_path=ModelConfig.DATA_FILE):
    """加载数据"""
    data = pd.read_csv(file_path)
    return data

# ==================== 工具函数模块 ====================

class PrintUtils:
    """打印工具类 - 统一的输出格式"""
    
    @staticmethod
    def print_section(title, width=50):
        """打印分节标题"""
        print(f"\n{'='*width}")
        print(title)
        print(f"{'='*width}")
    
    @staticmethod
    def print_feature_stats(original_count, current_count, removed_count):
        """打印特征统计"""
        reduction_pct = (removed_count / original_count * 100) if original_count > 0 else 0
        print(f"\n移除的特征数量: {removed_count}")
        print(f"处理后特征数量: {current_count}")
        print(f"特征减少比例: {reduction_pct:.2f}%")
    
    @staticmethod
    def print_model_scores(scores_dict, title="模型性能"):
        """打印模型分数"""
        sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
        print(f"\n{title}:")
        for rank, (name, score) in enumerate(sorted_scores, 1):
            print(f"  {rank}. {name:20s}: {score:.4f}")
        return sorted_scores

# ==================== 特征工程模块 ====================

class FeatureEngineer:
    """特征工程类 - 封装所有特征处理方法"""
    
    @staticmethod
    def remove_multicollinearity(X, threshold=ModelConfig.MULTICOLLINEARITY_THRESHOLD):
        """
        处理多重共线性问题
        优化点1: 移除高度相关的特征，减少冗余信息
        """
        PrintUtils.print_section("处理多重共线性")
        print(f"原始特征数量: {X.shape[1]}")
        
        # 计算相关系数矩阵
        corr_matrix = X.corr().abs()
        upper_triangle = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        # 找出高度相关的特征对
        high_corr_pairs = []
        for column in upper_triangle.columns:
            correlated_features = upper_triangle[column][upper_triangle[column] > threshold]
            if len(correlated_features) > 0:
                for corr_feature in correlated_features.index:
                    high_corr_pairs.append({
                        'feature1': column,
                        'feature2': corr_feature,
                        'correlation': upper_triangle.loc[corr_feature, column]
                    })
        
        # 打印高相关特征对
        if high_corr_pairs:
            print(f"\n发现 {len(high_corr_pairs)} 对高度相关的特征 (相关系数 > {threshold}):")
            for i, pair in enumerate(high_corr_pairs[:10], 1):
                print(f"  {i}. {pair['feature1']} <-> {pair['feature2']}: {pair['correlation']:.4f}")
            if len(high_corr_pairs) > 10:
                print(f"  ... 还有 {len(high_corr_pairs) - 10} 对")
        else:
            print(f"\n未发现相关系数超过 {threshold} 的特征对")
        
        # 识别需要移除的特征
        to_drop = set()
        for column in upper_triangle.columns:
            correlated = upper_triangle[column][upper_triangle[column] > threshold]
            if len(correlated) > 0 and column not in to_drop:
                to_drop.update(correlated.index.tolist())
        
        X_reduced = X.drop(columns=list(to_drop), errors='ignore')
        
        # 打印统计信息
        if len(to_drop) > 0:
            print(f"\n被移除的特征: {sorted(list(to_drop))[:20]}")
            if len(to_drop) > 20:
                print(f"  ... 还有 {len(to_drop) - 20} 个特征")
        
        PrintUtils.print_feature_stats(X.shape[1], X_reduced.shape[1], len(to_drop))
        
        return X_reduced, list(to_drop)

    @staticmethod
    def select_by_importance(X, y, threshold_percentile=ModelConfig.FEATURE_SELECTION_PERCENTILE, method='xgboost'):
        """
        基于特征重要性进行特征筛选
        优化点2: 使用模型的特征重要性移除低价值特征
        
        参数：
        - X: DataFrame，特征矩阵
        - y: Series，目标变量
        - threshold_percentile: int，保留特征的百分位（默认25，即保留前75%重要的特征）
        - method: str，使用的模型（'xgboost', 'lightgbm', 'catboost'）
        
        返回：
        - X_selected: DataFrame，筛选后的特征矩阵
        - selected_features: list，被选中的特征列表
        - feature_importance_df: DataFrame，特征重要性详情
        """
        PrintUtils.print_section("特征重要性筛选")
        print(f"原始特征数量: {X.shape[1]}")
        print(f"使用模型: {method}")
    
        # 训练模型获取特征重要性
        if method == 'xgboost':
            model = XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=ModelConfig.RANDOM_STATE,
                eval_metric='auc'
            )
        elif method == 'lightgbm':
            try:
                from lightgbm import LGBMClassifier
                model = LGBMClassifier(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    random_state=ModelConfig.RANDOM_STATE,
                    verbose=-1
                )
            except ImportError:
                print("LightGBM未安装，使用XGBoost")
                model = XGBClassifier(n_estimators=100, random_state=ModelConfig.RANDOM_STATE)
        elif method == 'catboost':
            try:
                from catboost import CatBoostClassifier
                model = CatBoostClassifier(
                    iterations=100,
                    depth=6,
                    learning_rate=0.1,
                    random_state=ModelConfig.RANDOM_STATE,
                    verbose=0
                )
            except ImportError:
                print("CatBoost未安装，使用XGBoost")
                model = XGBClassifier(n_estimators=100, random_state=ModelConfig.RANDOM_STATE)
        else:
            model = XGBClassifier(n_estimators=100, random_state=ModelConfig.RANDOM_STATE)
        
        # 训练模型
        print("训练模型以计算特征重要性...")
        model.fit(X, y)
        
        # 获取特征重要性
        importances = model.feature_importances_
        
        # 创建特征重要性DataFrame
        feature_importance_df = pd.DataFrame({
            'feature': X.columns,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        # 计算阈值
        threshold = np.percentile(importances, threshold_percentile)
        
        # 筛选重要特征
        important_features = feature_importance_df[
            feature_importance_df['importance'] > threshold
        ]['feature'].tolist()
        
        X_selected = X[important_features]
        
        print(f"\n筛选阈值 (第{threshold_percentile}百分位): {threshold:.6f}")
        print(f"筛选后特征数量: {len(important_features)}")
        print(f"移除的特征数量: {X.shape[1] - len(important_features)}")
        print(f"特征保留比例: {len(important_features)/X.shape[1]*100:.1f}%")
        
        # 显示Top 20重要特征
        print(f"\nTop 20 重要特征:")
        for i, row in feature_importance_df.head(20).iterrows():
            print(f"  {i+1:2d}. {row['feature']:40s}: {row['importance']:.6f}")
        
        # 显示被移除的特征（如果不多）
        removed_features = [f for f in X.columns if f not in important_features]
        if len(removed_features) <= 20:
            print(f"\n被移除的特征:")
            for f in removed_features:
                imp = feature_importance_df[feature_importance_df['feature'] == f]['importance'].values[0]
                print(f"  - {f}: {imp:.6f}")
        elif len(removed_features) > 0:
            print(f"\n移除了 {len(removed_features)} 个低重要性特征")
        
        return X_selected, important_features, feature_importance_df
    
    @staticmethod
    def standardize_features(X, feature_names=None):
        """标准化特征"""
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        if feature_names is not None:
            return pd.DataFrame(X_scaled, columns=feature_names, index=X.index if isinstance(X, pd.DataFrame) else None)
        return X_scaled

def preprocess_data(data, remove_collinearity=True, corr_threshold=ModelConfig.MULTICOLLINEARITY_THRESHOLD, 
                    use_feature_selection=True, selection_threshold=ModelConfig.FEATURE_SELECTION_PERCENTILE):
    """
    特征处理（整合多重共线性处理和特征重要性筛选）
    优化点4: 差异化特征策略 - 不同模型使用不同特征集
    
    返回两个特征集：
    - X_original: 只经过多重共线性处理（给LightGBM用）
    - X_selected: 经过多重共线性+特征筛选（给XGBoost和CatBoost用）
    
    参数：
    - data: DataFrame，原始数据
    - remove_collinearity: bool，是否移除多重共线性特征
    - corr_threshold: float，相关系数阈值
    - use_feature_selection: bool，是否使用特征重要性筛选
    - selection_threshold: int，特征筛选百分位阈值
    """
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    print(f"\n原始数据维度: {X.shape}")
    
    # 1. 处理多重共线性
    removed_features = []
    if remove_collinearity:
        X, removed_features = FeatureEngineer.remove_multicollinearity(X, threshold=corr_threshold)
    
    # 保存多重共线性处理后的特征（给LightGBM用）
    X_after_collinearity = X.copy()
    
    # 2. 特征重要性筛选（只对XGBoost和CatBoost）
    selected_features = []
    feature_importance_df = None
    X_selected = X.copy()
    
    if use_feature_selection:
        X_selected, selected_features, feature_importance_df = FeatureEngineer.select_by_importance(
            X, y, 
            threshold_percentile=selection_threshold,
            method='xgboost'
        )
    
    # 3. 特征标准化
    PrintUtils.print_section("特征标准化")
    
    # 标准化原始特征集（给LightGBM）
    X_original_df = FeatureEngineer.standardize_features(X_after_collinearity, X_after_collinearity.columns)
    
    # 标准化筛选后特征集（给XGBoost和CatBoost）
    X_selected_df = FeatureEngineer.standardize_features(X_selected, X_selected.columns)
    
    print(f"LightGBM特征数: {X_original_df.shape[1]}")
    print(f"XGBoost/CatBoost特征数: {X_selected_df.shape[1]}")
    
    return X_original_df, X_selected_df, y, removed_features, selected_features, feature_importance_df

# ==================== 模型管理模块 ====================

class ModelManager:
    """模型管理类 - 管理所有模型的配置和训练"""
    
    @staticmethod
    def get_base_models():
        """
        获取优化后的基础模型
        优化点3: 多模型集成 - XGBoost + LightGBM + CatBoost
        优化点5: 超参数优化 - 针对性的参数调优
        """
        models = {}
        
        # XGBoost - 使用原生接口支持早停（激进优化）
        models['XGBoost'] = (ModelConfig.XGBOOST_PARAMS.copy(), True)
        
        # LightGBM - 保守优化策略
        try:
            from lightgbm import LGBMClassifier
            models['LightGBM'] = (LGBMClassifier(**ModelConfig.LIGHTGBM_PARAMS), True)
        except ImportError:
            models['LightGBM'] = (None, False)
        
        # CatBoost - 原版稳定参数
        try:
            from catboost import CatBoostClassifier
            models['CatBoost'] = (CatBoostClassifier(**ModelConfig.CATBOOST_PARAMS), True)
        except ImportError:
            models['CatBoost'] = (None, False)
        
        return models
    
    @staticmethod
    def train_with_cv(model_name, model_params, X, y, n_splits=ModelConfig.N_SPLITS):
        """
        训练单个模型（支持早停）
        优化点6: 早停机制 - XGBoost的早停训练
        """
        PrintUtils.print_section(f"训练模型: {model_name}")
        
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=ModelConfig.RANDOM_STATE)
        oof_predictions = np.zeros(len(X))
        cv_scores = []
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
            print(f"  Fold {fold}/{n_splits}...", end=' ')
            
            if isinstance(X, pd.DataFrame):
                X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
                y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            else:
                X_train, X_val = X[train_idx], X[val_idx]
                y_train, y_val = y[train_idx], y[val_idx]
            
            # XGBoost使用早停
            if model_name == 'XGBoost':
                dtrain = xgb.DMatrix(X_train, label=y_train)
                dval = xgb.DMatrix(X_val, label=y_val)
                
                model = xgb.train(
                    model_params,
                    dtrain,
                    num_boost_round=ModelConfig.XGBOOST_ROUNDS,
                    evals=[(dval, 'val')],
                    early_stopping_rounds=ModelConfig.XGBOOST_EARLY_STOPPING,
                    verbose_eval=False
                )
                
                y_pred = model.predict(dval)
            else:
                # LightGBM和CatBoost - 使用原版训练方式
                model_params.fit(X_train, y_train)
                y_pred = model_params.predict_proba(X_val)[:, 1]
            
            oof_predictions[val_idx] = y_pred
            
            auc = roc_auc_score(y_val, y_pred)
            cv_scores.append(auc)
            print(f"AUC: {auc:.4f}")
        
        avg_auc = np.mean(cv_scores)
        std_auc = np.std(cv_scores)
        print(f"\n  {model_name} 平均 AUC: {avg_auc:.4f} ± {std_auc:.4f}")
        
        return oof_predictions, cv_scores, avg_auc

# ==================== 融合策略模块 ====================

class EnsembleStrategy:
    """融合策略类 - 实现多种模型融合方法"""
    
    @staticmethod
    def simple_average(predictions_dict, y_true):
        """简单平均融合"""
        PrintUtils.print_section("策略1: 简单平均融合")
        
        predictions = list(predictions_dict.values())
        ensemble_pred = np.mean(predictions, axis=0)
        auc = roc_auc_score(y_true, ensemble_pred)
        
        print(f"融合模型数量: {len(predictions)}")
        print(f"简单平均 AUC: {auc:.4f}")
        
        return ensemble_pred, auc
    
    @staticmethod
    def weighted_average(predictions_dict, weights, y_true):
        """加权平均融合"""
        PrintUtils.print_section("策略2: 加权平均融合")
        
        predictions = list(predictions_dict.values())
        weights = np.array(weights) / np.sum(weights)
        
        ensemble_pred = np.zeros(len(predictions[0]))
        for pred, weight in zip(predictions, weights):
            ensemble_pred += pred * weight
        
        auc = roc_auc_score(y_true, ensemble_pred)
        
        print(f"模型权重:")
        for name, weight in zip(predictions_dict.keys(), weights):
            print(f"  {name}: {weight:.4f}")
        print(f"加权平均 AUC: {auc:.4f}")
        
        return ensemble_pred, auc
    
    @staticmethod
    def rank_average(predictions_dict, y_true):
        """排名平均融合"""
        PrintUtils.print_section("策略3: 排名平均融合")
        
        rank_predictions = []
        for name, pred in predictions_dict.items():
            ranks = pd.Series(pred).rank(pct=True)
            rank_predictions.append(ranks.values)
        
        ensemble_pred = np.mean(rank_predictions, axis=0)
        auc = roc_auc_score(y_true, ensemble_pred)
        
        print(f"融合模型数量: {len(rank_predictions)}")
        print(f"排名平均 AUC: {auc:.4f}")
        
        return ensemble_pred, auc
    
    @staticmethod
    def stacking(predictions_dict, y_true, n_splits=ModelConfig.N_SPLITS):
        """Stacking融合"""
        PrintUtils.print_section("策略4: Stacking融合")
        
        X_meta = np.column_stack(list(predictions_dict.values()))
        
        print(f"元特征维度: {X_meta.shape}")
        print(f"基模型数量: {len(predictions_dict)}")
        
        y_true_array = y_true if isinstance(y_true, np.ndarray) else y_true.values
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=ModelConfig.RANDOM_STATE)
        meta_predictions = np.zeros(len(y_true_array))
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X_meta, y_true_array), 1):
            X_train, X_val = X_meta[train_idx], X_meta[val_idx]
            y_train, y_val = y_true_array[train_idx], y_true_array[val_idx]
            
            meta_model = LogisticRegression(random_state=ModelConfig.RANDOM_STATE, max_iter=1000)
            meta_model.fit(X_train, y_train)
            meta_predictions[val_idx] = meta_model.predict_proba(X_val)[:, 1]
        
        auc = roc_auc_score(y_true_array, meta_predictions)
        print(f"Stacking AUC: {auc:.4f}")
        
        final_meta = LogisticRegression(random_state=ModelConfig.RANDOM_STATE, max_iter=1000)
        final_meta.fit(X_meta, y_true_array)
        print(f"\n元学习器权重:")
        for name, coef in zip(predictions_dict.keys(), final_meta.coef_[0]):
            print(f"  {name}: {coef:.4f}")
        
        return meta_predictions, auc

# ==================== 主训练流程 ====================

def train_model_with_ensemble(X_original, X_selected, y, n_splits=ModelConfig.N_SPLITS, ensemble_methods='all'):
    """
    使用多个模型和融合策略进行训练
    优化点7: 多融合策略 - 简单平均/加权平均/排名平均/Stacking
    
    参数：
    - X_original: 原始特征（给LightGBM用）
    - X_selected: 筛选后特征（给XGBoost和CatBoost用）
    - y: 目标变量
    """
    PrintUtils.print_section("开始模型融合", 70)
    
    all_models = ModelManager.get_base_models()
    available_models = {name: params for name, (params, available) in all_models.items() if available}
    
    print(f"\n可用的优化模型:")
    for name in available_models.keys():
        feature_info = "原始特征" if name == 'LightGBM' else "筛选特征"
        if name == 'XGBoost':
            param_info = "优化参数+早停"
        elif name == 'LightGBM':
            param_info = "优化参数"
        else:  # CatBoost
            param_info = "原版参数"
        print(f"  ✓ {name} ({param_info} + {feature_info})")
    
    unavailable_models = [name for name, (_, available) in all_models.items() if not available]
    if unavailable_models:
        print(f"\n不可用的模型 (需要安装):")
        for name in unavailable_models:
            print(f"  ✗ {name}")
    
    PrintUtils.print_section("开始训练基础模型", 70)
    print(f"使用 {n_splits} 折交叉验证 + 早停机制")
    print(f"LightGBM: 使用原始特征 ({X_original.shape[1]}个)")
    print(f"XGBoost/CatBoost: 使用筛选特征 ({X_selected.shape[1]}个)")
    
    predictions_dict = {}
    model_scores = {}
    
    for name, params in available_models.items():
        # LightGBM使用原始特征，其他模型使用筛选后的特征
        X_to_use = X_original if name == 'LightGBM' else X_selected
        
        oof_pred, cv_scores, avg_auc = ModelManager.train_with_cv(
            name, params, X_to_use, y, n_splits
        )
        predictions_dict[name] = oof_pred
        model_scores[name] = avg_auc
    
    # 显示基础模型性能对比
    sorted_scores = PrintUtils.print_model_scores(model_scores, "基础模型性能对比")
    
    # 应用模型融合策略
    PrintUtils.print_section("应用模型融合策略", 70)
    
    ensemble_results = {}
    y_array = y if isinstance(y, np.ndarray) else y.values
    
    if ensemble_methods == 'all':
        methods = ['simple', 'weighted', 'rank', 'stacking']
    elif isinstance(ensemble_methods, str):
        methods = [ensemble_methods]
    else:
        methods = ensemble_methods
    
    if 'simple' in methods:
        pred, auc = EnsembleStrategy.simple_average(predictions_dict, y_array)
        ensemble_results['Simple Average'] = auc
    
    if 'weighted' in methods:
        weights = [model_scores[name] for name in predictions_dict.keys()]
        pred, auc = EnsembleStrategy.weighted_average(predictions_dict, weights, y_array)
        ensemble_results['Weighted Average'] = auc
    
    if 'rank' in methods:
        pred, auc = EnsembleStrategy.rank_average(predictions_dict, y_array)
        ensemble_results['Rank Average'] = auc
    
    if 'stacking' in methods:
        pred, auc = EnsembleStrategy.stacking(predictions_dict, y_array, n_splits)
        ensemble_results['Stacking'] = auc
    
    # 最终结果汇总
    PrintUtils.print_section("最终结果汇总", 70)
    
    print(f"\n基础模型:")
    for rank, (name, score) in enumerate(sorted_scores, 1):
        print(f"  {rank}. {name:20s}: {score:.4f}")
    
    if ensemble_results:
        sorted_ensemble = PrintUtils.print_model_scores(ensemble_results, "融合模型")
    
    all_results = {**model_scores, **ensemble_results}
    best_model = max(all_results.items(), key=lambda x: x[1])
    print(f"\n🏆 最佳模型: {best_model[0]}")
    print(f"   AUC分数: {best_model[1]:.4f}")
    
    best_base_auc = max(model_scores.values())
    if ensemble_results:
        best_ensemble_auc = max(ensemble_results.values())
        improvement = best_ensemble_auc - best_base_auc
        improvement_pct = (improvement / best_base_auc) * 100
        print(f"\n📈 融合提升:")
        print(f"   最佳基础模型 AUC: {best_base_auc:.4f}")
        print(f"   最佳融合模型 AUC: {best_ensemble_auc:.4f}")
        print(f"   绝对提升: {improvement:.4f}")
        print(f"   相对提升: {improvement_pct:.2f}%")
    
    return {
        'model_scores': model_scores,
        'ensemble_results': ensemble_results,
        'predictions': predictions_dict,
        'best_model': best_model
    }

# ==================== 主函数 ====================

def main(remove_collinearity=True, 
         corr_threshold=ModelConfig.MULTICOLLINEARITY_THRESHOLD, 
         use_feature_selection=True, 
         selection_threshold=ModelConfig.FEATURE_SELECTION_PERCENTILE,
         ensemble_methods='all', 
         n_splits=ModelConfig.N_SPLITS):
    """
    主函数（模块化重构版）
    优化点8: 模块化架构 - 清晰的代码组织结构
    
    相比基础版本(model.py)的8大优化点：
    1. ✅ 多重共线性处理 - 移除高度相关特征
    2. ✅ 特征重要性筛选 - 基于XGBoost重要性的特征选择
    3. ✅ 多模型集成 - XGBoost + LightGBM + CatBoost
    4. ✅ 差异化特征策略 - 不同模型使用不同特征集
    5. ✅ 超参数优化 - 针对性的参数调优
    6. ✅ 早停机制 - XGBoost的早停训练
    7. ✅ 多融合策略 - 简单平均/加权平均/排名平均/Stacking
    8. ✅ 模块化架构 - 清晰的代码组织结构
    
    差异化策略说明：
    - XGBoost:  筛选特征 + 优化参数 + 早停机制（激进优化）
    - LightGBM: 原始特征 + 优化参数（保守优化策略）
    - CatBoost: 筛选特征 + 原版参数（折中方案）
    
    参数：
    - remove_collinearity: bool，是否移除多重共线性特征
    - corr_threshold: float，相关系数阈值
    - use_feature_selection: bool，是否使用特征重要性筛选
    - selection_threshold: int，保留特征百分位（25=保留前75%）
    - ensemble_methods: str or list, 融合方法
    - n_splits: int, 交叉验证折数
    """
    PrintUtils.print_section("Model V1+V3 Update - 模块化重构版", 70)
    print("差异化优化策略:")
    print("  XGBoost:  筛选特征 + 优化参数 + 早停机制")
    print("  LightGBM: 原始特征 + 优化参数（保守优化）")
    print("  CatBoost: 筛选特征 + 原版参数（折中方案）")
    print("="*70)
    
    print("\n加载数据...")
    data = load_data(ModelConfig.DATA_FILE)
    print(f"数据维度: {data.shape}")
    
    print("\n特征处理...")
    X_original, X_selected, y, removed_features, selected_features, feature_importance_df = preprocess_data(
        data, 
        remove_collinearity=remove_collinearity,
        corr_threshold=corr_threshold,
        use_feature_selection=use_feature_selection,
        selection_threshold=selection_threshold
    )
    
    results = train_model_with_ensemble(
        X_original, X_selected, y, 
        n_splits=n_splits, 
        ensemble_methods=ensemble_methods
    )
    
    print("\n" + "="*70)
    print("完成！")
    print("="*70)
    
    results['removed_features'] = removed_features
    results['selected_features'] = selected_features
    results['feature_importance'] = feature_importance_df
    
    return results

if __name__ == "__main__":
    """
    模块化重构版本执行入口
    
    代码组织结构：
    1. 配置管理模块 (ModelConfig) - 集中管理所有配置参数
    2. 工具函数模块 (PrintUtils) - 统一的输出格式
    3. 特征工程模块 (FeatureEngineer) - 封装所有特征处理方法
    4. 模型管理模块 (ModelManager) - 管理模型配置和训练
    5. 融合策略模块 (EnsembleStrategy) - 实现多种模型融合方法
    6. 主训练流程 (train_model_with_ensemble, main) - 协调各模块
    
    相比基础版本的优势：
    - 代码更易维护：模块化设计，职责清晰
    - 配置更灵活：集中配置管理，易于调整
    - 扩展性更强：新增模型或策略只需修改相应模块
    - 复用性更高：各模块方法可独立使用
    
    核心优化策略：
    1. 特征差异化：
       - LightGBM: 原始特征（105个）+ 保守参数优化
       - XGBoost:  筛选特征（80个）+ 激进参数优化 + 早停
       - CatBoost: 筛选特征（80个）+ 原版稳定参数
    
    2. 配置参数（可在 ModelConfig 中修改）：
       - selection_threshold=25: 保留前75%重要特征
       - corr_threshold=0.95: 多重共线性阈值
       - n_splits=5: 交叉验证折数
       - 各模型的超参数配置
    """
    results = main(
        remove_collinearity=True,                              # 多重共线性处理
        corr_threshold=ModelConfig.MULTICOLLINEARITY_THRESHOLD,  # 相关系数阈值
        use_feature_selection=True,                             # 特征重要性筛选
        selection_threshold=ModelConfig.FEATURE_SELECTION_PERCENTILE,  # 保留前75%特征
        ensemble_methods='all',                                 # 所有融合策略
        n_splits=ModelConfig.N_SPLITS                          # 5折交叉验证
    )
