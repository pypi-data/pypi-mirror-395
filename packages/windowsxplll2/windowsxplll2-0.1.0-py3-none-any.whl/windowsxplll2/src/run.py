"""
Multi-round Semi-supervised Learning (Exported Version)

核心策略：
1. 去除MLP，仅使用LGB/XGB/CAT三个树模型
2. 使用调优后的最优参数 (Inlined)
3. 多轮次伪标签迭代
4. 当伪标签数量稳定时停止迭代

关键防泄露措施：
- Grid Search仅在原始OOF上学习
- 伪标签基于测试集预测（5-fold平均）
- Retrain使用完整5-Fold CV
- 每轮迭代记录伪标签数量，检测收敛性

预期改进：0.675 (V6.3) → 0.68+
"""

import os
import sys
import json
import pickle
import pandas as pd
import numpy as np
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier
from scipy.stats import rankdata
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression, Lasso, Ridge, BayesianRidge
from itertools import product
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# PyTorch imports
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# 项目路径配置 (Only linking to core project root if needed for data loader)
# Assuming run.py is in src/experiments/export/
project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
sys.path.insert(0, project_root)

# ==========================================
# Inlined Data Loader Functions
# ==========================================

def load_train_data():
    """
    Load training data (static + statement)
    Returns: (df_static, df_statement)
    """
    # Determine data directory (raw folder relative to run.py location)
    data_dir = os.path.join(os.path.dirname(__file__), 'raw')
    
    print(f"Loading train data from {data_dir}...")
    
    # Load static data
    static_path = os.path.join(data_dir, 'train.csv')
    if not os.path.exists(static_path):
        raise FileNotFoundError(f"File not found: {static_path}")
    df_static = pd.read_csv(static_path)
    print(f"Loaded train static data: {df_static.shape}")
    
    # Load bank statement data
    statement_path = os.path.join(data_dir, 'train_bank_statement.csv')
    if not os.path.exists(statement_path):
        raise FileNotFoundError(f"File not found: {statement_path}")
    df_statement = pd.read_csv(statement_path)
    print(f"Loaded train statement data: {df_statement.shape}")
    
    return df_static, df_statement


def load_test_data():
    """
    Load test data (static + statement)
    Returns: (df_static, df_statement)
    """
    # Determine data directory (raw folder relative to run.py location)
    data_dir = os.path.join(os.path.dirname(__file__), 'raw')
    
    print(f"Loading test data from {data_dir}...")
    
    # Load static data
    static_path = os.path.join(data_dir, 'testab_with_amount.csv')
    if not os.path.exists(static_path):
        raise FileNotFoundError(f"File not found: {static_path}")
    df_static = pd.read_csv(static_path)
    print(f"Loaded test static data: {df_static.shape}")
    
    # Load bank statement data
    statement_path = os.path.join(data_dir, 'testab_bank_statement.csv')
    if not os.path.exists(statement_path):
        raise FileNotFoundError(f"File not found: {statement_path}")
    df_statement = pd.read_csv(statement_path)
    print(f"Loaded test statement data: {df_statement.shape}")
    
    return df_static, df_statement


# ==========================================
# Inlined Evaluator Class
# ==========================================

class Evaluator:
    """Save and manage experiment results"""

    def __init__(self, experiments_dir='experiments'):
        """Initialize evaluator"""
        self.experiments_dir = experiments_dir
        if not os.path.exists(experiments_dir):
            os.makedirs(experiments_dir, exist_ok=True)

    def save_experiment_results(
        self,
        exp_name,
        df_train,
        oof_preds,
        test_preds,
        fold_scores,
        overall_auc,
        feature_importance_df=None,
        feature_names=None,
        df_test=None
    ):
        """
        Save all experiment results to a timestamped folder

        Args:
            exp_name: Experiment name
            df_train: Training data with id and label
            oof_preds: Out-of-fold predictions on training set
            test_preds: Predictions on test set
            fold_scores: AUC scores for each fold
            overall_auc: Overall AUC score
            feature_importance_df: DataFrame with feature importance
            feature_names: List of feature names
            df_test: Test data with id (optional, for test predictions saving)

        Returns:
            Path to results directory
        """
        # Create timestamped folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_dir = os.path.join(self.experiments_dir, f'{exp_name}_{timestamp}')
        os.makedirs(result_dir, exist_ok=True)

        # 1. Save OOF predictions
        oof_df = pd.DataFrame({
            'id': df_train['id'],
            'actual': df_train['label'] if 'label' in df_train.columns else np.nan,
            'prediction': oof_preds
        })
        oof_path = os.path.join(result_dir, 'oof_predictions.csv')
        oof_df.to_csv(oof_path, index=False)
        print(f"OOF predictions saved to: {oof_path}")

        # 2. Save test predictions
        if test_preds is not None:
            # Use df_test if provided, otherwise fallback to df_train (for compatibility)
            if df_test is not None and 'id' in df_test.columns:
                test_id = df_test['id'].values[:len(test_preds)]
            else:
                # Fallback: use df_train id (may not be correct, but maintains compatibility)
                test_id = df_train['id'].values[:len(test_preds)]
            
            test_df = pd.DataFrame({
                'id': test_id,
                'prediction': test_preds
            })
            test_path = os.path.join(result_dir, 'test_predictions.csv')
            test_df.to_csv(test_path, index=False)
            print(f"Test predictions saved to: {test_path}")

        # 3. Save fold scores
        scores_df = pd.DataFrame({
            'fold': range(1, len(fold_scores) + 1),
            'auc_score': fold_scores
        })
        scores_path = os.path.join(result_dir, 'fold_scores.csv')
        scores_df.to_csv(scores_path, index=False)
        print(f"Fold scores saved to: {scores_path}")

        # 4. Save summary
        summary = {
            'overall_auc': [overall_auc],
            'mean_auc': [np.mean(fold_scores)] if len(fold_scores) > 0 else [0.0],
            'std_auc': [np.std(fold_scores)] if len(fold_scores) > 0 else [0.0],
            'num_folds': [len(fold_scores)],
            'num_features': [len(feature_names)] if feature_names else [0]
        }
        summary_df = pd.DataFrame(summary)
        summary_path = os.path.join(result_dir, 'summary.csv')
        summary_df.to_csv(summary_path, index=False)
        print(f"Summary metrics saved to: {summary_path}")

        # 5. Save feature importance
        if feature_importance_df is not None:
            importance_path = os.path.join(result_dir, 'feature_importance.csv')
            feature_importance_df.to_csv(importance_path, index=False)
            print(f"Feature importance saved to: {importance_path}")

        print(f"\nAll results saved to: {result_dir}\n")
        return result_dir

    def log_experiment(self, exp_id, exp_name, overall_auc, mean_auc, std_auc,
                       num_features, new_features_count, auc_gain, notes=''):
        """
        Log experiment to global experiment_log.csv

        Args:
            exp_id: Experiment ID (e.g., 'exp001')
            exp_name: Experiment name
            overall_auc: Overall AUC score
            mean_auc: Mean AUC across folds
            std_auc: Std of AUC across folds
            num_features: Total number of features
            new_features_count: Number of newly added features
            auc_gain: AUC gain vs baseline
            notes: Additional notes
        """
        log_file = os.path.join(self.experiments_dir, 'experiment_log.csv')

        # Create new entry
        entry = {
            'exp_id': [exp_id],
            'exp_name': [exp_name],
            'date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'overall_auc': [f"{overall_auc:.5f}"],
            'mean_auc': [f"{mean_auc:.5f}"],
            'std_auc': [f"{std_auc:.5f}"],
            'num_features': [num_features],
            'new_features': [new_features_count],
            'auc_gain': [f"{auc_gain:+.5f}"],
            'notes': [notes]
        }

        entry_df = pd.DataFrame(entry)

        # Append to log file
        if os.path.exists(log_file):
            log_df = pd.read_csv(log_file)
            log_df = pd.concat([log_df, entry_df], ignore_index=True)
        else:
            log_df = entry_df

        log_df.to_csv(log_file, index=False)
        print(f"Experiment logged to: {log_file}")

    @staticmethod
    def print_feature_importance(feature_importance_df, top_n=10):
        """Print top-N important features"""
        print(f"\nTop-{top_n} Important Features:")
        print(feature_importance_df.head(top_n).to_string(index=False))


# ==========================================
# Helper Functions
# ==========================================

def is_stable(history, window=3, tolerance=0.05):
    """
    检查伪标签数量是否稳定
    
    Args:
        history: 伪标签数量列表
        window: 比较窗口大小
        tolerance: 容差百分比（5%）
    
    Returns:
        True 如果最后window个数值稳定
    """
    if len(history) < window:
        return False
    
    recent = history[-window:]
    mean_val = np.mean(recent)
    
    # 检查所有值是否在mean_val的tolerance范围内
    for val in recent:
        if abs(val - mean_val) / (mean_val + 1e-10) > tolerance:
            return False
    
    return True


def safe_logit(p, epsilon=1e-6):
    """
    将概率转换为Log Odds（对数几率）
    
    拉伸特征分布，让模型更容易学习非线性关系
    
    Args:
        p: 概率值（在[0,1]范围内）
        epsilon: 防止极端值的小值
    
    Returns:
        Log Odds值
    """
    p = np.clip(p, epsilon, 1 - epsilon)
    return np.log(p / (1 - p))


class EarlyStopping:
    """早停管理器 - 基于验证集AUC监测"""
    def __init__(self, patience=3, verbose=True):
        """
        Args:
            patience: 连续N轮无提升则停止
            verbose: 是否打印信息
        """
        self.patience = patience
        self.verbose = verbose
        self.best_auc = 0.0
        self.best_iteration = -1
        self.counter = 0
        self.best_state = {}
        
    def should_stop(self, current_auc, current_iteration, current_state=None):
        """检查是否应该停止"""
        if current_auc > self.best_auc:
            self.best_auc = current_auc
            self.best_iteration = current_iteration
            self.counter = 0
            self.best_state = current_state.copy() if current_state else {}
            if self.verbose:
                print(f"  [EarlyStopping] 新最佳AUC: {self.best_auc:.5f} (Iteration {self.best_iteration})")
            return False
        else:
            self.counter += 1
            if self.verbose:
                print(f"  [EarlyStopping] 无提升 ({self.counter}/{self.patience})")
            return self.counter >= self.patience
    
    def get_best_state(self):
        """获取最佳状态"""
        return self.best_state


# ==========================================
# 1. Feature Engineering Utilities (Inlined)
# ==========================================

