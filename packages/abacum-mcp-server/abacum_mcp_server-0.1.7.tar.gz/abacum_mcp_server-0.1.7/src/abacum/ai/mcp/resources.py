"""
MCP Resource Definitions
Resources are loaded at startup and cached for immediate access.
"""

from . import api
import json
from typing import Optional, Dict
# Cache for resource data - loaded at startup
_resource_cache: Dict[str, Optional[str]] = {
    "models": None,
    "scenarios": None,
    "variables": None
}


async def load_all_resources():
    """
    Load all resources at startup and cache them.
    Returns True if all resources loaded successfully, False otherwise.
    """
    all_success = True

    # Load models
    try:
        models_result = await api.list_models()
        _resource_cache["models"] = json.dumps(models_result, indent=2)
    except Exception as e:
        _resource_cache["models"] = json.dumps({"success": False, "error": str(e)}, indent=2)
        all_success = False

    # Load scenarios
    try:
        scenarios_result = await api.list_scenarios()
        _resource_cache["scenarios"] = json.dumps(scenarios_result, indent=2)
    except Exception as e:
        _resource_cache["scenarios"] = json.dumps({"success": False, "error": str(e)}, indent=2)
        all_success = False

    # Load variables
    try:
        variables_result = await api.list_variables(model_id=None)
        _resource_cache["variables"] = json.dumps(variables_result, indent=2)
    except Exception as e:
        _resource_cache["variables"] = json.dumps({"success": False, "error": str(e)}, indent=2)
        all_success = False

    return all_success
async def get_models_resource() -> str:
    """
    Returns cached list of all Abacum models.
    Data is loaded at server startup for immediate access.
    """
    if _resource_cache["models"] is None:
        return json.dumps({"success": False, "error": "Resources not loaded yet"}, indent=2)
    return _resource_cache["models"]


async def get_scenarios_resource() -> str:
    """
    Returns cached list of all Abacum scenarios.
    Data is loaded at server startup for immediate access.
    """
    if _resource_cache["scenarios"] is None:
        return json.dumps({"success": False, "error": "Resources not loaded yet"}, indent=2)
    return _resource_cache["scenarios"]


async def get_variables_resource() -> str:
    """
    Returns cached list of all Abacum variables.
    Data is loaded at server startup for immediate access.
    """
    if _resource_cache["variables"] is None:
        return json.dumps({"success": False, "error": "Resources not loaded yet"}, indent=2)
    return _resource_cache["variables"]

