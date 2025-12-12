import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score
from lightgbm import LGBMClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFromModel, VarianceThreshold
from sklearn.linear_model import LassoCV
from sklearn.ensemble import RandomForestClassifier
import time


# LASSO特征选择
def _lasso_feature_selection(X, X_scaled, y, alpha=0.01):
    print(f"\n=== LASSO特征选择 (alpha={alpha}) ===")
    
    # LASSO特征选择
    lasso = LassoCV(cv=5, random_state=42, max_iter=10000)
    lasso.fit(X_scaled.values, y)
    
    # 选择非零系数的特征
    selected_features = np.abs(lasso.coef_) > 0
    X_lasso = X.iloc[:, selected_features]
    
    print(f"选择的特征数量: {X_lasso.shape[1]}")
    return X_lasso 


# 运行所有模型并比较结果
def lasso_feature_selection(train_data: pd.DataFrame, 
                            label_name: str = 'label', 
                            id_name: str or None = 'id',
                            alpha: float = 0.01, 
                            file_name: str = 'lasso_reduce.csv'):
    """
    输入数据需要带着标签，不要预处理，对于不需要的列比如id需要自己处理。
    输出为筛选后的原始数据，并带着标签列
    最终输出为file_name,建议为csv格式
    train_data: 输入数据，不需要预处理，但需要自己处理不需要参数筛选的列，比如id，需要带有标签列
    label_name: 标签列名，需要在train_data中
    alpha: LASSO正则化参数，默认0.01
    file_name: 输出文件名，默认lasso_reduce.csv
    """
    if not label_name:
        raise ValueError('该方法label_name必须指定')
    if label_name not in train_data.columns:
        raise ValueError(f'label_name {label_name} 不在train_data中')
    X = train_data.drop([label_name], axis=1)
    y = train_data[label_name]
    id_num = train_data[id_name] if id_name else None
    if id_num is not None:
        X = X.drop([id_name], axis=1)


    print(f"原始数据特征数量: {X.shape[1]}")
    print(f"样本数量: {X.shape[0]}")

    # 处理非数值数据
    print("\n处理非数值数据...")
    # 检查并转换数据类型
    for col in X.columns:
        # 尝试将列转换为数值类型
        X[col] = pd.to_numeric(X[col], errors='coerce')

    # 检查是否还有非数值列
    print(f"处理后数据类型: {X.dtypes.unique()}")

    # 填充缺失值（先检查是否有全NaN列）
    print(f"原始数据缺失值数量: {X.isna().sum().sum()}")

    # 首先使用中位数填充，然后检查是否还有NaN值
    X = X.fillna(X.median())

    # 如果还有NaN值（可能是因为整列都是NaN），使用0填充
    X = X.fillna(0)

    print(f"处理后缺失值数量: {X.isna().sum().sum()}")

    # 标准化数据
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    
    # LASSO特征选择
    X_scaled_res = _lasso_feature_selection(X, X_scaled, y, alpha=alpha)
    if id_num is not None:
        X_scaled_res[id_name] = id_num
    X_scaled_res[label_name] = y
    
    X_scaled_res.to_csv(file_name, index=False)
    return X_scaled_res


if __name__ == "__main__":
    train_data = pd.read_csv('team_merged_train.csv')
    res = lasso_feature_selection(train_data, 'label', 'id', 0.01)
    print(res.iloc[0])