def process_static_features(df_static):
    """Process static features: encode categoricals (Simple Label Encoding)"""
    df = df_static.copy()
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col] = df[col].astype('category').cat.codes
    return df

def process_statement_features(df_statement, df_static=None, apply_time_filter=False):
    """Process statement features: aggregate by id"""
    df = df_statement.copy()
    
    # Apply time filtering to avoid data leakage
    if apply_time_filter and df_static is not None and 'record_time' in df_static.columns:
        id_to_record_time = df_static.set_index('id')['record_time'].to_dict()
        df['_record_time'] = df['id'].map(id_to_record_time)
        df = df[df['time'] < df['_record_time']].copy()
        df = df.drop(columns=['_record_time'])
    
    # Basic aggregations
    df['income'] = df.apply(lambda x: x['amount'] if x['direction'] == 0 else 0, axis=1)
    df['expense'] = df.apply(lambda x: x['amount'] if x['direction'] == 1 else 0, axis=1)
    
    agg_funcs = {
        'time': ['count'], 
        'income': ['sum', 'mean'],
        'expense': ['sum', 'mean'],
        'amount': ['std']
    }
    
    df_agg = df.groupby('id').agg(agg_funcs)
    df_agg.columns = ['_'.join(col).strip() for col in df_agg.columns.values]
    df_agg.reset_index(inplace=True)
    
    df_agg.rename(columns={
        'time_count': 'trans_count',
        'income_sum': 'income_sum',
        'income_mean': 'income_mean',
        'expense_sum': 'expense_sum',
        'expense_mean': 'expense_mean',
        'amount_std': 'amount_std'
    }, inplace=True)
    
    df_agg['balance_proxy'] = df_agg['income_sum'] - df_agg['expense_sum']
    return df_agg

class WOEEncoder:
    """WOE (Weight of Evidence) encoder for categorical variables."""
    def __init__(self, columns=None, binning_method='quantile', n_bins=5, min_samples_leaf=5, handle_missing=True):
        self.columns = columns
        self.binning_method = binning_method
        self.n_bins = n_bins
        self.min_samples_leaf = min_samples_leaf
        self.handle_missing = handle_missing
        self.woe_mappings = {}
        self.iv_scores = {}
        self.is_fitted = False

    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'WOEEncoder':
        X_copy = X.copy()
        if self.columns is None:
            self.columns = X_copy.select_dtypes(include=['object', 'category']).columns.tolist()
        y = (y > 0).astype(int)
        
        for col in self.columns:
            if col not in X_copy.columns: continue
            X_col = X_copy[col].astype(str)
            mask_missing = X_col.isin(['nan', 'None', ''])
            woe_map, iv_score = self._calculate_woe(X_col, y, mask_missing)
            self.woe_mappings[col] = woe_map
            self.iv_scores[col] = iv_score
            
        self.is_fitted = True
        return self

    def _calculate_woe(self, X_col, y, mask_missing):
        df_temp = pd.DataFrame({'feature': X_col.values, 'target': y.values, 'is_missing': mask_missing.values})
        if self.handle_missing and df_temp['is_missing'].any():
            df_temp.loc[df_temp['is_missing'], 'feature'] = '__MISSING__'
            
        event_count = y.sum()
        non_event_count = len(y) - event_count
        if event_count == 0 or non_event_count == 0: return {}, 0.0
        
        woe_map = {}
        iv_score = 0.0
        for category in df_temp['feature'].unique():
            mask = df_temp['feature'] == category
            events = (df_temp[mask]['target'] == 1).sum()
            non_events = (mask.sum()) - events
            if events == 0 or non_events == 0:
                woe_map[category] = 0.0
                continue
            
            event_pct = max(events / event_count, 1e-10)
            non_event_pct = max(non_events / non_event_count, 1e-10)
            woe = np.log(event_pct / non_event_pct)
            woe_map[category] = woe
            iv_score += (event_pct - non_event_pct) * woe
            
        return woe_map, iv_score

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.is_fitted: raise ValueError("Encoder must be fitted before transform")
        X_woe = X.copy()
        for col in self.woe_mappings.keys():
            if col not in X_woe.columns: continue
            X_str = X_woe[col].astype(str).replace(['nan', 'None', ''], '__MISSING__')
            X_woe[col] = X_str.map(self.woe_mappings[col]).fillna(0.0)
        return X_woe
        
    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X)

# ==========================================
# 2. Advanced Aggregation Features (Inlined)
# ==========================================

def q25(x): return x.quantile(0.25)
def q50(x): return x.quantile(0.50)
def q75(x): return x.quantile(0.75)
def kurt(x): return x.kurtosis()

class AdvancedAggregationFeatures:
    """Advanced statistical aggregations (Skew, Kurt, Quantiles)"""
    def __init__(self):
        self.agg_funcs = ['count', 'sum', 'mean', 'max', 'min', 'std', 'skew', kurt, q25, q50, q75]
        self.agg_names = ['count', 'sum', 'mean', 'max', 'min', 'std', 'skew', 'kurt', 'q25', 'q50', 'q75']

    def create_global_aggregation(self, bank_df):
        overall_agg = bank_df.groupby('id')['amount'].agg(self.agg_funcs)
        overall_agg.columns = [f'bank_all_{name}' for name in self.agg_names]
        return overall_agg

    def create_direction_aggregation(self, bank_df):
        direction_agg = bank_df.groupby(['id', 'direction'])['amount'].agg(self.agg_funcs).unstack()
        flat_cols = []
        for agg_func, direction in direction_agg.columns:
            name = agg_func if isinstance(agg_func, str) else agg_func.__name__
            flat_cols.append(f'bank_dir_{int(direction)}_{name}')
        direction_agg.columns = flat_cols
        return direction_agg

    def create_time_window_aggregation(self, bank_df, main_df, windows=[30, 90]):
        window_features = []
        if main_df is None or 'issue_time' not in main_df.columns: return window_features
        
        # Map issue_time (keep as numeric timestamp)
        issue_time_map = main_df.set_index('id')['issue_time']
        bank_df = bank_df.copy()
        bank_df['issue_time'] = bank_df['id'].map(issue_time_map)
        # Both 'time' and 'issue_time' are numeric Unix timestamps, so direct subtraction works
        bank_df['time_diff'] = bank_df['issue_time'] - bank_df['time']
        
        for days in windows:
            seconds = days * 24 * 3600
            mask = (bank_df['time_diff'] >= 0) & (bank_df['time_diff'] <= seconds)
            recent_df = bank_df[mask]
            
            if not recent_df.empty:
                recent_agg_funcs = ['count', 'sum', 'mean', 'max', 'min', 'std', q50]
                recent_agg_names = ['count', 'sum', 'mean', 'max', 'min', 'std', 'median']
                recent_agg = recent_df.groupby('id')['amount'].agg(recent_agg_funcs)
                recent_agg.columns = [f'bank_recent_{days}d_{name}' for name in recent_agg_names]
                window_features.append(recent_agg)
        return window_features

    def merge_aggregation_features(self, bank_df, main_df=None):
        features_list = [
            self.create_global_aggregation(bank_df),
            self.create_direction_aggregation(bank_df)
        ]
        
        last_time = bank_df.groupby('id')['time'].max()
        last_time.name = 'bank_last_time'
        features_list.append(last_time)
        
        first_time = bank_df.groupby('id')['time'].min()
        first_time.name = 'bank_first_time'
        features_list.append(first_time)
        
        time_span = last_time - first_time
        time_span.name = 'bank_time_span'
        features_list.append(time_span)
        
        # Volatility
        overall_agg = features_list[0]
        volatility = overall_agg['bank_all_std'] / (overall_agg['bank_all_mean'].abs() + 1e-6)
        volatility.name = 'bank_volatility'
        features_list.append(volatility)
        
        window_features = self.create_time_window_aggregation(bank_df, main_df)
        if window_features:
            features_list.extend(window_features)
            
        return pd.concat(features_list, axis=1)

# ==========================================
# 3. Component Extractors (Inlined)
# ==========================================

class BasicFeatureEnhancer:
    def __init__(self):
        self.zip_prefix_lengths = [3, 5]

    def extract_features(self, df_static):
        features_df = df_static[['id']].copy()
        
        # Zip features
        if 'zip_code' in df_static.columns:
            zip_codes = df_static['zip_code'].astype(str)
            for prefix_len in self.zip_prefix_lengths:
                features_df[f'zip_prefix_{prefix_len}d'] = pd.factorize(zip_codes.str[:prefix_len])[0]
            features_df['zip_code_encoded'] = pd.factorize(zip_codes)[0]
            
        # Business Ratios
        if 'loan' in df_static.columns and 'installment' in df_static.columns:
            features_df['loan_installment_ratio'] = df_static['loan'] / (df_static['installment'] + 1e-5)
        if 'balance' in df_static.columns and 'balance_limit' in df_static.columns:
            features_df['balance_utilization_rate'] = df_static['balance'] / (df_static['balance_limit'] + 1e-5)
        if 'loan' in df_static.columns and 'term' in df_static.columns:
            features_df['payment_per_term'] = df_static['loan'] / (df_static['term'] + 1e-5)
        if 'interest_rate' in df_static.columns and 'term' in df_static.columns:
            features_df['total_interest_cost'] = df_static['interest_rate'] * df_static['term']
            
        # Time Diffs - work on a copy to avoid modifying original df_static
        df_static_time = df_static[['record_time', 'history_time', 'issue_time']].copy() if all(c in df_static.columns for c in ['record_time', 'history_time', 'issue_time']) else df_static.copy()
        
        for col in ['record_time', 'history_time', 'issue_time']:
            if col in df_static_time.columns:
                try: df_static_time[col] = pd.to_datetime(df_static_time[col])
                except: pass
                
        if 'record_time' in df_static_time.columns:
            if 'history_time' in df_static_time.columns:
                features_df['history_days'] = (df_static_time['record_time'] - df_static_time['history_time']).dt.days
            if 'issue_time' in df_static_time.columns:
                features_df['loan_age_days'] = (df_static_time['record_time'] - df_static_time['issue_time']).dt.days
                
        return features_df.fillna(0)

