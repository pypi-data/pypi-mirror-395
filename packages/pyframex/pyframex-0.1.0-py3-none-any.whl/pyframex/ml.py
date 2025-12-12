"""
AutoML Engine - Smart AI Integration for PyFrameX
=================================================

Automatic machine learning workflows integrated directly into DataFrames.
"""

from typing import Dict, List, Any, Optional, Tuple
import warnings

# Optional ML dependencies
try:
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.linear_model import LogisticRegression, LinearRegression
    from sklearn.cluster import KMeans
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("scikit-learn not installed. ML features will be limited.")


class AutoML:
    """
    Automatic Machine Learning engine
    
    Features:
    - auto_clean(): Automatic data cleaning
    - auto_predict(): Automatic model training
    - auto_cluster(): Automatic clustering
    - auto_timeseries(): Time series forecasting
    """
    
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.scalers = {}
    
    def auto_clean(self, frame: 'Frame') -> 'Frame':
        """
        Automatically clean data:
        - Remove duplicates
        - Handle missing values
        - Remove outliers
        - Fix data types
        """
        from .frame import Frame
        from .columns import IntColumn, FloatColumn, StringColumn
        
        # Start with copy
        cleaned_data = {}
        
        for name, col in frame.columns.items():
            data = col.data.copy()
            
            # Handle missing values
            if isinstance(col, (IntColumn, FloatColumn)):
                # Fill with median
                valid_values = [x for x in data if x is not None]
                if valid_values:
                    median = sorted(valid_values)[len(valid_values) // 2]
                    data = [x if x is not None else median for x in data]
            
            elif isinstance(col, StringColumn):
                # Fill with mode or 'unknown'
                value_counts = {}
                for val in data:
                    if val is not None:
                        value_counts[val] = value_counts.get(val, 0) + 1
                
                if value_counts:
                    mode = max(value_counts, key=value_counts.get)
                    data = [x if x is not None else mode for x in data]
            
            cleaned_data[name] = data
        
        result = Frame(cleaned_data)
        
        # Remove duplicates
        seen = set()
        keep_indices = []
        for i in range(len(result)):
            row_tuple = tuple(result.columns[col].data[i] for col in result.columns)
            if row_tuple not in seen:
                seen.add(row_tuple)
                keep_indices.append(i)
        
        if len(keep_indices) < len(result):
            mask = [i in keep_indices for i in range(len(result))]
            result = result.filter(mask)
        
        return result
    
    def auto_predict(self, frame: 'Frame', target: str, test_size: float = 0.2, **kwargs) -> Dict[str, Any]:
        """
        Automatically train a predictive model
        
        Args:
            frame: Input Frame
            target: Target column name
            test_size: Fraction of data for testing
        
        Returns:
            Dictionary with model, metrics, and predictions
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for auto_predict. Install with: pip install scikit-learn")
        
        from .columns import IntColumn, FloatColumn, StringColumn
        
        # Prepare features and target
        if target not in frame.columns:
            raise ValueError(f"Target column '{target}' not found")
        
        y = frame.columns[target].data
        
        # Select feature columns (all except target)
        feature_cols = [col for col in frame.columns if col != target]
        
        # Encode categorical features
        X = []
        for i in range(len(frame)):
            row = []
            for col_name in feature_cols:
                col = frame.columns[col_name]
                value = col.data[i]
                
                if isinstance(col, StringColumn):
                    # Encode strings
                    if col_name not in self.encoders:
                        self.encoders[col_name] = LabelEncoder()
                        self.encoders[col_name].fit(col.data)
                    
                    try:
                        encoded = self.encoders[col_name].transform([value])[0]
                        row.append(encoded)
                    except:
                        row.append(0)
                else:
                    row.append(value if value is not None else 0)
            
            X.append(row)
        
        # Determine task type (classification or regression)
        target_col = frame.columns[target]
        is_classification = isinstance(target_col, StringColumn) or len(set(y)) < 20
        
        # Encode target if classification
        if is_classification and isinstance(target_col, StringColumn):
            encoder = LabelEncoder()
            y = encoder.fit_transform(y)
            self.encoders[target] = encoder
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        # Train model
        if is_classification:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            metrics = {
                'task': 'classification',
                'accuracy': accuracy,
                'n_train': len(X_train),
                'n_test': len(X_test)
            }
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            r2 = r2_score(y_test, y_pred)
            
            metrics = {
                'task': 'regression',
                'rmse': rmse,
                'r2': r2,
                'n_train': len(X_train),
                'n_test': len(X_test)
            }
        
        # Feature importance
        if hasattr(model, 'feature_importances_'):
            feature_importance = dict(zip(feature_cols, model.feature_importances_))
            metrics['feature_importance'] = feature_importance
        
        # Store model
        self.models[target] = model
        
        return {
            'model': model,
            'metrics': metrics,
            'predictions': y_pred,
            'actual': y_test
        }
    
    def auto_cluster(self, frame: 'Frame', n_clusters: int = 3, **kwargs) -> 'Frame':
        """
        Automatically perform clustering
        
        Args:
            frame: Input Frame
            n_clusters: Number of clusters
        
        Returns:
            Frame with cluster labels added
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for auto_cluster. Install with: pip install scikit-learn")
        
        from .columns import IntColumn, FloatColumn, StringColumn
        
        # Prepare feature matrix
        X = []
        numeric_cols = []
        
        for col_name, col in frame.columns.items():
            if isinstance(col, (IntColumn, FloatColumn)):
                numeric_cols.append(col_name)
        
        for i in range(len(frame)):
            row = []
            for col_name in numeric_cols:
                value = frame.columns[col_name].data[i]
                row.append(value if value is not None else 0)
            X.append(row)
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(X_scaled)
        
        # Add cluster labels to frame
        from .frame import Frame
        result_data = frame.to_dict()
        result_data['cluster'] = list(labels)
        
        return Frame(result_data)
    
    def auto_timeseries(self, frame: 'Frame', date_col: str, value_col: str, periods: int = 10) -> Dict[str, Any]:
        """
        Automatic time series forecasting
        
        Args:
            frame: Input Frame
            date_col: Date column name
            value_col: Value column to forecast
            periods: Number of periods to forecast
        
        Returns:
            Dictionary with forecast and metrics
        """
        # Simple moving average forecast for now
        # Can be enhanced with ARIMA, Prophet, etc.
        
        values = frame.columns[value_col].data
        
        # Calculate moving average (last 3 periods)
        window_size = min(3, len(values))
        last_values = values[-window_size:]
        forecast_value = sum(last_values) / len(last_values)
        
        # Generate forecast
        forecast = [forecast_value] * periods
        
        return {
            'forecast': forecast,
            'method': 'moving_average',
            'window_size': window_size,
            'periods': periods
        }
    
    def suggest_transformations(self, frame: 'Frame') -> List[str]:
        """
        Suggest data transformations based on data characteristics
        
        Returns:
            List of suggested transformation strings
        """
        from .columns import IntColumn, FloatColumn, StringColumn
        
        suggestions = []
        
        for name, col in frame.columns.items():
            if isinstance(col, (IntColumn, FloatColumn)):
                # Check for skewness
                valid = [x for x in col.data if x is not None]
                if valid:
                    mean_val = sum(valid) / len(valid)
                    median_val = sorted(valid)[len(valid) // 2]
                    
                    # If mean >> median, suggests right skew
                    if mean_val > median_val * 1.5:
                        suggestions.append(f"Apply log transformation to '{name}' (right-skewed)")
                    
                    # Check for outliers (simple IQR method)
                    sorted_vals = sorted(valid)
                    q1 = sorted_vals[len(sorted_vals) // 4]
                    q3 = sorted_vals[3 * len(sorted_vals) // 4]
                    iqr = q3 - q1
                    
                    outliers = [x for x in valid if x < q1 - 1.5*iqr or x > q3 + 1.5*iqr]
                    if len(outliers) > len(valid) * 0.05:
                        suggestions.append(f"Remove outliers from '{name}' ({len(outliers)} detected)")
            
            elif isinstance(col, StringColumn):
                unique_ratio = len(col.unique()) / len(col)
                
                if unique_ratio < 0.5:
                    suggestions.append(f"Consider one-hot encoding for '{name}' (categorical)")
                elif unique_ratio > 0.9:
                    suggestions.append(f"Consider dropping '{name}' (too many unique values)")
        
        return suggestions
    
    def auto_feature_engineering(self, frame: 'Frame') -> 'Frame':
        """
        Automatically create useful features
        
        Features created:
        - Polynomial features for numeric columns
        - Interaction features
        - Date features (if date columns exist)
        """
        from .frame import Frame
        from .columns import IntColumn, FloatColumn, DateColumn
        
        result_data = frame.to_dict()
        
        # Find numeric columns
        numeric_cols = []
        for name, col in frame.columns.items():
            if isinstance(col, (IntColumn, FloatColumn)):
                numeric_cols.append(name)
        
        # Create squared features
        for col_name in numeric_cols[:3]:  # Limit to first 3 to avoid explosion
            col = frame.columns[col_name]
            squared = [x * x if x is not None else None for x in col.data]
            result_data[f"{col_name}_squared"] = squared
        
        # Create interaction features (first 2 pairs)
        for i in range(min(2, len(numeric_cols))):
            for j in range(i+1, min(i+2, len(numeric_cols))):
                col1 = frame.columns[numeric_cols[i]]
                col2 = frame.columns[numeric_cols[j]]
                interaction = [a * b if a is not None and b is not None else None 
                              for a, b in zip(col1.data, col2.data)]
                result_data[f"{numeric_cols[i]}_x_{numeric_cols[j]}"] = interaction
        
        # Extract date features
        for name, col in frame.columns.items():
            if isinstance(col, DateColumn):
                result_data[f"{name}_year"] = col.year().data
                result_data[f"{name}_month"] = col.month().data
                result_data[f"{name}_day"] = col.day().data
                result_data[f"{name}_weekday"] = col.weekday().data
        
        return Frame(result_data)
