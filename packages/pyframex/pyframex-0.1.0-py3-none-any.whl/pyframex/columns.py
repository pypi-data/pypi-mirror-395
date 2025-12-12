"""
Column Engine - Native Column Types for PyFrameX
================================================

Pure Python columnar storage with type-specific optimizations.
"""

from typing import Any, List, Union, Optional, Callable
from datetime import datetime, date
import statistics


class BaseColumn:
    """Base class for all column types"""
    
    def __init__(self, data: List[Any], name: str = ""):
        self.data = list(data)
        self.name = name
        self._cached_stats = {}
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return self.__class__(self.data[idx], self.name)
        return self.data[idx]
    
    def __setitem__(self, idx, value):
        self.data[idx] = value
        self._cached_stats.clear()
    
    def __repr__(self) -> str:
        preview = self.data[:5]
        if len(self.data) > 5:
            preview_str = ", ".join(str(x) for x in preview) + ", ..."
        else:
            preview_str = ", ".join(str(x) for x in preview)
        return f"{self.__class__.__name__}([{preview_str}], length={len(self)})"
    
    def append(self, value):
        """Add a value to the column"""
        self.data.append(value)
        self._cached_stats.clear()
    
    def filter(self, mask: List[bool]) -> 'BaseColumn':
        """Filter column by boolean mask"""
        filtered = [val for val, keep in zip(self.data, mask) if keep]
        return self.__class__(filtered, self.name)
    
    def map(self, func: Callable) -> 'BaseColumn':
        """Apply function to each element"""
        return self.__class__([func(x) for x in self.data], self.name)
    
    def unique(self) -> List[Any]:
        """Get unique values"""
        seen = set()
        result = []
        for val in self.data:
            if val not in seen:
                seen.add(val)
                result.append(val)
        return result
    
    def value_counts(self) -> dict:
        """Count occurrences of each value"""
        counts = {}
        for val in self.data:
            counts[val] = counts.get(val, 0) + 1
        return counts


