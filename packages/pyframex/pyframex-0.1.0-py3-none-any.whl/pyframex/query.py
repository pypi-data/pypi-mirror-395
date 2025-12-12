"""
Query Planner - SQL Engine for PyFrameX
=======================================

Lightweight SQL parser and query executor that converts
SQL statements into Frame operations.
"""

import re
from typing import Dict, List, Any, Optional, Tuple


class QueryPlanner:
    """
    SQL query planner and executor
    
    Supports:
    - SELECT with columns or aggregations
    - WHERE conditions
    - GROUP BY
    - ORDER BY
    - LIMIT
    """
    
    def __init__(self):
        self.keywords = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'LIMIT', 'HAVING']
    
    def execute(self, query: str, frame: 'Frame') -> 'Frame':
        """
        Execute SQL query on Frame
        
        Example:
            SELECT region, SUM(revenue) FROM df WHERE year = 2024 GROUP BY region
        """
        # Parse query
        parsed = self._parse_query(query)
        
        # Start with original frame
        result = frame
        
        # Apply WHERE filter
        if parsed['where']:
            result = result.filter(parsed['where'])
        
        # Apply GROUP BY
        if parsed['group_by']:
            result = self._apply_groupby(result, parsed)
        else:
            # Apply SELECT without grouping
            result = self._apply_select(result, parsed)
        
        # Apply ORDER BY
        if parsed['order_by']:
            col, direction = parsed['order_by']
            result = result.sort(col, ascending=(direction == 'ASC'))
        
        # Apply LIMIT
        if parsed['limit']:
            result = result.head(parsed['limit'])
        
        return result
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """Parse SQL query into components"""
        query = query.strip()
        
        # Initialize result
        parsed = {
            'select': [],
            'from': None,
            'where': None,
            'group_by': [],
            'order_by': None,
            'limit': None
        }
        
        # Extract SELECT clause
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', query, re.IGNORECASE)
        if select_match:
            select_str = select_match.group(1)
            parsed['select'] = [col.strip() for col in select_str.split(',')]
        
        # Extract FROM clause
        from_match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
        if from_match:
            parsed['from'] = from_match.group(1)
        
        # Extract WHERE clause
        where_match = re.search(r'WHERE\s+(.*?)(?:GROUP BY|ORDER BY|LIMIT|$)', query, re.IGNORECASE)
        if where_match:
            where_str = where_match.group(1).strip()
            parsed['where'] = self._convert_sql_condition(where_str)
        
        # Extract GROUP BY clause
        group_match = re.search(r'GROUP BY\s+(.*?)(?:ORDER BY|LIMIT|$)', query, re.IGNORECASE)
        if group_match:
            group_str = group_match.group(1).strip()
            parsed['group_by'] = [col.strip() for col in group_str.split(',')]
        
        # Extract ORDER BY clause
        order_match = re.search(r'ORDER BY\s+(\w+)\s*(ASC|DESC)?', query, re.IGNORECASE)
        if order_match:
            col = order_match.group(1)
            direction = order_match.group(2).upper() if order_match.group(2) else 'ASC'
            parsed['order_by'] = (col, direction)
        
        # Extract LIMIT clause
        limit_match = re.search(r'LIMIT\s+(\d+)', query, re.IGNORECASE)
        if limit_match:
            parsed['limit'] = int(limit_match.group(1))
        
        return parsed
    
    def _convert_sql_condition(self, sql_condition: str) -> str:
        """
        Convert SQL WHERE condition to Python expression
        
        Examples:
            region = 'west' -> region == 'west'
            quantity > 100 -> quantity > 100
        """
        # Replace single = with ==
        condition = re.sub(r'\b(\w+)\s*=\s*', r'\1 == ', sql_condition)
        
        # Replace SQL AND/OR with Python and/or
        condition = re.sub(r'\bAND\b', 'and', condition, flags=re.IGNORECASE)
        condition = re.sub(r'\bOR\b', 'or', condition, flags=re.IGNORECASE)
        
        return condition
    
    def _apply_select(self, frame: 'Frame', parsed: Dict) -> 'Frame':
        """Apply SELECT clause without GROUP BY"""
        from .frame import Frame
        
        if not parsed['select'] or parsed['select'] == ['*']:
            return frame
        
        result_data = {}
        
        for expr in parsed['select']:
            expr = expr.strip()
            
            # Check if it's an aggregation function
            agg_match = re.match(r'(\w+)\s*\(\s*(\w+)\s*\)', expr, re.IGNORECASE)
            
            if agg_match:
                func_name = agg_match.group(1).upper()
                col_name = agg_match.group(2)
                
                if col_name not in frame.columns:
                    raise ValueError(f"Column '{col_name}' not found")
                
                col = frame.columns[col_name]
                
                # Calculate aggregation
                if func_name == 'SUM':
                    result_data[f"SUM_{col_name}"] = [col.sum()]
                elif func_name == 'AVG' or func_name == 'MEAN':
                    result_data[f"AVG_{col_name}"] = [col.mean()]
                elif func_name == 'COUNT':
                    result_data[f"COUNT_{col_name}"] = [len(col)]
                elif func_name == 'MIN':
                    result_data[f"MIN_{col_name}"] = [col.min()]
                elif func_name == 'MAX':
                    result_data[f"MAX_{col_name}"] = [col.max()]
                else:
                    raise ValueError(f"Unknown aggregation function: {func_name}")
            else:
                # Simple column selection
                if expr not in frame.columns:
                    raise ValueError(f"Column '{expr}' not found")
                result_data[expr] = frame.columns[expr].data
        
        return Frame(result_data)
    
    def _apply_groupby(self, frame: 'Frame', parsed: Dict) -> 'Frame':
        """Apply SELECT with GROUP BY"""
        group_cols = parsed['group_by']
        
        # Separate aggregations from group columns
        aggregations = {}
        
        for expr in parsed['select']:
            expr = expr.strip()
            
            # Check if it's an aggregation
            agg_match = re.match(r'(\w+)\s*\(\s*(\w+)\s*\)', expr, re.IGNORECASE)
            
            if agg_match:
                func_name = agg_match.group(1).lower()
                col_name = agg_match.group(2)
                aggregations[col_name] = func_name
        
        # Perform groupby
        grouped = frame.groupby(group_cols)
        return grouped.agg(aggregations)
    
    def explain(self, query: str) -> str:
        """
        Explain query execution plan
        
        Example:
            >>> planner.explain("SELECT * FROM df WHERE sales > 100")
        """
        parsed = self._parse_query(query)
        
        lines = []
        lines.append("Query Execution Plan:")
        lines.append("=" * 50)
        
        lines.append(f"1. SCAN Frame ({parsed['from']})")
        
        step = 2
        if parsed['where']:
            lines.append(f"{step}. FILTER: {parsed['where']}")
            step += 1
        
        if parsed['group_by']:
            lines.append(f"{step}. GROUP BY: {', '.join(parsed['group_by'])}")
            step += 1
            lines.append(f"{step}. AGGREGATE: {', '.join(parsed['select'])}")
            step += 1
        else:
            lines.append(f"{step}. SELECT: {', '.join(parsed['select'])}")
            step += 1
        
        if parsed['order_by']:
            col, direction = parsed['order_by']
            lines.append(f"{step}. ORDER BY: {col} {direction}")
            step += 1
        
        if parsed['limit']:
            lines.append(f"{step}. LIMIT: {parsed['limit']}")
        
        return "\n".join(lines)


