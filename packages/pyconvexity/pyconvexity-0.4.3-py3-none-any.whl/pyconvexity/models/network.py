"""
Network management operations for PyConvexity.

Provides operations for creating, managing, and querying energy system networks
including time periods, carriers, and network configuration.
"""

import sqlite3
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from pyconvexity.core.types import CreateNetworkRequest, TimePeriod, Network
from pyconvexity.core.errors import ValidationError, DatabaseError

logger = logging.getLogger(__name__)


def create_network(conn: sqlite3.Connection, request: CreateNetworkRequest) -> None:
    """
    Create network metadata and time periods (single network per database).

    Args:
        conn: Database connection
        request: Network creation request

    Raises:
        ValidationError: If required fields are missing
        DatabaseError: If creation fails
    """

    # Validate required fields
    if not request.start_time:
        raise ValidationError("start_time is required")
    if not request.end_time:
        raise ValidationError("end_time is required")

    time_resolution = request.time_resolution or "PT1H"

    # Insert into network_metadata table (single row per database)
    conn.execute(
        """
        INSERT INTO network_metadata (name, description, time_start, time_end, time_interval, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    """,
        (
            request.name,
            request.description
            or f"Created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            request.start_time,
            request.end_time,
            time_resolution,
        ),
    )

    # Automatically create time periods from the request parameters
    _create_time_periods_from_request(conn, request.start_time, request.end_time, time_resolution)


