import os

import optuna
import pandas as pd
import numpy as np
import yaml
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier


def load_data(file_path):
    """加载数据"""
    data = pd.read_csv(file_path)
    return data


def preprocess_data(data):
    """特征处理"""
    # 分离特征和目标变量
    # 假设最后一列是目标变量
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    # 特征标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y


def load_search_space(config_path):
    """加载搜索空间配置"""
    with open(config_path, "r") as f:
        search_space = yaml.safe_load(f)
    return search_space


def objective(trial, X, y, search_space, n_splits=5, model_type='xgboost'):
    """Optuna优化目标函数"""
    # 根据搜索空间生成参数
    params = {"random_state": 42}
    
    # 根据模型类型设置默认参数和评估指标
    if model_type == 'xgboost':
        params["eval_metric"] = "auc"
    elif model_type == 'lightgbm':
        params["metric"] = "auc"
    elif model_type == 'catboost':
        params["eval_metric"] = "AUC"

    for param_name, config in search_space.items():
        dist_type = config["distribution"]
        low = config["low"]
        high = config["high"]

        if dist_type == "int":
            params[param_name] = trial.suggest_int(param_name, low, high)
        elif dist_type == "float":
            params[param_name] = trial.suggest_float(param_name, low, high)
        elif dist_type == "uniform":
            params[param_name] = trial.suggest_float(param_name, low, high, log=False)
        elif dist_type == "loguniform":
            params[param_name] = trial.suggest_float(param_name, low, high, log=True)

    # 5折交叉验证
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    auc_scores = []

    for train_index, val_index in skf.split(X, y):
        # 检查X的数据类型
        if isinstance(X, pd.DataFrame):
            X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        else:
            X_train, X_val = X[train_index], X[val_index]
        
        # 检查y的数据类型
        if isinstance(y, pd.Series):
            y_train, y_val = y.iloc[train_index], y.iloc[val_index]
        else:
            y_train, y_val = y[train_index], y[val_index]

        # 根据模型类型选择模型和默认参数
        if model_type == 'xgboost':
            default_params = {
                "objective": "binary:logistic",
            }
            model = XGBClassifier(**default_params, **params)
        elif model_type == 'lightgbm':
            default_params = {
                "objective": "binary",
            }
            model = LGBMClassifier(**default_params, **params, verbose=-1)
        elif model_type == 'catboost':
            default_params = {
                "objective": "Logloss",
            }
            model = CatBoostClassifier(**default_params, **params, verbose=False)
        else:
            raise ValueError(f"不支持的模型类型: {model_type}")

        model.fit(X_train, y_train)

        y_pred_proba = model.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, y_pred_proba)
        auc_scores.append(auc)

    return np.mean(auc_scores)


def tune_hyperparameters(X, y, search_space, n_trials=50, n_splits=5, model_type='xgboost'):
    """使用Optuna进行超参数调优"""
    print(f"开始超参数调优...模型类型: {model_type}")

    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
    study.optimize(lambda trial: objective(trial, X, y, search_space, n_splits, model_type), n_trials=n_trials)

    print(f"\n最佳参数: {study.best_params}")
    print(f"最佳AUC: {study.best_value:.4f}")

    return study.best_params


def train_model_with_cv(X, y, n_splits=5, model_type='xgboost', **kwargs):
    """使用5折交叉验证训练模型"""
    # 创建5折交叉验证对象
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    auc_scores = []

    # 打印参数信息
    print(f"使用参数: {', '.join([f'{k}={v}' for k, v in kwargs.items()])}")

    # 进行5折交叉验证
    for fold, (train_index, val_index) in enumerate(skf.split(X, y)):
        print(f"第 {fold+1} 折交叉验证")

        # 分割数据
        # 检查X的数据类型
        if isinstance(X, pd.DataFrame):
            X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        else:
            X_train, X_val = X[train_index], X[val_index]
        
        # 检查y的数据类型
        if isinstance(y, pd.Series):
            y_train, y_val = y.iloc[train_index], y.iloc[val_index]
        else:
            y_train, y_val = y[train_index], y[val_index]

        # 根据模型类型选择模型和默认参数
        if model_type == 'xgboost':
            default_params = {
                "objective": "binary:logistic",
                "eval_metric": "auc",
                "random_state": 42
            }
            model = XGBClassifier(**default_params, **kwargs)
        elif model_type == 'lightgbm':
            default_params = {
                "objective": "binary",
                "metric": "auc",
                "random_state": 42,
                "verbose": -1
            }
            model = LGBMClassifier(**default_params, **kwargs)
        elif model_type == 'catboost':
            default_params = {
                "objective": "Logloss",
                "eval_metric": "AUC",
                "random_state": 42,
                "verbose": False
            }
            model = CatBoostClassifier(**default_params, **kwargs)
        else:
            raise ValueError(f"不支持的模型类型: {model_type}")

        # 训练模型
        model.fit(X_train, y_train)

        # 预测概率
        y_pred_proba = model.predict_proba(X_val)[:, 1]

        # 计算AUC
        auc = roc_auc_score(y_val, y_pred_proba)
        auc_scores.append(auc)
        print(f"第 {fold+1} 折 AUC: {auc:.4f}")

    # 计算平均AUC
    avg_auc = np.mean(auc_scores)
    print(f"\n平均 AUC: {avg_auc:.4f}")

    return avg_auc, auc_scores


def main(tune_hyper=False, n_trials=50):
    """主函数"""
    # 数据文件路径
    file_path = "./lasso_reduce.csv"

    # 检查数据文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 数据文件 {file_path} 不存在！")
        print("请确保数据文件存在于当前目录，或修改代码中的file_path变量。")
        return None, None

    # 检查配置文件是否存在
    config_path = os.path.join(os.path.dirname(__file__), "xgb_search_space.yaml")
    if tune_hyper and not os.path.exists(config_path):
        print(f"错误: 配置文件 {config_path} 不存在！")
        return None, None

    # 加载数据
    print("加载数据...")
    data = load_data(file_path)

    # 特征处理
    print("特征处理...")
    X, y = preprocess_data(data)

    if tune_hyper:
        # 加载搜索空间
        search_space = load_search_space(config_path)

        # 超参数调优
        best_params = tune_hyperparameters(X, y, search_space, n_trials=n_trials)

        # 使用最佳参数训练模型
        print("\n使用最佳参数进行最终模型训练...")
        avg_auc, auc_scores = train_model_with_cv(X, y, **best_params)
    else:
        # 使用默认参数训练模型
        print("开始5折交叉验证训练...")
        avg_auc, auc_scores = train_model_with_cv(X, y)

    return avg_auc, auc_scores


if __name__ == "__main__":
    # 开启超参数调优，默认50次试验
    main(tune_hyper=True, n_trials=50)
