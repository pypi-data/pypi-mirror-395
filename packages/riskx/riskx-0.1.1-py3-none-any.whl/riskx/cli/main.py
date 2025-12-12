"""
RiskX CLI - Command-Line Interface
==================================

Command-line interface for RiskX operations.
"""

import argparse
import sys
from pathlib import Path
import json


def create_parser():
    """Create CLI argument parser"""
    parser = argparse.ArgumentParser(
        prog='riskx',
        description='RiskX - End-to-End Automated Risk Scoring Platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Train a model
  riskx train --data data.csv --target default --output model.pkl
  
  # Score new data
  riskx score --model model.pkl --data new_data.csv --output scores.csv
  
  # Monitor for drift
  riskx monitor --baseline train.csv --current new_data.csv
  
  # Run full pipeline
  riskx pipeline --data data.csv --target default --config pipeline.json

For more information: https://github.com/idrissbado/RiskX
        """
    )
    
    parser.add_argument('--version', action='version', version='RiskX 0.1.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train risk scoring models')
    train_parser.add_argument('--data', required=True, help='Training data file (CSV)')
    train_parser.add_argument('--target', required=True, help='Target column name')
    train_parser.add_argument('--algorithms', nargs='+', default=['logistic', 'rf', 'xgboost'],
                             help='Algorithms to train (default: logistic rf xgboost)')
    train_parser.add_argument('--test-size', type=float, default=0.2,
                             help='Test set proportion (default: 0.2)')
    train_parser.add_argument('--output', default='model.pkl',
                             help='Output model file (default: model.pkl)')
    train_parser.add_argument('--calibrate', action='store_true',
                             help='Calibrate model probabilities')
    
    # Score command
    score_parser = subparsers.add_parser('score', help='Score new applications')
    score_parser.add_argument('--model', required=True, help='Trained model file')
    score_parser.add_argument('--data', required=True, help='Data to score (CSV)')
    score_parser.add_argument('--output', default='scores.csv',
                             help='Output scores file (default: scores.csv)')
    score_parser.add_argument('--score-min', type=int, default=300,
                             help='Minimum score (default: 300)')
    score_parser.add_argument('--score-max', type=int, default=850,
                             help='Maximum score (default: 850)')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor data drift')
    monitor_parser.add_argument('--baseline', required=True, help='Baseline data (CSV)')
    monitor_parser.add_argument('--current', required=True, help='Current data (CSV)')
    monitor_parser.add_argument('--threshold', type=float, default=0.25,
                               help='PSI alert threshold (default: 0.25)')
    monitor_parser.add_argument('--output', default='monitoring_report.json',
                               help='Output report file (default: monitoring_report.json)')
    
    # Pipeline command
    pipeline_parser = subparsers.add_parser('pipeline', help='Run full pipeline')
    pipeline_parser.add_argument('--data', required=True, help='Input data file (CSV)')
    pipeline_parser.add_argument('--target', required=True, help='Target column name')
    pipeline_parser.add_argument('--config', help='Pipeline configuration file (JSON)')
    pipeline_parser.add_argument('--output-dir', default='./output',
                                help='Output directory (default: ./output)')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show package information')
    
    return parser


def train_command(args):
    """Execute train command"""
    from riskx import RiskDataConnector, RiskCleaner, RiskFeatureEngine, RiskAutoModel
    from sklearn.model_selection import train_test_split
    
    print(f"\n{'='*60}")
    print("RiskX Training Pipeline")
    print(f"{'='*60}\n")
    
    # Load data
    print(f"Loading data from {args.data}...")
    connector = RiskDataConnector()
    data = connector.from_csv(args.data)
    print(f"✓ Loaded {len(data)} records\n")
    
    # Clean data
    print("Cleaning data...")
    cleaner = RiskCleaner()
    data_clean = cleaner.auto_clean(data, target_column=args.target)
    print(f"✓ Cleaned {len(data_clean)} records\n")
    
    # Engineer features
    print("Engineering features...")
    feature_engine = RiskFeatureEngine()
    data_features = feature_engine.auto_features(data_clean, target=args.target)
    print(f"✓ Created {len(data_features.columns)} features\n")
    
    # Split data
    print(f"Splitting data (test size: {args.test_size})...")
    X = data_features.drop(args.target, axis=1)
    y = data_features[args.target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42, stratify=y
    )
    print(f"✓ Train: {len(X_train)}, Test: {len(X_test)}\n")
    
    # Train models
    print(f"Training models: {', '.join(args.algorithms)}...")
    model = RiskAutoModel()
    results = model.train_auto(
        X_train, y_train,
        X_val=X_test, y_val=y_test,
        algorithms=args.algorithms
    )
    print(f"\n✓ Best model AUC: {model.best_score:.4f}\n")
    
    # Calibrate if requested
    if args.calibrate:
        print("Calibrating model...")
        model.calibrate_model(X_train, y_train)
        print("✓ Model calibrated\n")
    
    # Save model
    print(f"Saving model to {args.output}...")
    model.save_model(args.output)
    print(f"✓ Model saved\n")
    
    print(f"{'='*60}")
    print("Training Complete!")
    print(f"{'='*60}\n")


def score_command(args):
    """Execute score command"""
    from riskx import RiskAutoModel, ScoringEngine, RiskDataConnector
    
    print(f"\n{'='*60}")
    print("RiskX Scoring Pipeline")
    print(f"{'='*60}\n")
    
    # Load model
    print(f"Loading model from {args.model}...")
    model = RiskAutoModel()
    model.load_model(args.model)
    print("✓ Model loaded\n")
    
    # Load data
    print(f"Loading data from {args.data}...")
    connector = RiskDataConnector()
    data = connector.from_csv(args.data)
    print(f"✓ Loaded {len(data)} records\n")
    
    # Score
    print("Scoring...")
    scorer = ScoringEngine(model.get_best_model(), score_min=args.score_min, score_max=args.score_max)
    scores = scorer.score_batch(data)
    print(f"✓ Scored {len(scores)} records\n")
    
    # Save scores
    print(f"Saving scores to {args.output}...")
    scores.to_csv(args.output, index=False)
    print(f"✓ Scores saved\n")
    
    # Summary
    print("Score Distribution:")
    print(scores['rating'].value_counts().sort_index())
    print(f"\n{'='*60}")
    print("Scoring Complete!")
    print(f"{'='*60}\n")


def monitor_command(args):
    """Execute monitor command"""
    from riskx import RiskDataConnector, RiskMonitor
    import json
    
    print(f"\n{'='*60}")
    print("RiskX Monitoring Pipeline")
    print(f"{'='*60}\n")
    
    # Load baseline data
    print(f"Loading baseline from {args.baseline}...")
    connector = RiskDataConnector()
    baseline = connector.from_csv(args.baseline)
    print(f"✓ Loaded {len(baseline)} baseline records\n")
    
    # Load current data
    print(f"Loading current data from {args.current}...")
    current = connector.from_csv(args.current)
    print(f"✓ Loaded {len(current)} current records\n")
    
    # Monitor
    print(f"Monitoring for drift (threshold: {args.threshold})...")
    monitor = RiskMonitor(alert_threshold_psi=args.threshold)
    report = monitor.monitor_dataset(baseline, current)
    print(f"\n✓ Monitoring complete: {report['overall_status']}\n")
    
    if report['n_alerts'] > 0:
        print(f"⚠️  {report['n_alerts']} alert(s) detected:")
        for alert in report['alerts']:
            print(f"  - {alert['feature']}: {alert['metric']}={alert['score']:.4f}")
    
    # Save report
    print(f"\nSaving report to {args.output}...")
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✓ Report saved\n")
    
    print(f"{'='*60}")
    print("Monitoring Complete!")
    print(f"{'='*60}\n")


def pipeline_command(args):
    """Execute full pipeline command"""
    from riskx import RiskPipeline
    from pathlib import Path
    import json
    
    print(f"\n{'='*60}")
    print("RiskX Full Pipeline")
    print(f"{'='*60}\n")
    
    # Load config if provided
    config = {}
    if args.config:
        print(f"Loading configuration from {args.config}...")
        with open(args.config, 'r') as f:
            config = json.load(f)
        print("✓ Configuration loaded\n")
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run pipeline
    pipeline = RiskPipeline("cli_pipeline")
    results = pipeline.run_full_pipeline(
        source='csv',
        target=args.target,
        load_params={'path': args.data},
        **config
    )
    
    # Save results
    print(f"\nSaving results to {output_dir}...")
    pipeline.save_pipeline(str(output_dir / 'pipeline.pkl'))
    
    # Save execution log
    log_df = pipeline.get_execution_summary()
    log_df.to_csv(output_dir / 'execution_log.csv', index=False)
    
    print(f"✓ Results saved to {output_dir}\n")
    
    print(f"{'='*60}")
    print("Pipeline Complete!")
    print(f"Test AUC: {results['test_auc']:.4f}")
    print(f"{'='*60}\n")


def info_command(args):
    """Execute info command"""
    print("\n" + "="*60)
    print("RiskX - End-to-End Automated Risk Scoring Platform")
    print("="*60)
    print("\nVersion: 0.1.0")
    print("Author: Idriss Bado")
    print("Email: idrissbadoolivier@gmail.com")
    print("License: MIT")
    print("\nWebsite: https://github.com/idrissbado/RiskX")
    print("PyPI: https://pypi.org/project/riskx/")
    print("\nFeatures:")
    print("  ✓ Multi-source data loading")
    print("  ✓ Automated data cleaning")
    print("  ✓ Risk-specific feature engineering")
    print("  ✓ AutoML with 4 algorithms")
    print("  ✓ Production-ready scoring engine")
    print("  ✓ PSI/CSI monitoring")
    print("  ✓ SHAP/LIME explainability")
    print("  ✓ End-to-end pipeline orchestration")
    print("\nQuick Start:")
    print("  pip install riskx")
    print("  riskx train --data data.csv --target default")
    print("="*60 + "\n")


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'train':
            train_command(args)
        elif args.command == 'score':
            score_command(args)
        elif args.command == 'monitor':
            monitor_command(args)
        elif args.command == 'pipeline':
            pipeline_command(args)
        elif args.command == 'info':
            info_command(args)
        else:
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
