import pandas as pd
import numpy as np
import os
from main_stand import save_all_models, load_all_models, predict_with_all_models, predict_pipeline

X_test = pd.read_csv('test_feature.csv')

# 测试预测接口
def test_predict_pipeline():
    """测试完整的预测流水线"""
    print("\n测试完整的预测流水线...")
    
    # 检查模型文件是否存在
    model_path = "saved_models/model.pkl"
    if not os.path.exists(model_path):
        print(f"错误: 模型文件 {model_path} 不存在，请先运行训练脚本！")
        return False
    
    # 调用预测流水线
    y_pred_proba, y_pred = predict_pipeline(X_test, model_path, use_ensemble=True)
    
    if y_pred_proba is not None and y_pred is not None:
        print(f"\n预测结果:")
        print(f"预测概率形状: {y_pred_proba.shape}")
        print(f"预测类别形状: {y_pred.shape}")
        print(f"预测概率: {y_pred_proba[:5]}")
        print(f"预测类别: {y_pred[:5]}")
        
        # 将预测结果保存到CSV文件，保持原始特征顺序
        print("\n保存预测结果到CSV文件...")
        # result_df = X_test.copy()
        result_df = pd.DataFrame()
        result_df['pred_proba'] = y_pred_proba
        result_df['pred_class'] = y_pred
        
        # 保存文件
        output_path = "predictions.csv"
        result_df.to_csv(output_path, index=False)
        print(f"预测结果已保存到: {output_path}")
        print(f"输出文件形状: {result_df.shape}")
        return True
    else:
        print("预测流水线执行失败！")
        return False

# 测试单个模型预测
def test_single_model_predict():
    """测试单个模型预测"""
    print("\n测试单个模型预测...")
    
    # 检查模型文件是否存在
    model_path = "saved_models/model.pkl"
    if not os.path.exists(model_path):
        print(f"错误: 模型文件 {model_path} 不存在，请先运行训练脚本！")
        return False
    
    # 加载模型
    from main_stand import load_all_models
    config, all_fold_models = load_all_models(model_path)
    
    if config is None or all_fold_models is None:
        print("模型加载失败！")
        return False
    
    # 测试使用XGBoost模型预测
    y_pred_proba = predict_with_all_models(X_test, all_fold_models, use_ensemble=False, model_name="xgboost")
    
    if y_pred_proba is not None:
        print(f"\nXGBoost模型预测结果:")
        print(f"预测概率形状: {y_pred_proba.shape}")
        print(f"预测概率: {y_pred_proba[:5]}")
        return True
    else:
        print("单个模型预测执行失败！")
        return False

# 运行测试
if __name__ == "__main__":
    print("="*60)
    print("测试预测接口")
    print("="*60)
    
    # 运行测试
    test_predict_pipeline()
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)
