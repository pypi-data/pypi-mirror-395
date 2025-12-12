"""
MCP Tool Definitions
Wraps API functions with @mcp.tool()
"""
import json
from typing import Optional
from .server import mcp
from . import api
from . import resources
from . import data_processing
from .validators import JsonStringList


async def _call_api_safely(api_func, *args, **kwargs):
    """Wrapper to catch ApiErrors and return them as dicts."""
    try:
        return await api_func(*args, **kwargs)
    except api.ApiError as e:
        return e.to_dict()
    except Exception as e:
        return {
            "error": "An unexpected error occurred",
            "details": str(e)
        }


@mcp.tool()
async def get_abacum_model_actuals(
    model_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    variable_ids: JsonStringList = None
) -> dict:
    """
    Get actuals data for a specific Abacum model.

    CRITICAL: ALWAYS call discover_financial_models first to get valid
    model_id values. Do NOT assume model IDs from past conversations.

    PERFORMANCE OPTIMIZATION:
    - For profitability/performance reviews: Use last 3 months only (e.g., if today is Dec 2025, use start_date="2025-09", end_date="2025-11")
    - For trend analysis: Use last 6-12 months
    - Only request full history when explicitly asked by user

    Default to MINIMAL date ranges unless user specifies otherwise.

    Args:
        model_id: The ID of the model to retrieve actuals for
        start_date: Start date in YYYY-MM format. DEFAULT TO 3 MONTHS AGO unless user needs more history.
        end_date: End date in YYYY-MM format. DEFAULT TO LAST CLOSED MONTH.
        variable_ids: Optional list of variable IDs to filter the data

    Returns:
        Dictionary containing:
        - data: DataFrame in 'split' format (use pd.DataFrame(**data) to reconstruct)
        - metadata: Schema information about the data structure
        - cached: Boolean indicating whether data was served from cache
    """
    return await _call_api_safely(
        api.get_model_actuals,
        model_id=model_id, start_date=start_date, end_date=end_date, variable_ids=variable_ids
    )

@mcp.tool()
async def get_abacum_scenario_data(
    model_id: str,
    scenario_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    variable_ids: JsonStringList = None
) -> dict:
    """
    Get scenario data for a specific Abacum model and scenario.

    CRITICAL: ALWAYS call discover_financial_models first to get valid
    model_id values. Do NOT assume model IDs from past conversations.

    PERFORMANCE OPTIMIZATION:
    - For profitability/performance reviews: Use last 3 months only (e.g., if today is Dec 2025, use start_date="2025-09", end_date="2025-11")
    - For trend analysis: Use last 6-12 months
    - Only request full history when explicitly asked by user

    Default to MINIMAL date ranges unless user specifies otherwise.

    Args:
        model_id: The ID of the model to retrieve actuals for
        scenario_id: The ID of the scenario to retrieve data for
        start_date: Start date in YYYY-MM format. DEFAULT TO 3 MONTHS AGO unless user needs more history.
        end_date: End date in YYYY-MM format. DEFAULT TO LAST CLOSED MONTH.
        variable_ids: Optional list of variable IDs to filter the data

    Returns:
        Dictionary containing:
        - data: DataFrame in 'split' format (use pd.DataFrame(**data) to reconstruct)
        - metadata: Schema information about the data structure
        - cached: Boolean indicating whether data was served from cache
    """
    return await _call_api_safely(
        api.get_scenario_data,
        model_id=model_id, scenario_id=scenario_id,
        start_date=start_date, end_date=end_date, variable_ids=variable_ids
    )


@mcp.tool()
async def get_abacum_rolling_data(
    model_id: str,
    scenario_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    variable_ids: JsonStringList = None
) -> dict:
    """
    Get rolling forecast data for a specific Abacum model and scenario.

    CRITICAL: ALWAYS call discover_financial_models first to get valid
    model_id values. Do NOT assume model IDs from past conversations.

    PERFORMANCE OPTIMIZATION:
    - For profitability/performance reviews: Use last 3 months only (e.g., if today is Dec 2025, use start_date="2025-09", end_date="2025-11")
    - For trend analysis: Use last 6-12 months
    - Only request full history when explicitly asked by user

    Default to MINIMAL date ranges unless user specifies otherwise.

    Args:
        model_id: The ID of the model to retrieve rolling data for
        scenario_id: The ID of the scenario to retrieve data for
        start_date: Start date in YYYY-MM format. DEFAULT TO 3 MONTHS AGO unless user needs more history.
        end_date: End date in YYYY-MM format. DEFAULT TO LAST CLOSED MONTH.
        variable_ids: Optional list of variable IDs to filter the data

    Returns:
        Dictionary containing:
        - data: DataFrame in 'split' format (use pd.DataFrame(**data) to reconstruct)
        - metadata: Schema information about the data structure
        - cached: Boolean indicating whether data was served from cache
    """
    return await _call_api_safely(
        api.get_rolling_data,
        model_id=model_id, scenario_id=scenario_id,
        start_date=start_date, end_date=end_date,
        variable_ids=variable_ids
    )


