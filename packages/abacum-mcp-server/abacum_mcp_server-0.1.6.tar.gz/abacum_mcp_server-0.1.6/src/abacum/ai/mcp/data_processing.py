"""
Data Processing and Analysis Functions
Handles data transformations, calculations, and analysis operations.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
from datetime import datetime


def calculate_variance_analysis(
        actuals_result: dict,
        scenario_result: dict,
        scenario_id: str,
        scenario_category: str,
        groupby: Optional[list[str]] = None
) -> dict:
    """
    Calculate variance analysis from actuals and scenario data.

    This function only handles data processing - no API calls.

    Args:
        actuals_result: Result dict from get_model_actuals API call
        scenario_result: Result dict from get_scenario_data or get_rolling_data API call
        scenario_id: The ID of the scenario
        scenario_category: The category of the scenario ('budget', 'forecast', 'rolling')
        groupby: Optional list of dimension columns to group by

    Returns:
        Dictionary with merged data, variance calculations, and summary statistics
    """
    # Check if inputs are valid
    if not actuals_result.get("success"):
        return actuals_result

    if not scenario_result.get("success"):
        return scenario_result

    # Reconstruct DataFrames from split format
    actuals_df = pd.DataFrame(**actuals_result["data"])
    scenario_df = pd.DataFrame(**scenario_result["data"])

    # Perform variance calculations
    result_df, summary, merge_info = _calculate_variance(
        actuals_df=actuals_df,
        scenario_df=scenario_df,
        scenario_id=scenario_id,
        scenario_category=scenario_category,
        groupby=groupby
    )

    # Determine if data was cached (both must be cached for overall cache=True)
    cached = actuals_result.get("cached", False) and scenario_result.get("cached", False)

    return {
        "success": True,
        "model_id": actuals_result.get("model_id"),
        "scenario_id": scenario_id,
        "data": result_df.to_dict(orient='split'),
        "summary": summary,
        "metadata": {
            "actuals_metadata": actuals_result.get("metadata"),
            "scenario_metadata": scenario_result.get("metadata"),
            "merge_keys": merge_info["common_dimensions"],
            "dimension_handling": merge_info,
            "groupby": groupby
        },
        "timestamp": datetime.now().isoformat(),
        "cached": cached
    }


def _calculate_variance(
        actuals_df: pd.DataFrame,
        scenario_df: pd.DataFrame,
        scenario_id: str,
        scenario_category: str,
        groupby: Optional[list[str]] = None
) -> tuple[pd.DataFrame, Dict[str, Any], Dict[str, Any]]:
    """
    Calculate variance between actuals and scenario data with intelligent schema handling.

    Args:
        actuals_df: DataFrame with actuals data
        scenario_df: DataFrame with scenario data
        scenario_id: The scenario ID for metadata
        scenario_category: The scenario category for metadata
        groupby: Optional list of dimension columns to group by

    Returns:
        Tuple of (result_df, summary_dict, merge_info_dict)
    """
    # Identify dimension columns (all columns except 'value')
    value_col = 'value'

    if value_col not in actuals_df.columns or value_col not in scenario_df.columns:
        raise ValueError("Expected 'value' column not found in data")

    # Get dimension columns (all columns except 'value')
    actuals_dims = [col for col in actuals_df.columns if col != value_col]
    scenario_dims = [col for col in scenario_df.columns if col != value_col]

    # Find common dimensions for merging
    common_dims = list(set(actuals_dims) & set(scenario_dims))
    actuals_extra_dims = [col for col in actuals_dims if col not in common_dims]
    scenario_extra_dims = [col for col in scenario_dims if col not in common_dims]

    # Prepare dataframes for merge by aggregating extra dimensions
    if actuals_extra_dims:
        # Aggregate actuals data by summing over extra dimensions
        actuals_agg = actuals_df.groupby(common_dims, as_index=False, dropna=False)[value_col].sum()
    else:
        actuals_agg = actuals_df.copy()

    if scenario_extra_dims:
        # Aggregate scenario data by summing over extra dimensions
        scenario_agg = scenario_df.groupby(common_dims, as_index=False, dropna=False)[value_col].sum()
    else:
        scenario_agg = scenario_df.copy()

    # Fill NaN values with 0 before merge
    actuals_agg[value_col] = actuals_agg[value_col].fillna(0)
    scenario_agg[value_col] = scenario_agg[value_col].fillna(0)

    # Merge on common dimensions
    merged_df = pd.merge(
        actuals_agg,
        scenario_agg,
        on=common_dims,
        how='outer',
        suffixes=('_actual', '_baseline')
    )

    # Log dimension handling for debugging
    merge_info = {
        "common_dimensions": common_dims,
        "actuals_extra_dimensions": actuals_extra_dims,
        "scenario_extra_dimensions": scenario_extra_dims,
        "aggregation_performed": bool(actuals_extra_dims or scenario_extra_dims)
    }

    # Fill any remaining NaN values with 0 after merge
    merged_df['value_actual'] = merged_df['value_actual'].fillna(0)
    merged_df['value_baseline'] = merged_df['value_baseline'].fillna(0)

    # Calculate variance metrics
    merged_df['variance_abs'] = merged_df['value_actual'] - merged_df['value_baseline']

    # Calculate percentage variance, handling division by zero
    # Replace 0 in baseline with NaN to avoid division by zero, then fill result with 0
    baseline_safe = merged_df['value_baseline'].replace(0, np.nan)
    merged_df['variance_pct'] = (merged_df['variance_abs'] / baseline_safe * 100).fillna(0)

    # Apply groupby if specified
    if groupby:
        # Validate groupby columns exist in merged data
        invalid_cols = [col for col in groupby if col not in merged_df.columns]
        if invalid_cols:
            # Check if columns were removed during dimension aggregation
            aggregated_cols = actuals_extra_dims + scenario_extra_dims
            lost_cols = [col for col in invalid_cols if col in aggregated_cols]
            if lost_cols:
                raise ValueError(
                    f"Groupby columns {lost_cols} were aggregated away due to schema mismatch. "
                    f"Available dimensions: {common_dims}"
                )
            else:
                raise ValueError(f"Invalid groupby columns: {invalid_cols}")

        # Aggregate by groupby columns
        agg_dict = {
            'value_actual': 'sum',
            'value_baseline': 'sum',
            'variance_abs': 'sum'
        }

        grouped_df = merged_df.groupby(groupby, dropna=False).agg(agg_dict).reset_index()

        # Recalculate variance_pct after aggregation
        baseline_safe = grouped_df['value_baseline'].replace(0, np.nan)
        grouped_df['variance_pct'] = (grouped_df['variance_abs'] / baseline_safe * 100).fillna(0)

        result_df = grouped_df
    else:
        result_df = merged_df

    # Calculate summary statistics
    summary = {
        "total_actual": float(merged_df['value_actual'].sum()),
        "total_baseline": float(merged_df['value_baseline'].sum()),
        "total_variance_abs": float(merged_df['variance_abs'].sum()),
        "scenario_id": scenario_id,
        "scenario_category": scenario_category
    }

    # Calculate total variance percentage
    if summary["total_baseline"] != 0:
        summary["total_variance_pct"] = (summary["total_variance_abs"] / summary["total_baseline"]) * 100
    else:
        summary["total_variance_pct"] = 0.0

    return result_df, summary, merge_info

