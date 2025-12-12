#!/usr/bin/env python3
"""
Test script to demonstrate auto-detection functionality
"""

import pandas as pd
import numpy as np
from evaluate_synthetic_data import auto_detect_target_column, evaluate_pre_post_processing

def test_auto_detection():
    """Test auto-detection with different scenarios."""
    
    print("🧪 TESTING AUTO-DETECTION FUNCTIONALITY")
    print("="*50)
    
    # Test 1: Regression dataset (last numerical column)
    print("\n📊 Test 1: Regression Dataset")
    pre_df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'target': np.random.randn(100)  # Should be detected
    })
    post_df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'target': np.random.randn(100)
    })
    
    detected = auto_detect_target_column(pre_df, post_df)
    print(f"Detected target: {detected}")
    
    # Test 2: Classification dataset (categorical target)
    print("\n📊 Test 2: Classification Dataset")
    pre_df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'class': np.random.choice(['A', 'B', 'C'], 100)  # Should be detected
    })
    post_df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'class': np.random.choice(['A', 'B', 'C'], 100)
    })
    
    detected = auto_detect_target_column(pre_df, post_df)
    print(f"Detected target: {detected}")
    
    # Test 3: Keyword-based detection
    print("\n📊 Test 3: Keyword-based Detection")
    pre_df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'prediction': np.random.randn(100)  # Should be detected (keyword)
    })
    post_df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'prediction': np.random.randn(100)
    })
    
    detected = auto_detect_target_column(pre_df, post_df)
    print(f"Detected target: {detected}")
    
    # Test 4: No common columns
    print("\n📊 Test 4: No Common Columns")
    pre_df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100)
    })
    post_df = pd.DataFrame({
        'feature3': np.random.randn(100),
        'feature4': np.random.randn(100)
    })
    
    detected = auto_detect_target_column(pre_df, post_df)
    print(f"Detected target: {detected}")

if __name__ == "__main__":
    test_auto_detection()
    print("\n✅ Auto-detection test completed!") 