class ShortWindowStatementFeatureExtractor:
    def __init__(self, window_days=[7, 30]):
        self.window_days = window_days

    def extract_features(self, df_static, df_statement):
        # Time conversion setup
        df_static_copy = df_static[['id', 'record_time']].copy()
        try: df_static_copy['record_time'] = pd.to_datetime(df_static_copy['record_time'], unit='s')
        except: pass
        
        df_stmt = df_statement.copy()
        try: df_stmt['time'] = pd.to_datetime(df_stmt['time'], unit='s')
        except: pass
        
        features_df = df_static_copy[['id']].copy()
        
        for window_days in self.window_days:
            window_period = pd.Timedelta(days=window_days)
            df_merged = pd.merge(df_stmt, df_static_copy, on='id', how='left')
            mask = (df_merged['time'] >= df_merged['record_time'] - window_period) & (df_merged['time'] <= df_merged['record_time'])
            df_window = df_merged[mask].copy()
            
            df_income = df_window[df_window['direction'] == 0]
            df_expense = df_window[df_window['direction'] == 1]
            
            w_feat = pd.DataFrame({'id': df_static_copy['id'].unique()})
            
            w_feat = w_feat.merge(df_window.groupby('id').size().reset_index(name=f'trans_count_{window_days}d'), on='id', how='left')
            w_feat = w_feat.merge(df_income.groupby('id')['amount'].sum().reset_index(name=f'income_sum_{window_days}d'), on='id', how='left')
            w_feat = w_feat.merge(df_income.groupby('id')['amount'].mean().reset_index(name=f'income_mean_{window_days}d'), on='id', how='left')
            w_feat = w_feat.merge(df_expense.groupby('id')['amount'].sum().reset_index(name=f'expense_sum_{window_days}d'), on='id', how='left')
            w_feat = w_feat.merge(df_expense.groupby('id')['amount'].mean().reset_index(name=f'expense_mean_{window_days}d'), on='id', how='left')
            
            w_feat = w_feat.fillna(0)
            
            w_feat[f'net_flow_{window_days}d'] = w_feat[f'income_sum_{window_days}d'] - w_feat[f'expense_sum_{window_days}d']
            w_feat[f'income_expense_ratio_{window_days}d'] = w_feat[f'income_sum_{window_days}d'] / (w_feat[f'expense_sum_{window_days}d'] + 1e-5)
            w_feat[f'saving_rate_{window_days}d'] = w_feat[f'net_flow_{window_days}d'] / (w_feat[f'income_sum_{window_days}d'] + 1e-5)
            
            features_df = features_df.merge(w_feat, on='id', how='left')
            
        return features_df.fillna(0)  # Keep 'id' column for merging

# ==========================================
# 4. Unified Feature Extractor
# ==========================================

class UnifiedFeatureExtractor:
    """
    Consolidated Feature Engineering Pipeline.
    Combines Baseline, WOE, Enhanced(Zip/Ratio), ShortWindow, Groupby(Level/LoanBin), Poly, and AdvancedAggs.
    """
    def __init__(self):
        self.basic_enhancer = BasicFeatureEnhancer()
        self.short_window = ShortWindowStatementFeatureExtractor()
        self.woe_encoder = None
        self.adv_agg = AdvancedAggregationFeatures()
        
        # Groupby Keys configuration
        self.groupby_keys = ['level_ordinal', 'loan_bin', 'zip_prefix_3d', 'loan_level_combo', 'residence_level_combo']
        self.agg_values = ['interest_rate', 'balance', 'installment', 'income_sum_7d']

    def merge_features(self, df_static, df_statement, y_train=None, fold_mode=False):
        print("=" * 70)
        print("FEATURE ENGINEERING LOOP (Consolidated - Matching exp023_pseudo_stacking)")
        print("=" * 70)
        
        # [Step 1] Baseline Features (Static + Statement)
        print("[1/7] Baseline Features...")
        df_static_proc = process_static_features(df_static)
        df_stmt_proc = process_statement_features(df_statement, df_static, apply_time_filter=False)
        df_all = pd.merge(df_static_proc, df_stmt_proc, on='id', how='left')
        
        # [Step 2] Enhanced Features (Zip, Ratios, Time)
        print("[2/7] Enhanced Features...")
        df_enhanced = self.basic_enhancer.extract_features(df_static)
        df_all = pd.merge(df_all, df_enhanced, on='id', how='left')
        
        # [Step 3] Short Window Features
        print("[3/7] Short Window Features...")
        # Note: extract_features returns DF with 'id' if we modified it to do so. 
        # My implementation of extract_features above returns features_df which has 'id'.
        df_short = self.short_window.extract_features(df_static, df_statement)
        if 'id' in df_short.columns:
            df_all = pd.merge(df_all, df_short, on='id', how='left')
        else:
             # Fallback if id missing (should not happen with current code)
             pass 

        # [Step 4] WOE Encoding
        print("[4/7] WOE Encoding...")
        cols_to_woe = ['title', 'career', 'residence', 'level', 'syndicated']
        # We need original categoricals. process_static_features encoded them.
        # But we can recover from df_static.
        if fold_mode:
            print("  Skipping WOE application in fold mode (will fit later)")
        else:
            cat_data = df_static[['id'] + [c for c in cols_to_woe if c in df_static.columns]].copy()
            if y_train is not None:
                self.woe_encoder = WOEEncoder(columns=cols_to_woe)
                df_woe = self.woe_encoder.fit_transform(cat_data.drop('id', axis=1), y_train)
            else:
                if self.woe_encoder is None: raise ValueError("WOE not fitted")
                df_woe = self.woe_encoder.transform(cat_data.drop('id', axis=1))
            
            df_woe['id'] = cat_data['id']
            # Rename WOE columns (before adding id)
            woe_cols = [c for c in df_woe.columns if c != 'id']
            rename_dict = {col: f'{col}_woe' for col in woe_cols}
            df_woe = df_woe.rename(columns=rename_dict)
            df_all = pd.merge(df_all, df_woe, on='id', how='left')
            
            # Drop original categorical columns (they were label-encoded by process_static_features)
            cols_to_drop = [c for c in cols_to_woe if c in df_all.columns]
            if cols_to_drop:
                df_all = df_all.drop(columns=cols_to_drop)
                print(f"  Dropped original categorical columns: {cols_to_drop}")

        # [Step 5] Groupby Features (Legacy Exp009 logic)
        print("[5/7] Groupby & Statistical Features...")
        
        # 5.1 Fix Level Encoding (Ordinal)
        # Create level_ordinal from original df_static
        level_map = {'A0':0, 'A1':1, 'A2':2, 'A3':3, 'A4':4, 'A5':5,
                     'B0':6, 'B1':7, 'B2':8, 'B3':9, 'B4':10, 'B5':11,
                     'C1':12, 'C2':13, 'C3':14, 'C4':15, 'C5':16,
                     'D1':17, 'D2':18, 'D3':19, 'D4':20, 'D5':21,
                     'E1':22, 'E2':23, 'E3':24, 'E4':25, 'E5':26}
        if 'level' in df_static.columns:
            df_all['level_ordinal'] = df_all['id'].map(df_static.set_index('id')['level']).map(level_map).fillna(-1).astype(int)
        else:
            df_all['level_ordinal'] = 0
            
        # 5.2 Loan Bin
        if 'loan' in df_all.columns:
            df_all['loan_bin'] = pd.qcut(df_all['loan'], q=5, labels=False, duplicates='drop')
        else:
            df_all['loan_bin'] = 0
            
        # 5.3 Combo Keys
        df_all['loan_level_combo'] = df_all['loan_bin'].astype(str) + '_' + df_all['level_ordinal'].astype(str)
        # Residence recovery for combo
        if 'residence' in df_static.columns:
            res_raw = df_all['id'].map(df_static.set_index('id')['residence']).fillna(-1).astype(str)
            df_all['residence_level_combo'] = res_raw + '_' + df_all['level_ordinal'].astype(str)
        else:
             df_all['residence_level_combo'] = '0_0'
             
        # 5.4 Aggregation Loop
        for key in self.groupby_keys:
            if key not in df_all.columns: continue
            for value in self.agg_values:
                if value not in df_all.columns: continue
                
                # Transform to avoid leakage (Global transform, ideally should be fold-wise but keeping legacy logic)
                group_mean = df_all.groupby(key)[value].transform('mean')
                group_std = df_all.groupby(key)[value].transform('std').fillna(1e-8)
                
                df_all[f'{key}_{value}_mean'] = group_mean
                df_all[f'{key}_{value}_diff'] = df_all[value] - group_mean
                df_all[f'{key}_{value}_ratio'] = df_all[value] / (group_mean + 1e-8)
                df_all[f'{key}_{value}_zscore'] = (df_all[value] - group_mean) / (group_std + 1e-8)
                df_all[f'{key}_{value}_rank_pct'] = df_all.groupby(key)[value].rank(pct=True)

        # Encode combos
        for col in ['loan_level_combo', 'residence_level_combo']:
            if col in df_all.columns:
                df_all[col] = df_all[col].astype('category').cat.codes

        # [Step 6] Polynomial Features (matching exp010_polynomial)
        print("[6/7] Polynomial Features (Log/Square/Interaction)...")
        # Log1p Transformation (Money/Count)
        log_candidates = [
            'total_interest_cost',
            'balance_accounts',
            'balance_proxy',
            'balance_limit'
        ]
        for col in log_candidates:
            if col in df_all.columns:
                df_all[f'{col}_log1p'] = np.log1p(df_all[col].clip(lower=0))
        
        # Square Transformation (Rate)
        square_candidates = [
            'interest_rate',
            'residence_level_combo_interest_rate_mean',
            'balance_utilization_rate'
        ]
        for col in square_candidates:
            if col in df_all.columns:
                df_all[f'{col}_squared'] = df_all[col] ** 2
        
        # Interaction (Rate * Balance)
        if 'interest_rate' in df_all.columns and 'balance_limit' in df_all.columns:
            df_all['interest_rate_x_balance_limit'] = df_all['interest_rate'] * df_all['balance_limit']
             
        # [Step 7] Advanced Aggregation Features (matching exp023_pseudo_stacking)
        print("[7/7] Advanced Aggregations (Skew/Kurt/Quantiles)...")
        # This requires raw statement data again
        bank_agg = self.adv_agg.merge_aggregation_features(df_statement, df_static)
        new_cols = [c for c in bank_agg.columns if c not in df_all.columns]
        df_all = df_all.join(bank_agg[new_cols], on='id', how='left')
        
        # Final cleanup
        df_all = df_all.fillna(0)
        
        # Feature Selection (Drop ID/Label/Objects)
        feature_cols = [c for c in df_all.columns if c not in ['id', 'label'] and df_all[c].dtype != 'object']
        
        # Ensure only numeric - handle both train (with label) and test (without label)
        if 'label' in df_all.columns:
            df_final = df_all[['id', 'label'] + feature_cols].copy()
        else:
            df_final = df_all[['id'] + feature_cols].copy()
            df_final['label'] = 0  # Add dummy label column for consistency
        
        print(f"Total Features: {len(feature_cols)}")
        return df_final


