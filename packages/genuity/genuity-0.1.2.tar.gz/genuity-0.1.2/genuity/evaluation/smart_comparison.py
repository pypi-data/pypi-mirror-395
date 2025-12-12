#!/usr/bin/env python3
"""
Smart DataFrame Comparison Framework
Automatically handles pre-post vs post-pre comparisons based on data compatibility
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from scipy.stats import ks_2samp
import warnings
warnings.filterwarnings('ignore')

def smart_dataframe_comparison(pre_processed_df, post_processed_df, target_column=None):
    """
    Smart comparison that automatically chooses the best comparison method.
    
    Args:
        pre_processed_df: Your pre-processed DataFrame (input to model)
        post_processed_df: Your post-processed DataFrame (output from model)
        target_column: Target column name
    
    Returns:
        dict: Evaluation results
    """
    print("🧠 SMART DATAFRAME COMPARISON")
    print("="*60)
    
    # Step 1: Analyze data compatibility
    print("🔍 Analyzing data compatibility...")
    
    compatibility = analyze_compatibility(pre_processed_df, post_processed_df, target_column)
    
    print(f"📊 Compatibility Score: {compatibility['score']:.4f}")
    print(f"🎯 Recommended Method: {compatibility['recommended_method']}")
    
    # Step 2: Choose comparison method
    if compatibility['recommended_method'] == 'pre_post':
        print("\n✅ Using PRE-PROCESSED vs POST-PROCESSED comparison")
        return evaluate_pre_post_processing(pre_processed_df, post_processed_df, target_column)
    
    elif compatibility['recommended_method'] == 'post_pre':
        print("\n🔄 Using POST-PROCESSED vs PRE-PROCESSED comparison")
        return evaluate_post_pre_processing(post_processed_df, pre_processed_df, target_column)
    
    else:
        print("\n⚠️ Using FALLBACK comparison method")
        return evaluate_fallback_comparison(pre_processed_df, post_processed_df, target_column)

def analyze_compatibility(pre_df, post_df, target_column):
    """
    Analyze which comparison method will work best.
    """
    compatibility = {
        'score': 0,
        'recommended_method': 'fallback',
        'issues': []
    }
    
    # Check 1: Column compatibility
    pre_cols = set(pre_df.columns)
    post_cols = set(post_df.columns)
    common_cols = pre_cols & post_cols
    
    if len(common_cols) < 3:
        compatibility['issues'].append("Too few common columns")
        compatibility['score'] -= 0.3
    
    # Check 2: Target column availability
    if target_column not in pre_cols:
        compatibility['issues'].append(f"Target column '{target_column}' missing in pre-processed data")
        compatibility['score'] -= 0.2
    
    if target_column not in post_cols:
        compatibility['issues'].append(f"Target column '{target_column}' missing in post-processed data")
        compatibility['score'] -= 0.2
    
    # Check 3: Data type compatibility
    if target_column in pre_cols and target_column in post_cols:
        pre_dtype = pre_df[target_column].dtype
        post_dtype = post_df[target_column].dtype
        
        if pre_dtype != post_dtype:
            compatibility['issues'].append(f"Target column data type mismatch: {pre_dtype} vs {post_dtype}")
            compatibility['score'] -= 0.1
    
    # Check 4: NaN issues
    if target_column in post_cols:
        nan_count = post_df[target_column].isna().sum()
        total_count = len(post_df)
        nan_ratio = nan_count / total_count
        
        if nan_ratio > 0.5:
            compatibility['issues'].append(f"High NaN ratio in target column: {nan_ratio:.2%}")
            compatibility['score'] -= 0.4
        elif nan_ratio > 0.1:
            compatibility['issues'].append(f"Moderate NaN ratio in target column: {nan_ratio:.2%}")
            compatibility['score'] -= 0.2
    
    # Check 5: Value range compatibility
    if target_column in pre_cols and target_column in post_cols:
        pre_range = pre_df[target_column].max() - pre_df[target_column].min()
        post_range = post_df[target_column].max() - post_df[target_column].min()
        
        if pre_range > 0 and post_range > 0:
            range_ratio = min(pre_range, post_range) / max(pre_range, post_range)
            if range_ratio < 0.1:
                compatibility['issues'].append("Very different value ranges")
                compatibility['score'] -= 0.3
    
    # Determine recommended method
    if compatibility['score'] >= 0.5:
        compatibility['recommended_method'] = 'pre_post'
    elif compatibility['score'] >= 0.0:
        compatibility['recommended_method'] = 'post_pre'
    else:
        compatibility['recommended_method'] = 'fallback'
    
    return compatibility

def evaluate_pre_post_processing(pre_df, post_df, target_column=None):
    """
    Standard pre-processed vs post-processed comparison.
    """
    print("🔍 EVALUATING PRE-PROCESSED VS POST-PROCESSED")
    print("="*60)
    
    results = {}
    
    # Basic info
    print(f"📊 Pre-processed shape: {pre_df.shape}")
    print(f"📊 Post-processed shape: {post_df.shape}")
    
    # Handle NaN values in target
    if target_column in post_df.columns:
        nan_count = post_df[target_column].isna().sum()
        if nan_count > 0:
            print(f"⚠️ Found {nan_count} NaN values in target column. Filling with mean...")
            post_df[target_column] = post_df[target_column].fillna(post_df[target_column].mean())
    
    # Run standard evaluation
    results = run_standard_evaluation(pre_df, post_df, target_column, "Pre-processed", "Post-processed")
    
    return results

def evaluate_post_pre_processing(post_df, pre_df, target_column=None):
    """
    Post-processed vs pre-processed comparison (reversed).
    """
    print("🔄 EVALUATING POST-PROCESSED VS PRE-PROCESSED")
    print("="*60)
    
    results = {}
    
    # Basic info
    print(f"📊 Post-processed shape: {post_df.shape}")
    print(f"📊 Pre-processed shape: {pre_df.shape}")
    
    # Handle NaN values in target
    if target_column in post_df.columns:
        nan_count = post_df[target_column].isna().sum()
        if nan_count > 0:
            print(f"⚠️ Found {nan_count} NaN values in target column. Filling with mean...")
            post_df[target_column] = post_df[target_column].fillna(post_df[target_column].mean())
    
    # Run standard evaluation (reversed)
    results = run_standard_evaluation(post_df, pre_df, target_column, "Post-processed", "Pre-processed")
    
    return results

def evaluate_fallback_comparison(pre_df, post_df, target_column=None):
    """
    Fallback comparison when standard methods fail.
    """
    print("⚠️ FALLBACK COMPARISON METHOD")
    print("="*60)
    
    results = {}
    
    # Basic info
    print(f"📊 Pre-processed shape: {pre_df.shape}")
    print(f"📊 Post-processed shape: {post_df.shape}")
    
    # Find common numerical columns
    pre_numerical = pre_df.select_dtypes(include=[np.number]).columns
    post_numerical = post_df.select_dtypes(include=[np.number]).columns
    common_numerical = list(set(pre_numerical) & set(post_numerical))
    
    print(f"📊 Common numerical columns: {len(common_numerical)}")
    
    if len(common_numerical) == 0:
        print("❌ No common numerical columns found!")
        return {'error': 'No common numerical columns'}
    
    # Basic statistics comparison
    print("\n📊 Basic Statistics Comparison (Common columns):")
    for col in common_numerical[:5]:
        pre_mean = pre_df[col].mean()
        post_mean = post_df[col].mean()
        pre_std = pre_df[col].std()
        post_std = post_df[col].std()
        
        mean_diff = abs(pre_mean - post_mean) / pre_mean if pre_mean != 0 else 0
        std_diff = abs(pre_std - post_std) / pre_std if pre_std != 0 else 0
        
        print(f"  {col}: Mean diff={mean_diff:.4f}, Std diff={std_diff:.4f}")
    
    # Simple correlation comparison
    if len(common_numerical) > 2:
        pre_corr = pre_df[common_numerical[:5]].corr()
        post_corr = post_df[common_numerical[:5]].corr()
        
        corr_diff = np.mean(np.abs(pre_corr - post_corr))
        results['correlation_diff'] = corr_diff
        print(f"\n📊 Average correlation difference: {corr_diff:.4f}")
    
    # Generate basic plots
    print("\n📊 Generating basic comparison plots...")
    plot_basic_comparison(pre_df, post_df, common_numerical)
    
    return results

def run_standard_evaluation(df1, df2, target_column, label1, label2):
    """
    Run standard evaluation metrics.
    """
    results = {}
    
    # 1. Basic Statistics Comparison
    print(f"\n📊 Basic Statistics Comparison:")
    numerical_cols = df1.select_dtypes(include=[np.number]).columns
    numerical_cols = [col for col in numerical_cols if col != target_column]
    
    for col in numerical_cols[:5]:  # First 5 columns
        if col in df1.columns and col in df2.columns:
            mean1 = df1[col].mean()
            mean2 = df2[col].mean()
            std1 = df1[col].std()
            std2 = df2[col].std()
            
            mean_diff = abs(mean1 - mean2) / mean1 if mean1 != 0 else 0
            std_diff = abs(std1 - std2) / std1 if std1 != 0 else 0
            
            print(f"  {col}: Mean diff={mean_diff:.4f}, Std diff={std_diff:.4f}")
    
    # 2. Kolmogorov-Smirnov Test
    print(f"\n🔍 Kolmogorov-Smirnov Test (First 3 numerical columns):")
    ks_scores = []
    for col in numerical_cols[:3]:
        if col in df1.columns and col in df2.columns:
            ks_stat, p_value = ks_2samp(
                df1[col].dropna(), 
                df2[col].dropna()
            )
            ks_scores.append(ks_stat)
            print(f"  {col}: KS={ks_stat:.4f}, p={p_value:.4f}")
    
    results['avg_ks'] = np.mean(ks_scores) if ks_scores else 0
    
    # 3. TSTR Evaluation
    print(f"\n🎯 TSTR ({label1} vs {label2}):")
    if target_column in df1.columns and target_column in df2.columns:
        X1 = df1.drop(columns=[target_column])
        y1 = df1[target_column]
        X2 = df2.drop(columns=[target_column])
        y2 = df2[target_column]
        
        # Remove non-numeric columns for simplicity
        X1 = X1.select_dtypes(include=[np.number])
        X2 = X2.select_dtypes(include=[np.number])
        
        if len(X1.columns) > 0 and len(X2.columns) > 0:
            # Align columns
            common_cols = set(X1.columns) & set(X2.columns)
            X1 = X1[list(common_cols)]
            X2 = X2[list(common_cols)]
            
            # Determine if classification or regression
            is_classification = y1.dtype == 'object' or len(y1.unique()) < 10
            
            if is_classification:
                model = RandomForestClassifier(n_estimators=50, random_state=42)
                model.fit(X1, y1)
                y_pred = model.predict(X2)
                accuracy = accuracy_score(y2, y_pred)
                results['tstr_accuracy'] = accuracy
                print(f"  Classification Accuracy: {accuracy:.4f}")
            else:
                model = RandomForestRegressor(n_estimators=50, random_state=42)
                model.fit(X1, y1)
                y_pred = model.predict(X2)
                r2 = r2_score(y2, y_pred)
                mse = mean_squared_error(y2, y_pred)
                results['tstr_r2'] = r2
                results['tstr_mse'] = mse
                print(f"  Regression R²: {r2:.4f}, MSE: {mse:.4f}")
    
    # 4. Overall Quality Score
    print(f"\n🏆 Overall Quality Assessment:")
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
    print(f"\n📊 Generating comparison plots...")
    plot_comparison(df1, df2, target_column, label1, label2)
    
    return results

def plot_comparison(df1, df2, target_column, label1, label2):
    """Generate comparison plots."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'{label1} vs {label2} Comparison', fontsize=14)
    
    # Get numerical columns
    numerical_cols = df1.select_dtypes(include=[np.number]).columns
    numerical_cols = [col for col in numerical_cols if col in df2.columns]
    
    # Plot 1: First numerical column distribution
    if len(numerical_cols) > 0:
        col = numerical_cols[0]
        axes[0, 0].hist(df1[col].dropna(), alpha=0.7, label=label1, bins=20, density=True)
        axes[0, 0].hist(df2[col].dropna(), alpha=0.7, label=label2, bins=20, density=True)
        axes[0, 0].set_title(f'Distribution: {col}')
        axes[0, 0].legend()
    
    # Plot 2: Second numerical column distribution
    if len(numerical_cols) > 1:
        col = numerical_cols[1]
        axes[0, 1].hist(df1[col].dropna(), alpha=0.7, label=label1, bins=20, density=True)
        axes[0, 1].hist(df2[col].dropna(), alpha=0.7, label=label2, bins=20, density=True)
        axes[0, 1].set_title(f'Distribution: {col}')
        axes[0, 1].legend()
    
    # Plot 3: Target variable comparison
    if target_column in numerical_cols:
        axes[1, 0].boxplot([df1[target_column].dropna(), 
                           df2[target_column].dropna()],
                          labels=[label1, label2])
        axes[1, 0].set_title(f'Target: {target_column}')
    
    # Plot 4: Correlation comparison (if multiple numerical columns)
    if len(numerical_cols) > 2:
        corr1 = df1[numerical_cols[:5]].corr()
        corr2 = df2[numerical_cols[:5]].corr()
        
        im = axes[1, 1].imshow(corr1 - corr2, cmap='RdBu', vmin=-1, vmax=1)
        axes[1, 1].set_title(f'Correlation Difference\n({label1} - {label2})')
        plt.colorbar(im, ax=axes[1, 1])
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Plots generated successfully!")

