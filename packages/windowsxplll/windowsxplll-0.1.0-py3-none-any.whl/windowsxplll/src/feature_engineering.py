from typing import Tuple, Dict, Any, Optional

import numpy as np
import optuna
import pandas as pd
from optbinning import BinningProcess
from sklearn.feature_selection import RFE, SelectFromModel
from sklearn.linear_model import Lasso
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

# ==================== 配置管理 ====================


class ModelConfig:
    """模型配置类 - 集中管理所有配置参数"""

    # 特征工程配置
    MULTICOLLINEARITY_THRESHOLD = 0.95
    FEATURE_SELECTION_PERCENTILE = 25  # 保留前75%特征
    RANDOM_STATE = 42


# ==================== 工具函数 ====================


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


# ==================== 分箱相关函数 ====================


def decision_tree_binning_objective(trial, X, y, n_splits=5, replace=False):
    """决策树分箱参数优化的目标函数"""
    # 建议参数范围
    max_depth = trial.suggest_int("max_depth", 2, 8)
    min_samples_leaf = trial.suggest_float("min_samples_leaf", 0.01, 0.2)

    # 使用分箱后的数据训练XGB模型并评估AUC
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    auc_scores = []

    for train_index, val_index in skf.split(X, y):
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, pd.Series):
            y = y.values

        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]
        new_feats_train = []
        new_feats_val = []
        for col in range(X_train.shape[1]):
            dt = DecisionTreeClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=42)
            dt.fit(X_train[:, col].reshape(-1, 1), y_train)
            bins = np.sort(dt.tree_.threshold[dt.tree_.threshold != -2])
            if len(bins) > 0:
                new_col_train = np.digitize(X_train[:, col], bins)
                new_col_val = np.digitize(X_val[:, col], bins)
                if replace:
                    X_train[:, col] = new_col_train
                    X_val[:, col] = new_col_val
                else:
                    new_feats_train.append(new_col_train)
                    new_feats_val.append(new_col_val)
        X_train = np.column_stack((X_train, *new_feats_train))
        X_val = np.column_stack((X_val, *new_feats_val))

        # 训练模型
        model = XGBClassifier(random_state=42, eval_metric="auc")
        model.fit(X_train, y_train)

        # 预测并计算AUC
        y_pred_proba = model.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, y_pred_proba)
        auc_scores.append(auc)

    return np.mean(auc_scores)


def tune_decision_tree_binning(X, y, n_trials=10, replace=False):
    """使用Optuna优化决策树分箱参数"""
    print("开始决策树分箱参数调优...")

    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
    study.optimize(lambda trial: decision_tree_binning_objective(trial, X, y, replace=replace), n_trials=n_trials)

    print(f"\n决策树分箱最佳参数: {study.best_params}")
    print(f"最佳AUC: {study.best_value:.4f}")

    return study.best_params


def decision_tree_binning(
    X,
    y=None,
    max_depth=3,
    min_samples_leaf=0.05,
    tune_params=False,
    n_trials=10,
    bins_dict=None,
    replace=False,
):
    """使用决策树对连续型变量进行分箱，支持参数调优和测试集一致性处理

    Args:
        X: 输入特征数据 (DataFrame 或 numpy array)
        y: 目标变量 (用于训练时拟合分箱，测试时不需要)
        max_depth: 决策树最大深度
        min_samples_leaf: 叶节点最小样本比例
        tune_params: 是否调优参数
        n_trials: 调优尝试次数
        bins_dict: 预先计算的分箱信息 (用于测试集应用已训练的分箱规则)

    Returns:
        X_binned: 分箱后的特征数据
        bins_info: 分箱信息字典 (仅在训练时返回，测试时不返回)
    """
    PrintUtils.print_section("执行决策树分箱")
    print(f"原始特征数量: {X.shape[1]}")

    # 如果提供了bins_dict，则说明是对测试集进行分箱
    if bins_dict is not None:
        print("应用预训练的分箱规则到测试集...")
        return _apply_precomputed_binning(X, bins_dict, replace=replace)

    # 训练模式：需要拟合分箱规则
    # 如果需要调优参数
    if tune_params and y is not None:
        best_params = tune_decision_tree_binning(X, y, n_trials=n_trials, replace=replace)
        max_depth = best_params["max_depth"]
        min_samples_leaf = best_params["min_samples_leaf"]

    # 检查X的类型
    is_df = hasattr(X, "iloc")

    X_binned = X.copy()
    bins_info = {}

    # 对每个特征进行分箱
    if is_df:
        # X是DataFrame
        new_feats = {}
        cols_to_remove = []
        for col in X.columns:
            dt = DecisionTreeClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=42)
            dt.fit(X[[col]], y)
            bins = np.sort(dt.tree_.threshold[dt.tree_.threshold != -2])
            bins_info[col] = bins  # 保存分箱边界
            if len(bins) > 0:
                binned = np.digitize(X[col], bins)
                if replace:
                    X_binned[col] = binned
                else:
                    new_feats[f"{col}_binned"] = binned
            else:
                cols_to_remove.append(col)
        if replace:
            # drop 分箱后没有有效分箱边界的特征
            X_binned.drop(columns=cols_to_remove, inplace=True)
        else:
            X_binned = pd.concat([X_binned, pd.DataFrame(new_feats, index=X_binned.index)], axis=1)
    else:
        # X是numpy数组
        new_feats = []
        cols_to_remove = []
        for i in range(X.shape[1]):
            dt = DecisionTreeClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=42)
            dt.fit(X[:, i].reshape(-1, 1), y)
            bins = np.sort(dt.tree_.threshold[dt.tree_.threshold != -2])
            bins_info[f"feature_{i}"] = bins  # 保存分箱边界
            if len(bins) > 0:
                binned = np.digitize(X[:, i], bins)
                if replace:
                    X_binned[:, i] = binned
                else:
                    new_feats.append(binned)
            else:
                cols_to_remove.append(i)
        if replace:
            # drop 分箱后没有有效分箱边界的特征
            X_binned = np.delete(X_binned, cols_to_remove, axis=1)
        else:
            X_binned = np.concatenate([X_binned, *new_feats], axis=1)

    print(f"决策树分箱后特征数量: {X_binned.shape[1]}")
    return X_binned, bins_info