# ==========================================
# 5. Weight Optimizer (Inlined)
# ==========================================

class EnsembleWeightOptimizer:
    """Ensemble权重优化器"""
    def __init__(self, search_space='coarse', metric='auc', use_rank=True, verbose=True):
        self.search_space = search_space
        self.metric = metric
        self.use_rank = use_rank
        self.verbose = verbose
        
    def optimize(self, oof_predictions_dict, y_true, center_weights=None):
        model_names = list(oof_predictions_dict.keys())
        n_models = len(model_names)
        
        if self.search_space == 'coarse':
            weight_range = np.arange(0.0, 1.01, 0.1)
        elif self.search_space == 'fine':
            weight_range = np.arange(0.0, 1.01, 0.01) # Simplified fine range
            
        if self.use_rank:
            oof_to_use = {name: rankdata(preds)/len(preds) for name, preds in oof_predictions_dict.items()}
        else:
            oof_to_use = oof_predictions_dict
            
        best_score = 0
        best_weights_list = None
        
        # Grid Search
        for weights_tuple in product(weight_range, repeat=n_models):
            if abs(sum(weights_tuple) - 1.0) > 0.01: continue
            
            ensemble_pred = np.zeros(len(y_true))
            for i, name in enumerate(model_names):
                ensemble_pred += weights_tuple[i] * oof_to_use[name]
                
            score = roc_auc_score(y_true, ensemble_pred)
            if score > best_score:
                best_score = score
                best_weights_list = weights_tuple
                
        best_weights = {name: w for name, w in zip(model_names, best_weights_list)}
        if self.verbose:
            print(f"Best AUC: {best_score:.5f}, Weights: {best_weights}")
            
        return best_weights, best_score

def simple_grid_search_weights(oof_dict, y_true, step=0.1, use_rank=True, verbose=True):
    optimizer = EnsembleWeightOptimizer(search_space='coarse' if step >= 0.1 else 'fine', use_rank=use_rank, verbose=verbose)
    return optimizer.optimize(oof_dict, y_true)


# ==========================================
# 6. Main Model Class
# ==========================================

