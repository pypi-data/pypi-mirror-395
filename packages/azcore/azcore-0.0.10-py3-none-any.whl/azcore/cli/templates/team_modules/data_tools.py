 """Data analysis and processing tools."""

import json
import csv
from typing import Dict, Any, List
from langchain_core.tools import tool
import io
from .utils import load_prompt


@tool
def analyze_csv_data(csv_content: str) -> Dict[str, Any]:
    """Analyze CSV data and provide statistics.

    Args:
        csv_content: CSV content as string

    Returns:
        Dict containing data analysis results
    """
    try:
        reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(reader)
        
        if not rows:
            return {"status": "error", "message": "No data found"}
        
        return {
            "status": "success",
            "row_count": len(rows),
            "columns": list(rows[0].keys()) if rows else [],
            "sample_data": rows[:3],
            "message": f"Analyzed {len(rows)} rows"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def convert_json_to_csv(json_data: str) -> str:
    """Convert JSON data to CSV format.

    Args:
        json_data: JSON string containing array of objects

    Returns:
        CSV formatted string
    """
    try:
        data = json.loads(json_data)
        if not isinstance(data, list) or not data:
            return "Error: JSON must be an array of objects"
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        return output.getvalue()
    except Exception as e:
        return f"Error converting JSON to CSV: {str(e)}"


@tool
def filter_data(json_data: str, field: str, value: str) -> List[Dict[str, Any]]:
    """Filter JSON data by field and value.

    Args:
        json_data: JSON string containing array of objects
        field: Field name to filter by
        value: Value to match

    Returns:
        List of filtered objects
    """
    try:
        data = json.loads(json_data)
        if not isinstance(data, list):
            return []
        
        filtered = [item for item in data if str(item.get(field)) == value]
        return filtered
    except Exception as e:
        return []


@tool
def calculate_statistics(numbers: str) -> Dict[str, float]:
    """Calculate basic statistics for a list of numbers.

    Args:
        numbers: Comma-separated list of numbers

    Returns:
        Dict with statistical measures
    """
    try:
        nums = [float(n.strip()) for n in numbers.split(',')]
        
        if not nums:
            return {"error": "No valid numbers provided"}
        
        nums_sorted = sorted(nums)
        n = len(nums)
        
        return {
            "count": n,
            "sum": sum(nums),
            "mean": sum(nums) / n,
            "min": min(nums),
            "max": max(nums),
            "median": nums_sorted[n // 2] if n % 2 == 1 else (nums_sorted[n // 2 - 1] + nums_sorted[n // 2]) / 2,
            "range": max(nums) - min(nums)
        }
    except Exception as e:
        return {"error": str(e)}


@tool
def aggregate_data(json_data: str, group_by: str, aggregate_field: str, operation: str = "sum") -> Dict[str, Any]:
    """Aggregate data by grouping and performing operations.

    Args:
        json_data: JSON string containing array of objects
        group_by: Field to group by
        aggregate_field: Field to aggregate
        operation: Operation to perform (sum, avg, count, min, max)

    Returns:
        Dict with aggregated results
    """
    try:
        data = json.loads(json_data)
        if not isinstance(data, list):
            return {"error": "Invalid data format"}
        
        groups = {}
        for item in data:
            key = str(item.get(group_by, "unknown"))
            if key not in groups:
                groups[key] = []
            
            if operation in ["sum", "avg", "min", "max"]:
                try:
                    groups[key].append(float(item.get(aggregate_field, 0)))
                except (ValueError, TypeError):
                    pass
            else:
                groups[key].append(item)
        
        results = {}
        for key, values in groups.items():
            if operation == "sum":
                results[key] = sum(values)
            elif operation == "avg":
                results[key] = sum(values) / len(values) if values else 0
            elif operation == "count":
                results[key] = len(values)
            elif operation == "min":
                results[key] = min(values) if values else None
            elif operation == "max":
                results[key] = max(values) if values else None
        
        return {"status": "success", "results": results}
    except Exception as e:
        return {"error": str(e)}


# Export tools list
data_tools = [
    analyze_csv_data,
    convert_json_to_csv,
    filter_data,
    calculate_statistics,
    aggregate_data
]

# Team configuration
data_team_config = {
    "name": "data_team",
    "prompt": load_prompt("data_team"),
    "description": "Data analysis and processing with statistical capabilities",
    "rl_config": {
        "q_table_path": "rl_data/data_q_table.pkl",
        "exploration_rate": 0.1,
        "use_embeddings": False,
        "success_reward": 1.0,
        "failure_reward": -0.5,
        "empty_penalty": -0.5,
    }
}
