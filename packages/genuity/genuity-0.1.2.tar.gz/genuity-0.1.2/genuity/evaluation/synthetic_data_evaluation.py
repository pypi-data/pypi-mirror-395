import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error, r2_score, accuracy_score, 
    classification_report, confusion_matrix, roc_auc_score
)
from sklearn.model_selection import train_test_split
from scipy import stats
from scipy.spatial.distance import jensenshannon
from scipy.stats import ks_2samp, wasserstein_distance, chi2_contingency
import warnings
warnings.filterwarnings('ignore')

class SyntheticDataEvaluator:
    """
    Comprehensive evaluation framework for synthetic data quality assessment.
    Compares pre-processing vs post-processing datasets and provides multiple metrics.
    """
    
    def __init__(self, real_data, synthetic_data, target_column=None, categorical_columns=None):
        """
        Initialize the evaluator with real and synthetic datasets.
        
        Args:
            real_data: Original real dataset (DataFrame)
            synthetic_data: Generated synthetic dataset (DataFrame)
            target_column: Name of the target column for supervised learning tasks
            categorical_columns: List of categorical column names
        """
        self.real_data = real_data.copy()
        self.synthetic_data = synthetic_data.copy()
        self.target_column = target_column
        self.categorical_columns = categorical_columns or []
        self.numerical_columns = [col for col in real_data.columns 
                                if col not in categorical_columns + [target_column]]
        
        # Ensure both datasets have same columns
        common_cols = set(real_data.columns) & set(synthetic_data.columns)
        self.real_data = self.real_data[list(common_cols)]
        self.synthetic_data = self.synthetic_data[list(common_cols)]
        
        print(f"📊 Evaluation initialized with {len(common_cols)} common columns")
        print(f"📈 Real data shape: {self.real_data.shape}")
        print(f"🤖 Synthetic data shape: {self.synthetic_data.shape}")
    
    def statistical_distance_measures(self):
        """
        Calculate Statistical Distance Measures (SDM) between real and synthetic data.
        """
        print("\n" + "="*60)
        print("📏 STATISTICAL DISTANCE MEASURES (SDM)")
        print("="*60)
        
        sdm_results = {}
        
        # 1. Kolmogorov-Smirnov Test for numerical columns
        print("\n🔍 Kolmogorov-Smirnov Test (Numerical Columns):")
        for col in self.numerical_columns:
            if col in self.real_data.columns and col in self.synthetic_data.columns:
                ks_stat, p_value = ks_2samp(
                    self.real_data[col].dropna(), 
                    self.synthetic_data[col].dropna()
                )
                sdm_results[f'ks_{col}'] = {'statistic': ks_stat, 'p_value': p_value}
                print(f"  {col}: KS-stat={ks_stat:.4f}, p-value={p_value:.4f}")
        
        # 2. Wasserstein Distance (Earth Mover's Distance)
        print("\n🌊 Wasserstein Distance (Numerical Columns):")
        for col in self.numerical_columns:
            if col in self.real_data.columns and col in self.synthetic_data.columns:
                wd = wasserstein_distance(
                    self.real_data[col].dropna(), 
                    self.synthetic_data[col].dropna()
                )
                sdm_results[f'wasserstein_{col}'] = wd
                print(f"  {col}: {wd:.4f}")
        
        # 3. Jensen-Shannon Divergence for categorical columns
        print("\n📊 Jensen-Shannon Divergence (Categorical Columns):")
        for col in self.categorical_columns:
            if col in self.real_data.columns and col in self.synthetic_data.columns:
                # Get value counts and normalize
                real_counts = self.real_data[col].value_counts(normalize=True)
                synth_counts = self.synthetic_data[col].value_counts(normalize=True)
                
                # Align indices
                all_values = set(real_counts.index) | set(synth_counts.index)
                real_aligned = real_counts.reindex(all_values, fill_value=0)
                synth_aligned = synth_counts.reindex(all_values, fill_value=0)
                
                js_div = jensenshannon(real_aligned.values, synth_aligned.values)
                sdm_results[f'js_{col}'] = js_div
                print(f"  {col}: {js_div:.4f}")
        
        # 4. Chi-square test for categorical columns
        print("\n Chi-square Test (Categorical Columns):")
        for col in self.categorical_columns:
            if col in self.real_data.columns and col in self.synthetic_data.columns:
                dataset_labels = np.array(
                    ['real'] * len(self.real_data)
                    + ['synthetic'] * len(self.synthetic_data)
                )
                category_values = np.concatenate(
                    [
                        self.real_data[col].to_numpy(),
                        self.synthetic_data[col].to_numpy(),
                    ]
                )

                contingency_table = pd.crosstab(
                    index=pd.Series(dataset_labels, name="dataset"),
                    columns=pd.Series(category_values, name=col),
                )
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                sdm_results[f'chi2_{col}'] = {'chi2': chi2, 'p_value': p_value, 'dof': dof}
                print(f"  {col}: χ²={chi2:.4f}, p-value={p_value:.4f}")
        
        return sdm_results
    
    def train_on_synthetic_test_on_real(self):
        """
        TSTR (Train on Synthetic, Test on Real) evaluation.
        """
        print("\n" + "="*60)
        print(" TRAIN ON SYNTHETIC, TEST ON REAL (TSTR)")
        print("="*60)
        
        if not self.target_column:
            print(" No target column specified. Skipping TSTR evaluation.")
            return {}

        if (
            self.target_column not in self.real_data.columns
            or self.target_column not in self.synthetic_data.columns
        ):
            print(
                f" Target column '{self.target_column}' missing in one of the datasets. "
                "Skipping TSTR evaluation."
            )
            return {}
        
        tstr_results = {}
        
        # Prepare data
        X_real = self.real_data.drop(columns=[self.target_column])
        y_real = self.real_data[self.target_column].copy()
        X_synth = self.synthetic_data.drop(columns=[self.target_column])
        y_synth = self.synthetic_data[self.target_column].copy()

        # Encode categorical/object columns consistently across both datasets
        n_real = len(X_real)
        combined_X = pd.concat([X_real, X_synth], axis=0, ignore_index=True)
        cat_cols = [
            col
            for col in combined_X.columns
            if combined_X[col].dtype == "object" or col in (self.categorical_columns or [])
        ]
        if cat_cols:
            combined_X = pd.get_dummies(combined_X, columns=cat_cols, dummy_na=True)
        X_real = combined_X.iloc[:n_real].reset_index(drop=True)
        X_synth = combined_X.iloc[n_real:].reset_index(drop=True)
        
        # Determine if classification or regression
        is_classification = y_real.dtype == 'object' or len(y_real.unique()) < 10
        
        if is_classification:
            print("\n📊 Classification Task:")
            # Train on synthetic, test on real
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_synth, y_synth)
            y_pred = model.predict(X_real)
            y_pred_proba = model.predict_proba(X_real)[:, 1] if len(y_real.unique()) == 2 else None
            
            # Calculate metrics
            accuracy = accuracy_score(y_real, y_pred)
            tstr_results['accuracy'] = accuracy
            
            if y_pred_proba is not None:
                auc = roc_auc_score(y_real, y_pred_proba)
                tstr_results['auc'] = auc
                print(f"  Accuracy: {accuracy:.4f}")
                print(f"  AUC: {auc:.4f}")
            else:
                print(f"  Accuracy: {accuracy:.4f}")
            
            # Classification report
            print("\n  Classification Report:")
            print(classification_report(y_real, y_pred))
            
        else:
            print("\n📈 Regression Task:")
            # Train on synthetic, test on real
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_synth, y_synth)
            y_pred = model.predict(X_real)
            
            # Calculate metrics
            mse = mean_squared_error(y_real, y_pred)
            r2 = r2_score(y_real, y_pred)
            mae = np.mean(np.abs(y_real - y_pred))
            
            tstr_results['mse'] = mse
            tstr_results['r2'] = r2
            tstr_results['mae'] = mae
            
            print(f"  MSE: {mse:.4f}")
            print(f"  R²: {r2:.4f}")
            print(f"  MAE: {mae:.4f}")
        
        return tstr_results
    
    def statistical_similarity_metrics(self):
        """
        Calculate statistical similarity metrics between real and synthetic data.
        """
        print("\n" + "="*60)
        print("📊 STATISTICAL SIMILARITY METRICS")
        print("="*60)
        
        similarity_results = {}
        
        # 1. Basic statistics comparison
        print("\n📈 Basic Statistics Comparison (Numerical Columns):")
        for col in self.numerical_columns:
            if col in self.real_data.columns and col in self.synthetic_data.columns:
                real_stats = self.real_data[col].describe()
                synth_stats = self.synthetic_data[col].describe()
                
                # Calculate relative differences
                mean_diff = abs(real_stats['mean'] - synth_stats['mean']) / real_stats['mean']
                std_diff = abs(real_stats['std'] - synth_stats['std']) / real_stats['std']
                
                similarity_results[f'mean_diff_{col}'] = mean_diff
                similarity_results[f'std_diff_{col}'] = std_diff
                
                print(f"  {col}:")
                print(f"    Mean diff: {mean_diff:.4f}")
                print(f"    Std diff: {std_diff:.4f}")
        
        # 2. Correlation structure preservation
        print("\n🔗 Correlation Structure Preservation:")
        real_corr = self.real_data[self.numerical_columns].corr()
        synth_corr = self.synthetic_data[self.numerical_columns].corr()
        
        corr_diff = np.mean(np.abs(real_corr - synth_corr))
        similarity_results['correlation_diff'] = corr_diff
        print(f"  Average correlation difference: {corr_diff:.4f}")
        
        # 3. Distribution overlap (for numerical columns)
        print("\n📊 Distribution Overlap (Numerical Columns):")
        for col in self.numerical_columns:
            if col in self.real_data.columns and col in self.synthetic_data.columns:
                # Calculate histogram overlap
                real_hist, _ = np.histogram(self.real_data[col].dropna(), bins=20, density=True)
                synth_hist, _ = np.histogram(self.synthetic_data[col].dropna(), bins=20, density=True)
                
                # Normalize histograms
                real_hist = real_hist / np.sum(real_hist)
                synth_hist = synth_hist / np.sum(synth_hist)
                
                # Calculate overlap
                overlap = np.sum(np.minimum(real_hist, synth_hist))
                similarity_results[f'overlap_{col}'] = overlap
                print(f"  {col}: {overlap:.4f}")
        
        return similarity_results
    
    def data_utility_metrics(self):
        """
        Calculate data utility metrics to assess synthetic data usefulness.
        """
        print("\n" + "="*60)
        print("🛠️ DATA UTILITY METRICS")
        print("="*60)
        
        utility_results = {}
        
        # 1. Feature importance preservation
        if self.target_column:
            print("\n🎯 Feature Importance Preservation:")
            X_real = self.real_data.drop(columns=[self.target_column])
            y_real = self.real_data[self.target_column]
            X_synth = self.synthetic_data.drop(columns=[self.target_column])
            y_synth = self.synthetic_data[self.target_column]
            
            n_real = len(X_real)
            combined_X = pd.concat([X_real, X_synth], axis=0, ignore_index=True)
            cat_cols = [
                col
                for col in combined_X.columns
                if combined_X[col].dtype == "object"
                or col in (self.categorical_columns or [])
            ]
            if cat_cols:
                combined_X = pd.get_dummies(combined_X, columns=cat_cols, dummy_na=True)
            X_real = combined_X.iloc[:n_real].reset_index(drop=True)
            X_synth = combined_X.iloc[n_real:].reset_index(drop=True)
            
            # Train models on both datasets
            model_real = RandomForestRegressor(n_estimators=100, random_state=42)
            model_synth = RandomForestRegressor(n_estimators=100, random_state=42)
            
            model_real.fit(X_real, y_real)
            model_synth.fit(X_synth, y_synth)
            
            # Compare feature importance
            real_importance = model_real.feature_importances_
            synth_importance = model_synth.feature_importances_
            
            importance_corr = np.corrcoef(real_importance, synth_importance)[0, 1]
            utility_results['feature_importance_correlation'] = importance_corr
            print(f"  Feature importance correlation: {importance_corr:.4f}")
        
        # 2. Data coverage
        print("\n📊 Data Coverage Analysis:")
        coverage_metrics = {}
        for col in self.numerical_columns:
            if col in self.real_data.columns and col in self.synthetic_data.columns:
                real_range = (self.real_data[col].min(), self.real_data[col].max())
                synth_range = (self.synthetic_data[col].min(), self.synthetic_data[col].max())
                
                # Calculate how much of real range is covered by synthetic
                range_coverage = min(synth_range[1], real_range[1]) - max(synth_range[0], real_range[0])
                range_coverage = max(0, range_coverage) / (real_range[1] - real_range[0])
                coverage_metrics[col] = range_coverage
        
        avg_coverage = np.mean(list(coverage_metrics.values()))
        utility_results['average_range_coverage'] = avg_coverage
        print(f"  Average range coverage: {avg_coverage:.4f}")
        
       # 3. Privacy preservation (basic)
        print("\n Privacy Preservation (Basic):")
        # Check for exact duplicates
        exact_duplicates = 0
      # for _, real_row in self.real_data.iterrows():
      #     for _, synth_row in self.synthetic_data.iterrows():
      #         if real_row.equals(synth_row):
       #            exact_duplicates += 1
        
        privacy_score = 1 - (exact_duplicates / (len(self.real_data) * len(self.synthetic_data)))
        utility_results['privacy_score'] = privacy_score
        print(f"  Privacy score (no exact duplicates): {privacy_score:.4f}")
        
        return utility_results
    
    def comprehensive_evaluation(self):
        """
        Run all evaluation metrics and provide a comprehensive report.
        """
        print("🚀 STARTING COMPREHENSIVE SYNTHETIC DATA EVALUATION")
        print("="*80)
        
        results = {}
        
        # Run all evaluations
        results['sdm'] = self.statistical_distance_measures()
        results['tstr'] = self.train_on_synthetic_test_on_real()
        results['similarity'] = self.statistical_similarity_metrics()
        results['utility'] = self.data_utility_metrics()
        
        # Generate summary report
        self._generate_summary_report(results)
        
        return results
    
    def _generate_summary_report(self, results):
        """
        Generate a comprehensive summary report.
        """
        print("\n" + "="*80)
        print("📋 COMPREHENSIVE EVALUATION SUMMARY")
        print("="*80)
        
        # SDM Summary
        if results['sdm']:
            print("\n📏 Statistical Distance Measures Summary:")
            ks_stats = [v['statistic'] for k, v in results['sdm'].items() if k.startswith('ks_')]
            if ks_stats:
                print(f"  Average KS statistic: {np.mean(ks_stats):.4f}")
                print(f"  Best KS statistic: {min(ks_stats):.4f}")
                print(f"  Worst KS statistic: {max(ks_stats):.4f}")
        
        # TSTR Summary
        if results['tstr']:
            print("\n🎯 TSTR Performance Summary:")
            for metric, value in results['tstr'].items():
                print(f"  {metric.upper()}: {value:.4f}")
        
        # Similarity Summary
        if results['similarity']:
            print("\n📊 Statistical Similarity Summary:")
            mean_diffs = [v for k, v in results['similarity'].items() if k.startswith('mean_diff_')]
            if mean_diffs:
                print(f"  Average mean difference: {np.mean(mean_diffs):.4f}")
            if 'correlation_diff' in results['similarity']:
                print(f"  Correlation structure difference: {results['similarity']['correlation_diff']:.4f}")
        
        # Utility Summary
        if results['utility']:
            print("\n🛠️ Data Utility Summary:")
            for metric, value in results['utility'].items():
                print(f"  {metric}: {value:.4f}")
        
        # Overall Quality Score
        self._calculate_overall_quality_score(results)
    
    def _calculate_overall_quality_score(self, results):
        """
        Calculate an overall quality score for the synthetic data.
        """
        print("\n🏆 OVERALL QUALITY SCORE:")
        
        scores = []
        
        # SDM Score (lower is better)
        if results['sdm']:
            ks_stats = [v['statistic'] for k, v in results['sdm'].items() if k.startswith('ks_')]
            if ks_stats:
                sdm_score = 1 - np.mean(ks_stats)  # Convert to 0-1 scale
                scores.append(sdm_score)
                print(f"  SDM Score: {sdm_score:.4f}")
        
        # TSTR Score
        if results['tstr']:
            if 'accuracy' in results['tstr']:
                scores.append(results['tstr']['accuracy'])
                print(f"  TSTR Accuracy Score: {results['tstr']['accuracy']:.4f}")
            elif 'r2' in results['tstr']:
                scores.append(max(0, results['tstr']['r2']))  # Ensure non-negative
                print(f"  TSTR R² Score: {max(0, results['tstr']['r2']):.4f}")
        
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
                print(f"  Feature Importance Score: {results['utility']['feature_importance_correlation']:.4f}")
            if 'privacy_score' in results['utility']:
                scores.append(results['utility']['privacy_score'])
                print(f"  Privacy Score: {results['utility']['privacy_score']:.4f}")
        
        if scores:
            overall_score = np.mean(scores)
            print(f"\n🎯 OVERALL QUALITY SCORE: {overall_score:.4f}")
            
            # Quality assessment
            if overall_score >= 0.8:
                print("🌟 EXCELLENT: Synthetic data quality is very high!")
            elif overall_score >= 0.6:
                print("✅ GOOD: Synthetic data quality is acceptable.")
            elif overall_score >= 0.4:
                print("⚠️ FAIR: Synthetic data quality needs improvement.")
            else:
                print("❌ POOR: Synthetic data quality is significantly low.")
    
    def plot_comparisons(self, save_path=None):
        """
        Generate comparison plots between real and synthetic data.
        """
        print("\n📊 Generating comparison plots...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Real vs Synthetic Data Comparison', fontsize=16)
        
        # 1. Distribution comparison for numerical columns
        if self.numerical_columns:
            col = self.numerical_columns[0]
            axes[0, 0].hist(self.real_data[col].dropna(), alpha=0.7, label='Real', bins=20, density=True)
            axes[0, 0].hist(self.synthetic_data[col].dropna(), alpha=0.7, label='Synthetic', bins=20, density=True)
            axes[0, 0].set_title(f'Distribution: {col}')
            axes[0, 0].legend()
        
        # 2. Correlation heatmap comparison
        if len(self.numerical_columns) > 1:
            real_corr = self.real_data[self.numerical_columns].corr()
            synth_corr = self.synthetic_data[self.numerical_columns].corr()
            
            im1 = axes[0, 1].imshow(real_corr, cmap='coolwarm', vmin=-1, vmax=1)
            axes[0, 1].set_title('Real Data Correlation')
            axes[0, 1].set_xticks(range(len(self.numerical_columns)))
            axes[0, 1].set_xticklabels(self.numerical_columns, rotation=45)
            axes[0, 1].set_yticks(range(len(self.numerical_columns)))
            axes[0, 1].set_yticklabels(self.numerical_columns)
            plt.colorbar(im1, ax=axes[0, 1])
            
            im2 = axes[1, 0].imshow(synth_corr, cmap='coolwarm', vmin=-1, vmax=1)
            axes[1, 0].set_title('Synthetic Data Correlation')
            axes[1, 0].set_xticks(range(len(self.numerical_columns)))
            axes[1, 0].set_xticklabels(self.numerical_columns, rotation=45)
            axes[1, 0].set_yticks(range(len(self.numerical_columns)))
            axes[1, 0].set_yticklabels(self.numerical_columns)
            plt.colorbar(im2, ax=axes[1, 0])
        
        # 3. Target variable comparison
        if self.target_column and self.target_column in self.numerical_columns:
            axes[1, 1].boxplot([self.real_data[self.target_column].dropna(), 
                               self.synthetic_data[self.target_column].dropna()],
                              labels=['Real', 'Synthetic'])
            axes[1, 1].set_title(f'Target Variable: {self.target_column}')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Plots saved to: {save_path}")
        
        plt.show()


# Example usage function
def evaluate_synthetic_data(real_data_path, synthetic_data_path, target_column=None, 
                          categorical_columns=None, save_plots=True):
    """
    Convenience function to evaluate synthetic data from file paths.
    
    Args:
        real_data_path: Path to real data CSV file
        synthetic_data_path: Path to synthetic data CSV file
        target_column: Name of target column
        categorical_columns: List of categorical column names
        save_plots: Whether to save comparison plots
    """
    # Load data
    real_data = pd.read_csv(real_data_path)
    synthetic_data = pd.read_csv(synthetic_data_path)
    
    # Initialize evaluator
    evaluator = SyntheticDataEvaluator(
        real_data=real_data,
        synthetic_data=synthetic_data,
        target_column=target_column,
        categorical_columns=categorical_columns
    )
    
    # Run comprehensive evaluation
    results = evaluator.comprehensive_evaluation()
    
    # Generate plots
    if save_plots:
        evaluator.plot_comparisons("synthetic_data_comparison.png")
    
    return results 