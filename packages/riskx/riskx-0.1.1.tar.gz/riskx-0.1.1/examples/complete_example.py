"""
RiskX Complete Example - End-to-End Credit Scoring
==================================================

This example demonstrates the full RiskX workflow from data loading
to model training, scoring, monitoring, and explainability.
"""

import pandas as pd
import numpy as np
from riskx import (
    RiskDataConnector, RiskCleaner, RiskFeatureEngine,
    RiskAutoModel, ScoringEngine, RiskMonitor, RiskExplain,
    RiskPipeline
)

# Set random seed for reproducibility
np.random.seed(42)

print("="*70)
print("RiskX Complete Example - Credit Scoring Pipeline")
print("="*70)

# ============================================================================
# Example 1: Quick Start with Automated Pipeline
# ============================================================================

print("\n" + "="*70)
print("Example 1: Automated Pipeline (Easiest Way)")
print("="*70 + "\n")

# Create sample data
n_samples = 1000
data = pd.DataFrame({
    'customer_id': range(n_samples),
    'age': np.random.randint(18, 70, n_samples),
    'income': np.random.randint(20000, 150000, n_samples),
    'debt_ratio': np.random.uniform(0, 0.8, n_samples),
    'credit_history_years': np.random.randint(0, 30, n_samples),
    'num_accounts': np.random.randint(1, 15, n_samples),
    'employment_status': np.random.choice(['employed', 'self-employed', 'unemployed'], n_samples),
    'default': np.random.choice([0, 1], n_samples, p=[0.85, 0.15])  # 15% default rate
})

# Save to CSV for example
data.to_csv('sample_credit_data.csv', index=False)

# Use automated pipeline
pipeline = RiskPipeline("credit_scoring_pipeline")

results = pipeline.run_full_pipeline(
    source='csv',
    target='default',
    algorithms=['logistic', 'rf', 'xgboost'],
    load_params={'path': 'sample_credit_data.csv'},
    auto_clean=True,
    auto_features=True,
    test_size=0.2,
    score_min=300,
    score_max=850
)

print(f"\nPipeline Results:")
print(f"  Test AUC: {results['test_auc']:.4f}")
print(f"  Best Model: {pipeline.model.best_model}")

# Score a new application
new_application = {
    'age': 35,
    'income': 75000,
    'debt_ratio': 0.25,
    'credit_history_years': 8,
    'num_accounts': 5
}

# Note: In real use, you'd preprocess this through the same pipeline
print(f"\nNew Application Score: (would need preprocessing)")

# ============================================================================
# Example 2: Step-by-Step Manual Control
# ============================================================================

print("\n" + "="*70)
print("Example 2: Manual Step-by-Step (Full Control)")
print("="*70 + "\n")

# Step 1: Load data
print("Step 1: Loading data...")
connector = RiskDataConnector()
data = connector.from_csv('sample_credit_data.csv')
print(f"✓ Loaded {len(data)} records")

# Step 2: Data cleaning
print("\nStep 2: Cleaning data...")
cleaner = RiskCleaner()

# Profile data quality
profile = cleaner.profile(data)
print(f"✓ Data quality profile: {profile['n_missing_total']} missing values")

# Auto-clean
data_clean = cleaner.auto_clean(data, target_column='default')
print(f"✓ Cleaned data: {len(data_clean)} records, {len(data_clean.columns)} columns")

# Step 3: Feature engineering
print("\nStep 3: Engineering features...")
feature_engine = RiskFeatureEngine()

# Compute WOE/IV for important features
woe_df, iv = feature_engine.compute_woe_iv(data_clean, 'income', 'default', n_bins=10)
print(f"✓ Income IV: {iv:.4f}")

# Auto-generate all features
data_features = feature_engine.auto_features(data_clean, target='default')
print(f"✓ Feature engineering complete: {len(data_features.columns)} features")

# Step 4: Train models
print("\nStep 4: Training models...")
from sklearn.model_selection import train_test_split

X = data_features.drop(['default', 'customer_id'], axis=1, errors='ignore')
y = data_features['default']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RiskAutoModel()
results = model.train_auto(
    X_train, y_train,
    X_val=X_test, y_val=y_test,
    algorithms=['logistic', 'rf', 'xgboost'],
    metric='auc'
)

print(f"✓ Best model: {type(model.best_model).__name__}")
print(f"✓ Best AUC: {model.best_score:.4f}")

# Calibrate model
calibrated_model = model.calibrate_model(X_train, y_train, method='isotonic')
print(f"✓ Model calibrated")

# Step 5: Scoring
print("\nStep 5: Setting up scoring...")
scorer = ScoringEngine(calibrated_model, score_min=300, score_max=850)

# Batch scoring
test_scores = scorer.score_batch(X_test)
print(f"✓ Scored {len(test_scores)} test records")

print(f"\nScore distribution:")
print(test_scores['rating'].value_counts().sort_index())

