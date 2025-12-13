import numpy as np
from typing import Dict, Any, List, Tuple
from sklearn.base import ClassifierMixin, BaseEstimator
from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

class ModelEnsemble:
    def __init__(self, config: Dict[str, Any], base_models: Dict[str, ClassifierMixin]):
        self.config = config
        self.base_models = base_models
        self.ensemble_model = None
    
    def create_ensemble(self) -> bool:
        """创建融合模型"""
        if not self.config.get("enable", False):
            print("模型融合未启用")
            return False
        
        method = self.config.get("method", "weighted_average")
        params = self.config.get("params", {})
        
        if method == "weighted_average":
            self.ensemble_model = self._create_weighted_average_ensemble(params)
        else:
            print(f"不支持的融合方法: {method}")
            return False
        
        print(f"已创建{method}融合模型")
        return True
    
    def _create_weighted_average_ensemble(self, params: Dict[str, Any]) -> ClassifierMixin:
        """创建加权平均融合模型"""
        weights = params.get("weights", [1.0 / len(self.base_models)] * len(self.base_models))
        
        # 确保权重数量与模型数量一致
        if len(weights) != len(self.base_models):
            print(f"权重数量({len(weights)})与模型数量({len(self.base_models)})不匹配，使用均匀权重")
            weights = [1.0 / len(self.base_models)] * len(self.base_models)
        
        return WeightedAverageEnsemble(
            base_models=list(self.base_models.items()),
            weights=weights
        )
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """训练融合模型"""
        if self.ensemble_model is None:
            raise ValueError("融合模型未创建，请先调用create_ensemble()")
        
        print("训练融合模型...")
        self.ensemble_model.fit(X, y)
    
    def evaluate(self, X: np.ndarray, y: np.ndarray, cv_folds: int = 5) -> Dict[str, float]:
        """评估融合模型"""
        if self.ensemble_model is None:
            raise ValueError("融合模型未创建，请先调用create_ensemble()")
        
        # 创建交叉验证对象
        skf = StratifiedKFold(
            n_splits=cv_folds,
            shuffle=True,
            random_state=self.config.get("data", {}).get("random_state", 42)
        )
        
        auc_scores = []
        
        for fold, (train_index, val_index) in enumerate(skf.split(X, y)):
            print(f"\n融合模型第 {fold+1} 折交叉验证")
            
            # 分割数据
            X_train, X_val = X[train_index], X[val_index]
            y_train, y_val = y[train_index], y[val_index]
            
            # 训练模型
            fold_model = self.ensemble_model.__class__(
                **self.ensemble_model.get_params()
            )
            fold_model.fit(X_train, y_train)
            
            # 预测概率
            y_pred_proba = fold_model.predict_proba(X_val)[:, 1]
            
            # 计算AUC
            auc = roc_auc_score(y_val, y_pred_proba)
            auc_scores.append(auc)
            print(f"第 {fold+1} 折 AUC: {auc:.4f}")
        
        # 计算平均AUC
        avg_auc = np.mean(auc_scores)
        std_auc = np.std(auc_scores)
        
        print(f"\n融合模型平均 AUC: {avg_auc:.4f}, 标准差: {std_auc:.4f}")
        
        return {
            "avg_auc": avg_auc,
            "std_auc": std_auc,
            "auc_scores": auc_scores
        }
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """预测概率"""
        if self.ensemble_model is None:
            raise ValueError("融合模型未创建，请先调用create_ensemble()")
        
        return self.ensemble_model.predict_proba(X)[:, 1]
    
    def get_ensemble_model(self) -> ClassifierMixin:
        """获取融合模型"""
        return self.ensemble_model

class WeightedAverageEnsemble(BaseEstimator, ClassifierMixin):
    """加权平均融合模型"""
    def __init__(self, base_models: List[Tuple[str, ClassifierMixin]], weights: List[float]):
        self.base_models = base_models
        self.weights = weights
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> "WeightedAverageEnsemble":
        """训练所有基模型"""
        for name, model in self.base_models:
            model.fit(X, y)
        return self
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """预测概率"""
        # 获取所有基模型的预测概率
        predictions = []
        for name, model in self.base_models:
            pred = model.predict_proba(X)[:, 1]
            predictions.append(pred)
        
        # 加权平均
        weighted_avg = np.average(predictions, axis=0, weights=self.weights)
        
        # 返回概率矩阵 [1-p, p]
        return np.column_stack([1 - weighted_avg, weighted_avg])
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """预测类别"""
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)