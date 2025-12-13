import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_score, recall_score
from sklearn.base import ClassifierMixin

class ModelEvaluator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cv_folds = config.get("evaluation", {}).get("cv_folds", 5)
        self.random_state = config.get("data", {}).get("random_state", 42)
        self.metrics = config.get("evaluation", {}).get("metrics", ["auc"])
    
    def evaluate_single_model(self, X: Any, y: np.ndarray, model: ClassifierMixin, model_name: str) -> Dict[str, Any]:
        """评估单个模型"""
        print(f"\n开始评估模型: {model_name}")
        
        # 将DataFrame转换为numpy数组
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        # 创建5折交叉验证对象
        skf = StratifiedKFold(
            n_splits=self.cv_folds,
            shuffle=True,
            random_state=self.random_state
        )
        
        # 初始化评估指标结果
        results = {
            "model_name": model_name,
            "cv_folds": self.cv_folds,
            "metrics": {
                "auc": [],
                "accuracy": [],
                "f1": [],
                "precision": [],
                "recall": []
            }
        }
        
        # 获取模型类和参数，用于后续重新创建模型
        model_class = model.__class__
        model_params = model.get_params()
        
        # 进行5折交叉验证
        for fold, (train_index, val_index) in enumerate(skf.split(X, y)):
            print(f"第 {fold+1} 折交叉验证")
            
            # 分割数据
            X_train, X_val = X[train_index], X[val_index]
            y_train, y_val = y[train_index], y[val_index]
            
            # 重新创建模型实例
            fold_model = model_class(**model_params)
            
            # 训练模型
            fold_model.fit(X_train, y_train)
            
            # 预测概率和类别
            y_pred_proba = fold_model.predict_proba(X_val)[:, 1]
            y_pred = (y_pred_proba >= 0.5).astype(int)
            
            # 计算各指标
            auc = roc_auc_score(y_val, y_pred_proba)
            accuracy = accuracy_score(y_val, y_pred)
            f1 = f1_score(y_val, y_pred)
            precision = precision_score(y_val, y_pred)
            recall = recall_score(y_val, y_pred)
            
            # 保存结果
            results["metrics"]["auc"].append(auc)
            results["metrics"]["accuracy"].append(accuracy)
            results["metrics"]["f1"].append(f1)
            results["metrics"]["precision"].append(precision)
            results["metrics"]["recall"].append(recall)
            
            # 打印当前折的结果
            if self.config.get("evaluation", {}).get("verbose", True):
                print(f"第 {fold+1} 折结果:")
                print(f"  AUC: {auc:.4f}")
                print(f"  Accuracy: {accuracy:.4f}")
                print(f"  F1: {f1:.4f}")
                print(f"  Precision: {precision:.4f}")
                print(f"  Recall: {recall:.4f}")
        
        # 计算平均指标
        results["average_metrics"] = {}
        for metric, scores in results["metrics"].items():
            results["average_metrics"][metric] = np.mean(scores)
            results["average_metrics"][f"{metric}_std"] = np.std(scores)
        
        # 打印平均结果
        print(f"\n{model_name} 平均评估结果:")
        for metric, avg_score in results["average_metrics"].items():
            if "std" in metric:
                print(f"  {metric}: {avg_score:.4f}")
            else:
                print(f"  {metric}: {avg_score:.4f} (±{results['average_metrics'][f'{metric}_std']:.4f})")
        
        return results
    
    def evaluate_multiple_models(self, X: np.ndarray, y: np.ndarray, models: Dict[str, ClassifierMixin]) -> Dict[str, Dict[str, Any]]:
        """评估多个模型"""
        all_results = {}
        for model_name, model in models.items():
            results = self.evaluate_single_model(X, y, model, model_name)
            all_results[model_name] = results
        return all_results
    
    def evaluate_ensemble(self, X: np.ndarray, y: np.ndarray, ensemble_model: ClassifierMixin, ensemble_name: str = "ensemble") -> Dict[str, Any]:
        """评估融合模型"""
        return self.evaluate_single_model(X, y, ensemble_model, ensemble_name)
    
    def generate_evaluation_report(self, results: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
        """生成评估报告"""
        report_data = []
        
        for model_name, result in results.items():
            row = {
                "model_name": model_name
            }
            
            # 添加平均指标
            for metric, value in result["average_metrics"].items():
                row[metric] = value
            
            report_data.append(row)
        
        # 创建DataFrame
        df_report = pd.DataFrame(report_data)
        
        # 按AUC排序
        if "auc" in df_report.columns:
            df_report = df_report.sort_values(by="auc", ascending=False)
        
        # 重置索引
        df_report = df_report.reset_index(drop=True)
        
        return df_report
    
    def print_evaluation_report(self, report_df: pd.DataFrame) -> None:
        """打印评估报告"""
        print("\n" + "="*60)
        print("模型评估报告")
        print("="*60)
        print(report_df.to_string(index=False, float_format="{:.4f}".format))
        print("="*60)
    
    def save_evaluation_report(self, report_df: pd.DataFrame, file_path: str = "evaluation_report.csv") -> None:
        """保存评估报告到文件"""
        report_df.to_csv(file_path, index=False, float_format="{:.4f}".format)
        print(f"\n评估报告已保存到: {file_path}")
    
    def compare_models(self, results: Dict[str, Dict[str, Any]]) -> str:
        """比较模型，返回最佳模型名称"""
        best_model = None
        best_auc = -1
        
        for model_name, result in results.items():
            auc = result["average_metrics"]["auc"]
            if auc > best_auc:
                best_auc = auc
                best_model = model_name
        
        if best_model:
            print(f"\n最佳模型: {best_model}，平均AUC: {best_auc:.4f}")
        
        return best_model
    
    def get_best_model_results(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """获取最佳模型结果"""
        best_model = self.compare_models(results)
        return results[best_model] if best_model else None