def plot_basic_comparison(df1, df2, common_cols):
    """Generate basic comparison plots for fallback method."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Basic DataFrame Comparison', fontsize=14)
    
    # Plot 1: First common column distribution
    if len(common_cols) > 0:
        col = common_cols[0]
        axes[0, 0].hist(df1[col].dropna(), alpha=0.7, label='DataFrame 1', bins=20, density=True)
        axes[0, 0].hist(df2[col].dropna(), alpha=0.7, label='DataFrame 2', bins=20, density=True)
        axes[0, 0].set_title(f'Distribution: {col}')
        axes[0, 0].legend()
    
    # Plot 2: Second common column distribution
    if len(common_cols) > 1:
        col = common_cols[1]
        axes[0, 1].hist(df1[col].dropna(), alpha=0.7, label='DataFrame 1', bins=20, density=True)
        axes[0, 1].hist(df2[col].dropna(), alpha=0.7, label='DataFrame 2', bins=20, density=True)
        axes[0, 1].set_title(f'Distribution: {col}')
        axes[0, 1].legend()
    
    # Plot 3: Third common column distribution
    if len(common_cols) > 2:
        col = common_cols[2]
        axes[1, 0].hist(df1[col].dropna(), alpha=0.7, label='DataFrame 1', bins=20, density=True)
        axes[1, 0].hist(df2[col].dropna(), alpha=0.7, label='DataFrame 2', bins=20, density=True)
        axes[1, 0].set_title(f'Distribution: {col}')
        axes[1, 0].legend()
    
    # Plot 4: Correlation comparison
    if len(common_cols) > 2:
        corr1 = df1[common_cols[:5]].corr()
        corr2 = df2[common_cols[:5]].corr()
        
        im = axes[1, 1].imshow(corr1 - corr2, cmap='RdBu', vmin=-1, vmax=1)
        axes[1, 1].set_title('Correlation Difference')
        plt.colorbar(im, ax=axes[1, 1])
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Basic plots generated successfully!")

if __name__ == "__main__":
    print("🧠 Smart DataFrame Comparison Tool")
    print("Use: from smart_comparison import smart_dataframe_comparison") 