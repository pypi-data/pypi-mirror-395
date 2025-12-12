import unittest
import pandas as pd
import numpy as np
import warnings
import os
import sys

# Add src to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from model_monitoring.performance_measures import PerformancesMeasures
from model_monitoring.data_drift import DataDrift
# Import other components if needed, e.g. FairnessMeasures, XAI
# from model_monitoring.fairness_measures import FairnessMeasures
# from model_monitoring.XAI import XAI

class TestModelMonitoring(unittest.TestCase):

    def setUp(self):
        # Suppress warnings for cleaner output
        warnings.filterwarnings("ignore")
        
        # Sample data for classification
        self.df_classification = pd.DataFrame({
            'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            'pred': [0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
            'prob': [0.1, 0.9, 0.2, 0.4, 0.3, 0.8, 0.6, 0.7, 0.1, 0.9]
        })

        # Sample data for regression
        self.df_regression = pd.DataFrame({
            'target': np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
            'pred': np.array([1.1, 1.9, 3.2, 3.8, 5.1])
        })

        # Sample data for clustering
        self.data_matrix = pd.DataFrame({
            'col1': np.random.rand(100),
            'col2': np.random.rand(100)
        })
        self.cluster_labels = np.random.randint(0, 3, 100)

        # Sample data for Data Drift
        self.data_stor = pd.DataFrame({
            'feature_num': np.random.normal(0, 1, 100),
            'feature_cat': np.random.choice(['A', 'B', 'C'], 100)
        })
        self.data_curr = pd.DataFrame({
            'feature_num': np.random.normal(0.1, 1, 100), # Slight drift
            'feature_cat': np.random.choice(['A', 'B', 'C'], 100)
        })

    def test_performance_measures_classification(self):
        print("\nTesting PerformancesMeasures (Classification)...")
        pm = PerformancesMeasures(model_type="classification", set_metrics="standard")
        metrics = pm.compute_metrics(
            target=self.df_classification['target'],
            predictions=self.df_classification['pred'],
            prob=self.df_classification['prob']
        )
        self.assertIn('accuracy_score', metrics)
        self.assertIn('roc_auc_score', metrics)
        print("Metrics:", metrics)

    def test_performance_measures_regression(self):
        print("\nTesting PerformancesMeasures (Regression)...")
        pm = PerformancesMeasures(model_type="regression", set_metrics="standard")
        metrics = pm.compute_metrics(
            target=self.df_regression['target'],
            predictions=self.df_regression['pred']
        )
        self.assertIn('mean_squared_error', metrics)
        self.assertIn('r2_score', metrics)
        print("Metrics:", metrics)

    def test_performance_measures_clustering(self):
        print("\nTesting PerformancesMeasures (Clustering)...")
        pm = PerformancesMeasures(approach_type="unsupervised", model_type="clustering", set_metrics="standard")
        metrics = pm.compute_metrics(
            cluster_labels=self.cluster_labels,
            data_matrix=self.data_matrix
        )
        self.assertIn('classification_clustering', metrics)
        print("Metrics:", metrics)

    def test_data_drift_psi(self):
        print("\nTesting DataDrift (PSI)...")
        dd = DataDrift(self.data_stor, self.data_curr, type_data="data")
        report = dd.report_drift(stat="psi")
        self.assertIsInstance(report, pd.DataFrame)
        self.assertIn('total_psi', report.columns)
        print("Report Head:\n", report.head())

    def test_data_drift_pval(self):
        print("\nTesting DataDrift (P-Value)...")
        dd = DataDrift(self.data_stor, self.data_curr, type_data="data")
        report = dd.report_drift(stat="pval")
        self.assertIsInstance(report, pd.DataFrame)
        self.assertIn('common_pval', report.columns)
        print("Report Head:\n", report.head())

if __name__ == '__main__':
    unittest.main()
