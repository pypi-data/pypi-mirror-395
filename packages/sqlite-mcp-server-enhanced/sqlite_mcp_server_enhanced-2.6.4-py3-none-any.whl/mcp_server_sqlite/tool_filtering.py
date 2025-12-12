"""Tool filtering for SQLite MCP Server.

Provides environment-based filtering to expose only a subset of tools,
useful for staying under tool limits (e.g., Windsurf's 100-tool limit).

Configuration via environment variable:
  SQLITE_MCP_TOOL_FILTER  Comma-separated filter rules processed left-to-right

Filter syntax:
  -group    Disable all tools in a group (e.g., -vector, -stats)
  -tool     Disable a specific tool (e.g., -write_query)
  +tool     Enable a specific tool (e.g., +read_query)

Examples:
  "-vector,-stats"                    Disable vector and stats groups
  "-admin,+vacuum_database"           Disable admin group but keep vacuum_database
  "-vector,-stats,+semantic_search"   Disable groups but re-enable one tool

If not set or empty, all tools are enabled (no filtering).

Available groups: core, fts, vector, json, virtual, spatial, text, stats, admin, misc

MCP Config:
    {
        "mcpServers": {
            "sqlite": {
                "command": "python",
                "args": ["-m", "mcp_server_sqlite", "--db-path", "~/my.db"],
                "env": {
                    "SQLITE_MCP_TOOL_FILTER": "-vector,-stats,-text,-virtual,-spatial"
                }
            }
        }
    }

"""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import mcp.types as types

logger = logging.getLogger("mcp_sqlite_server")

# Tool groups - each group maps to a set of tool names
TOOL_GROUPS: dict[str, set[str]] = {
    "core": {
        "read_query",
        "write_query",
        "create_table",
        "list_tables",
        "describe_table",
    },
    "fts": {
        "fts_search",
        "create_fts_table",
        "rebuild_fts_index",
        "hybrid_search",
    },
    "vector": {
        "semantic_search",
        "semantic_query",
        "setup_semantic_search",
        "create_embeddings_table",
        "store_embedding",
        "create_vector_index",
        "analyze_vector_index",
        "rebuild_vector_index",
        "optimize_vector_search",
        "batch_similarity_search",
        "calculate_similarity",
    },
    "json": {
        "json_query",
        "json_select",
        "json_insert",
        "json_update",
        "json_merge",
        "json_validate_path",
        "validate_json",
        "analyze_json_schema",
        "create_json_collection_table",
    },
    "virtual": {
        "create_csv_table",
        "create_enhanced_csv_table",
        "create_rtree_table",
        "create_series_table",
        "list_virtual_tables",
        "drop_virtual_table",
        "virtual_table_info",
        "analyze_csv_schema",
    },
    "spatial": {
        "load_spatialite",
        "create_spatial_table",
        "spatial_query",
        "spatial_analysis",
        "spatial_index",
        "geometry_operations",
        "import_shapefile",
    },
    "text": {
        "fuzzy_match",
        "phonetic_match",
        "regex_extract",
        "regex_replace",
        "text_normalize",
        "text_similarity",
        "text_validation",
    },
    "stats": {
        "descriptive_statistics",
        "correlation_analysis",
        "distribution_analysis",
        "hypothesis_testing",
        "outlier_detection",
        "percentile_analysis",
        "moving_averages",
        "regression_analysis",
    },
    "admin": {
        "vacuum_database",
        "optimize_database",
        "analyze_database",
        "integrity_check",
        "backup_database",
        "restore_database",
        "verify_backup",
        "database_stats",
        "index_usage_stats",
        "pragma_compile_options",
        "pragma_database_list",
        "pragma_optimize",
        "pragma_settings",
        "pragma_table_info",
    },
    "misc": {
        "append_insight",
        "summarize_table",
        "hybrid_search_workflow",
        "advanced_search",
        "test_jsonb_conversion",
    },
}

# All available tools (derived from groups)
ALL_TOOLS: set[str] = set().union(*TOOL_GROUPS.values())


@lru_cache(maxsize=1)
def get_included_tools() -> frozenset[str]:
    """Determine which tools to include based on SQLITE_MCP_TOOL_FILTER.

    Starts with all tools enabled, then processes filter rules left-to-right:
      -name   Disable group or tool
      +name   Enable tool (can restore after group disable)

    Returns:
        Frozen set of tool names to include. If env var not set, returns empty
        frozenset (meaning no filtering - all tools enabled).
    """
    filter_env = os.environ.get("SQLITE_MCP_TOOL_FILTER", "").strip()

    if not filter_env:
        logger.debug("SQLITE_MCP_TOOL_FILTER not set - all tools enabled")
        return frozenset()

    # Start with all tools
    result: set[str] = ALL_TOOLS.copy()
    rules = [r.strip() for r in filter_env.split(",") if r.strip()]

    for rule in rules:
        if rule.startswith("-"):
            name = rule[1:]
            if name in TOOL_GROUPS:
                removed = result & TOOL_GROUPS[name]
                result -= TOOL_GROUPS[name]
                if removed:
                    logger.info(f"Disabled group '{name}': -{len(removed)} tools")
            elif name in ALL_TOOLS:
                if name in result:
                    result.discard(name)
                    logger.info(f"Disabled tool '{name}'")
            else:
                logger.warning(f"Unknown group/tool ignored: '{name}'")
        elif rule.startswith("+"):
            name = rule[1:]
            if name in ALL_TOOLS:
                if name not in result:
                    result.add(name)
                    logger.info(f"Enabled tool '{name}'")
            else:
                logger.warning(f"Unknown tool ignored: '{name}'")
        else:
            logger.warning(f"Invalid filter rule (must start with + or -): '{rule}'")

    logger.info(f"Tool filtering active: {len(result)}/{len(ALL_TOOLS)} tools enabled")
    return frozenset(result)


def is_tool_enabled(name: str) -> bool:
    """Check if a tool is enabled.

    Args:
        name: Tool name to check.

    Returns:
        True if tool is enabled, False if disabled by filtering.
    """
    included = get_included_tools()
    # Empty set means no filtering (all enabled)
    if not included:
        return True
    return name in included


def filter_tools(tools: list["types.Tool"]) -> list["types.Tool"]:
    """Filter a list of tools based on environment configuration.

    Args:
        tools: List of MCP Tool objects to filter.

    Returns:
        Filtered list containing only enabled tools.
    """
    included = get_included_tools()
    # Empty set means no filtering
    if not included:
        return tools
    return [t for t in tools if t.name in included]


def clear_cache() -> None:
    """Clear the cached included tools. Useful for testing."""
    get_included_tools.cache_clear()


def get_available_groups() -> dict[str, set[str]]:
    """Return available tool groups for documentation/CLI purposes."""
    return TOOL_GROUPS.copy()


def get_all_tool_names() -> set[str]:
    """Return all known tool names."""
    return ALL_TOOLS.copy()