def _apply_precomputed_binning(X, bins_dict, replace=False):
    """应用预先计算的分箱规则到数据"""
    is_df = hasattr(X, "iloc")
    X_binned = X.copy()

    col_no_bins = []
    if is_df:
        # X是DataFrame
        new_feats = {}
        for col in X.columns:
            if col in bins_dict:
                bins = bins_dict[col]
                binned = np.digitize(X[col], bins)
                if len(bins) > 0:
                    if replace:
                        X_binned[col] = binned
                    else:
                        new_feats[f"{col}_binned"] = binned
                else:
                    col_no_bins.append(col)
        if replace:
            X_binned.drop(columns=col_no_bins, inplace=True)
        else:
            X_binned = pd.concat([X_binned, pd.DataFrame(new_feats, index=X_binned.index)], axis=1)
    else:
        # X是numpy数组
        for i in range(X.shape[1]):
            col_name = f"feature_{i}"
            if col_name in bins_dict:
                bins = bins_dict[col_name]
                if len(bins) > 0:
                    binned = np.digitize(X[:, i], bins)
                    if replace:
                        X_binned[:, i] = binned
                    else:
                        new_feats.append(binned)
                else:
                    col_no_bins.append(col_name)
        if replace:
            X_binned = np.delete(X_binned, col_no_bins, axis=1)
        else:
            X_binned = np.concatenate([X_binned, *new_feats], axis=1)

    if len(col_no_bins) > 0:
        print(f"警告: 以下特征没有有效分箱边界, 将不进行分箱: {col_no_bins}")
    return X_binned


def opt_iv_binning(X, y, categorical_threshold=20):
    """
    使用最大化IV值法对特征进行分箱, 利用optbinning库

    默认特征unique值数量小于等于20的为类别型特征
    """
    PrintUtils.print_section("执行IV值分箱")
    print(f"原始特征数量: {X.shape[1]}")
    # 获取特征名称
    variable_names = X.columns.tolist()

    categorical_variables = [col for col in variable_names if len(X[col].unique()) <= categorical_threshold]

    # 应用最优分箱处理数值特征
    binning_process = BinningProcess(
        variable_names=variable_names,
        categorical_variables=categorical_variables,
        binning_fit_params={"random_state": 42},
    )
    X_binned = binning_process.fit_transform(X, y)

    print(f"IV值分箱后特征数量: {X_binned.shape[1]}")
    return X_binned


# ==================== 增强特征工程类 ====================


