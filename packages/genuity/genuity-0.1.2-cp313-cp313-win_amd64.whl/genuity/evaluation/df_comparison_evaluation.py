#!/usr/bin/env python3
"""
Simple DataFrame Comparison for Pre-processing vs Post-processing Evaluation
Compares pre-processing vs post-processing DataFrames directly
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from scipy.stats import ks_2samp, wasserstein_distance
import warnings
warnings.filterwarnings('ignore')

def compare_dataframes(pre_df, post_df, target_column='expenses'):
    """
    Compare pre-processing vs post-processing DataFrames
    
    Args:
        pre_df: Pre-processed DataFrame
        post_df: Post-processed DataFrame  
        target_column: Target column name
    
    Returns:
        dict: Comparison results
    """
    print("🔄 PRE-PROCESSING VS POST-PROCESSING COMPARISON")
    print("="*60)
    
    results = {}
    
    # Basic info
    print(f"📊 Pre-processing shape: {pre_df.shape}")
    print(f"📊 Post-processing shape: {post_df.shape}")
    
    # Column comparison
    pre_cols = set(pre_df.columns)
    post_cols = set(post_df.columns)
    common_cols = pre_cols & post_cols
    print(f"📋 Common columns: {len(common_cols)}")
    print(f"📋 Pre-only columns: {len(pre_cols - post_cols)}")
    print(f"📋 Post-only columns: {len(post_cols - pre_cols)}")
    
    # 1. Basic Statistics Comparison
    print("\n📈 Basic Statistics Comparison:")
    numerical_cols = pre_df.select_dtypes(include=[np.number]).columns
    numerical_cols = [col for col in numerical_cols if col in common_cols]
    
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
    
    # 4. Value Range Comparison
    print("\n📊 Value Range Comparison:")
    for col in numerical_cols[:3]:
        if col in pre_df.columns and col in post_df.columns:
            pre_range = pre_df[col].max() - pre_df[col].min()
            post_range = post_df[col].max() - post_df[col].min()
            range_diff = abs(pre_range - post_range) / pre_range if pre_range != 0 else 0
            print(f"  {col}: Range difference = {range_diff:.4f}")
    
    # 5. Overall Quality Score
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
    
    return results

def plot_df_comparison(pre_df, post_df, target_column='expenses', save_path=None):
    """
    Generate comparison plots for DataFrames
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

def quick_df_evaluation(pre_df, post_df, target_column='expenses'):
    """
    Quick evaluation of DataFrame similarity.
    """
    print("🚀 QUICK DATAFRAME EVALUATION")
    print("="*50)
    
    results = compare_dataframes(pre_df, post_df, target_column)
    plot_df_comparison(pre_df, post_df, target_column, "df_comparison.png")
    
    return results

# Main function for your notebook
def evaluate_pre_post_processing(pre_processed_df, post_processed_df, target_column='expenses'):
    """
    Main function to evaluate pre-processing vs post-processing DataFrames.
    
    Args:
        pre_processed_df: Your pre-processed DataFrame
        post_processed_df: Your post-processed DataFrame
        target_column: Target column name
    
    Returns:
        dict: Evaluation results
    """
    print("🔍 EVALUATING PRE-PROCESSING VS POST-PROCESSING")
    print("="*60)
    
    # Run comparison
    results = quick_df_evaluation(pre_processed_df, post_processed_df, target_column)
    
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