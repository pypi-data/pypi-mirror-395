# AutoDataMind 🧠

**Zero-Code Automated Data Science**

[![PyPI version](https://badge.fury.io/py/autodatamind.svg)](https://pypi.org/project/autodatamind/)
[![Python](https://img.shields.io/pypi/pyversions/autodatamind.svg)](https://pypi.org/project/autodatamind/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

AutoDataMind is your **Native Intelligence Layer** for data science. No Pandas knowledge required. No ML expertise needed. Just simple function calls for complete automation.

## 🌍 Philosophy

**Data science should be accessible to everyone, everywhere.**

AutoDataMind democratizes data science for:
- **Emerging Markets**: Africa, Asia, Latin America
- **Small Businesses**: No data science budget
- **Students**: Learning without complexity
- **Non-Technical Users**: Business analysts, researchers

## ✨ Features

### 🎯 Zero-Code Automation
```python
import autodatamind as adm

# Automatic data analysis - ONE line
adm.analyze("sales.csv")

# Automatic ML training - ONE line
model = adm.autotrain("sales.csv", target="revenue")

# Automatic dashboard - ONE line
adm.dashboard("sales.csv")

# Automatic deep learning - ONE line
dl_model = adm.auto_deep("data.csv", target="category")

# Automatic insights report - ONE line
report = adm.generate_insights("sales.csv")
```

### 🤖 6 Native Intelligence Agents

1. **DataAgent**: Universal data loading (CSV, Excel, JSON, Parquet)
2. **ProfileAgent**: Automatic data profiling and analysis
3. **VizAgent**: Beautiful HTML dashboards
4. **MLAgent**: Automatic machine learning
5. **DLAgent**: Automatic deep learning (PyTorch)
6. **InsightAgent**: Natural language insights

### 🚀 What AutoDataMind Does

- **Loads Data**: CSV, Excel, JSON, Parquet - auto-detected
- **Cleans Data**: Duplicates, missing values, outliers - automatic
- **Analyzes Data**: Statistics, correlations, insights - comprehensive
- **Visualizes Data**: HTML dashboards - professional
- **Trains ML Models**: Regression, classification - auto-selected
- **Trains Deep Models**: Neural networks - auto-built
- **Generates Reports**: Narratives, recommendations - human-readable

## 📦 Installation

```bash
pip install autodatamind
```

## 🎓 Quick Start

### Analyze Any Dataset

```python
import autodatamind as adm

# Load and analyze - returns complete analysis
analysis = adm.analyze("your_data.csv")

# Access results
print(analysis['overview'])
print(analysis['statistics'])
print(analysis['insights'])
```

### Train ML Model - Zero Code

```python
# Automatic ML training
result = adm.autotrain("sales.csv", target="revenue")

# Get trained model
model = result['model']

# Get metrics
print(result['metrics'])
# {'rmse': 1234.56, 'mae': 987.65, 'r2': 0.89}

# Model saved automatically!
```

### Create Dashboard - One Line

```python
# Generate professional HTML dashboard
adm.dashboard("sales.csv")
# Opens in browser automatically!
```

### Deep Learning - No PyTorch Knowledge

```python
# Automatic deep learning
result = adm.auto_deep(
    "data.csv",
    target="category",
    epochs=50
)

# Get model and metrics
model = result['model']
print(result['metrics'])
# {'accuracy': 0.95}
```

### Get Business Insights

```python
# Generate narrative report
report = adm.generate_insights("sales.csv", target="revenue")

# Report includes:
# - Executive summary
# - Key findings
# - Statistical insights
# - Recommendations
# - Data quality assessment
```

## 📊 Complete Example

```python
import autodatamind as adm

# 1. Load data (auto-detected format)
df = adm.read_data("sales.csv")

# 2. Clean data (automatic)
df_clean = adm.autoclean(df)

# 3. Analyze data
analysis = adm.analyze(df_clean)

# 4. Create dashboard
adm.dashboard(df_clean)

# 5. Train ML model
ml_result = adm.autotrain(df_clean, target="revenue")

# 6. Train deep learning model
dl_result = adm.auto_deep(df_clean, target="revenue", epochs=100)

# 7. Generate insights report
report = adm.generate_insights(df_clean, target="revenue")

# Done! 🎉
```

## 🎯 Use Cases

### Business Analytics
```python
# Analyze sales data
adm.analyze("sales_2024.csv")
adm.dashboard("sales_2024.csv")
adm.generate_insights("sales_2024.csv", target="total_sales")
```

### Predictive Modeling
```python
# Predict customer churn
result = adm.autotrain("customers.csv", target="churn")
print(f"Model accuracy: {result['metrics']['accuracy']:.2%}")
```

### Data Exploration
```python
# Explore new dataset
adm.analyze("new_data.csv")  # Get overview
adm.dashboard("new_data.csv")  # Visual exploration
```

### Report Generation
```python
# Generate executive report
report = adm.generate_insights(
    "quarterly_data.csv",
    target="profit",
    save_report=True
)
```

## 🏗️ Architecture

AutoDataMind uses **6 Native Intelligence Agents**:

```
autodatamind/
├── core/               # Core functionality
│   ├── reader.py      # Universal data loader
│   ├── cleaner.py     # Automatic data cleaning
│   ├── utils.py       # Helper functions
│   └── validator.py   # Data validation
├── agents/            # Intelligence agents
│   ├── data_agent.py       # Data handling
│   ├── profile_agent.py    # Analysis & profiling
│   ├── viz_agent.py        # Visualization
│   ├── ml_agent.py         # Machine learning
│   ├── dl_agent.py         # Deep learning
│   └── insight_agent.py    # Narrative generation
└── models/            # ML/DL engines
    ├── auto_ml.py     # AutoML engine
    └── auto_dl.py     # AutoDL engine
```

## 💡 Philosophy: Native Intelligence Layer

**Traditional Data Science**:
```python
# 40 lines of Pandas code
import pandas as pd
df = pd.read_csv("data.csv")
df = df.dropna()
df = df.drop_duplicates()
# ... 35 more lines ...
```

**AutoDataMind**:
```python
# 1 line
adm.analyze("data.csv")
```

**No Pandas knowledge required. No ML expertise needed.**

## 🌍 Target Markets

### Emerging Economies
- **Africa**: Kenya, Nigeria, South Africa, Ghana
- **Asia**: India, Bangladesh, Philippines, Vietnam  
- **Latin America**: Brazil, Mexico, Colombia

### User Segments
- **Students**: Learn data science without complexity
- **Small Businesses**: No data science budget
- **Researchers**: Focus on insights, not code
- **Analysts**: Fast results without programming

## 🔬 Technical Details

### Supported Data Formats
- **CSV**: Auto-encoding detection (UTF-8, Latin-1, ISO-8859-1)
- **Excel**: .xlsx, .xls
- **JSON**: Multiple orientations
- **Parquet**: High-performance columnar

### Auto-Cleaning Features
- Duplicate removal
- Missing value handling (auto/drop/mean/median/mode)
- Type fixing
- Outlier removal
- Data validation

### ML Algorithms
- **Classification**: RandomForest, GradientBoosting, Logistic Regression, KNN, Naive Bayes
- **Regression**: RandomForest, GradientBoosting, Linear Regression, Ridge, Lasso

### DL Architectures
- **MLP**: Simple multilayer perceptron
- **Deep**: Deep neural networks (128→64→32)
- **Wide**: Wide networks (256→128→64)
- **Auto-selection** based on data size

## 📈 Performance

### Speed
- **Small datasets** (<10K rows): <1 second
- **Medium datasets** (10K-100K): <5 seconds
- **Large datasets** (>100K): <30 seconds

### Accuracy
- **AutoML**: Competitive with manual tuning
- **AutoDL**: State-of-the-art architectures
- **Auto-hyperparameter tuning**: GridSearchCV optimization

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Additional data formats
- More ML algorithms
- Advanced DL architectures
- New visualization types
- Documentation improvements

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 👤 Author

**Idriss Olivier Bado**
- Email: idrissbadoolivier@gmail.com
- GitHub: [@idrissbado](https://github.com/idrissbado)

## 🙏 Acknowledgments

Built with:
- **pandas**: Data manipulation
- **scikit-learn**: Machine learning
- **PyTorch**: Deep learning
- **matplotlib/seaborn**: Visualization

## 🔗 Links

- **PyPI**: [https://pypi.org/project/autodatamind/](https://pypi.org/project/autodatamind/)
- **GitHub**: [https://github.com/idrissbado/autodatamind](https://github.com/idrissbado/autodatamind)
- **Documentation**: [https://github.com/idrissbado/autodatamind#readme](https://github.com/idrissbado/autodatamind#readme)
- **Issues**: [https://github.com/idrissbado/autodatamind/issues](https://github.com/idrissbado/autodatamind/issues)

---

**Made with ❤️ for the global data science community**

**Democratizing AI, one line of code at a time**