class MultiRoundSemiSupervised:
    """Semi-supervised Learning Model"""
    
    def __init__(self, verbose=True):
        """
        初始化多轮半监督学习模型
        
        Args:
            verbose: 是否打印详细信息
        """
        self.feature_extractor = UnifiedFeatureExtractor()
        self.skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        self.best_weights = None
        self.iteration_history = []  # Track iteration metrics
        self.verbose = verbose
    
    def prepare_data(self, include_test=False):
        """Prepare data using Unified Feature Extractor"""
        print("\n[Data Preparation] Loading raw data...")
        df_static_train, df_statement_train = load_train_data()
        y_train = df_static_train['label'].copy()
        
        print("[Data Preparation] Merging features (Train)...")
        # Pass y_train for WOE fitting
        df_train_full = self.feature_extractor.merge_features(df_static_train, df_statement_train, y_train=y_train)
        
        # Minimal feature cleaning (matching exp023_pseudo_stacking strategy)
        print("\n[Data Preparation] Minimal feature cleaning...")
        X_train_all = df_train_full.drop(['id', 'label'], axis=1)
        X_columns_all = X_train_all.columns.tolist()
        
        # Simple cleaning: remove NaN/Inf/zero-variance features (matching exp023)
        selected_features = []
        for col in X_columns_all:
            if col in ['id', 'label']:
                continue
            if (df_train_full[col].isnull().any() or
                np.isinf(df_train_full[col]).any() or
                df_train_full[col].std() < 1e-10):
                continue
            selected_features.append(col)
        
        feature_cols = selected_features
        print(f"Selected {len(feature_cols)} features (removed {len(X_columns_all) - len(feature_cols)})")
        
        X_train = df_train_full[feature_cols].values
        y_train_vals = df_train_full['label'].values
        
        if include_test:
            print("[Data Preparation] Merging features (Test)...")
            df_static_test, df_statement_test = load_test_data()
            # y_train=None means apply existing WOE
            df_test_full = self.feature_extractor.merge_features(df_static_test, df_statement_test, y_train=None)
            
            # Align columns (ensure test has same columns as train, using deduplicated features)
            missing_cols = set(feature_cols) - set(df_test_full.columns)
            for c in missing_cols: df_test_full[c] = 0
            # Reorder to match deduplicated features, but preserve 'id' column
            df_test_full = df_test_full[['id'] + feature_cols]
            
            X_test = df_test_full[feature_cols].values
            return X_train, y_train_vals, X_test, df_train_full[['id', 'label'] + feature_cols], df_test_full[['id'] + feature_cols], feature_cols
            
        return X_train, y_train_vals, df_train_full[['id', 'label'] + feature_cols], feature_cols
    
    def load_tuned_params(self):
        """Hardcoded tuned parameters"""
        # LightGBM
        lgb_params = {
          "learning_rate": 0.0269340130300808, "num_leaves": 39, "max_depth": 11,
          "min_child_samples": 65, "min_child_weight": 0.005122798925581198,
          "subsample": 0.9612210708283709, "subsample_freq": 4, "colsample_bytree": 0.7021125482710724,
          "reg_alpha": 5.0845598702702155, "reg_lambda": 0.0033481114357430393,
          "max_bin": 202, "min_data_in_bin": 9, "objective": "binary", "metric": "auc",
          "boosting_type": "gbdt", "seed": 42, "n_jobs": 4, "n_estimators": 155
        }
        # XGBoost
        xgb_params = {
          "learning_rate": 0.05110592807148005, "max_depth": 4, "min_child_weight": 3.362587491042113,
          "gamma": 3.1350070676872397, "reg_alpha": 7.139083653838582, "reg_lambda": 3.9000982718178756,
          "subsample": 0.904267985531743, "colsample_bytree": 0.8557160447101594,
          "colsample_bylevel": 0.8249783596002899, "n_estimators": 195
        }
        # CatBoost
        cat_params = {
          "learning_rate": 0.03586333041639407, "depth": 6, "l2_leaf_reg": 3.446604220600197,
          "random_strength": 5.445981291350253e-08, "grow_policy": "Lossguide",
          "border_count": 114, "min_data_in_leaf": 97, "bootstrap_type": "Bernoulli",
          "subsample": 0.6459304178774811, "max_leaves": 26, "n_estimators": 234
        }
        return lgb_params, xgb_params, cat_params
    
    def generate_oof_predictions_base_models(self, X_train, y_train, lgb_params, xgb_params, cat_params):
        """
        生成3个模型的OOF预测（LGB/XGB/CAT）
        完全复刻 run2.py 的实现
        """
        print("\n" + "="*70)
        print("GENERATING BASE MODEL OOF PREDICTIONS (LGB/XGB/CAT)")
        print("="*70)
        
        # 1. LightGBM OOF
        print("\n[1/3] LightGBM OOF...")
        lgb_oof = self._generate_lgb_oof(X_train, y_train, lgb_params)
        
        # 2. XGBoost OOF
        print("[2/3] XGBoost OOF...")
        xgb_oof = self._generate_xgb_oof(X_train, y_train, xgb_params)
        
        # 3. CatBoost OOF
        print("[3/3] CatBoost OOF...")
        cat_oof = self._generate_cat_oof(X_train, y_train, cat_params)
        
        return {
            'lgb': lgb_oof,
            'xgb': xgb_oof,
            'cat': cat_oof
        }
    
    def _generate_lgb_oof(self, X_train, y_train, lgb_params):
        """LightGBM OOF预测"""
        lgb_params_copy = lgb_params.copy()
        n_estimators = lgb_params_copy.pop('n_estimators', 1000)
        
        # 只保留lgb支持的参数
        lgb_params_copy.update({
            'objective': 'binary',
            'metric': 'auc',
            'verbose': -1
        })
        
        oof = np.zeros(len(X_train))
        fold_scores = []
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            X_val, y_val = X_train[val_idx], y_train[val_idx]
            
            dtrain = lgb.Dataset(X_tr, label=y_tr)
            dval = lgb.Dataset(X_val, label=y_val, reference=dtrain)
            
            clf = lgb.train(
                lgb_params_copy, dtrain,
                num_boost_round=n_estimators,
                valid_sets=[dval],
                callbacks=[lgb.early_stopping(50), lgb.log_evaluation(period=0)]
            )
            
            oof[val_idx] = clf.predict(X_val)
            fold_auc = roc_auc_score(y_val, clf.predict(X_val))
            fold_scores.append(fold_auc)
            print(f"  Fold {fold_idx+1}: {fold_auc:.5f}")
        
        overall = roc_auc_score(y_train, oof)
        print(f"LGB OOF AUC: {overall:.5f}")
        return oof
    
    def _generate_xgb_oof(self, X_train, y_train, xgb_params):
        """XGBoost OOF预测"""
        xgb_params_copy = xgb_params.copy()
        n_estimators = xgb_params_copy.pop('n_estimators', 1000)
        xgb_params_copy['n_estimators'] = n_estimators
        xgb_params_copy['random_state'] = 42
        xgb_params_copy['verbosity'] = 0
        
        oof = np.zeros(len(X_train))
        fold_scores = []
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            X_val, y_val = X_train[val_idx], y_train[val_idx]
            
            clf = xgb.XGBClassifier(**xgb_params_copy)
            clf.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
            
            oof[val_idx] = clf.predict_proba(X_val)[:, 1]
            fold_auc = roc_auc_score(y_val, clf.predict_proba(X_val)[:, 1])
            fold_scores.append(fold_auc)
            print(f"  Fold {fold_idx+1}: {fold_auc:.5f}")
        
        overall = roc_auc_score(y_train, oof)
        print(f"XGB OOF AUC: {overall:.5f}")
        return oof
    
    def _generate_cat_oof(self, X_train, y_train, cat_params):
        """CatBoost OOF预测"""
        cat_params_copy = cat_params.copy()
        n_estimators = cat_params_copy.pop('n_estimators', 1000)
        
        cat_params_copy.update({
            'iterations': n_estimators,
            'random_state': 42,
            'verbose': 0,
            'thread_count': -1
        })
        
        oof = np.zeros(len(X_train))
        fold_scores = []
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            X_val, y_val = X_train[val_idx], y_train[val_idx]
            
            clf = CatBoostClassifier(**cat_params_copy)
            clf.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
            
            oof[val_idx] = clf.predict_proba(X_val)[:, 1]
            fold_auc = roc_auc_score(y_val, clf.predict_proba(X_val)[:, 1])
            fold_scores.append(fold_auc)
            print(f"  Fold {fold_idx+1}: {fold_auc:.5f}")
        
        overall = roc_auc_score(y_train, oof)
        print(f"CAT OOF AUC: {overall:.5f}")
        return oof
    
    def train_lgb_stacking(self, oof_lgb, oof_xgb, oof_cat, oof_weighted, y_train):
        """训练浅层LightGBM Stacking模型 - 与run2.py完全一致"""
        X_stacking = np.column_stack([
            safe_logit(oof_lgb), safe_logit(oof_xgb),
            safe_logit(oof_cat), safe_logit(oof_weighted)
        ])
        
        lgb_stacking_params = {
            'objective': 'binary', 'metric': 'auc', 'boosting_type': 'gbdt',
            'n_estimators': 1000, 'learning_rate': 0.01, 'num_leaves': 3,
            'max_depth': 2, 'min_child_samples': 50, 'reg_alpha': 0.1,
            'reg_lambda': 0.1, 'subsample': 0.8, 'colsample_bytree': 0.8,
            'seed': 42, 'verbose': -1
        }
        
        oof_lgb_stacking = np.zeros(len(y_train))
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_stacking, y_train)):
            X_tr, y_tr = X_stacking[train_idx], y_train[train_idx]
            X_val, y_val = X_stacking[val_idx], y_train[val_idx]
            
            dtrain = lgb.Dataset(X_tr, label=y_tr)
            dval = lgb.Dataset(X_val, label=y_val, reference=dtrain)
            
            clf = lgb.train(lgb_stacking_params, dtrain, num_boost_round=100,
                          valid_sets=[dval], callbacks=[lgb.early_stopping(50), lgb.log_evaluation(period=0)])
            
            oof_lgb_stacking[val_idx] = clf.predict(X_val)
            if self.verbose:
                print(f"    LGB-Stacking Fold {fold_idx+1}: {roc_auc_score(y_val, clf.predict(X_val)):.5f}")
        
        lgb_stacking_auc = roc_auc_score(y_train, oof_lgb_stacking)
        if self.verbose:
            print(f"  LGB Stacking OOF AUC: {lgb_stacking_auc:.5f}")
        return oof_lgb_stacking, lgb_stacking_auc
    
    def train_lr_stacking(self, oof_lgb, oof_xgb, oof_cat, oof_weighted, y_train):
        """训练Logistic Regression Stacking - 与run2.py完全一致"""
        X_stacking = np.column_stack([oof_lgb, oof_xgb, oof_cat, oof_weighted])
        oof_lr = np.zeros(len(y_train))
        
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_stacking, y_train)):
            X_tr, y_tr = X_stacking[train_idx], y_train[train_idx]
            X_val, y_val = X_stacking[val_idx], y_train[val_idx]
            
            clf = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
            clf.fit(X_tr, y_tr)
            oof_lr[val_idx] = clf.predict_proba(X_val)[:, 1]
            
            if self.verbose:
                print(f"    LR Fold {fold_idx+1}: {roc_auc_score(y_val, oof_lr[val_idx]):.5f}")
        
        lr_auc = roc_auc_score(y_train, oof_lr)
        if self.verbose:
            print(f"  LR Stacking OOF AUC: {lr_auc:.5f}")
        return oof_lr, lr_auc
    
    def train_lasso_stacking(self, oof_lgb, oof_xgb, oof_cat, oof_weighted, y_train):
        """Lasso回归堆叠 - 与run2.py完全一致"""
        X_stacking = np.column_stack([oof_lgb, oof_xgb, oof_cat, oof_weighted])
        oof_lasso = np.zeros(len(y_train))
        
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_stacking, y_train)):
            X_tr, y_tr = X_stacking[train_idx], y_train[train_idx]
            X_val, y_val = X_stacking[val_idx], y_train[val_idx]
            
            clf = Lasso(alpha=0.0001, max_iter=5000, random_state=42)
            clf.fit(X_tr, y_tr)
            oof_lasso[val_idx] = np.clip(clf.predict(X_val), 0, 1)
            
            if self.verbose:
                print(f"    Lasso Fold {fold_idx+1}: {roc_auc_score(y_val, oof_lasso[val_idx]):.5f}")
        
        lasso_auc = roc_auc_score(y_train, oof_lasso)
        if self.verbose:
            print(f"  Lasso Stacking OOF AUC: {lasso_auc:.5f}")
        return oof_lasso, lasso_auc
    
    def train_ridge_stacking(self, oof_lgb, oof_xgb, oof_cat, oof_weighted, y_train):
        """Ridge回归堆叠 - 与run2.py完全一致"""
        X_stacking = np.column_stack([oof_lgb, oof_xgb, oof_cat, oof_weighted])
        oof_ridge = np.zeros(len(y_train))
        
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_stacking, y_train)):
            X_tr, y_tr = X_stacking[train_idx], y_train[train_idx]
            X_val, y_val = X_stacking[val_idx], y_train[val_idx]
            
            clf = Ridge(alpha=0.1, random_state=42)
            clf.fit(X_tr, y_tr)
            oof_ridge[val_idx] = np.clip(clf.predict(X_val), 0, 1)
            
            if self.verbose:
                print(f"    Ridge Fold {fold_idx+1}: {roc_auc_score(y_val, oof_ridge[val_idx]):.5f}")
        
        ridge_auc = roc_auc_score(y_train, oof_ridge)
        if self.verbose:
            print(f"  Ridge Stacking OOF AUC: {ridge_auc:.5f}")
        return oof_ridge, ridge_auc
    
    def train_bayesian_ridge_stacking(self, oof_lgb, oof_xgb, oof_cat, oof_weighted, y_train):
        """贝叶斯Ridge回归堆叠 - 与run2.py完全一致"""
        X_stacking = np.column_stack([oof_lgb, oof_xgb, oof_cat, oof_weighted])
        oof_br = np.zeros(len(y_train))
        
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_stacking, y_train)):
            X_tr, y_tr = X_stacking[train_idx], y_train[train_idx]
            X_val, y_val = X_stacking[val_idx], y_train[val_idx]
            
            clf = BayesianRidge(max_iter=500)
            clf.fit(X_tr, y_tr)
            oof_br[val_idx] = np.clip(clf.predict(X_val), 0, 1)
            
            if self.verbose:
                print(f"    BayesianRidge Fold {fold_idx+1}: {roc_auc_score(y_val, oof_br[val_idx]):.5f}")
        
        br_auc = roc_auc_score(y_train, oof_br)
        if self.verbose:
            print(f"  BayesianRidge Stacking OOF AUC: {br_auc:.5f}")
        return oof_br, br_auc
    
    def compute_ensemble_aucs(self, oof_lgb, oof_xgb, oof_cat, y_train):
        """计算6种融合方式的AUC - 与run2.py完全一致"""
        # 方式1：加权融合
        oof_weighted = (
            self.best_weights['lgb'] * oof_lgb +
            self.best_weights['xgb'] * oof_xgb +
            self.best_weights['cat'] * oof_cat
        )
        weighted_auc = roc_auc_score(y_train, oof_weighted)
        
        # 为Stacking构建输入（使用rank average）
        rank_oof = {
            'lgb': rankdata(oof_lgb) / len(oof_lgb),
            'xgb': rankdata(oof_xgb) / len(oof_xgb),
            'cat': rankdata(oof_cat) / len(oof_cat)
        }
        oof_weighted_rank = (
            self.best_weights['lgb'] * rank_oof['lgb'] +
            self.best_weights['xgb'] * rank_oof['xgb'] +
            self.best_weights['cat'] * rank_oof['cat']
        )
        
        # 方式2-6：各种Stacking
        print("  [2/6] Training LGB Stacking (with Logit Transform)...")
        oof_lgb_stacking, lgb_stacking_auc = self.train_lgb_stacking(oof_lgb, oof_xgb, oof_cat, oof_weighted_rank, y_train)
        
        print("  [3/6] Training LR Stacking...")
        oof_lr, lr_auc = self.train_lr_stacking(oof_lgb, oof_xgb, oof_cat, oof_weighted_rank, y_train)
        
        print("  [4/6] Training Lasso Stacking...")
        oof_lasso, lasso_auc = self.train_lasso_stacking(oof_lgb, oof_xgb, oof_cat, oof_weighted_rank, y_train)
        
        print("  [5/6] Training Ridge Stacking...")
        oof_ridge, ridge_auc = self.train_ridge_stacking(oof_lgb, oof_xgb, oof_cat, oof_weighted_rank, y_train)
        
        print("  [6/6] Training BayesianRidge Stacking...")
        oof_br, br_auc = self.train_bayesian_ridge_stacking(oof_lgb, oof_xgb, oof_cat, oof_weighted_rank, y_train)
        
        return (weighted_auc, lgb_stacking_auc, lr_auc, lasso_auc, ridge_auc, br_auc,
                oof_weighted, oof_lgb_stacking, oof_lr, oof_lasso, oof_ridge, oof_br)
    
    def _retrain_lgb_with_pseudo_labels(self, X_train, y_train, X_pseudo, y_pseudo, lgb_params):
        """用伪标签重新训练LGB - 与run2.py完全一致"""
        lgb_params_copy = lgb_params.copy()
        n_estimators = lgb_params_copy.pop('n_estimators', 1000)
        lgb_params_copy.update({'objective': 'binary', 'metric': 'auc', 'seed': 42, 'verbose': -1})
        
        oof = np.zeros(len(X_train))
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            X_val, y_val = X_train[val_idx], y_train[val_idx]
            
            X_combined = np.vstack([X_tr, X_pseudo])
            y_combined = np.concatenate([y_tr, y_pseudo])
            sample_weight = np.concatenate([np.ones(len(y_tr)), np.ones(len(y_pseudo)) * 0.5])
            
            dtrain = lgb.Dataset(X_combined, label=y_combined, weight=sample_weight)
            clf = lgb.train(lgb_params_copy, dtrain, num_boost_round=n_estimators, callbacks=[lgb.log_evaluation(period=0)])
            
            oof[val_idx] = clf.predict(X_val)
            if self.verbose:
                print(f"    Fold {fold_idx+1}: {roc_auc_score(y_val, oof[val_idx]):.5f}")
        
        overall = roc_auc_score(y_train, oof)
        if self.verbose:
            print(f"    LGB Retrained OOF AUC: {overall:.5f}")
        return oof
    
    def _retrain_xgb_with_pseudo_labels(self, X_train, y_train, X_pseudo, y_pseudo, xgb_params):
        """用伪标签重新训练XGB - 与run2.py完全一致"""
        xgb_params_copy = xgb_params.copy()
        n_estimators = xgb_params_copy.pop('n_estimators', 1000)
        xgb_params_copy.update({'n_estimators': n_estimators, 'random_state': 42, 'verbosity': 0})
        
        oof = np.zeros(len(X_train))
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            X_val, y_val = X_train[val_idx], y_train[val_idx]
            
            X_combined = np.vstack([X_tr, X_pseudo])
            y_combined = np.concatenate([y_tr, y_pseudo]).astype(int)
            sample_weight = np.concatenate([np.ones(len(y_tr)), np.ones(len(y_pseudo)) * 0.5])
            
            clf = xgb.XGBClassifier(**xgb_params_copy)
            clf.fit(X_combined, y_combined, sample_weight=sample_weight, eval_set=[(X_val, y_val)], verbose=False)
            
            oof[val_idx] = clf.predict_proba(X_val)[:, 1]
            if self.verbose:
                print(f"    Fold {fold_idx+1}: {roc_auc_score(y_val, oof[val_idx]):.5f}")
        
        overall = roc_auc_score(y_train, oof)
        if self.verbose:
            print(f"    XGB Retrained OOF AUC: {overall:.5f}")
        return oof
    
    def _retrain_cat_with_pseudo_labels(self, X_train, y_train, X_pseudo, y_pseudo, cat_params):
        """用伪标签重新训练CAT - 与run2.py完全一致"""
        cat_params_copy = cat_params.copy()
        n_estimators = cat_params_copy.pop('n_estimators', 1000)
        cat_params_copy.update({'iterations': n_estimators, 'random_state': 42, 'verbose': 0, 'thread_count': -1})
        
        oof = np.zeros(len(X_train))
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            X_val, y_val = X_train[val_idx], y_train[val_idx]
            
            X_combined = np.vstack([X_tr, X_pseudo])
            y_combined = np.concatenate([y_tr, y_pseudo]).astype(int)
            sample_weight = np.concatenate([np.ones(len(y_tr)), np.ones(len(y_pseudo)) * 0.5])
            
            clf = CatBoostClassifier(**cat_params_copy)
            clf.fit(X_combined, y_combined, sample_weight=sample_weight, eval_set=[(X_val, y_val)], verbose=False)
            
            oof[val_idx] = clf.predict_proba(X_val)[:, 1]
            if self.verbose:
                print(f"    Fold {fold_idx+1}: {roc_auc_score(y_val, oof[val_idx]):.5f}")
        
        overall = roc_auc_score(y_train, oof)
        if self.verbose:
            print(f"    CAT Retrained OOF AUC: {overall:.5f}")
        return oof
    
    def _retrain_model(self, model_type, X_train, y_train, X_pseudo, y_pseudo, params):
        """Generic retrain helper"""
        oof = np.zeros(len(X_train))
        
        p = params.copy()
        est = p.pop('n_estimators') if 'n_estimators' in p else p.pop('iterations', 100)
        
        for fold, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            
            # Combine
            X_comb = np.vstack([X_tr, X_pseudo]) if len(X_pseudo) > 0 else X_tr
            y_comb = np.concatenate([y_tr, y_pseudo]) if len(y_pseudo) > 0 else y_tr
            w = np.concatenate([np.ones(len(y_tr)), np.ones(len(y_pseudo))*0.5]) if len(y_pseudo) > 0 else None
            
            if model_type == 'lgb':
                p.update({'verbose': -1, 'objective': 'binary', 'metric': 'auc'})
                clf = lgb.train(p, lgb.Dataset(X_comb, y_comb, weight=w), num_boost_round=est, callbacks=[lgb.log_evaluation(0)])
                oof[val_idx] = clf.predict(X_train[val_idx])
            elif model_type == 'xgb':
                p.update({'n_estimators': est, 'verbosity': 0})
                clf = xgb.XGBClassifier(**p)
                clf.fit(X_comb, y_comb, sample_weight=w, verbose=False)
                oof[val_idx] = clf.predict_proba(X_train[val_idx])[:, 1]
            elif model_type == 'cat':
                p.update({'iterations': est, 'verbose': 0})
                clf = CatBoostClassifier(**p)
                clf.fit(X_comb, y_comb.astype(int), sample_weight=w, verbose=False)
                oof[val_idx] = clf.predict_proba(X_train[val_idx])[:, 1]
                
        return oof

    def generate_test_predictions(self, X_test, X_train, y_train, lgb_params, xgb_params, cat_params):
        """生成测试集预测（merged 模式：伪标签参与fold分割）"""
        print("\n" + "="*70)
        print("GENERATING TEST PREDICTIONS")
        print("="*70)
        
        # 1. LGB
        print("\n[1/3] LightGBM test predictions...")
        lgb_test = self._generate_lgb_test_preds(X_test, X_train, y_train, lgb_params)
        
        # 2. XGB  
        print("[2/3] XGBoost test predictions...")
        xgb_test = self._generate_xgb_test_preds(X_test, X_train, y_train, xgb_params)
        
        # 3. CAT
        print("[3/3] CatBoost test predictions...")
        cat_test = self._generate_cat_test_preds(X_test, X_train, y_train, cat_params)
        
        return {
            'lgb': lgb_test,
            'xgb': xgb_test,
            'cat': cat_test
        }
    
    def _generate_lgb_test_preds(self, X_test, X_train, y_train, lgb_params):
        """LGB测试集预测（merged模式）"""
        lgb_params_copy = lgb_params.copy()
        n_estimators = lgb_params_copy.pop('n_estimators', 1000)
        lgb_params_copy.update({'objective': 'binary', 'metric': 'auc', 'seed': 42, 'verbose': -1})
        
        test_preds = np.zeros(len(X_test))
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            dtrain = lgb.Dataset(X_tr, label=y_tr)
            clf = lgb.train(lgb_params_copy, dtrain, num_boost_round=n_estimators, callbacks=[lgb.log_evaluation(period=0)])
            test_preds += clf.predict(X_test) / 5
        return test_preds
    
    def _generate_xgb_test_preds(self, X_test, X_train, y_train, xgb_params):
        """XGB测试集预测（merged模式）"""
        xgb_params_copy = xgb_params.copy()
        n_estimators = xgb_params_copy.pop('n_estimators', 1000)
        xgb_params_copy['n_estimators'] = n_estimators
        xgb_params_copy['random_state'] = 42
        xgb_params_copy['verbosity'] = 0
        
        test_preds = np.zeros(len(X_test))
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            clf = xgb.XGBClassifier(**xgb_params_copy)
            clf.fit(X_tr, y_tr, verbose=False)
            test_preds += clf.predict_proba(X_test)[:, 1] / 5
        return test_preds
    
    def _generate_cat_test_preds(self, X_test, X_train, y_train, cat_params):
        """CAT测试集预测（merged模式）"""
        cat_params_copy = cat_params.copy()
        n_estimators = cat_params_copy.pop('n_estimators', 1000)
        cat_params_copy.update({'iterations': n_estimators, 'random_state': 42, 'verbose': 0, 'thread_count': -1})
        
        test_preds = np.zeros(len(X_test))
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            clf = CatBoostClassifier(**cat_params_copy)
            clf.fit(X_tr, y_tr, verbose=False)
            test_preds += clf.predict_proba(X_test)[:, 1] / 5
        return test_preds
    
    def generate_test_predictions_retrained(self, X_test, X_train, y_train, X_pseudo, y_pseudo, lgb_params, xgb_params, cat_params):
        """用重新训练的模型生成测试集预测（最终预测时使用）"""
        if self.verbose:
            print("\n" + "="*70)
            print("GENERATING TEST PREDICTIONS: Retrained Models")
            print("="*70)
        
        # LGB test predictions (with pseudo-labels)
        print("\n[1/3] LightGBM test predictions...")
        lgb_test = self._generate_lgb_test_preds_retrained(X_test, X_train, y_train, X_pseudo, y_pseudo, lgb_params)
        
        # XGB test predictions (with pseudo-labels)
        print("[2/3] XGBoost test predictions...")
        xgb_test = self._generate_xgb_test_preds_retrained(X_test, X_train, y_train, X_pseudo, y_pseudo, xgb_params)
        
        # CAT test predictions (with pseudo-labels)
        print("[3/3] CatBoost test predictions...")
        cat_test = self._generate_cat_test_preds_retrained(X_test, X_train, y_train, X_pseudo, y_pseudo, cat_params)
        
        return {
            'lgb': lgb_test,
            'xgb': xgb_test,
            'cat': cat_test
        }
    
    def _generate_lgb_test_preds_retrained(self, X_test, X_train, y_train, X_pseudo, y_pseudo, lgb_params):
        """LGB测试集预测（用伪标签重新训练）"""
        lgb_params_copy = lgb_params.copy()
        n_estimators = lgb_params_copy.pop('n_estimators', 1000)
        lgb_params_copy.update({
            'objective': 'binary',
            'metric': 'auc',
            'seed': 42,
            'verbose': -1
        })
        
        test_preds = np.zeros(len(X_test))
        
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            
            # 合并伪标签
            X_combined = np.vstack([X_tr, X_pseudo])
            y_combined = np.concatenate([y_tr, y_pseudo])
            y_combined = np.asarray(y_combined).ravel().astype(int)
            
            sample_weight = np.concatenate([
                np.ones(len(y_tr)),
                np.ones(len(y_pseudo)) * 0.5
            ])
            
            assert len(y_combined) == X_combined.shape[0], f"标签长度 {len(y_combined)} 不匹配数据长度 {X_combined.shape[0]}"
            
            dtrain = lgb.Dataset(X_combined, label=y_combined, weight=sample_weight)
            clf = lgb.train(
                lgb_params_copy, dtrain,
                num_boost_round=n_estimators,
                callbacks=[lgb.log_evaluation(period=0)]
            )
            
            test_preds += clf.predict(X_test) / 5
        
        return test_preds
    
    def _generate_xgb_test_preds_retrained(self, X_test, X_train, y_train, X_pseudo, y_pseudo, xgb_params):
        """XGB测试集预测（用伪标签重新训练）"""
        xgb_params_copy = xgb_params.copy()
        n_estimators = xgb_params_copy.pop('n_estimators', 1000)
        xgb_params_copy['n_estimators'] = n_estimators
        xgb_params_copy['random_state'] = 42
        xgb_params_copy['verbosity'] = 0
        
        test_preds = np.zeros(len(X_test))
        
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            
            X_combined = np.vstack([X_tr, X_pseudo])
            y_combined = np.concatenate([y_tr, y_pseudo])
            y_combined = np.asarray(y_combined).ravel().astype(int)
            
            sample_weight = np.concatenate([
                np.ones(len(y_tr)),
                np.ones(len(y_pseudo)) * 0.5
            ])
            
            clf = xgb.XGBClassifier(**xgb_params_copy)
            clf.fit(
                X_combined, y_combined,
                sample_weight=sample_weight,
                verbose=False
            )
            
            test_preds += clf.predict_proba(X_test)[:, 1] / 5
        
        return test_preds
    
    def _generate_cat_test_preds_retrained(self, X_test, X_train, y_train, X_pseudo, y_pseudo, cat_params):
        """CAT测试集预测（用伪标签重新训练）"""
        cat_params_copy = cat_params.copy()
        n_estimators = cat_params_copy.pop('n_estimators', 1000)
        cat_params_copy.update({
            'iterations': n_estimators,
            'random_state': 42,
            'verbose': 0,
            'thread_count': -1
        })
        
        test_preds = np.zeros(len(X_test))
        
        for fold_idx, (train_idx, val_idx) in enumerate(self.skf.split(X_train, y_train)):
            X_tr, y_tr = X_train[train_idx], y_train[train_idx]
            
            X_combined = np.vstack([X_tr, X_pseudo])
            y_combined = np.concatenate([y_tr, y_pseudo])
            y_combined = np.asarray(y_combined).ravel().astype(int)
            
            sample_weight = np.concatenate([
                np.ones(len(y_tr)),
                np.ones(len(y_pseudo)) * 0.5
            ])
            
            clf = CatBoostClassifier(**cat_params_copy)
            clf.fit(
                X_combined, y_combined,
                sample_weight=sample_weight,
                verbose=False
            )
            
            test_preds += clf.predict_proba(X_test)[:, 1] / 5
        
        return test_preds

