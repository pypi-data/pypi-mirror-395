"""
AutoDataMind - Advanced Usage Examples
=======================================

Advanced features and customization options.
"""

import autodatamind as adm
import pandas as pd

print("AutoDataMind - Advanced Examples\n")

# =============================================================================
# Example 1: Custom Data Cleaning
# =============================================================================
print("=" * 70)
print("Example 1: Advanced Data Cleaning with Custom Options")
print("=" * 70)

df = adm.read_data("data.csv")

# Custom cleaning options
df_clean = adm.autoclean(
    df,
    remove_duplicates=True,
    handle_missing='median',  # mean, median, mode, drop, forward_fill
    fix_types=True,
    remove_outliers=True,
    outlier_method='iqr',
    verbose=True
)

# Get data quality report
from autodatamind.core.cleaner import get_data_quality_report
quality_report = get_data_quality_report(df, df_clean)
print("\n📊 Data Quality Report:")
print(quality_report)


# =============================================================================
# Example 2: Advanced ML Training with Hyperparameter Tuning
# =============================================================================
print("\n" + "=" * 70)
print("Example 2: ML Training with Full Control")
print("=" * 70)

# Use MLAgent for more control
from autodatamind.agents.ml_agent import MLAgent

agent = MLAgent()

# Train with custom settings
result = agent.train(
    "data.csv",
    target="revenue",
    test_size=0.25,
    auto_clean=True,
    save_model=True,
    model_path="my_model.joblib",
    verbose=True
)

# Make predictions
new_data = pd.read_csv("new_data.csv")
predictions = agent.predict(new_data)
print(f"\n✓ Predictions: {predictions[:10]}")


# =============================================================================
# Example 3: Deep Learning with Custom Architecture
# =============================================================================
print("\n" + "=" * 70)
print("Example 3: Advanced Deep Learning")
print("=" * 70)

# Use DLAgent for more control
from autodatamind.agents.dl_agent import DLAgent

dl_agent = DLAgent()

# Train with custom settings
dl_result = dl_agent.train(
    "data.csv",
    target="category",
    task='classification',  # or 'regression', 'auto'
    epochs=100,
    batch_size=64,
    learning_rate=0.0001,
    auto_clean=True,
    save_model=True,
    model_path="my_deep_model.pth",
    verbose=True
)

print(f"\n✓ Training complete!")
print(f"  Final accuracy: {dl_result['metrics']['accuracy']:.4f}")
print(f"  Training history: {len(dl_result['history']['train_loss'])} epochs")


# =============================================================================
# Example 4: Using AutoML Engine Directly
# =============================================================================
print("\n" + "=" * 70)
print("Example 4: Direct AutoML Engine Usage")
print("=" * 70)

from autodatamind.models.auto_ml import AutoMLEngine

# Load and prepare data
df = adm.read_data("data.csv")
df_clean = adm.autoclean(df)

X = df_clean.drop(columns=['target'])
y = df_clean['target']

# Create AutoML engine
automl = AutoMLEngine(problem_type='auto')  # or 'classification', 'regression'

# Train with full control
results = automl.fit(
    X, y,
    test_size=0.2,
    cv_folds=5,
    tune_hyperparameters=True,
    verbose=True
)

print(f"\n✓ Best model: {results['best_model_name']}")
print(f"  CV score: {results['cv_score']:.4f}")
print(f"  All models tested:")
for name, model_result in automl.results.items():
    print(f"    {name}: {model_result['cv_score']:.4f}")


# =============================================================================
# Example 5: Using AutoDL Engine Directly
# =============================================================================
print("\n" + "=" * 70)
print("Example 5: Direct AutoDL Engine Usage")
print("=" * 70)

from autodatamind.models.auto_dl import AutoDLEngine

# Create AutoDL engine
autodl = AutoDLEngine(
    task='classification',
    architecture='deep'  # 'mlp', 'deep', 'wide', 'auto'
)

# Train with full control
dl_results = autodl.fit(
    X, y,
    epochs=100,
    batch_size=32,
    learning_rate=0.001,
    validation_split=0.2,
    early_stopping_patience=10,
    verbose=True
)

print(f"\n✓ Deep learning complete!")
print(f"  Architecture: {autodl.architecture}")
print(f"  Device: {autodl.device}")


# =============================================================================
# Example 6: Batch Processing Multiple Files
# =============================================================================
print("\n" + "=" * 70)
print("Example 6: Batch Processing")
print("=" * 70)

import glob

