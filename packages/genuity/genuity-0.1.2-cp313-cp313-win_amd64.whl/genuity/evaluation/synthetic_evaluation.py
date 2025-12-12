import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, roc_auc_score
from scipy import stats
from scipy.spatial.distance import jensenshannon
from scipy.stats import ks_2samp, wasserstein_distance, chi2_contingency
import warnings
warnings.filterwarnings('ignore')

class SyntheticDataEvaluator:
    """Comprehensive evaluation framework for pre-processing vs post-processing DataFrame comparison."""
    
    def __init__(self, pre_df, post_df, target_column=None, categorical_columns=None):
        self.pre_df = pre_df.copy()
        self.post_df = post_df.copy()
        self.target_column = target_column
        self.categorical_columns = categorical_columns or []
        self.numerical_columns = [col for col in pre_df.columns 
                                if col not in categorical_columns + [target_column]]
        
        # Ensure same columns
        common_cols = set(pre_df.columns) & set(post_df.columns)
        self.pre_df = self.pre_df[list(common_cols)]
        self.post_df = self.post_df[list(common_cols)]
        
        print(f"Evaluation: {len(common_cols)} columns, Pre: {self.pre_df.shape}, Post: {self.post_df.shape}")
    
    def statistical_distance_measures(self):
        """Calculate SDM (Statistical Distance Measures)."""
        print("\nSTATISTICAL DISTANCE MEASURES (SDM)")
        print("="*50)
        
        sdm_results = {}
        
        # Kolmogorov-Smirnov Test for numerical columns
        print("\nKolmogorov-Smirnov Test:")
        for col in self.numerical_columns:
            if col in self.pre_df.columns and col in self.post_df.columns:
                ks_stat, p_value = ks_2samp(
                    self.pre_df[col].dropna(), 
                    self.post_df[col].dropna()
                )
                sdm_results[f'ks_{col}'] = {'statistic': ks_stat, 'p_value': p_value}
                print(f"  {col}: KS={ks_stat:.4f}, p={p_value:.4f}")
        
        # Wasserstein Distance
        print("\nWasserstein Distance:")
        for col in self.numerical_columns:
            if col in self.pre_df.columns and col in self.post_df.columns:
                wd = wasserstein_distance(
                    self.pre_df[col].dropna(), 
                    self.post_df[col].dropna()
                )
                sdm_results[f'wasserstein_{col}'] = wd
                print(f"  {col}: {wd:.4f}")
        
        # Jensen-Shannon Divergence for categorical
        print("\nJensen-Shannon Divergence (Categorical):")
        for col in self.categorical_columns:
            if col in self.pre_df.columns and col in self.post_df.columns:
                pre_counts = self.pre_df[col].value_counts(normalize=True)
                post_counts = self.post_df[col].value_counts(normalize=True)
                
                all_values = set(pre_counts.index) | set(post_counts.index)
                pre_aligned = pre_counts.reindex(all_values, fill_value=0)
                post_aligned = post_counts.reindex(all_values, fill_value=0)
                
                js_div = jensenshannon(pre_aligned.values, post_aligned.values)
                sdm_results[f'js_{col}'] = js_div
                print(f"  {col}: {js_div:.4f}")
        
        return sdm_results
    
    def train_on_pre_test_on_post(self):
        """TSTR (Train on Pre, Test on Post) evaluation."""
        print("\nTRAIN ON PRE, TEST ON POST (TSTR)")
        print("="*50)
        
        if not self.target_column:
            print("No target column specified. Skipping TSTR.")
            return {}
        
        tstr_results = {}
        
        X_pre = self.pre_df.drop(columns=[self.target_column])
        y_pre = self.pre_df[self.target_column]
        X_post = self.post_df.drop(columns=[self.target_column])
        y_post = self.post_df[self.target_column]
        
        # Determine if classification or regression
        is_classification = y_pre.dtype == 'object' or len(y_pre.unique()) < 10
        
        if is_classification:
            print("Classification Task:")
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_pre, y_pre)
            y_pred = model.predict(X_post)
            y_pred_proba = model.predict_proba(X_post)[:, 1] if len(y_post.unique()) == 2 else None
            
            accuracy = accuracy_score(y_post, y_pred)
            tstr_results['accuracy'] = accuracy
            
            if y_pred_proba is not None:
                auc = roc_auc_score(y_post, y_pred_proba)
                tstr_results['auc'] = auc
                print(f"  Accuracy: {accuracy:.4f}, AUC: {auc:.4f}")
            else:
                print(f"  Accuracy: {accuracy:.4f}")
            
        else:
            print("Regression Task:")
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_pre, y_pre)
            y_pred = model.predict(X_post)
            
            mse = mean_squared_error(y_post, y_pred)
            r2 = r2_score(y_post, y_pred)
            mae = np.mean(np.abs(y_post - y_pred))
            
            tstr_results['mse'] = mse
            tstr_results['r2'] = r2
            tstr_results['mae'] = mae
            
            print(f"  MSE: {mse:.4f}, R2: {r2:.4f}, MAE: {mae:.4f}")
        
        return tstr_results
    
    def statistical_similarity_metrics(self):
        """Calculate statistical similarity metrics."""
        print("\nSTATISTICAL SIMILARITY METRICS")
        print("="*50)
        
        similarity_results = {}
        
        # Basic statistics comparison
        print("\nBasic Statistics Comparison:")
        for col in self.numerical_columns:
            if col in self.pre_df.columns and col in self.post_df.columns:
                pre_stats = self.pre_df[col].describe()
                post_stats = self.post_df[col].describe()
                
                mean_diff = abs(pre_stats['mean'] - post_stats['mean']) / pre_stats['mean']
                std_diff = abs(pre_stats['std'] - post_stats['std']) / pre_stats['std']
                
                similarity_results[f'mean_diff_{col}'] = mean_diff
                similarity_results[f'std_diff_{col}'] = std_diff
                
                print(f"  {col}: Mean diff={mean_diff:.4f}, Std diff={std_diff:.4f}")
        
        # Correlation structure preservation
        if len(self.numerical_columns) > 1:
            pre_corr = self.pre_df[self.numerical_columns].corr()
            post_corr = self.post_df[self.numerical_columns].corr()
            
            corr_diff = np.mean(np.abs(pre_corr - post_corr))
            similarity_results['correlation_diff'] = corr_diff
            print(f"  Correlation difference: {corr_diff:.4f}")
        
        return similarity_results
    
    def data_utility_metrics(self):
        """Calculate data utility metrics."""
        print("\nDATA UTILITY METRICS")
        print("="*50)
        
        utility_results = {}
        
        # Feature importance preservation
        if self.target_column:
            print("\nFeature Importance Preservation:")
            X_pre = self.pre_df.drop(columns=[self.target_column])
            y_pre = self.pre_df[self.target_column]
            X_post = self.post_df.drop(columns=[self.target_column])
            y_post = self.post_df[self.target_column]
            
            model_pre = RandomForestRegressor(n_estimators=100, random_state=42)
            model_post = RandomForestRegressor(n_estimators=100, random_state=42)
            
            model_pre.fit(X_pre, y_pre)
            model_post.fit(X_post, y_post)
            
            pre_importance = model_pre.feature_importances_
            post_importance = model_post.feature_importances_
            
            importance_corr = np.corrcoef(pre_importance, post_importance)[0, 1]
            utility_results['feature_importance_correlation'] = importance_corr
            print(f"  Feature importance correlation: {importance_corr:.4f}")
        
        # Value range preservation
        print("\nValue Range Preservation:")
        range_scores = []
        for col in self.numerical_columns[:5]:  # First 5 columns
            if col in self.pre_df.columns and col in self.post_df.columns:
                pre_range = self.pre_df[col].max() - self.pre_df[col].min()
                post_range = self.post_df[col].max() - self.post_df[col].min()
                
                if pre_range != 0:
                    range_preservation = 1 - abs(pre_range - post_range) / pre_range
                    range_scores.append(range_preservation)
        
        if range_scores:
            avg_range_preservation = np.mean(range_scores)
            utility_results['range_preservation'] = avg_range_preservation
            print(f"  Average range preservation: {avg_range_preservation:.4f}")
        
        return utility_results
    
    def comprehensive_evaluation(self):
        """Run all evaluation metrics."""
        print("COMPREHENSIVE PRE-PROCESSING VS POST-PROCESSING EVALUATION")
        print("="*70)
        
        results = {}
        results['sdm'] = self.statistical_distance_measures()
        results['tstr'] = self.train_on_pre_test_on_post()
        results['similarity'] = self.statistical_similarity_metrics()
        results['utility'] = self.data_utility_metrics()
        
        self._generate_summary_report(results)
        return results
    
    def _generate_summary_report(self, results):
        """Generate summary report."""
        print("\nEVALUATION SUMMARY")
        print("="*60)
        
        # SDM Summary
        if results['sdm']:
            ks_stats = [v['statistic'] for k, v in results['sdm'].items() if k.startswith('ks_')]
            if ks_stats:
                print(f"Average KS statistic: {np.mean(ks_stats):.4f}")
        
        # TSTR Summary
        if results['tstr']:
            print("TSTR Performance:")
            for metric, value in results['tstr'].items():
                print(f"  {metric.upper()}: {value:.4f}")
        
        # Similarity Summary
        if results['similarity']:
            mean_diffs = [v for k, v in results['similarity'].items() if k.startswith('mean_diff_')]
            if mean_diffs:
                print(f"Average mean difference: {np.mean(mean_diffs):.4f}")
        
        # Utility Summary
        if results['utility']:
            for metric, value in results['utility'].items():
                print(f"{metric}: {value:.4f}")
        
        # Overall Quality Score
        self._calculate_overall_quality_score(results)
    
    def _calculate_overall_quality_score(self, results):
        """Calculate overall quality score."""
        print("\nOVERALL QUALITY SCORE:")
        
        scores = []
        
        # SDM Score (lower is better)
        if results['sdm']:
            ks_stats = [v['statistic'] for k, v in results['sdm'].items() if k.startswith('ks_')]
            if ks_stats:
                sdm_score = 1 - np.mean(ks_stats)
                scores.append(sdm_score)
                print(f"  SDM Score: {sdm_score:.4f}")
        
        # TSTR Score
        if results['tstr']:
            if 'accuracy' in results['tstr']:
                scores.append(results['tstr']['accuracy'])
                print(f"  TSTR Accuracy: {results['tstr']['accuracy']:.4f}")
            elif 'r2' in results['tstr']:
                scores.append(max(0, results['tstr']['r2']))
                print(f"  TSTR R2: {max(0, results['tstr']['r2']):.4f}")
        
        # Similarity Score
        if results['similarity']:
            mean_diffs = [v for k, v in results['similarity'].items() if k.startswith('mean_diff_')]
            if mean_diffs:
                similarity_score = 1 - np.mean(mean_diffs)
                scores.append(similarity_score)
                print(f"  Similarity Score: {similarity_score:.4f}")
        
        # Utility Score
        if results['utility']:
            if 'feature_importance_correlation' in results['utility']:
                scores.append(results['utility']['feature_importance_correlation'])
                print(f"  Feature Importance: {results['utility']['feature_importance_correlation']:.4f}")
            if 'range_preservation' in results['utility']:
                scores.append(results['utility']['range_preservation'])
                print(f"  Range Preservation: {results['utility']['range_preservation']:.4f}")
        
        if scores:
            overall_score = np.mean(scores)
            print(f"\nOVERALL QUALITY SCORE: {overall_score:.4f}")
            
            if overall_score >= 0.8:
                print("EXCELLENT: Very similar data!")
            elif overall_score >= 0.6:
                print("GOOD: Acceptable similarity.")
            elif overall_score >= 0.4:
                print("FAIR: Some differences detected.")
            else:
                print("POOR: Significant differences.")
    
    def plot_comparisons(self, save_path=None):
        """Generate comparison plots."""
        print("\nGenerating comparison plots...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Pre-processing vs Post-processing Comparison', fontsize=16)
        
        # Distribution comparison
        if self.numerical_columns:
            col = self.numerical_columns[0]
            axes[0, 0].hist(self.pre_df[col].dropna(), alpha=0.7, label='Pre-processing', bins=20, density=True)
            axes[0, 0].hist(self.post_df[col].dropna(), alpha=0.7, label='Post-processing', bins=20, density=True)
            axes[0, 0].set_title(f'Distribution: {col}')
            axes[0, 0].legend()
        
        # Correlation comparison
        if len(self.numerical_columns) > 1:
            pre_corr = self.pre_df[self.numerical_columns].corr()
            post_corr = self.post_df[self.numerical_columns].corr()
            
            im1 = axes[0, 1].imshow(pre_corr, cmap='coolwarm', vmin=-1, vmax=1)
            axes[0, 1].set_title('Pre-processing Correlation')
            plt.colorbar(im1, ax=axes[0, 1])
            
            im2 = axes[1, 0].imshow(post_corr, cmap='coolwarm', vmin=-1, vmax=1)
            axes[1, 0].set_title('Post-processing Correlation')
            plt.colorbar(im2, ax=axes[1, 0])
        
        # Target comparison
        if self.target_column and self.target_column in self.numerical_columns:
            axes[1, 1].boxplot([self.pre_df[self.target_column].dropna(), 
                               self.post_df[self.target_column].dropna()],
                               labels=['Pre-processing', 'Post-processing'])
            axes[1, 1].set_title(f'Target: {self.target_column}')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plots saved to: {save_path}")
        
        plt.show()


def evaluate_pre_post_dataframes(pre_df, post_df, target_column=None, 
                               categorical_columns=None, save_plots=True):
    """Convenience function to evaluate pre-processing vs post-processing DataFrames."""
    evaluator = SyntheticDataEvaluator(
        pre_df=pre_df,
        post_df=post_df,
        target_column=target_column,
        categorical_columns=categorical_columns
    )
    
    results = evaluator.comprehensive_evaluation()
    
    if save_plots:
        evaluator.plot_comparisons("pre_post_comparison.png")
    
    return results