@mcp.tool()
async def discover_financial_models(invalidate_cache: bool = False) -> dict:
    """
    Discover all available Abacum financial models, scenarios, and variables.

    This tool provides access to the resource data that would normally be loaded
    at startup. Use this to explore what models, scenarios, and variables are
    available in your Abacum instance.

    Args:
        invalidate_cache: Ignore the cached resource data and force a reload. Use this if
        resources were updated after server startup.

    Returns:
        Dictionary containing:
        - models: List of all financial models with their IDs and metadata
        - scenarios: List of all scenarios with their IDs and metadata
        - variables: List of all variables available across models
        - success: Boolean indicating if data was loaded successfully
    """
    try:
        # If invalidate_cache is True, reload all resources
        if invalidate_cache:
            await resources.load_all_resources()

        # Get cached resource data
        models_str = await resources.get_models_resource()
        scenarios_str = await resources.get_scenarios_resource()
        variables_str = await resources.get_variables_resource()

        # Parse JSON strings back to dicts
        models = json.loads(models_str)
        scenarios = json.loads(scenarios_str)
        variables = json.loads(variables_str)

        # Check if any resource failed to load
        if (isinstance(models, dict) and not models.get("success")) or \
           (isinstance(scenarios, dict) and not scenarios.get("success")) or \
           (isinstance(variables, dict) and not variables.get("success")):
            return {
                "success": False,
                "error": "Resources not loaded or failed to load",
                "models": models,
                "scenarios": scenarios,
                "variables": variables
            }

        return {
            "success": True,
            "models": models,
            "scenarios": scenarios,
            "variables": variables
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve resources: {str(e)}"
        }


@mcp.tool()
async def get_variance_analysis(
    model_id: str,
    scenario_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    variable_ids: JsonStringList = None,
    groupby: JsonStringList = None
) -> dict:
    """
    Compare actuals vs budget/forecast with automatic variance calculations.

    Use this tool for board prep, profitability reviews, and forecast accuracy analysis.
    Returns actual values, baseline (budget/forecast), variance_abs, and variance_pct.

    CRITICAL: ALWAYS call discover_financial_models first to get valid model_id
    and scenario_id values. Do NOT assume IDs from past conversations.

    PERFORMANCE OPTIMIZATION:
    - For profitability/performance reviews: Use last 3 months only (e.g., if today is Dec 2025, use start_date="2025-09", end_date="2025-11")
    - For trend analysis: Use last 6-12 months
    - Only request full history when explicitly asked by user

    Default to MINIMAL date ranges unless user specifies otherwise.

    Args:
        model_id: The ID of the model to analyze
        scenario_id: The ID of the scenario to compare against (UUID)
        start_date: Start date in YYYY-MM format. DEFAULT TO 3 MONTHS AGO unless user needs more history.
        end_date: End date in YYYY-MM format. DEFAULT TO LAST CLOSED MONTH.
        variable_ids: Optional list of variable IDs to filter the analysis
        groupby: Optional list of dimension columns to group by (e.g., ["department"], ["region", "product_line"])

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the analysis completed successfully
        - data: DataFrame in 'split' format with columns: value_actual, value_baseline, variance_abs, variance_pct
        - summary: Aggregated totals and variance metrics
        - metadata: Schema information about the data structure
        - cached: Boolean indicating whether data was served from cache
    """
    try:
        # Step 1: Get scenario metadata to determine category and name
        scenarios_str = await resources.get_scenarios_resource()
        scenarios_data = json.loads(scenarios_str)

        if not scenarios_data.get("success"):
            return {
                "success": False,
                "error": "Failed to load scenarios metadata. Call discover_financial_models first."
            }

        # Find the scenario to get its version_category and name
        scenario_category = None
        scenario_name = None
        version_name = None
        for scenario in scenarios_data.get("scenarios", []):
            if scenario.get("id") == scenario_id:
                scenario_category = scenario.get("version_category", "Forecast")
                scenario_name = scenario.get("scenario_name", "Unknown")
                version_name = scenario.get("version_name", "Unknown")
                break

        if scenario_category is None or scenario_name is None:
            return {
                "success": False,
                "error": f"Scenario ID '{scenario_id}' not found. Call discover_financial_models to get valid scenario IDs."
            }

        # Step 2: Fetch actuals data using API
        actuals_result = await api.get_model_actuals(
            model_id=model_id,
            start_date=start_date,
            end_date=end_date,
            variable_ids=variable_ids
        )

        if not actuals_result.get("success"):
            return actuals_result

        # Step 3: Fetch scenario data - only use scenario_data API since there's no rolling endpoint needed
        # Both Budget and Forecast data comes from the same API endpoint
        scenario_result = await api.get_scenario_data(
            model_id=model_id,
            scenario_id=scenario_id,
            start_date=start_date,
            end_date=end_date,
            variable_ids=variable_ids
        )

        if not scenario_result.get("success"):
            return scenario_result

        # Step 4: Process the data to calculate variances
        result = data_processing.calculate_variance_analysis(
            actuals_result=actuals_result,
            scenario_result=scenario_result,
            scenario_id=scenario_id,
            scenario_category=scenario_category,
            groupby=groupby
        )

        # Add scenario information to summary if successful
        if isinstance(result, dict) and result.get("success") and "summary" in result:
            result["summary"]["scenario_name"] = scenario_name
            result["summary"]["version_name"] = version_name
            result["summary"]["version_category"] = scenario_category

        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to perform variance analysis: {str(e)}"
        }