def main(verbose=True):
    """主程序 - 多轮半监督学习（完全对齐 run2.py）"""
    model = MultiRoundSemiSupervised(verbose=verbose)
    
    print("\n" + "="*70 + "\nSTEP 0: DATA PREPARATION\n" + "="*70)
    X_train, y_train, X_test, df_train, df_test, selected_features = model.prepare_data(include_test=True)
    lgb_params, xgb_params, cat_params = model.load_tuned_params()
    
    print("\n" + "="*70 + "\nSTEP 1: INITIAL TRAINING & GRID SEARCH\n" + "="*70)
    oof_preds = model.generate_oof_predictions_base_models(X_train, y_train, lgb_params, xgb_params, cat_params)
    best_weights, best_auc = simple_grid_search_weights(oof_preds, y_train, step=0.1, use_rank=True, verbose=True)
    model.best_weights = best_weights
    
    print("\n" + "="*70 + "\nSTEP 2: MULTI-ROUND SEMI-SUPERVISED LEARNING\n" + "="*70)
    X_train_current = X_train.copy()
    y_train_current = y_train.copy()
    X_pseudo_accumulated = np.empty((0, X_train.shape[1]))
    y_pseudo_accumulated = np.empty(0)
    pseudo_label_candidates = {}  # 存储(idx): (X, y)的候选伪标签
    
    # 早停管理器
    early_stopping = EarlyStopping(patience=3, verbose=True)
    max_iterations = 5  # 限制最大迭代次数为5
    best_iteration_fusion = None
    
    for iteration in range(1, max_iterations + 1): 
        print(f"\n{'='*70}")
        print(f"ITERATION {iteration} | Accumulated Pseudo: {len(y_pseudo_accumulated)}")
        print(f"{'='*70}")
        
        # 步骤1：重新训练模型
        print(f"\n[Round {iteration}] 重新训练（含伪标签）+验证（原始数据）...")
        print(f"  Training on: {len(X_train)} + {len(X_pseudo_accumulated)} samples")
        
        print("  [1/3] Retraining LGB...")
        lgb_oof = model._retrain_lgb_with_pseudo_labels(X_train, y_train, X_pseudo_accumulated, y_pseudo_accumulated, lgb_params)
        
        print("  [2/3] Retraining XGB...")
        xgb_oof = model._retrain_xgb_with_pseudo_labels(X_train, y_train, X_pseudo_accumulated, y_pseudo_accumulated, xgb_params)
        
        print("  [3/3] Retraining CAT...")
        cat_oof = model._retrain_cat_with_pseudo_labels(X_train, y_train, X_pseudo_accumulated, y_pseudo_accumulated, cat_params)
        
        oof_preds = {'lgb': lgb_oof, 'xgb': xgb_oof, 'cat': cat_oof}
        
        # 步骤2：重新优化权重
        print(f"\n[Round {iteration}] Grid Search优化权重（基于原始训练集）...")
        best_weights, best_auc = simple_grid_search_weights(oof_preds, y_train, step=0.1, use_rank=True, verbose=False)
        model.best_weights = best_weights
        print(f"  新权重: LGB={best_weights['lgb']:.3f}, XGB={best_weights['xgb']:.3f}, CAT={best_weights['cat']:.3f}")
        
        # 步骤3：计算6种融合方式的AUC
        print(f"\n[Round {iteration}] 计算6种融合方式的AUC（基于原始训练集）...")
        print("  [1/6] Weighted Ensemble (Rank Averaging)...")
        (weighted_auc, lgb_stacking_auc, lr_auc, lasso_auc, ridge_auc, br_auc,
         oof_weighted, oof_lgb_stacking, oof_lr, oof_lasso, oof_ridge, oof_br) = model.compute_ensemble_aucs(
            oof_preds['lgb'], oof_preds['xgb'], oof_preds['cat'], y_train)
        
        # 选择最佳融合方式
        aucs = {
            'Weighted': weighted_auc, 'LGB': lgb_stacking_auc, 'LR': lr_auc,
            'Lasso': lasso_auc, 'Ridge': ridge_auc, 'BayesianRidge': br_auc
        }
        best_fusion = max(aucs, key=aucs.get)
        best_fusion_auc = aucs[best_fusion]
        
        print(f"\n  Fusion Results:")
        for name, auc in aucs.items():
            print(f"    {name} AUC: {auc:.5f}")
        print(f"    🏆 Best: {best_fusion} ({best_fusion_auc:.5f})")
        
        # 步骤4：检查早停
        current_state = {
            'iteration': iteration, 'best_weights': best_weights.copy(),
            'weighted_auc': weighted_auc, 'lgb_stacking_auc': lgb_stacking_auc,
            'lr_auc': lr_auc, 'lasso_auc': lasso_auc, 'ridge_auc': ridge_auc,
            'br_auc': br_auc, 'best_fusion': best_fusion,
            'X_pseudo_accumulated': X_pseudo_accumulated.copy() if len(X_pseudo_accumulated) > 0 else np.empty((0, X_train.shape[1])),
            'y_pseudo_accumulated': y_pseudo_accumulated.copy() if len(y_pseudo_accumulated) > 0 else np.empty(0)
        }
        
        should_stop = early_stopping.should_stop(best_fusion_auc, iteration, current_state)
        
        # 步骤5：生成全量测试集的预测（使用Train+Pseudo进行模型训练）
        print(f"\n[Round {iteration}] 生成完整测试集预测... ({len(X_test)} samples)")
        # 为测试集预测组织Train+Pseudo数据
        X_train_for_test = np.vstack([X_train, X_pseudo_accumulated]) if len(X_pseudo_accumulated) > 0 else X_train
        y_train_for_test = np.concatenate([y_train, y_pseudo_accumulated]) if len(y_pseudo_accumulated) > 0 else y_train
        test_preds_full = model.generate_test_predictions(X_test, X_train_for_test, y_train_for_test, lgb_params, xgb_params, cat_params)
        
        # 步骤6：融合测试集预测（使用最优权重和Rank Averaging）
        rank_test = {}
        for name, preds in test_preds_full.items():
            rank_test[name] = rankdata(preds) / len(preds)
        
        ensemble_test = (
            best_weights['lgb'] * rank_test['lgb'] +
            best_weights['xgb'] * rank_test['xgb'] +
            best_weights['cat'] * rank_test['cat']
        )
        
        # 步骤7：从完整测试集中选择满足0.95阈值的样本
        print(f"\n[Round {iteration}] 从完整测试集选择满足0.95阈值的伪标签...")
        high_conf_mask = (ensemble_test > 0.95) | (ensemble_test < 0.05)
        high_conf_indices = np.where(high_conf_mask)[0]
        
        # 更新候选伪标签：添加新的满足阈值的样本
        for idx in high_conf_indices:
            if idx not in pseudo_label_candidates:
                # 新增候选
                pseudo_label_candidates[idx] = (
                    X_test[idx],
                    int(ensemble_test[idx] > 0.5)
                )
        
        # 移除不满足阈值的候选伪标签（回溯检查）
        indices_to_remove = [idx for idx in pseudo_label_candidates if idx not in high_conf_indices]
        for idx in indices_to_remove:
            del pseudo_label_candidates[idx]
        
        # 重新构建X_pseudo_accumulated和y_pseudo_accumulated（只保留当前满足的）
        if len(pseudo_label_candidates) > 0:
            X_pseudo_accumulated = np.array([pseudo_label_candidates[idx][0] for idx in sorted(pseudo_label_candidates.keys())])
            y_pseudo_accumulated = np.array([pseudo_label_candidates[idx][1] for idx in sorted(pseudo_label_candidates.keys())])
            new_count = len(pseudo_label_candidates)
        else:
            X_pseudo_accumulated = np.empty((0, X_train.shape[1]))
            y_pseudo_accumulated = np.empty(0)
            new_count = 0
        
        print(f"\n  满足阈值的候选伪标签: {new_count} / {len(X_test)} ({new_count/len(X_test)*100:.1f}%)")
        if indices_to_remove:
            print(f"  本轮移除不满足阈值的伪标签: {len(indices_to_remove)}")
        if new_count > 0:
            print(f"  伪标签正样本比例: {y_pseudo_accumulated.mean():.3f}")
        
        # 记录迭代信息
        model.iteration_history.append({
            'iteration': iteration,
            'weighted_auc': float(weighted_auc),
            'lgb_stacking_auc': float(lgb_stacking_auc),
            'lr_auc': float(lr_auc),
            'lasso_auc': float(lasso_auc),
            'ridge_auc': float(ridge_auc),
            'br_auc': float(br_auc),
            'best_fusion': best_fusion,
            'weights': best_weights.copy(),
            'total_pseudo_labels': new_count,
            'removed_pseudo_labels': len(indices_to_remove)
        })
        
        # 检查停止条件
        if new_count == 0:
            print(f"\n[STOP] 没有满足阈值的伪标签，停止迭代")
            break
        
        if should_stop:
            print(f"\n[STOP] 早停触发：连续3轮AUC无提升，停止迭代")
            print(f"  最佳迭代: {early_stopping.best_iteration}")
            break
        
        if iteration >= max_iterations:
            print(f"\n[STOP] 达到最大迭代次数 {max_iterations}，停止迭代")
            break
        
        # 步骤8：继续下一轮迭代（X_pseudo_accumulated已在上面重新构建）
        # 注意：X_train_current和y_train_current不再用于OOF生成，只用于测试集预测
    
    # =========================================================
    # [关键修复] 循环结束后，强制加载历史最佳状态
    # =========================================================
    # 问题：当迭代达到max_iterations时，循环末尾生成的新伪标签（Step 7产出）
    #      会覆盖内存，但这些伪标签从未被验证过，可能包含噪声
    # 
    # 解决：无论如何，EarlyStopping对象中保存的best_state永远是历史上
    #      经过验证的最好状态。我们必须强制恢复它。
    
    best_state_from_es = early_stopping.get_best_state()
    
    # 只要有过最佳记录 (best_auc > 0)，就强制回滚
    if early_stopping.best_auc > 0 and best_state_from_es:
        print(f"\n[ROLLBACK] 正在恢复最佳迭代 (Iteration {early_stopping.best_iteration}) 的状态...")
        print(f"  当前内存伪标签数: {len(y_pseudo_accumulated)} (将被丢弃)")
        
        # 强制覆盖当前内存中的变量
        best_weights = best_state_from_es['best_weights']
        model.best_weights = best_weights
        
        # 关键：恢复产生最佳AUC时的输入数据
        X_pseudo_accumulated = best_state_from_es['X_pseudo_accumulated']
        y_pseudo_accumulated = best_state_from_es['y_pseudo_accumulated']
        best_iteration_fusion = best_state_from_es['best_fusion']
        
        print(f"  恢复伪标签数量: {len(y_pseudo_accumulated)} (这是产生最佳AUC {early_stopping.best_auc:.5f} 的功臣)")
        print(f"  最佳融合方式: {best_iteration_fusion}")
        print(f"  Weighted AUC: {best_state_from_es['weighted_auc']:.5f}")
        print(f"  LGB Stacking AUC: {best_state_from_es['lgb_stacking_auc']:.5f}")
        print(f"  LR AUC: {best_state_from_es['lr_auc']:.5f}")
        print(f"  Lasso AUC: {best_state_from_es['lasso_auc']:.5f}")
        print(f"  Ridge AUC: {best_state_from_es['ridge_auc']:.5f}")
        print(f"  BayesianRidge AUC: {best_state_from_es['br_auc']:.5f}")
    else:
        print("\n[WARNING] 未找到最佳状态，将使用最后一次迭代的数据")
        best_iteration_fusion = None
    
    # 最终训练：使用所有累积的伪标签
    print("\n" + "="*70)
    print("STEP 3: FINAL TRAINING WITH ALL PSEUDO-LABELS")
    print("="*70)
    
    print(f"\n总累积伪标签数: {len(y_pseudo_accumulated)}")
    print(f"最终训练集大小: {len(X_train) + len(y_pseudo_accumulated)}")
    
    # 用最终训练集重新训练模型
    print("\n[最终] 用所有累积伪标签重新训练模型...")
    
    print("  [1/3] Retraining LGB...")
    lgb_oof_final = model._retrain_lgb_with_pseudo_labels(X_train, y_train, X_pseudo_accumulated, y_pseudo_accumulated, lgb_params)
    
    print("  [2/3] Retraining XGB...")
    xgb_oof_final = model._retrain_xgb_with_pseudo_labels(X_train, y_train, X_pseudo_accumulated, y_pseudo_accumulated, xgb_params)
    
    print("  [3/3] Retraining CAT...")
    cat_oof_final = model._retrain_cat_with_pseudo_labels(X_train, y_train, X_pseudo_accumulated, y_pseudo_accumulated, cat_params)
    
    # 最终融合 - 计算6种方式的AUC
    print("\n[最终] 计算6种融合方式的最终AUC...")
    
    # 方式1：加权融合（使用原始概率，不使用rank average）
    ensemble_oof_final_weighted = (
        model.best_weights['lgb'] * lgb_oof_final +
        model.best_weights['xgb'] * xgb_oof_final +
        model.best_weights['cat'] * cat_oof_final
    )
    weighted_auc_final = roc_auc_score(y_train, ensemble_oof_final_weighted)
    
    # 为Stacking模型构建输入特征（使用rank average）
    rank_oof_final = {
        'lgb': rankdata(lgb_oof_final) / len(lgb_oof_final),
        'xgb': rankdata(xgb_oof_final) / len(xgb_oof_final),
        'cat': rankdata(cat_oof_final) / len(cat_oof_final)
    }
    ensemble_oof_final_weighted_rank = (
        model.best_weights['lgb'] * rank_oof_final['lgb'] +
        model.best_weights['xgb'] * rank_oof_final['xgb'] +
        model.best_weights['cat'] * rank_oof_final['cat']
    )
    
    # 方式2：LGB Stacking（浅层，使用logit变换+rank average）
    print("  Training final LGB Stacking (with Logit Transform)...")
    oof_lgb_stacking_final, lgb_stacking_auc_final = model.train_lgb_stacking(
        lgb_oof_final, xgb_oof_final, cat_oof_final, ensemble_oof_final_weighted_rank, y_train
    )
    
    # 方式3：LR Stacking（Logistic回归）
    print("  Training final LR Stacking...")
    oof_lr_final, lr_auc_final = model.train_lr_stacking(
        lgb_oof_final, xgb_oof_final, cat_oof_final, ensemble_oof_final_weighted_rank, y_train
    )
    
    # 方式4：Lasso Stacking（L1正则化）
    print("  Training final Lasso Stacking...")
    oof_lasso_final, lasso_auc_final = model.train_lasso_stacking(
        lgb_oof_final, xgb_oof_final, cat_oof_final, ensemble_oof_final_weighted_rank, y_train
    )
    
    # 方式5：Ridge Stacking（L2正则化）
    print("  Training final Ridge Stacking...")
    oof_ridge_final, ridge_auc_final = model.train_ridge_stacking(
        lgb_oof_final, xgb_oof_final, cat_oof_final, ensemble_oof_final_weighted_rank, y_train
    )
    
    # 方式6：BayesianRidge Stacking（概率线性回归）
    print("  Training final BayesianRidge Stacking...")
    oof_br_final, br_auc_final = model.train_bayesian_ridge_stacking(
        lgb_oof_final, xgb_oof_final, cat_oof_final, ensemble_oof_final_weighted_rank, y_train
    )
    
    # 选择最佳融合方式作为最终预测
    final_aucs = {
        'Weighted': weighted_auc_final,
        'LGB-Stacking': lgb_stacking_auc_final,
        'LR': lr_auc_final,
        'Lasso': lasso_auc_final,
        'Ridge': ridge_auc_final,
        'BayesianRidge': br_auc_final
    }
    best_final_fusion = max(final_aucs, key=final_aucs.get)
    best_final_auc = final_aucs[best_final_fusion]
    
    if best_final_fusion == 'Weighted':
        ensemble_oof_final = ensemble_oof_final_weighted
    elif best_final_fusion == 'LGB-Stacking':
        ensemble_oof_final = oof_lgb_stacking_final
    elif best_final_fusion == 'LR':
        ensemble_oof_final = oof_lr_final
    elif best_final_fusion == 'Lasso':
        ensemble_oof_final = oof_lasso_final
    elif best_final_fusion == 'Ridge':
        ensemble_oof_final = oof_ridge_final
    else:  # BayesianRidge
        ensemble_oof_final = oof_br_final
    
    print(f"\n最终融合结果:")
    print(f"  Weighted Ensemble Final AUC: {weighted_auc_final:.5f}")
    print(f"  LGB Stacking Final AUC: {lgb_stacking_auc_final:.5f}")
    print(f"  LR Stacking Final AUC: {lr_auc_final:.5f}")
    print(f"  Lasso Stacking Final AUC: {lasso_auc_final:.5f}")
    print(f"  Ridge Stacking Final AUC: {ridge_auc_final:.5f}")
    print(f"  BayesianRidge Stacking Final AUC: {br_auc_final:.5f}")
    print(f"  🏆 最佳融合方式: {best_final_fusion} ({best_final_auc:.5f})")
    
    # 生成最终测试集预测
    print("\n" + "="*70)
    print("STEP 4: GENERATING FINAL TEST PREDICTIONS")
    print("="*70)
    
    test_preds_final = model.generate_test_predictions_retrained(X_test, X_train, y_train, X_pseudo_accumulated, y_pseudo_accumulated, lgb_params, xgb_params, cat_params)
    
    # 使用最佳融合方式进行测试集预测
    if best_final_fusion == 'Weighted':
        # 加权融合：使用原始概率，不使用rank average
        ensemble_test_final = (
            model.best_weights['lgb'] * test_preds_final['lgb'] +
            model.best_weights['xgb'] * test_preds_final['xgb'] +
            model.best_weights['cat'] * test_preds_final['cat']
        )
    else:
        # 对于MLP/LR，需要基于测试集预测重新训练
        # 这里简化处理，直接使用加权融合的原始概率预测作为fallback
        ensemble_test_final = (
            model.best_weights['lgb'] * test_preds_final['lgb'] +
            model.best_weights['xgb'] * test_preds_final['xgb'] +
            model.best_weights['cat'] * test_preds_final['cat']
        )
    
    # 保存结果
    print("\n" + "="*70)
    print("STEP 5: SAVING RESULTS")
    print("="*70)
    
    experiments_dir = os.path.join(project_root, 'experiments')
    evaluator = Evaluator(experiments_dir=experiments_dir)
    
    result_dir = evaluator.save_experiment_results(
        exp_name='export',
        df_train=df_train[['id', 'label']],
        oof_preds=ensemble_oof_final,
        test_preds=ensemble_test_final,
        fold_scores=[],
        overall_auc=best_final_auc,
        feature_importance_df=None,
        feature_names=selected_features,
        df_test=df_test[['id']] if 'df_test' in locals() else None
    )
    
    print(f"\n✅ Export complete. Final AUC: {best_final_auc:.5f}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Multi-round Semi-supervised Learning (完全对齐 run2.py)')
    parser.add_argument('--verbose', type=bool, default=True,
                        help='是否打印详细信息')
    
    args = parser.parse_args()
    main(verbose=args.verbose)