class IntColumn(BaseColumn):
    """Integer column with numeric operations"""
    
    def __init__(self, data: List[Union[int, None]], name: str = ""):
        super().__init__(data, name)
        self.dtype = "int"
    
    def sum(self) -> int:
        """Sum of all values (excluding None)"""
        if 'sum' not in self._cached_stats:
            self._cached_stats['sum'] = sum(x for x in self.data if x is not None)
        return self._cached_stats['sum']
    
    def mean(self) -> float:
        """Average of all values"""
        if 'mean' not in self._cached_stats:
            valid = [x for x in self.data if x is not None]
            self._cached_stats['mean'] = sum(valid) / len(valid) if valid else 0
        return self._cached_stats['mean']
    
    def min(self) -> int:
        """Minimum value"""
        valid = [x for x in self.data if x is not None]
        return min(valid) if valid else None
    
    def max(self) -> int:
        """Maximum value"""
        valid = [x for x in self.data if x is not None]
        return max(valid) if valid else None
    
    def median(self) -> float:
        """Median value"""
        valid = [x for x in self.data if x is not None]
        return statistics.median(valid) if valid else None
    
    def __add__(self, other):
        """Add operation"""
        if isinstance(other, (int, float)):
            return IntColumn([x + other if x is not None else None for x in self.data], self.name)
        elif isinstance(other, IntColumn):
            return IntColumn([a + b if a is not None and b is not None else None 
                             for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot add IntColumn and {type(other)}")
    
    def __sub__(self, other):
        """Subtract operation"""
        if isinstance(other, (int, float)):
            return IntColumn([x - other if x is not None else None for x in self.data], self.name)
        elif isinstance(other, IntColumn):
            return IntColumn([a - b if a is not None and b is not None else None 
                             for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot subtract {type(other)} from IntColumn")
    
    def __mul__(self, other):
        """Multiply operation"""
        if isinstance(other, (int, float)):
            return IntColumn([x * other if x is not None else None for x in self.data], self.name)
        elif isinstance(other, IntColumn):
            return IntColumn([a * b if a is not None and b is not None else None 
                             for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot multiply IntColumn and {type(other)}")
    
    def __truediv__(self, other):
        """Divide operation"""
        if isinstance(other, (int, float)):
            return FloatColumn([x / other if x is not None and other != 0 else None for x in self.data], self.name)
        elif isinstance(other, IntColumn):
            return FloatColumn([a / b if a is not None and b is not None and b != 0 else None 
                               for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot divide IntColumn by {type(other)}")
    
    def __eq__(self, other):
        """Equality comparison"""
        if isinstance(other, (int, float)):
            return [x == other if x is not None else False for x in self.data]
        elif isinstance(other, IntColumn):
            return [a == b if a is not None and b is not None else False 
                   for a, b in zip(self.data, other.data)]
        return False
    
    def __gt__(self, other):
        """Greater than comparison"""
        if isinstance(other, (int, float)):
            return [x > other if x is not None else False for x in self.data]
        elif isinstance(other, IntColumn):
            return [a > b if a is not None and b is not None else False 
                   for a, b in zip(self.data, other.data)]
        return False
    
    def __lt__(self, other):
        """Less than comparison"""
        if isinstance(other, (int, float)):
            return [x < other if x is not None else False for x in self.data]
        elif isinstance(other, IntColumn):
            return [a < b if a is not None and b is not None else False 
                   for a, b in zip(self.data, other.data)]
        return False


class FloatColumn(BaseColumn):
    """Float column with numeric operations"""
    
    def __init__(self, data: List[Union[float, None]], name: str = ""):
        super().__init__(data, name)
        self.dtype = "float"
    
    def sum(self) -> float:
        """Sum of all values"""
        if 'sum' not in self._cached_stats:
            self._cached_stats['sum'] = sum(x for x in self.data if x is not None)
        return self._cached_stats['sum']
    
    def mean(self) -> float:
        """Average of all values"""
        if 'mean' not in self._cached_stats:
            valid = [x for x in self.data if x is not None]
            self._cached_stats['mean'] = sum(valid) / len(valid) if valid else 0.0
        return self._cached_stats['mean']
    
    def min(self) -> float:
        """Minimum value"""
        valid = [x for x in self.data if x is not None]
        return min(valid) if valid else None
    
    def max(self) -> float:
        """Maximum value"""
        valid = [x for x in self.data if x is not None]
        return max(valid) if valid else None
    
    def median(self) -> float:
        """Median value"""
        valid = [x for x in self.data if x is not None]
        return statistics.median(valid) if valid else None
    
    def std(self) -> float:
        """Standard deviation"""
        valid = [x for x in self.data if x is not None]
        return statistics.stdev(valid) if len(valid) > 1 else 0.0
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return FloatColumn([x + other if x is not None else None for x in self.data], self.name)
        elif isinstance(other, (IntColumn, FloatColumn)):
            return FloatColumn([a + b if a is not None and b is not None else None 
                               for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot add FloatColumn and {type(other)}")
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return FloatColumn([x - other if x is not None else None for x in self.data], self.name)
        elif isinstance(other, (IntColumn, FloatColumn)):
            return FloatColumn([a - b if a is not None and b is not None else None 
                               for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot subtract {type(other)} from FloatColumn")
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return FloatColumn([x * other if x is not None else None for x in self.data], self.name)
        elif isinstance(other, (IntColumn, FloatColumn)):
            return FloatColumn([a * b if a is not None and b is not None else None 
                               for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot multiply FloatColumn and {type(other)}")
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return FloatColumn([x / other if x is not None and other != 0 else None for x in self.data], self.name)
        elif isinstance(other, (IntColumn, FloatColumn)):
            return FloatColumn([a / b if a is not None and b is not None and b != 0 else None 
                               for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot divide FloatColumn by {type(other)}")


class StringColumn(BaseColumn):
    """String column with text operations"""
    
    def __init__(self, data: List[Union[str, None]], name: str = ""):
        super().__init__(data, name)
        self.dtype = "string"
    
    def lower(self) -> 'StringColumn':
        """Convert all strings to lowercase"""
        return StringColumn([x.lower() if x else None for x in self.data], self.name)
    
    def upper(self) -> 'StringColumn':
        """Convert all strings to uppercase"""
        return StringColumn([x.upper() if x else None for x in self.data], self.name)
    
    def strip(self) -> 'StringColumn':
        """Strip whitespace from all strings"""
        return StringColumn([x.strip() if x else None for x in self.data], self.name)
    
    def contains(self, substring: str) -> List[bool]:
        """Check if each string contains substring"""
        return [substring in x if x else False for x in self.data]
    
    def startswith(self, prefix: str) -> List[bool]:
        """Check if each string starts with prefix"""
        return [x.startswith(prefix) if x else False for x in self.data]
    
    def endswith(self, suffix: str) -> List[bool]:
        """Check if each string ends with suffix"""
        return [x.endswith(suffix) if x else False for x in self.data]
    
    def replace(self, old: str, new: str) -> 'StringColumn':
        """Replace substring in all strings"""
        return StringColumn([x.replace(old, new) if x else None for x in self.data], self.name)
    
    def split(self, sep: str = None) -> List[List[str]]:
        """Split each string"""
        return [x.split(sep) if x else [] for x in self.data]
    
    def len(self) -> IntColumn:
        """Get length of each string"""
        return IntColumn([len(x) if x else 0 for x in self.data], f"{self.name}_len")
    
    def __eq__(self, other):
        if isinstance(other, str):
            return [x == other if x is not None else False for x in self.data]
        elif isinstance(other, StringColumn):
            return [a == b if a is not None and b is not None else False 
                   for a, b in zip(self.data, other.data)]
        return False


class DateColumn(BaseColumn):
    """Date column with datetime operations"""
    
    def __init__(self, data: List[Union[datetime, date, str, None]], name: str = ""):
        # Convert strings to datetime objects
        processed = []
        for val in data:
            if isinstance(val, str):
                try:
                    processed.append(datetime.fromisoformat(val))
                except:
                    processed.append(None)
            else:
                processed.append(val)
        super().__init__(processed, name)
        self.dtype = "date"
    
    def year(self) -> IntColumn:
        """Extract year from dates"""
        return IntColumn([x.year if x else None for x in self.data], f"{self.name}_year")
    
    def month(self) -> IntColumn:
        """Extract month from dates"""
        return IntColumn([x.month if x else None for x in self.data], f"{self.name}_month")
    
    def day(self) -> IntColumn:
        """Extract day from dates"""
        return IntColumn([x.day if x else None for x in self.data], f"{self.name}_day")
    
    def weekday(self) -> IntColumn:
        """Get weekday (0=Monday, 6=Sunday)"""
        return IntColumn([x.weekday() if x else None for x in self.data], f"{self.name}_weekday")
    
    def min(self) -> datetime:
        """Earliest date"""
        valid = [x for x in self.data if x is not None]
        return min(valid) if valid else None
    
    def max(self) -> datetime:
        """Latest date"""
        valid = [x for x in self.data if x is not None]
        return max(valid) if valid else None


class BoolColumn(BaseColumn):
    """Boolean column with logical operations"""
    
    def __init__(self, data: List[Union[bool, None]], name: str = ""):
        super().__init__(data, name)
        self.dtype = "bool"
    
    def sum(self) -> int:
        """Count True values"""
        return sum(1 for x in self.data if x)
    
    def all(self) -> bool:
        """Check if all values are True"""
        return all(x for x in self.data if x is not None)
    
    def any(self) -> bool:
        """Check if any value is True"""
        return any(x for x in self.data if x is not None)
    
    def __and__(self, other):
        """Logical AND"""
        if isinstance(other, BoolColumn):
            return BoolColumn([a and b if a is not None and b is not None else None 
                              for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot AND BoolColumn and {type(other)}")
    
    def __or__(self, other):
        """Logical OR"""
        if isinstance(other, BoolColumn):
            return BoolColumn([a or b if a is not None and b is not None else None 
                              for a, b in zip(self.data, other.data)], self.name)
        raise TypeError(f"Cannot OR BoolColumn and {type(other)}")
    
    def __invert__(self):
        """Logical NOT"""
        return BoolColumn([not x if x is not None else None for x in self.data], self.name)


def infer_column_type(data: List[Any], name: str = "") -> BaseColumn:
    """Automatically infer the best column type for the data"""
    if not data:
        return StringColumn([], name)
    
    # Sample first non-None value
    sample = next((x for x in data if x is not None), None)
    if sample is None:
        return StringColumn(data, name)
    
    # Check type
    if isinstance(sample, bool):
        return BoolColumn(data, name)
    elif isinstance(sample, int):
        return IntColumn(data, name)
    elif isinstance(sample, float):
        return FloatColumn(data, name)
    elif isinstance(sample, (datetime, date)):
        return DateColumn(data, name)
    else:
        return StringColumn(data, name)