def _create_time_periods_from_request(
    conn: sqlite3.Connection,
    start_time: str,
    end_time: str,
    time_resolution: str,
) -> None:
    """
    Create time periods from network request parameters.

    Args:
        conn: Database connection
        start_time: Start time string (YYYY-MM-DD HH:MM:SS)
        end_time: End time string (YYYY-MM-DD HH:MM:SS)
        time_resolution: ISO 8601 duration (PT1H, PT30M, PT2H, etc.)
    """
    # Parse start and end times
    start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    # Parse time resolution to seconds
    interval_seconds = _parse_iso8601_duration_to_seconds(time_resolution)

    # Calculate period count (inclusive of both start and end)
    total_seconds = int((end_dt - start_dt).total_seconds())
    period_count = (total_seconds // interval_seconds) + 1

    # Get Unix timestamp for start
    start_timestamp = int(start_dt.timestamp())

    # Insert time periods
    conn.execute(
        """
        INSERT INTO network_time_periods (period_count, start_timestamp, interval_seconds)
        VALUES (?, ?, ?)
        """,
        (period_count, start_timestamp, interval_seconds),
    )


def _parse_iso8601_duration_to_seconds(duration: str) -> int:
    """
    Parse ISO 8601 duration string to seconds.

    Supports: PT1H (1 hour), PT30M (30 minutes), PT2H (2 hours), PT15M (15 minutes), etc.

    Args:
        duration: ISO 8601 duration string

    Returns:
        Duration in seconds

    Raises:
        ValidationError: If duration format is invalid
    """
    if not duration.startswith("PT"):
        raise ValidationError(f"Invalid ISO 8601 duration format: {duration}. Must start with 'PT'")

    remaining = duration[2:]  # Remove 'PT' prefix
    total_seconds = 0

    # Parse hours
    if "H" in remaining:
        parts = remaining.split("H")
        hours = int(parts[0]) if parts[0] else 0
        total_seconds += hours * 3600
        remaining = parts[1] if len(parts) > 1 else ""

    # Parse minutes
    if "M" in remaining:
        parts = remaining.split("M")
        minutes = int(parts[0]) if parts[0] else 0
        total_seconds += minutes * 60
        remaining = parts[1] if len(parts) > 1 else ""

    # Parse seconds
    if "S" in remaining:
        parts = remaining.split("S")
        seconds = int(parts[0]) if parts[0] else 0
        total_seconds += seconds

    if total_seconds == 0:
        raise ValidationError(f"Invalid ISO 8601 duration: {duration}. Could not parse any time components.")

    return total_seconds


def get_network_info(conn: sqlite3.Connection) -> Dict[str, Any]:
    """
    Get network information (single network per database).

    Args:
        conn: Database connection

    Returns:
        Dictionary with network information

    Raises:
        ValidationError: If network metadata doesn't exist
    """
    cursor = conn.execute(
        """
        SELECT name, description, time_start, time_end, time_interval, created_at, updated_at
        FROM network_metadata 
        LIMIT 1
    """
    )

    row = cursor.fetchone()
    if not row:
        raise ValidationError("No network metadata found in database")

    return {
        "name": row[0],
        "description": row[1],
        "time_start": row[2],
        "time_end": row[3],
        "time_interval": row[4],
        "created_at": row[5],
        "updated_at": row[6],
    }


def get_network_time_periods(conn: sqlite3.Connection) -> List[TimePeriod]:
    """
    Get network time periods using optimized storage (single network per database).

    Args:
        conn: Database connection

    Returns:
        List of TimePeriod objects ordered by period_index
    """
    cursor = conn.execute(
        """
        SELECT period_count, start_timestamp, interval_seconds 
        FROM network_time_periods 
        LIMIT 1
    """
    )

    row = cursor.fetchone()
    if not row:
        return []  # No time periods defined

    period_count, start_timestamp, interval_seconds = row

    # Generate all time periods computationally
    periods = []
    for period_index in range(period_count):
        timestamp = start_timestamp + (period_index * interval_seconds)

        # Format timestamp as string for compatibility - ALWAYS use UTC to avoid DST duplicates
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")

        periods.append(
            TimePeriod(
                timestamp=timestamp,
                period_index=period_index,
                formatted_time=formatted_time,
            )
        )

    return periods


def list_networks(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """
    Get network information (returns single network in list for backward compatibility).

    Args:
        conn: Database connection

    Returns:
        List with single network dictionary (for backward compatibility)
    """
    try:
        network_info = get_network_info(conn)
        return [network_info]
    except ValidationError:
        return []


def get_first_network(conn: sqlite3.Connection) -> Optional[Dict[str, Any]]:
    """
    Get network (for backward compatibility with single-network-per-database).

    Args:
        conn: Database connection

    Returns:
        Network dictionary or None if no network exists
    """
    try:
        return get_network_info(conn)
    except ValidationError:
        return None


def get_network_by_name(
    conn: sqlite3.Connection, name: str
) -> Optional[Dict[str, Any]]:
    """
    Get network by name (for backward compatibility - checks if name matches).

    Args:
        conn: Database connection
        name: Network name to match

    Returns:
        Network dictionary if name matches, None otherwise
    """
    try:
        network_info = get_network_info(conn)
        if network_info.get("name") == name:
            return network_info
        return None
    except ValidationError:
        return None


def create_carrier(
    conn: sqlite3.Connection,
    name: str,
    co2_emissions: float = 0.0,
    color: Optional[str] = None,
    nice_name: Optional[str] = None,
) -> int:
    """
    Create a carrier record and return carrier ID (single network per database).

    Args:
        conn: Database connection
        name: Carrier name
        co2_emissions: CO2 emissions factor
        color: Display color
        nice_name: Human-readable name

    Returns:
        ID of the newly created carrier
    """
    cursor = conn.execute(
        """
        INSERT INTO carriers (name, co2_emissions, color, nice_name)
        VALUES (?, ?, ?, ?)
    """,
        (name, co2_emissions, color, nice_name),
    )

    carrier_id = cursor.lastrowid
    if not carrier_id:
        raise DatabaseError("Failed to create carrier")

    return carrier_id


def list_carriers(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """
    List all carriers (single network per database).

    Args:
        conn: Database connection

    Returns:
        List of carrier dictionaries
    """
    cursor = conn.execute(
        """
        SELECT id, name, co2_emissions, color, nice_name
        FROM carriers 
        ORDER BY name
    """
    )

    carriers = []
    for row in cursor.fetchall():
        carriers.append(
            {
                "id": row[0],
                "name": row[1],
                "co2_emissions": row[2],
                "color": row[3],
                "nice_name": row[4],
            }
        )

    return carriers


def get_network_config(
    conn: sqlite3.Connection, scenario_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get network configuration with scenario-aware fallback (single network per database).

    Priority order:
    1. Scenario-specific config (network_config WHERE scenario_id = X)
    2. Network default config (network_config WHERE scenario_id IS NULL)
    3. System default value

    Args:
        conn: Database connection
        scenario_id: Optional scenario ID

    Returns:
        Dictionary with network configuration
    """
    config = {}

    # Load from network_config table with scenario fallback
    cursor = conn.execute(
        """
        SELECT param_name, param_type, param_value
        FROM network_config 
        WHERE (scenario_id = ? OR scenario_id IS NULL)
        ORDER BY scenario_id DESC NULLS LAST  -- Scenario-specific values first
    """,
        (scenario_id,),
    )

    seen_params = set()
    for row in cursor.fetchall():
        param_name, param_type, param_value = row

        # Skip if we already have this parameter (scenario-specific takes precedence)
        if param_name in seen_params:
            continue
        seen_params.add(param_name)

        # Parse value based on type
        try:
            if param_type == "boolean":
                config[param_name] = param_value.lower() == "true"
            elif param_type == "real":
                config[param_name] = float(param_value)
            elif param_type == "integer":
                config[param_name] = int(param_value)
            elif param_type == "json":
                config[param_name] = json.loads(param_value)
            else:  # string
                config[param_name] = param_value
        except (ValueError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to parse config parameter {param_name}: {e}")
            continue

    # Apply system defaults for missing parameters
    defaults = {
        "unmet_load_active": True,
        "discount_rate": 0.0,  # No discounting by default
        "solver_name": "default",
    }

    for param, default_value in defaults.items():
        if param not in config:
            config[param] = default_value

    return config


def set_network_config(
    conn: sqlite3.Connection,
    param_name: str,
    param_value: Any,
    param_type: str,
    scenario_id: Optional[int] = None,
    description: Optional[str] = None,
) -> None:
    """
    Set network configuration parameter (single network per database).

    Args:
        conn: Database connection
        param_name: Parameter name
        param_value: Parameter value
        param_type: Parameter type ('boolean', 'real', 'integer', 'string', 'json')
        scenario_id: Optional scenario ID (NULL for base network)
        description: Optional parameter description

    Raises:
        ValidationError: If parameter type is invalid or serialization fails
    """

    # Validate parameter type
    valid_types = {"boolean", "real", "integer", "string", "json"}
    if param_type not in valid_types:
        raise ValidationError(
            f"Invalid parameter type: {param_type}. Must be one of {valid_types}"
        )

    # Serialize value based on type
    try:
        if param_type == "boolean":
            serialized = str(param_value).lower()
            if serialized not in {"true", "false"}:
                raise ValidationError(
                    f"Boolean parameter must be True/False, got: {param_value}"
                )
        elif param_type == "real":
            serialized = str(float(param_value))
        elif param_type == "integer":
            serialized = str(int(param_value))
        elif param_type == "json":
            serialized = json.dumps(param_value)
        else:  # string
            serialized = str(param_value)
    except (ValueError, TypeError) as e:
        raise ValidationError(
            f"Failed to serialize parameter {param_name} as {param_type}: {e}"
        )

    # Insert or update parameter
    conn.execute(
        """
        INSERT OR REPLACE INTO network_config 
        (scenario_id, param_name, param_type, param_value, param_description, updated_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """,
        (scenario_id, param_name, param_type, serialized, description),
    )


def get_component_counts(conn: sqlite3.Connection) -> Dict[str, int]:
    """
    Get component counts by type (single network per database).

    Args:
        conn: Database connection

    Returns:
        Dictionary mapping component types to counts
    """
    cursor = conn.execute(
        """
        SELECT component_type, COUNT(*) FROM components 
        GROUP BY component_type
    """
    )

    counts = {}
    for row in cursor.fetchall():
        counts[row[0].lower()] = row[1]

    return counts
