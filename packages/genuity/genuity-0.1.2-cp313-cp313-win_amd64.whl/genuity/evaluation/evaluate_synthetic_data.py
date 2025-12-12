#!/usr/bin/env python3
"""
Simple Synthetic Data Evaluation Script
Works with DataFrames directly for pre-processing vs post-processing comparison.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, roc_auc_score
from scipy.stats import ks_2samp, wasserstein_distance
from scipy.spatial.distance import jensenshannon
import warnings
warnings.filterwarnings('ignore')

def auto_detect_target_column(pre_df, post_df):
    """
    Auto-detect target column from DataFrames.
    
    Args:
        pre_df: Pre-processed DataFrame
        post_df: Post-processed DataFrame
    
    Returns:
        str: Detected target column name or None
    """
    # Find common columns
    common_cols = set(pre_df.columns) & set(post_df.columns)
    
    if len(common_cols) == 0:
        print("⚠️ No common columns found between DataFrames")
        return None
    
    # Strategy 1: Look for common target column names
    target_keywords = ['target', 'label', 'class', 'outcome', 'result', 'prediction', 'y']
    for col in common_cols:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in target_keywords):
            print(f"🎯 Auto-detected target column: '{col}' (keyword match)")
            return col
    
    # Strategy 2: Look for last numerical column (common regression target position)
    numerical_cols = [col for col in common_cols if pre_df[col].dtype in ['int64', 'float64']]
    if numerical_cols:
        # Get the last numerical column
        last_numerical = numerical_cols[-1]
        print(f"🎯 Auto-detected target column: '{last_numerical}' (last numerical column)")
        return last_numerical
    
    # Strategy 3: Look for column with fewest unique values (classification target)
    categorical_cols = [col for col in common_cols if pre_df[col].dtype == 'object']
    if categorical_cols:
        # Find column with fewest unique values
        min_unique = float('inf')
        best_categorical = None
        for col in categorical_cols:
            unique_count = len(pre_df[col].unique())
            if unique_count < min_unique and unique_count > 1:
                min_unique = unique_count
                best_categorical = col
        
        if best_categorical:
            print(f"🎯 Auto-detected target column: '{best_categorical}' (categorical with {min_unique} unique values)")
            return best_categorical
    
    print("⚠️ Could not auto-detect target column. Please specify manually.")
    return None

def quick_evaluation(pre_df, post_df, target_column=None):
    """
    Quick evaluation of pre-processing vs post-processing DataFrames.
    
    Args:
        pre_df: Pre-processed DataFrame
        post_df: Post-processed DataFrame
        target_column: Name of target column for TSTR evaluation (auto-detected if None)
    
    Returns:
        dict: Evaluation results
    """
    print("🚀 QUICK PRE-PROCESSING VS POST-PROCESSING EVALUATION")
    print("="*60)
    
    # Auto-detect target column if not provided
    if target_column is None:
        target_column = auto_detect_target_column(pre_df, post_df)
        if target_column is None:
            print("❌ No target column specified and auto-detection failed.")
            print("💡 Please specify target_column manually or check your data.")
            return {}
    
    results = {}
    
    # Basic info
    print(f"📊 Pre-processing shape: {pre_df.shape}")
    print(f"📊 Post-processing shape: {post_df.shape}")
    print(f"🎯 Target column: {target_column}")
    
    # 1. Basic Statistics Comparison
    print("\n📊 Basic Statistics Comparison:")
    numerical_cols = pre_df.select_dtypes(include=[np.number]).columns
    numerical_cols = [col for col in numerical_cols if col != target_column]
    
    for col in numerical_cols[:5]:  # First 5 columns
        if col in pre_df.columns and col in post_df.columns:
            pre_mean = pre_df[col].mean()
            post_mean = post_df[col].mean()
            pre_std = pre_df[col].std()
            post_std = post_df[col].std()
            
            mean_diff = abs(pre_mean - post_mean) / pre_mean if pre_mean != 0 else 0
            std_diff = abs(pre_std - post_std) / pre_std if pre_std != 0 else 0
            
            print(f"  {col}: Mean diff={mean_diff:.4f}, Std diff={std_diff:.4f}")
    
    # 2. Kolmogorov-Smirnov Test
    print("\n🔍 Kolmogorov-Smirnov Test (First 3 numerical columns):")
    ks_scores = []
    for col in numerical_cols[:3]:
        if col in pre_df.columns and col in post_df.columns:
            ks_stat, p_value = ks_2samp(
                pre_df[col].dropna(), 
                post_df[col].dropna()
            )
            ks_scores.append(ks_stat)
            print(f"  {col}: KS={ks_stat:.4f}, p={p_value:.4f}")
    
    results['avg_ks'] = np.mean(ks_scores) if ks_scores else 0
    
    # 3. TSTR Evaluation (Train on Pre, Test on Post)
    print("\n🎯 TSTR (Train on Pre, Test on Post):")
    if target_column in pre_df.columns and target_column in post_df.columns:
        X_pre = pre_df.drop(columns=[target_column])
        y_pre = pre_df[target_column]
        X_post = post_df.drop(columns=[target_column])
        y_post = post_df[target_column]
        
        # Remove non-numeric columns for simplicity
        X_pre = X_pre.select_dtypes(include=[np.number])
        X_post = X_post.select_dtypes(include=[np.number])
        
        if len(X_pre.columns) > 0 and len(X_post.columns) > 0:
            # Align columns
            common_cols = set(X_pre.columns) & set(X_post.columns)
            X_pre = X_pre[list(common_cols)]
            X_post = X_post[list(common_cols)]
            
            # Determine if classification or regression
            is_classification = y_pre.dtype == 'object' or len(y_pre.unique()) < 10
            
            if is_classification:
                model = RandomForestClassifier(n_estimators=50, random_state=42)
                model.fit(X_pre, y_pre)
                y_pred = model.predict(X_post)
                accuracy = accuracy_score(y_post, y_pred)
                results['tstr_accuracy'] = accuracy
                print(f"  Classification Accuracy: {accuracy:.4f}")
            else:
                model = RandomForestRegressor(n_estimators=50, random_state=42)
                model.fit(X_pre, y_pre)
                y_pred = model.predict(X_post)
                r2 = r2_score(y_post, y_pred)
                mse = mean_squared_error(y_post, y_pred)
                results['tstr_r2'] = r2
                results['tstr_mse'] = mse
                print(f"  Regression R²: {r2:.4f}, MSE: {mse:.4f}")
    
    # 4. Overall Quality Score
    print("\n🏆 Overall Quality Assessment:")
    scores = []
    
    # SDM Score (lower KS is better)
    if 'avg_ks' in results:
        sdm_score = 1 - results['avg_ks']
        scores.append(sdm_score)
        print(f"  SDM Score: {sdm_score:.4f}")
    
    # TSTR Score
    if 'tstr_accuracy' in results:
        scores.append(results['tstr_accuracy'])
        print(f"  TSTR Accuracy: {results['tstr_accuracy']:.4f}")
    elif 'tstr_r2' in results:
        scores.append(max(0, results['tstr_r2']))
        print(f"  TSTR R²: {max(0, results['tstr_r2']):.4f}")
    
    if scores:
        overall_score = np.mean(scores)
        results['overall_score'] = overall_score
        print(f"\n🎯 OVERALL QUALITY SCORE: {overall_score:.4f}")
        
        if overall_score >= 0.8:
            print("🌟 EXCELLENT: Very similar data!")
        elif overall_score >= 0.6:
            print("✅ GOOD: Acceptable similarity.")
        elif overall_score >= 0.4:
            print("⚠️ FAIR: Some differences detected.")
        else:
            print("❌ POOR: Significant differences.")
    
    # 5. Generate plots
    print("\n📊 Generating comparison plots...")
    plot_df_comparison(pre_df, post_df, target_column)
    
    return results

def compare_pre_post_processing(pre_df, post_df, target_column=None):
    """
    Compare pre-processing vs post-processing DataFrames.
    
    Args:
        pre_df: Pre-processed DataFrame
        post_df: Post-processed DataFrame
        target_column: Target column name
    
    Returns:
        dict: Comparison results
    """
    print("\n🔄 PRE-PROCESSING VS POST-PROCESSING COMPARISON")
    print("="*60)
    
    # Quick comparison
    results = quick_evaluation(pre_df, post_df, target_column)
    
    # Additional comparison metrics
    print("\n📊 Additional Comparison Metrics:")
    
    # Column comparison
    pre_cols = set(pre_df.columns)
    post_cols = set(post_df.columns)
    common_cols = pre_cols & post_cols
    print(f"  Common columns: {len(common_cols)}")
    print(f"  Pre-only columns: {len(pre_cols - post_cols)}")
    print(f"  Post-only columns: {len(post_cols - pre_cols)}")
    
    # Value range comparison for numerical columns
    numerical_cols = pre_df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols[:3]:  # First 3 columns
        if col in pre_df.columns and col in post_df.columns:
            pre_range = pre_df[col].max() - pre_df[col].min()
            post_range = post_df[col].max() - post_df[col].min()
            range_diff = abs(pre_range - post_range) / pre_range if pre_range != 0 else 0
            print(f"  {col}: Range difference = {range_diff:.4f}")
    
    return results

def plot_df_comparison(pre_df, post_df, target_column=None, save_path=None):
    """
    Generate comparison plots for DataFrames.
    
    Args:
        pre_df: Pre-processed DataFrame
        post_df: Post-processed DataFrame
        target_column: Target column name
        save_path: Path to save plot
    """
    print("\n📊 Generating DataFrame comparison plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Pre-processing vs Post-processing Comparison', fontsize=14)
    
    # Get numerical columns
    numerical_cols = pre_df.select_dtypes(include=[np.number]).columns
    numerical_cols = [col for col in numerical_cols if col in post_df.columns]
    
    # Plot 1: First numerical column distribution
    if len(numerical_cols) > 0:
        col = numerical_cols[0]
        axes[0, 0].hist(pre_df[col].dropna(), alpha=0.7, label='Pre-processing', bins=20, density=True)
        axes[0, 0].hist(post_df[col].dropna(), alpha=0.7, label='Post-processing', bins=20, density=True)
        axes[0, 0].set_title(f'Distribution: {col}')
        axes[0, 0].legend()
    
    # Plot 2: Second numerical column distribution
    if len(numerical_cols) > 1:
        col = numerical_cols[1]
        axes[0, 1].hist(pre_df[col].dropna(), alpha=0.7, label='Pre-processing', bins=20, density=True)
        axes[0, 1].hist(post_df[col].dropna(), alpha=0.7, label='Post-processing', bins=20, density=True)
        axes[0, 1].set_title(f'Distribution: {col}')
        axes[0, 1].legend()
    
    # Plot 3: Target variable comparison
    if target_column in numerical_cols:
        axes[1, 0].boxplot([pre_df[target_column].dropna(), 
                           post_df[target_column].dropna()],
                          labels=['Pre-processing', 'Post-processing'])
        axes[1, 0].set_title(f'Target: {target_column}')
    
    # Plot 4: Correlation comparison (if multiple numerical columns)
    if len(numerical_cols) > 2:
        pre_corr = pre_df[numerical_cols[:5]].corr()
        post_corr = post_df[numerical_cols[:5]].corr()
        
        im = axes[1, 1].imshow(pre_corr - post_corr, cmap='RdBu', vmin=-1, vmax=1)
        axes[1, 1].set_title('Correlation Difference\n(Pre - Post)')
        plt.colorbar(im, ax=axes[1, 1])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Plot saved to: {save_path}")
    
    plt.show()

def quick_df_evaluation(pre_df, post_df, target_column=None):
    """
    Quick evaluation of DataFrame similarity.
    """
    print("🚀 QUICK DATAFRAME EVALUATION")
    print("="*50)
    
    results = compare_pre_post_processing(pre_df, post_df, target_column)
    plot_df_comparison(pre_df, post_df, target_column, "df_comparison.png")
    
    return results

# Main function for your notebook
def evaluate_pre_post_processing(pre_processed_df, post_processed_df, target_column=None):
    """
    Main function to evaluate pre-processing vs post-processing DataFrames.
    
    Args:
        pre_processed_df: Your pre-processed DataFrame
        post_processed_df: Your post-processed DataFrame
        target_column: Target column name (auto-detected if None)
    
    Returns:
        dict: Evaluation results
    """
    print("🔍 EVALUATING PRE-PROCESSING VS POST-PROCESSING")
    print("="*60)
    
    # Run comparison
    results = quick_evaluation(pre_processed_df, post_processed_df, target_column)
    
    # Print summary
    print("\n📋 SUMMARY:")
    print(f"  Overall Quality Score: {results.get('overall_score', 0):.4f}")
    print(f"  Average KS Statistic: {results.get('avg_ks', 0):.4f}")
    
    if 'tstr_r2' in results:
        print(f"  TSTR R² Score: {results['tstr_r2']:.4f}")
    elif 'tstr_accuracy' in results:
        print(f"  TSTR Accuracy: {results['tstr_accuracy']:.4f}")
    
    return results

if __name__ == "__main__":
    print("🤖 DataFrame Comparison Tool")
    print("Use evaluate_pre_post_processing(pre_df, post_df, target_column) function") 