class ExpressionOptimizer:
    """
    Optimize column expressions and operations
    
    Features:
    - Constant folding
    - Dead code elimination
    - Filter pushdown
    - Column pruning
    """
    
    def __init__(self):
        self.optimizations = []
    
    def optimize_filter(self, condition: str) -> str:
        """Optimize filter conditions"""
        # Remove redundant conditions
        condition = re.sub(r'\(True\s+and\s+(.+?)\)', r'\1', condition)
        condition = re.sub(r'\((.+?)\s+and\s+True\)', r'\1', condition)
        
        # Simplify comparisons
        condition = re.sub(r'(\w+)\s+==\s+\1', 'True', condition)
        
        return condition
    
    def can_pushdown(self, condition: str, available_cols: List[str]) -> bool:
        """Check if filter can be pushed down"""
        # Extract column names from condition
        cols_in_condition = re.findall(r'\b([a-zA-Z_]\w*)\b', condition)
        return all(col in available_cols for col in cols_in_condition)
    
    def estimate_selectivity(self, condition: str) -> float:
        """Estimate filter selectivity (0.0 to 1.0)"""
        # Simple heuristic-based estimation
        if '==' in condition:
            return 0.1  # Equality is selective
        elif '>' in condition or '<' in condition:
            return 0.5  # Range queries
        else:
            return 0.8  # Conservative estimate
    
    def choose_join_order(self, tables: List[str], sizes: Dict[str, int]) -> List[str]:
        """Choose optimal join order (smallest table first)"""
        return sorted(tables, key=lambda t: sizes.get(t, float('inf')))


class QueryCache:
    """Cache query results for performance"""
    
    def __init__(self, max_size: int = 100):
        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, query: str) -> Optional[Any]:
        """Get cached result"""
        if query in self.cache:
            self.hits += 1
            return self.cache[query]
        self.misses += 1
        return None
    
    def put(self, query: str, result: Any):
        """Cache result"""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (simple FIFO)
            self.cache.pop(next(iter(self.cache)))
        self.cache[query] = result
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.cache)
        }