# Process all CSV files
csv_files = glob.glob("data/*.csv")

for file in csv_files:
    print(f"\nProcessing: {file}")
    
    # Analyze
    analysis = adm.analyze(file, verbose=False)
    print(f"  ✓ Analysis: {len(analysis['insights'])} insights")
    
    # Dashboard
    dashboard = adm.dashboard(file, save_html=True, open_browser=False)
    print(f"  ✓ Dashboard: {dashboard}")
    
    # Insights report
    report = adm.generate_insights(file, save_report=True, verbose=False)
    print(f"  ✓ Report: Generated")


# =============================================================================
# Example 7: Custom Visualization with VizAgent
# =============================================================================
print("\n" + "=" * 70)
print("Example 7: Custom Visualization")
print("=" * 70)

from autodatamind.agents.viz_agent import VizAgent

viz = VizAgent()

# Load data
df = adm.read_data("data.csv")

# Create custom dashboard
dashboard_html = viz.create_dashboard(
    df,
    title="My Custom Dashboard",
    save_path="custom_dashboard.html",
    open_browser=True
)

print(f"✓ Custom dashboard created!")


# =============================================================================
# Example 8: Insight Agent for Custom Reports
# =============================================================================
print("\n" + "=" * 70)
print("Example 8: Custom Insight Reports")
print("=" * 70)

from autodatamind.agents.insight_agent import InsightAgent

insight_agent = InsightAgent()

# Generate comprehensive report
report = insight_agent.generate(
    "data.csv",
    target="revenue",
    auto_clean=True,
    save_report=True,
    report_path="comprehensive_report.txt",
    verbose=True
)

print(f"\n✓ Comprehensive report generated!")
print(f"  Report length: {len(report)} characters")


# =============================================================================
# Example 9: Data Validation
# =============================================================================
print("\n" + "=" * 70)
print("Example 9: Data Validation Before Training")
print("=" * 70)

from autodatamind.core.validator import validate_data

df = adm.read_data("data.csv")

# Validate data quality
validation_result = validate_data(df)

if validation_result['is_valid']:
    print("✓ Data is valid and ready for training!")
else:
    print("⚠ Data quality issues detected:")
    for issue in validation_result['issues']:
        print(f"  • {issue}")
    
    print("\nWarnings:")
    for warning in validation_result['warnings']:
        print(f"  • {warning}")


# =============================================================================
# Example 10: Complete Production Pipeline
# =============================================================================
print("\n" + "=" * 70)
print("Example 10: Production-Ready Pipeline")
print("=" * 70)

def production_pipeline(data_path, target_column, output_dir="output"):
    """Complete production pipeline."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Load and validate
    print("1. Loading and validating data...")
    df = adm.read_data(data_path)
    validation = validate_data(df)
    
    if not validation['is_valid']:
        print("⚠ Data validation failed!")
        return None
    
    # 2. Clean
    print("2. Cleaning data...")
    df_clean = adm.autoclean(df, verbose=False)
    
    # 3. Analyze
    print("3. Analyzing data...")
    analysis = adm.analyze(df_clean, verbose=False)
    
    # 4. Dashboard
    print("4. Creating dashboard...")
    dashboard_path = adm.dashboard(
        df_clean,
        save_html=True,
        html_path=f"{output_dir}/dashboard.html",
        open_browser=False
    )
    
    # 5. Train ML model
    print("5. Training ML model...")
    ml_result = adm.autotrain(
        df_clean,
        target=target_column,
        save_model=True,
        model_path=f"{output_dir}/ml_model.joblib",
        verbose=False
    )
    
    # 6. Train DL model
    print("6. Training DL model...")
    dl_result = adm.auto_deep(
        df_clean,
        target=target_column,
        epochs=50,
        save_model=True,
        model_path=f"{output_dir}/dl_model.pth",
        verbose=False
    )
    
    # 7. Generate report
    print("7. Generating insights report...")
    report = adm.generate_insights(
        df_clean,
        target=target_column,
        save_report=True,
        report_path=f"{output_dir}/insights_report.txt",
        verbose=False
    )
    
    print(f"\n✓ Pipeline complete! Results in '{output_dir}/'")
    
    return {
        'analysis': analysis,
        'ml_result': ml_result,
        'dl_result': dl_result,
        'dashboard': dashboard_path,
        'report': report,
    }

# Run production pipeline
results = production_pipeline("data.csv", "target_column")


print("\n" + "=" * 70)
print("✓ All advanced examples complete!")
print("=" * 70)