class EnhancedFeatureEngineer:
    """增强特征工程类 - 封装所有增强特征处理方法"""

    @staticmethod
    def remove_multicollinearity(X, threshold=ModelConfig.MULTICOLLINEARITY_THRESHOLD):
        """
        处理多重共线性问题
        """
        PrintUtils.print_section("处理多重共线性")
        print(f"原始特征数量: {X.shape[1]}")

        # 计算相关系数矩阵
        corr_matrix = X.corr().abs()
        upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

        # 找出高度相关的特征对
        high_corr_pairs = []
        for column in upper_triangle.columns:
            correlated_features = upper_triangle[column][upper_triangle[column] > threshold]
            if len(correlated_features) > 0:
                for corr_feature in correlated_features.index:
                    high_corr_pairs.append(
                        {
                            "feature1": column,
                            "feature2": corr_feature,
                            "correlation": upper_triangle.loc[corr_feature, column],
                        }
                    )

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

        X_reduced = X.drop(columns=list(to_drop), errors="ignore")

        # 打印统计信息
        if len(to_drop) > 0:
            print(f"\n被移除的特征: {sorted(list(to_drop))[:20]}")
            if len(to_drop) > 20:
                print(f"  ... 还有 {len(to_drop) - 20} 个特征")

        PrintUtils.print_feature_stats(X.shape[1], X_reduced.shape[1], len(to_drop))

        return X_reduced, list(to_drop)

    @staticmethod
    def select_by_importance(X, y, threshold_percentile=ModelConfig.FEATURE_SELECTION_PERCENTILE, method="xgboost"):
        """
        基于特征重要性进行特征筛选
        """
        PrintUtils.print_section("特征重要性筛选")
        print(f"原始特征数量: {X.shape[1]}")
        print(f"使用模型: {method}")

        # 训练模型获取特征重要性
        if method == "xgboost":
            model = XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=ModelConfig.RANDOM_STATE,
                eval_metric="auc",
            )
        elif method == "lightgbm":
            try:
                from lightgbm import LGBMClassifier

                model = LGBMClassifier(
                    n_estimators=100, max_depth=6, learning_rate=0.1, random_state=ModelConfig.RANDOM_STATE, verbose=-1
                )
            except ImportError:
                print("LightGBM未安装，使用XGBoost")
                model = XGBClassifier(n_estimators=100, random_state=ModelConfig.RANDOM_STATE)
        elif method == "catboost":
            try:
                from catboost import CatBoostClassifier

                model = CatBoostClassifier(
                    iterations=100, depth=6, learning_rate=0.1, random_state=ModelConfig.RANDOM_STATE, verbose=0
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
        feature_importance_df = pd.DataFrame({"feature": X.columns, "importance": importances}).sort_values(
            "importance", ascending=False
        )

        # 计算阈值
        threshold = np.percentile(importances, threshold_percentile)

        # 筛选重要特征
        important_features = feature_importance_df[feature_importance_df["importance"] > threshold]["feature"].tolist()

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
                imp = feature_importance_df[feature_importance_df["feature"] == f]["importance"].values[0]
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


def preprocess_enhanced_data(
    data,
    remove_collinearity=True,
    corr_threshold=ModelConfig.MULTICOLLINEARITY_THRESHOLD,
    use_feature_selection=True,
    selection_threshold=ModelConfig.FEATURE_SELECTION_PERCENTILE,
):
    """
    增强特征处理（整合多重共线性处理和特征重要性筛选）

    返回两个特征集：
    - X_original: 只经过多重共线性处理（给LightGBM用）
    - X_selected: 经过多重共线性+特征筛选（给XGBoost和CatBoost用）
    """
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    print(f"\n原始数据维度: {X.shape}")

    # 1. 处理多重共线性
    removed_features = []
    if remove_collinearity:
        X, removed_features = EnhancedFeatureEngineer.remove_multicollinearity(X, threshold=corr_threshold)

    # 保存多重共线性处理后的特征（给LightGBM用）
    X_after_collinearity = X.copy()

    # 2. 特征重要性筛选
    selected_features = []
    feature_importance_df = None
    X_selected = X.copy()

    if use_feature_selection:
        X_selected, selected_features, feature_importance_df = EnhancedFeatureEngineer.select_by_importance(
            X, y, threshold_percentile=selection_threshold, method="xgboost"
        )

    # 3. 特征标准化
    PrintUtils.print_section("特征标准化")

    # 标准化原始特征集（给LightGBM）
    X_original_df = EnhancedFeatureEngineer.standardize_features(X_after_collinearity, X_after_collinearity.columns)

    # 标准化筛选后特征集（给XGBoost和CatBoost）
    X_selected_df = EnhancedFeatureEngineer.standardize_features(X_selected, X_selected.columns)

    print(f"LightGBM特征数: {X_original_df.shape[1]}")
    print(f"XGBoost/CatBoost特征数: {X_selected_df.shape[1]}")

    return X_original_df, X_selected_df, y


class FeatureEngineering:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.feature_selector = None

    def process(self, data: pd.DataFrame) -> Tuple[Any, Optional[np.ndarray]]:
        """执行特征工程

        Args:
            data: 输入数据

        Returns:
            处理后的特征矩阵和目标变量（预测模式下目标变量为None）
            - 当使用增强特征工程时，返回一个字典，包含两个特征集：'original'和'selected'
            - 否则返回单个特征矩阵
        """
        # 检查是否启用特征工程
        fe_config = self.config.get("feature_engineering", self.config)
        fe_enable = fe_config.get("enable", True)

        # 如果不启用特征工程
        if not fe_enable:
            # 分离特征和目标变量
            X, y = self._split_features_target(data)
            return X.values, y.values

        # 检查是否启用增强特征工程
        enhanced_fe_config = fe_config.get("enhanced_feature_engineering", {})
        enhanced_enabled = enhanced_fe_config.get("enable", False)

        # 如果启用增强特征工程且不是预测模式，使用增强特征工程流程
        if enhanced_enabled:
            # 使用增强特征工程流程
            PrintUtils.print_section("执行增强特征工程")

            # 获取配置参数
            corr_threshold = enhanced_fe_config.get("corr_threshold", ModelConfig.MULTICOLLINEARITY_THRESHOLD)
            selection_threshold = enhanced_fe_config.get(
                "selection_threshold", ModelConfig.FEATURE_SELECTION_PERCENTILE
            )
            remove_collinearity = enhanced_fe_config.get("remove_collinearity", True)
            use_feature_selection = enhanced_fe_config.get("use_feature_selection", True)

            # 执行增强特征工程
            X_original, X_selected, y = preprocess_enhanced_data(
                data,
                remove_collinearity=remove_collinearity,
                corr_threshold=corr_threshold,
                use_feature_selection=use_feature_selection,
                selection_threshold=selection_threshold,
            )

            # 返回包含两个特征集的字典
            feature_sets = {"original": X_original, "selected": X_selected}

            return feature_sets, y.values
        else:
            # 分离特征和目标变量
            X, y = self._split_features_target(data)

            # 特征缩放和缺失值处理配置已移除，相关逻辑已精简
            # 如需启用，请在config.yaml中重新添加相应配置

            # 特征选择
            if fe_config.get("feature_selection", {}).get("enable", False) and y is not None:
                X = self._select_features(X, y)

            return X, y.values if y is not None else None

    def _split_features_target(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """分离特征和目标变量"""
        target_column = self.config.get("data", {}).get("target_column")
        if target_column is None:
            # 假设最后一列是目标变量
            X = data.iloc[:, :-1]
            y = data.iloc[:, -1]
        else:
            X = data.drop(columns=[target_column])
            y = data[target_column]
        return X, y

    # _handle_missing_values和_scale_features方法已删除，因为相关配置已移除
    # 如需重新启用，请在config.yaml中添加相应配置并恢复方法实现

    def _select_features(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """特征选择"""
        selection_config = self.config.get("feature_selection", {})
        method = selection_config.get("method", "lasso")
        params = selection_config.get("params", {})

        if method == "lasso":
            return self._select_features_lasso(X, y, params)
        elif method == "tree_importance":
            return self._select_features_tree_importance(X, y, params)
        elif method == "rfe":
            return self._select_features_rfe(X, y, params)
        else:
            return X

    def _select_features_lasso(self, X: np.ndarray, y: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        """使用LASSO进行特征选择"""
        threshold = params.get("threshold", 0.01)
        lasso = Lasso(alpha=0.1, random_state=self.config.get("data", {}).get("random_state", 42))
        selector = SelectFromModel(lasso, threshold=threshold)
        self.feature_selector = selector
        return selector.fit_transform(X, y)

    def _select_features_tree_importance(self, X: np.ndarray, y: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        """使用树模型特征重要性进行选择"""
        # 这里使用XGBoost作为默认的树模型
        from xgboost import XGBClassifier

        threshold = params.get("threshold", "mean")
        model = XGBClassifier(random_state=self.config.get("data", {}).get("random_state", 42), n_estimators=100)
        selector = SelectFromModel(model, threshold=threshold)
        self.feature_selector = selector
        return selector.fit_transform(X, y)

    def _select_features_rfe(self, X: np.ndarray, y: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        """使用递归特征消除进行选择"""
        from sklearn.ensemble import RandomForestClassifier

        n_features_to_select = params.get("n_features_to_select", 0.8)
        model = RandomForestClassifier(
            random_state=self.config.get("data", {}).get("random_state", 42), n_estimators=100
        )
        selector = RFE(model, n_features_to_select=n_features_to_select)
        self.feature_selector = selector
        return selector.fit_transform(X, y)

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """使用已拟合的变换器转换新数据"""
        if not self.config.get("enable", True):
            return X.values

        # 特征选择
        if self.feature_selector is not None:
            X = self.feature_selector.transform(X)

        return X
