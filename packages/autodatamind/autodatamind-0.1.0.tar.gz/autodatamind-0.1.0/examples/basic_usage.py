"""
AutoDataMind - Basic Usage Examples
====================================

Simple examples demonstrating zero-code automation.
"""

import autodatamind as adm

# Example 1: Analyze Data
print("=" * 60)
print("Example 1: Automatic Data Analysis")
print("=" * 60)

# Just one line!
analysis = adm.analyze("your_data.csv")

# Access results
print("\n📊 Data Overview:")
print(analysis['overview'])

print("\n📈 Statistics:")
for col, stats in analysis['statistics'].items():
    print(f"  {col}: {stats}")

print("\n💡 Insights:")
for insight in analysis['insights']:
    print(f"  • {insight}")

print("\n✅ Recommendations:")
for rec in analysis['recommendations']:
    print(f"  → {rec}")


# Example 2: Create Dashboard
print("\n" + "=" * 60)
print("Example 2: Automatic HTML Dashboard")
print("=" * 60)

# Generate beautiful dashboard
dashboard_path = adm.dashboard("your_data.csv")
print(f"\n✓ Dashboard created: {dashboard_path}")
print("  Opens automatically in your browser!")


# Example 3: Train ML Model
print("\n" + "=" * 60)
print("Example 3: Automatic Machine Learning")
print("=" * 60)

# Train model automatically
result = adm.autotrain(
    "your_data.csv",
    target="target_column",
    test_size=0.2,
    save_model=True
)

print(f"\n🤖 Model trained: {result['problem_type']}")
print(f"📊 Metrics:")
for metric, value in result['metrics'].items():
    print(f"  {metric}: {value:.4f}")

print(f"\n💾 Model saved automatically!")


# Example 4: Deep Learning
print("\n" + "=" * 60)
print("Example 4: Automatic Deep Learning")
print("=" * 60)

# Train deep learning model
dl_result = adm.auto_deep(
    "your_data.csv",
    target="target_column",
    epochs=50,
    batch_size=32
)

print(f"\n🧠 Deep learning model trained!")
print(f"📊 Metrics:")
for metric, value in dl_result['metrics'].items():
    print(f"  {metric}: {value:.4f}")


# Example 5: Generate Insights
print("\n" + "=" * 60)
print("Example 5: Automatic Insights Report")
print("=" * 60)

# Generate narrative report
report = adm.generate_insights(
    "your_data.csv",
    target="target_column",
    save_report=True
)

print("\n📝 Insights report generated!")
print(report[:500] + "...")


# Example 6: Complete Pipeline
print("\n" + "=" * 60)
print("Example 6: Complete Automated Pipeline")
print("=" * 60)

# Load data
df = adm.read_data("your_data.csv")
print(f"✓ Loaded: {len(df)} rows")

# Clean data
df_clean = adm.autoclean(df)
print(f"✓ Cleaned: {len(df_clean)} rows")

# Analyze
analysis = adm.analyze(df_clean)
print(f"✓ Analysis complete: {len(analysis['insights'])} insights")

# Dashboard
dashboard = adm.dashboard(df_clean)
print(f"✓ Dashboard: {dashboard}")

# ML model
ml_model = adm.autotrain(df_clean, target="target_column")
print(f"✓ ML model: {ml_model['best_model_name']}")

# Insights
report = adm.generate_insights(df_clean, target="target_column")
print(f"✓ Report: {len(report)} characters")

print("\n🎉 Pipeline complete!")


# Example 7: Prediction
print("\n" + "=" * 60)
print("Example 7: Making Predictions")
print("=" * 60)

# Load new data for prediction
new_data = adm.read_data("new_data.csv")

# Use trained model from Example 3
predictions = result['model'].predict(new_data.drop(columns=['target_column']))
print(f"\n✓ Predictions made: {len(predictions)} samples")
print(f"  First 5 predictions: {predictions[:5]}")


print("\n" + "=" * 60)
print("✓ All examples complete!")
print("=" * 60)
