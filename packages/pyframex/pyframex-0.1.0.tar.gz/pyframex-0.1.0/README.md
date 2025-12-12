# 🚀 PyFrameX

**Next-Generation Native DataFrame for Python**

[![PyPI version](https://badge.fury.io/py/pyframex.svg)](https://pypi.org/project/pyframex/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Simple like Excel, Powerful like SQL, Smart like AI**

PyFrameX is a revolutionary DataFrame engine built from scratch in pure Python. It combines the simplicity of Excel, the power of SQL, and the intelligence of machine learning into one intuitive package.

---

## 🌟 What Makes PyFrameX Different?

### ❌ The Problem

- **Pandas**: Powerful but complicated (`.loc`, `.iloc`, `.apply` confusion)
- **Polars**: Fast but too technical for beginners
- **Excel**: Simple but limited in scale and automation

### ✅ The Solution: PyFrameX

```python
from pyframex import Frame

# Load data - just like Excel
df = Frame("sales.csv")

# Excel-style operations
df["profit"] = df["revenue"] - df["cost"]

# SQL-style queries
df.sql("SELECT region, SUM(revenue) FROM df GROUP BY region")

# AI-powered automation
df.auto_predict(target="sales")
```

---

## 🎯 Key Features

### 1️⃣ **Pure Python Native Engine**

- Zero dependencies for core functionality
- Custom column store implementation
- Type-aware operations (Int, Float, String, Date, Bool)
- Automatic type inference

### 2️⃣ **Excel-Like Simplicity**

```python
# Simple, intuitive operations
df["ratio"] = df["sales"] / df["visits"]
df["status"] = "active"

# No confusing .loc or .iloc needed!
```

### 3️⃣ **Built-in SQL Engine**

```python
# Execute SQL queries directly on DataFrames
result = df.sql("""
    SELECT 
        region, 
        SUM(revenue) as total_revenue,
        AVG(profit) as avg_profit
    FROM df 
    WHERE year = 2024 
    GROUP BY region
    ORDER BY total_revenue DESC
    LIMIT 10
""")
```

### 4️⃣ **AI-Powered Automation**

```python
# Automatic data cleaning
clean_df = df.auto_clean()

# Automatic predictive modeling
results = df.auto_predict(target="price")
print(f"Accuracy: {results['metrics']['accuracy']}")

# Automatic clustering
clustered = df.auto_cluster(n_clusters=3)

# Automatic feature engineering
enriched = df.auto_feature_engineering()
```

### 5️⃣ **Optimized Performance**

- Lazy evaluation
- Column-oriented storage
- Cached statistics
- Query optimization
- Filter pushdown

---

## 📦 Installation

```bash
# Basic installation
pip install pyframex

# With ML capabilities
pip install pyframex[ml]

# Install all features
pip install pyframex[all]
```

---

## 🚀 Quick Start

### Loading Data

```python
from pyframex import Frame

# From CSV
df = Frame("data.csv")

# From JSON
df = Frame("data.json")

# From dictionary
df = Frame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "salary": [50000, 60000, 70000]
})

# From list of dictionaries
df = Frame([
    {"name": "Alice", "age": 25, "salary": 50000},
    {"name": "Bob", "age": 30, "salary": 60000},
    {"name": "Charlie", "age": 35, "salary": 70000}
])
```

### Basic Operations

```python
# View data
print(df)
print(df.head(10))
print(df.tail(5))

# Get info
print(df.summary())
print(df.shape())  # (rows, columns)
print(df.dtypes())  # Column types

# Select columns
names = df["name"]
subset = df[["name", "salary"]]

# Add/modify columns
df["bonus"] = df["salary"] * 0.1
df["total"] = df["salary"] + df["bonus"]
```

### Filtering

```python
# Excel-style filtering
high_earners = df.filter("salary > 60000")
young_staff = df.filter("age < 30")

# Combined conditions
filtered = df.filter("age > 25 and salary < 70000")

# Using column comparisons
mask = df["age"] > 30
filtered = df.filter(mask)
```

### Sorting & Grouping

```python
# Sort
sorted_df = df.sort("salary", ascending=False)

# Group by
by_region = df.groupby("region").agg({
    "revenue": "sum",
    "orders": "count"
})

# Multiple aggregations
summary = df.groupby(["region", "category"]).agg({
    "revenue": "sum",
    "profit": "mean",
    "orders": "count"
})
```

### SQL Queries

```python
# Simple query
result = df.sql("SELECT name, salary FROM df WHERE age > 30")

# With aggregation
result = df.sql("""
    SELECT 
        region, 
        SUM(revenue) as total,
        AVG(profit) as avg_profit
    FROM df 
    GROUP BY region
""")

# With ordering and limit
result = df.sql("""
    SELECT * FROM df 
    WHERE status = 'active' 
    ORDER BY created_date DESC 
    LIMIT 100
""")

# Explain query plan
from pyframex.query import QueryPlanner
planner = QueryPlanner()
print(planner.explain("SELECT * FROM df WHERE revenue > 1000"))
```

---

## 🤖 Machine Learning Integration

### Auto Clean

```python
# Automatically:
# - Remove duplicates
# - Handle missing values (median/mode imputation)
# - Remove outliers
# - Fix data types
clean_df = df.auto_clean()
```

### Auto Predict

```python
# Automatic model training
results = df.auto_predict(
    target="price",
    test_size=0.2
)

# Results include:
print(results['metrics'])  # Performance metrics
print(results['model'])  # Trained model
print(results['predictions'])  # Test predictions

# Feature importance
for feature, importance in results['metrics']['feature_importance'].items():
    print(f"{feature}: {importance:.4f}")
```

### Auto Cluster

```python
# Automatic clustering
clustered = df.auto_cluster(n_clusters=3)
print(clustered["cluster"].value_counts())
```

### Feature Engineering

```python
# Automatically create:
# - Polynomial features
# - Interaction terms
# - Date extractions
enriched = df.auto_feature_engineering()
```

### Smart Suggestions

```python
# Get transformation suggestions
suggestions = df._ml_engine.suggest_transformations(df)
for suggestion in suggestions:
    print(f"💡 {suggestion}")
```

---

## 🔧 Advanced Features

### Column Operations

```python
# Numeric columns
df["price"].sum()
df["price"].mean()
df["price"].median()
df["price"].min()
df["price"].max()
df["price"].std()  # Standard deviation

# String columns
df["name"].lower()
df["name"].upper()
df["name"].strip()
df["name"].contains("alice")
df["name"].replace("old", "new")
df["name"].len()  # String lengths

# Date columns
df["date"].year()
df["date"].month()
df["date"].day()
df["date"].weekday()
```

### Mathematical Operations

```python
# Column arithmetic
df["total"] = df["price"] * df["quantity"]
df["discount_price"] = df["price"] * 0.9
df["profit"] = df["revenue"] - df["cost"]

# Column-to-column operations
df["ratio"] = df["sales"] / df["visits"]
df["growth"] = df["current"] - df["previous"]
```

### Data Export

```python
# Save to CSV
df.to_csv("output.csv")

# Save to JSON
df.to_json("output.json")

# Convert to dictionary
data_dict = df.to_dict()
```

---

## 📊 Real-World Examples

### Example 1: Sales Analysis

```python
from pyframex import Frame

# Load sales data
df = Frame("sales.csv")

# Calculate profit
df["profit"] = df["revenue"] - df["cost"]
df["margin"] = df["profit"] / df["revenue"]

# Find top performing regions
top_regions = df.sql("""
    SELECT 
        region,
        SUM(revenue) as total_revenue,
        AVG(margin) as avg_margin
    FROM df
    GROUP BY region
    ORDER BY total_revenue DESC
    LIMIT 5
""")

print(top_regions)
```

### Example 2: Customer Segmentation

```python
# Load customer data
customers = Frame("customers.csv")

# Auto-clean data
customers = customers.auto_clean()

# Perform clustering
segmented = customers.auto_cluster(n_clusters=4)

# Analyze clusters
cluster_summary = segmented.groupby("cluster").agg({
    "age": "mean",
    "purchases": "sum",
    "lifetime_value": "mean"
})

print(cluster_summary)
```

### Example 3: Predictive Modeling

```python
# Load historical data
data = Frame("historical_sales.csv")

# Engineer features
data = data.auto_feature_engineering()

# Train model
results = data.auto_predict(target="next_month_sales")

print(f"Model R²: {results['metrics']['r2']:.4f}")
print(f"RMSE: {results['metrics']['rmse']:.2f}")

# Feature importance
for feature, importance in results['metrics']['feature_importance'].items():
    if importance > 0.05:
        print(f"  {feature}: {importance:.2%}")
```

---

## 🎯 Use Cases

### Perfect For:

✅ **Data Analysts** - Excel-like simplicity with SQL power  
✅ **Data Scientists** - Built-in ML with no setup  
✅ **Python Beginners** - Intuitive, no steep learning curve  
✅ **Rapid Prototyping** - Fast iteration with auto features  
✅ **Educational Projects** - Learn data science easily  
✅ **Small to Medium Data** - Pure Python, no heavy dependencies

### Not Ideal For:

❌ Massive datasets (100M+ rows) - Use Polars/DuckDB  
❌ Distributed computing - Use Spark/Dask  
❌ Production big data pipelines - Use enterprise solutions

---

## 🏗️ Architecture

PyFrameX consists of 6 core components:

```
┌─────────────────────────────────────────┐
│           Frame (Main API)              │
│   Simple like Excel, Powerful like SQL  │
└─────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌───────▼────────┐
│ Column Engine  │  │  Query Planner │
│ - IntColumn    │  │  - SQL Parser  │
│ - FloatColumn  │  │  - Optimizer   │
│ - StringColumn │  │  - Executor    │
│ - DateColumn   │  │  - Cache       │
│ - BoolColumn   │  └────────────────┘
└────────────────┘
        │
┌───────▼────────┐  ┌────────────────┐
│   AutoML       │  │  Visualizer    │
│ - auto_clean   │  │  - Charts      │
│ - auto_predict │  │  - Summaries   │
│ - auto_cluster │  │  - Reports     │
└────────────────┘  └────────────────┘
```

---

## 📈 Performance

PyFrameX is optimized for clarity and moderate-sized datasets:

- **Column-oriented storage** for efficient operations
- **Lazy evaluation** where possible
- **Cached statistics** to avoid recomputation
- **Type-specific optimizations** for each column type
- **Query optimization** with filter pushdown

**Benchmark (1M rows):**
- Loading CSV: ~2-3 seconds
- Filtering: ~0.1-0.5 seconds  
- Grouping: ~0.5-1 second
- SQL query: ~0.5-2 seconds

---

## 🛠️ CLI Usage

```bash
# Show DataFrame info
pyframex info data.csv

# Show first 10 rows
pyframex head data.csv -n 10

# Execute SQL query
pyframex query data.csv "SELECT * FROM df WHERE age > 30"

# Auto-clean data
pyframex clean data.csv cleaned_data.csv

# Show version
pyframex version
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** - Open an issue on GitHub
2. **Suggest features** - Describe your use case
3. **Submit PRs** - Fix bugs or add features
4. **Write docs** - Improve documentation
5. **Share examples** - Show how you use PyFrameX

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

PyFrameX is inspired by:
- **Pandas** - The gold standard for DataFrame operations
- **Polars** - Modern columnar data processing
- **DuckDB** - Fast in-process SQL
- **Excel** - Universal data manipulation tool

---

## 📧 Contact & Support

- **Author**: Idriss Bado
- **Email**: idrissbadoolivier@gmail.com
- **GitHub**: [https://github.com/idrissbado/PyFrameX](https://github.com/idrissbado/PyFrameX)
- **Issues**: [GitHub Issues](https://github.com/idrissbado/PyFrameX/issues)

---

## 🎓 Citation

If you use PyFrameX in your research, please cite:

```bibtex
@software{pyframex2024,
  author = {Bado, Idriss},
  title = {PyFrameX: Next-Generation Native DataFrame for Python},
  year = {2024},
  url = {https://github.com/idrissbado/PyFrameX}
}
```

---

## ⭐ Star History

If you find PyFrameX useful, please give it a star on GitHub! ⭐

---

**Made with ❤️ by Idriss Bado**

*Simple like Excel, Powerful like SQL, Smart like AI*