# Single prediction with reason codes
single_sample = X_test.iloc[0:1]
single_result = scorer.score_single(single_sample.to_dict('records')[0])
print(f"\nSingle prediction example:")
print(f"  Score: {single_result['score']}")
print(f"  Rating: {single_result['rating']}")
print(f"  Risk Level: {single_result['risk_level']}")
print(f"  Top reason codes:")
for rc in single_result['reason_codes'][:3]:
    print(f"    - {rc['code']}: {rc['description']}")

# Step 6: Monitoring
print("\nStep 6: Setting up monitoring...")
monitor = RiskMonitor(alert_threshold_psi=0.25)
monitor.set_baseline(X_train)

# Simulate new data (with slight drift)
X_new = X_test.copy()
X_new['income'] = X_new['income'] * 1.15  # 15% income increase (drift)

# Monitor for drift
report = monitor.monitor_dataset(X_train, X_new)
print(f"✓ Monitoring report: {report['overall_status']}")
if report['n_alerts'] > 0:
    print(f"⚠️  {report['n_alerts']} alert(s) detected")

# Track model performance
from sklearn.metrics import roc_auc_score
test_auc = roc_auc_score(y_test, test_scores['probability'])
perf_metrics = monitor.track_model_performance(
    y_test, 
    (test_scores['probability'] > 0.5).astype(int),
    test_scores['probability']
)
print(f"✓ Performance tracked: AUC={perf_metrics['auc']:.4f}")

# Step 7: Explainability
print("\nStep 7: Model explainability...")
explainer = RiskExplain(model.best_model)

# Global feature importance
try:
    importance_df = explainer.global_feature_importance(X_test.head(100), method='shap')
    print(f"✓ Top 5 important features:")
    for idx, row in importance_df.head(5).iterrows():
        print(f"  {idx+1}. {row['feature']}: {row['importance_normalized']:.4f}")
except Exception as e:
    print(f"  Note: SHAP explanations require 'shap' package: pip install shap")
    print(f"  Using model feature importance instead...")
    if hasattr(model.best_model, 'feature_importances_'):
        importance_df = explainer.global_feature_importance(X_test, method='model')
        print(f"✓ Top 5 important features:")
        for idx, row in importance_df.head(5).iterrows():
            print(f"  {idx+1}. {row['feature']}: {row['importance_normalized']:.4f}")

# ============================================================================
# Example 3: Production Deployment
# ============================================================================

print("\n" + "="*70)
print("Example 3: Production Deployment")
print("="*70 + "\n")

# Save model for production
print("Saving model for production...")
model.save_model("production_credit_model.pkl")
print("✓ Model saved")

# Simulate production scoring
print("\nProduction scoring example:")
new_applications = pd.DataFrame([
    {'age': 28, 'income': 45000, 'debt_ratio': 0.45, 'credit_history_years': 3, 'num_accounts': 2},
    {'age': 42, 'income': 95000, 'debt_ratio': 0.20, 'credit_history_years': 15, 'num_accounts': 8},
    {'age': 35, 'income': 65000, 'debt_ratio': 0.35, 'credit_history_years': 7, 'num_accounts': 4},
])

# In production, you would:
# 1. Load the saved model
# 2. Apply same preprocessing pipeline
# 3. Score in real-time or batch

print("\nExample applications for scoring:")
for idx, app in new_applications.iterrows():
    print(f"\nApplication {idx+1}:")
    print(f"  Age: {app['age']}, Income: ${app['income']:,}, Debt Ratio: {app['debt_ratio']:.2%}")
    print(f"  → Would be scored in production system")

# Export API specification
api_spec = scorer.export_api_spec()
print(f"\n✓ API specification ready for integration")
print(f"  Endpoints: {list(api_spec['endpoints'].keys())}")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "="*70)
print("RiskX Example Complete!")
print("="*70)

print("\n✓ What we demonstrated:")
print("  1. Automated end-to-end pipeline")
print("  2. Manual step-by-step control")
print("  3. Data loading and cleaning")
print("  4. Feature engineering (WOE/IV, auto-features)")
print("  5. Model training (Logistic, RF, XGBoost)")
print("  6. Model calibration")
print("  7. Credit scoring (300-850 range)")
print("  8. Monitoring and drift detection")
print("  9. Model explainability")
print("  10. Production deployment")

print("\n✓ Key Results:")
print(f"  - Best Model AUC: {model.best_score:.4f}")
print(f"  - Test Set AUC: {test_auc:.4f}")
print(f"  - Score Range: 300-850")
print(f"  - Monitoring Status: {report['overall_status']}")

print("\n✓ Next Steps:")
print("  - Integrate with your data sources")
print("  - Deploy to cloud (Azure, AWS, GCP)")
print("  - Set up real-time API endpoints")
print("  - Configure monitoring alerts")
print("  - Customize score ranges and bins")

print("\n" + "="*70)
print("For more information: https://github.com/idrissbado/RiskX")
print("="*70 + "\n")
