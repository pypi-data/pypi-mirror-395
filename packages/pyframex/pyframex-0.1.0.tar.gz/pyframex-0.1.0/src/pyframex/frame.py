"""
Frame Engine - Core DataFrame Implementation
============================================

The main Frame class that provides Excel-like simplicity 
with SQL-like power.
"""

from typing import Any, Dict, List, Union, Optional, Callable
import csv
import json
from pathlib import Path

from .columns import (
    BaseColumn, IntColumn, FloatColumn, StringColumn, 
    DateColumn, BoolColumn, infer_column_type
)
from .query import QueryPlanner
from .ml import AutoML


class Frame:
    """
    PyFrameX DataFrame - Simple like Excel, Powerful like SQL, Smart like AI
    
    Examples:
        >>> df = Frame("sales.csv")
        >>> df["profit"] = df["revenue"] - df["cost"]
        >>> df.filter("region == 'west'")
        >>> df.sql("SELECT region, SUM(revenue) FROM df GROUP BY region")
        >>> df.auto_predict(target="price")
    """
    
    def __init__(self, data: Union[str, Dict[str, List], List[Dict]], columns: Optional[List[str]] = None):
        """
        Initialize a Frame from various sources
        
        Args:
            data: CSV file path, dictionary of columns, or list of rows
            columns: Optional column names (for list of rows)
        """
        self.columns: Dict[str, BaseColumn] = {}
        self._query_planner = None
        self._ml_engine = None
        
        if isinstance(data, str):
            # Load from file
            self._load_file(data)
        elif isinstance(data, dict):
            # Dictionary of columns
            self._load_dict(data)
        elif isinstance(data, list):
            # List of rows
            self._load_rows(data, columns)
        else:
            raise ValueError(f"Cannot create Frame from {type(data)}")
    
    def _load_file(self, filepath: str):
        """Load data from file (CSV, JSON)"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if path.suffix == '.csv':
            self._load_csv(filepath)
        elif path.suffix == '.json':
            self._load_json(filepath)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
    
    def _load_csv(self, filepath: str):
        """Load CSV file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if not rows:
            return
        
        # Convert to columnar format
        col_data = {key: [] for key in rows[0].keys()}
        for row in rows:
            for key, value in row.items():
                # Try to convert to appropriate type
                try:
                    if '.' in value:
                        col_data[key].append(float(value))
                    else:
                        col_data[key].append(int(value))
                except (ValueError, AttributeError):
                    col_data[key].append(value)
        
        # Create columns with type inference
        for name, data in col_data.items():
            self.columns[name] = infer_column_type(data, name)
    
    def _load_json(self, filepath: str):
        """Load JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            self._load_rows(data)
        elif isinstance(data, dict):
            self._load_dict(data)
    
    def _load_dict(self, data: Dict[str, List]):
        """Load from dictionary of columns"""
        for name, values in data.items():
            self.columns[name] = infer_column_type(values, name)
    
    def _load_rows(self, rows: List[Dict], columns: Optional[List[str]] = None):
        """Load from list of row dictionaries"""
        if not rows:
            return
        
        if columns is None:
            columns = list(rows[0].keys())
        
        col_data = {col: [] for col in columns}
        for row in rows:
            for col in columns:
                col_data[col].append(row.get(col))
        
        for name, data in col_data.items():
            self.columns[name] = infer_column_type(data, name)
    
    def __getitem__(self, key: Union[str, List[str]]) -> Union[BaseColumn, 'Frame']:
        """
        Get column(s) - Excel-style access
        
        Examples:
            >>> df["sales"]  # Get single column
            >>> df[["name", "sales"]]  # Get multiple columns
        """
        if isinstance(key, str):
            if key not in self.columns:
                raise KeyError(f"Column '{key}' not found")
            return self.columns[key]
        elif isinstance(key, list):
            # Return new Frame with selected columns
            new_frame = Frame({})
            for col in key:
                if col not in self.columns:
                    raise KeyError(f"Column '{col}' not found")
                new_frame.columns[col] = self.columns[col]
            return new_frame
        else:
            raise TypeError(f"Invalid key type: {type(key)}")
    
    def __setitem__(self, key: str, value: Union[BaseColumn, List, Any]):
        """
        Set column - Excel-style assignment
        
        Examples:
            >>> df["profit"] = df["revenue"] - df["cost"]
            >>> df["category"] = "default"
        """
        if isinstance(value, BaseColumn):
            if len(value) != len(self) and len(self) > 0:
                raise ValueError(f"Column length mismatch: {len(value)} != {len(self)}")
            value.name = key
            self.columns[key] = value
        elif isinstance(value, list):
            self.columns[key] = infer_column_type(value, key)
        else:
            # Broadcast scalar value
            length = len(self) if len(self) > 0 else 1
            self.columns[key] = infer_column_type([value] * length, key)
    
    def __len__(self) -> int:
        """Number of rows"""
        if not self.columns:
            return 0
        return len(next(iter(self.columns.values())))
    
    def __repr__(self) -> str:
        """Pretty print the Frame"""
        if not self.columns:
            return "Frame(empty)"
        
        lines = []
        lines.append(f"Frame({len(self)} rows × {len(self.columns)} columns)")
        lines.append("")
        
        # Column names
        col_names = list(self.columns.keys())
        lines.append("  " + " | ".join(f"{name:>10}" for name in col_names))
        lines.append("  " + "-" * (len(col_names) * 13))
        
        # First 10 rows
        num_rows = min(10, len(self))
        for i in range(num_rows):
            row_data = []
            for col_name in col_names:
                value = self.columns[col_name][i]
                row_data.append(f"{str(value):>10}")
            lines.append("  " + " | ".join(row_data))
        
        if len(self) > 10:
            lines.append(f"  ... ({len(self) - 10} more rows)")
        
        return "\n".join(lines)
    
    def head(self, n: int = 5) -> 'Frame':
        """Return first n rows"""
        new_frame = Frame({})
        for name, col in self.columns.items():
            new_frame.columns[name] = col[:n]
        return new_frame
    
    def tail(self, n: int = 5) -> 'Frame':
        """Return last n rows"""
        new_frame = Frame({})
        for name, col in self.columns.items():
            new_frame.columns[name] = col[-n:]
        return new_frame
    
    def shape(self) -> tuple:
        """Return (rows, columns)"""
        return (len(self), len(self.columns))
    
    def dtypes(self) -> Dict[str, str]:
        """Get column data types"""
        return {name: col.dtype for name, col in self.columns.items()}
    
    def summary(self) -> str:
        """Generate statistical summary"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"Frame Summary: {len(self)} rows × {len(self.columns)} columns")
        lines.append("=" * 60)
        lines.append("")
        
        for name, col in self.columns.items():
            lines.append(f"Column: {name} ({col.dtype})")
            
            if isinstance(col, (IntColumn, FloatColumn)):
                lines.append(f"  Min:    {col.min()}")
                lines.append(f"  Max:    {col.max()}")
                lines.append(f"  Mean:   {col.mean():.2f}")
                lines.append(f"  Median: {col.median()}")
                if isinstance(col, FloatColumn):
                    lines.append(f"  Std:    {col.std():.2f}")
            elif isinstance(col, StringColumn):
                unique = col.unique()
                lines.append(f"  Unique: {len(unique)}")
                lines.append(f"  Sample: {unique[:3]}")
            elif isinstance(col, DateColumn):
                lines.append(f"  Min:    {col.min()}")
                lines.append(f"  Max:    {col.max()}")
            elif isinstance(col, BoolColumn):
                lines.append(f"  True:   {col.sum()}")
                lines.append(f"  False:  {len(col) - col.sum()}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def filter(self, condition: Union[str, List[bool]]) -> 'Frame':
        """
        Filter rows based on condition
        
        Examples:
            >>> df.filter("sales > 100")
            >>> df.filter(df["region"] == "west")
        """
        if isinstance(condition, str):
            # Parse string condition
            mask = self._eval_condition(condition)
        else:
            mask = condition
        
        new_frame = Frame({})
        for name, col in self.columns.items():
            new_frame.columns[name] = col.filter(mask)
        return new_frame
    
    def _eval_condition(self, condition: str) -> List[bool]:
        """Evaluate condition string to boolean mask"""
        # Simple eval-based approach (can be enhanced with AST parser)
        # Replace column names with actual data access
        namespace = {name: col for name, col in self.columns.items()}
        
        try:
            result = eval(condition, {"__builtins__": {}}, namespace)
            if isinstance(result, list):
                return result
            else:
                return [result] * len(self)
        except Exception as e:
            raise ValueError(f"Invalid condition: {condition}. Error: {e}")
    
    def select(self, *columns: str) -> 'Frame':
        """Select specific columns"""
        return self[list(columns)]
    
    def drop(self, *columns: str) -> 'Frame':
        """Drop columns"""
        new_frame = Frame({})
        for name, col in self.columns.items():
            if name not in columns:
                new_frame.columns[name] = col
        return new_frame
    
    def sort(self, by: str, ascending: bool = True) -> 'Frame':
        """Sort by column"""
        if by not in self.columns:
            raise KeyError(f"Column '{by}' not found")
        
        # Create index pairs
        col = self.columns[by]
        indexed = list(enumerate(col.data))
        indexed.sort(key=lambda x: x[1] if x[1] is not None else float('inf'), reverse=not ascending)
        
        # Reorder all columns
        new_frame = Frame({})
        sorted_indices = [idx for idx, _ in indexed]
        
        for name, original_col in self.columns.items():
            new_data = [original_col.data[i] for i in sorted_indices]
            new_frame.columns[name] = infer_column_type(new_data, name)
        
        return new_frame
    
    def groupby(self, by: Union[str, List[str]]) -> 'GroupBy':
        """Group by column(s)"""
        if isinstance(by, str):
            by = [by]
        return GroupBy(self, by)
    
    def sql(self, query: str) -> 'Frame':
        """
        Execute SQL query on the Frame
        
        Example:
            >>> df.sql("SELECT region, SUM(revenue) FROM df GROUP BY region")
        """
        if self._query_planner is None:
            self._query_planner = QueryPlanner()
        
        return self._query_planner.execute(query, self)
    
    def to_dict(self) -> Dict[str, List]:
        """Convert to dictionary of columns"""
        return {name: col.data for name, col in self.columns.items()}
    
    def to_csv(self, filepath: str):
        """Save to CSV file"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Header
            writer.writerow(self.columns.keys())
            # Rows
            for i in range(len(self)):
                row = [col.data[i] for col in self.columns.values()]
                writer.writerow(row)
    
    def to_json(self, filepath: str):
        """Save to JSON file"""
        data = []
        for i in range(len(self)):
            row = {name: col.data[i] for name, col in self.columns.items()}
            data.append(row)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    # ML Integration
    def auto_clean(self) -> 'Frame':
        """Automatically clean the data"""
        if self._ml_engine is None:
            self._ml_engine = AutoML()
        return self._ml_engine.auto_clean(self)
    
    def auto_predict(self, target: str, **kwargs) -> dict:
        """Automatically train a predictive model"""
        if self._ml_engine is None:
            self._ml_engine = AutoML()
        return self._ml_engine.auto_predict(self, target, **kwargs)
    
    def auto_cluster(self, n_clusters: int = 3, **kwargs) -> 'Frame':
        """Automatically perform clustering"""
        if self._ml_engine is None:
            self._ml_engine = AutoML()
        return self._ml_engine.auto_cluster(self, n_clusters, **kwargs)


class GroupBy:
    """GroupBy operation handler"""
    
    def __init__(self, frame: Frame, by: List[str]):
        self.frame = frame
        self.by = by
        self._groups = self._create_groups()
    
    def _create_groups(self) -> Dict[tuple, List[int]]:
        """Create groups mapping"""
        groups = {}
        
        for i in range(len(self.frame)):
            key = tuple(self.frame.columns[col].data[i] for col in self.by)
            if key not in groups:
                groups[key] = []
            groups[key].append(i)
        
        return groups
    
    def agg(self, operations: Dict[str, str]) -> Frame:
        """
        Aggregate with operations
        
        Example:
            >>> df.groupby("region").agg({"revenue": "sum", "orders": "count"})
        """
        result_data = {col: [] for col in self.by}
        
        for col, op in operations.items():
            result_data[f"{col}_{op}"] = []
        
        for key, indices in self._groups.items():
            # Add group keys
            for i, col in enumerate(self.by):
                result_data[col].append(key[i])
            
            # Calculate aggregations
            for col, op in operations.items():
                column = self.frame.columns[col]
                group_data = [column.data[i] for i in indices]
                
                if op == "sum":
                    result = sum(x for x in group_data if x is not None)
                elif op == "mean":
                    valid = [x for x in group_data if x is not None]
                    result = sum(valid) / len(valid) if valid else None
                elif op == "count":
                    result = len(group_data)
                elif op == "min":
                    valid = [x for x in group_data if x is not None]
                    result = min(valid) if valid else None
                elif op == "max":
                    valid = [x for x in group_data if x is not None]
                    result = max(valid) if valid else None
                else:
                    raise ValueError(f"Unknown operation: {op}")
                
                result_data[f"{col}_{op}"].append(result)
        
        return Frame(result_data)
    
    def sum(self) -> Frame:
        """Sum all numeric columns"""
        ops = {}
        for name, col in self.frame.columns.items():
            if isinstance(col, (IntColumn, FloatColumn)) and name not in self.by:
                ops[name] = "sum"
        return self.agg(ops)
    
    def mean(self) -> Frame:
        """Average all numeric columns"""
        ops = {}
        for name, col in self.frame.columns.items():
            if isinstance(col, (IntColumn, FloatColumn)) and name not in self.by:
                ops[name] = "mean"
        return self.agg(ops)
    
    def count(self) -> Frame:
        """Count rows per group"""
        result_data = {col: [] for col in self.by}
        result_data["count"] = []
        
        for key, indices in self._groups.items():
            for i, col in enumerate(self.by):
                result_data[col].append(key[i])
            result_data["count"].append(len(indices))
        
        return Frame(result_data)
