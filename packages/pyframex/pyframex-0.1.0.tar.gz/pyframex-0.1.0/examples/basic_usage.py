"""
PyFrameX Examples - Comprehensive Usage Demonstrations
======================================================
"""

from pyframex import Frame

print("=" * 70)
print("PyFrameX - Next-Generation DataFrame Examples")
print("=" * 70)
print()

# Example 1: Basic Operations
print("📊 Example 1: Basic DataFrame Operations")
print("-" * 70)

# Create from dictionary
df = Frame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [25, 30, 35, 28, 32],
    "salary": [50000, 60000, 70000, 55000, 65000],
    "department": ["Sales", "Engineering", "Sales", "Marketing", "Engineering"]
})

print(df)
print()
print(df.summary())
print()

# Example 2: Column Operations
print("\n📊 Example 2: Column Operations")
print("-" * 70)

# Excel-style calculations
df["bonus"] = df["salary"] * 0.1
df["total_comp"] = df["salary"] + df["bonus"]
df["age_group"] = "30+"

print(df[["name", "salary", "bonus", "total_comp"]])
print()

# Example 3: Filtering
print("\n📊 Example 3: Filtering")
print("-" * 70)

# High earners
high_earners = df.filter("salary > 60000")
print("High earners (salary > 60000):")
print(high_earners[["name", "salary"]])
print()

# Young high earners
young_high = df.filter("age < 30 and salary > 55000")
print("Young high earners:")
print(young_high[["name", "age", "salary"]])
print()

# Example 4: Grouping and Aggregation
print("\n📊 Example 4: Grouping and Aggregation")
print("-" * 70)

dept_stats = df.groupby("department").agg({
    "salary": "mean",
    "age": "mean"
})

print("Department Statistics:")
print(dept_stats)
print()

# Example 5: SQL Queries
print("\n📊 Example 5: SQL Queries")
print("-" * 70)

result = df.sql("""
    SELECT 
        department,
        AVG(salary) as avg_salary,
        COUNT(name) as employee_count
    FROM df
    GROUP BY department
    ORDER BY avg_salary DESC
""")

print("SQL Query Result:")
print(result)
print()

# Example 6: String Operations
print("\n📊 Example 6: String Operations")
print("-" * 70)

# Create sample data with strings
text_df = Frame({
    "product": ["Apple iPhone", "Samsung Galaxy", "Google Pixel", "Apple iPad"],
    "category": ["Phone", "Phone", "Phone", "Tablet"],
    "price": [999, 899, 799, 599]
})

# String operations
text_df["product_upper"] = text_df["product"].upper()
text_df["is_apple"] = text_df["product"].contains("Apple")
text_df["name_length"] = text_df["product"].len()

print(text_df)
print()

# Example 7: Sorting
print("\n📊 Example 7: Sorting")
print("-" * 70)

sorted_df = df.sort("salary", ascending=False)
print("Employees sorted by salary (descending):")
print(sorted_df[["name", "salary"]])
print()

# Example 8: ML - Auto Cleaning
print("\n📊 Example 8: Auto Data Cleaning")
print("-" * 70)

# Create data with issues
messy_df = Frame({
    "id": [1, 2, 3, 3, 4, 5],  # Duplicate
    "value": [10, None, 30, 30, 50, 60],  # Missing value
    "category": ["A", "B", None, "A", "B", "A"]
})

print("Before cleaning:")
print(messy_df)
print()

cleaned_df = messy_df.auto_clean()
print("After auto_clean():")
print(cleaned_df)
print()

# Example 9: ML - Auto Predict (requires scikit-learn)
print("\n📊 Example 9: Auto Prediction")
print("-" * 70)

try:
    # Create training data
    ml_df = Frame({
        "experience": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "education": [1, 1, 2, 2, 2, 3, 3, 3, 3, 3],
        "salary": [40, 45, 55, 60, 65, 75, 80, 85, 90, 95]
    })
    
    # Auto predict
    results = ml_df.auto_predict(target="salary", test_size=0.3)
    
    print(f"Task: {results['metrics']['task']}")
    print(f"R² Score: {results['metrics']['r2']:.4f}")
    print(f"RMSE: {results['metrics']['rmse']:.2f}")
    print(f"Training samples: {results['metrics']['n_train']}")
    print(f"Test samples: {results['metrics']['n_test']}")
    print()
    
except ImportError:
    print("⚠️ scikit-learn not installed. Install with: pip install pyframex[ml]")
    print()

# Example 10: ML - Auto Clustering (requires scikit-learn)
print("\n📊 Example 10: Auto Clustering")
print("-" * 70)

try:
    cluster_df = Frame({
        "x": [1, 2, 2, 8, 9, 9, 25, 26, 27],
        "y": [1, 2, 3, 8, 9, 10, 25, 26, 27]
    })
    
    clustered = cluster_df.auto_cluster(n_clusters=3)
    print(clustered)
    print()
    
    cluster_counts = clustered.groupby("cluster").count()
    print("Cluster sizes:")
    print(cluster_counts)
    print()
    
except ImportError:
    print("⚠️ scikit-learn not installed. Install with: pip install pyframex[ml]")
    print()

# Example 11: Save and Load
print("\n📊 Example 11: Save and Load")
print("-" * 70)

# Save to CSV
df.to_csv("example_output.csv")
print("✓ Saved to example_output.csv")

# Save to JSON
df.to_json("example_output.json")
print("✓ Saved to example_output.json")

# Load back
loaded = Frame("example_output.csv")
print("✓ Loaded from example_output.csv")
print(f"  Shape: {loaded.shape()}")
print()

# Example 12: Complex Query with Multiple Operations
print("\n📊 Example 12: Complex Pipeline")
print("-" * 70)

# Create sample sales data
sales = Frame({
    "region": ["West", "East", "West", "North", "East", "South", "West", "North"],
    "product": ["A", "B", "A", "C", "B", "A", "C", "B"],
    "revenue": [1000, 1500, 1200, 800, 1600, 900, 1100, 1400],
    "cost": [600, 800, 700, 500, 900, 500, 650, 750]
})

# Complex analysis pipeline
sales["profit"] = sales["revenue"] - sales["cost"]
sales["margin"] = sales["profit"] / sales["revenue"]

# SQL analysis
top_performers = sales.sql("""
    SELECT 
        region,
        SUM(revenue) as total_revenue,
        SUM(profit) as total_profit,
        AVG(margin) as avg_margin
    FROM df
    GROUP BY region
    ORDER BY total_profit DESC
""")

print("Regional Performance:")
print(top_performers)
print()

print("=" * 70)
print("✓ All examples completed!")
print("=" * 70)
