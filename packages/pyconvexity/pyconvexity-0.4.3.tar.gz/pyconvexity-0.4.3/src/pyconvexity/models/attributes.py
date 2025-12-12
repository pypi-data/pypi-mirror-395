"""
Attribute management operations for PyConvexity.

Provides operations for setting, getting, and managing component attributes
with support for both static values and timeseries data.
"""

import sqlite3
import json
import logging
from typing import Dict, Any, Optional, List, Union
import pandas as pd
from io import BytesIO
import pyarrow as pa
import pyarrow.parquet as pq

from pyconvexity.core.types import (
    StaticValue,
    Timeseries,
    TimeseriesMetadata,
    AttributeValue,
    TimePeriod,
)
from pyconvexity.core.errors import (
    ComponentNotFound,
    AttributeNotFound,
    ValidationError,
    TimeseriesError,
)

logger = logging.getLogger(__name__)


def set_static_attribute(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
    value: StaticValue,
    scenario_id: Optional[int] = None,
) -> None:
    """
    Set a static attribute value for a component in a specific scenario.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Name of the attribute
        value: Static value to set
        scenario_id: Scenario ID (uses master scenario if None)

    Raises:
        ComponentNotFound: If component doesn't exist
        ValidationError: If attribute doesn't allow static values or validation fails
    """
    # 1. Get component type
    from pyconvexity.models.components import get_component_type

    component_type = get_component_type(conn, component_id)

    # 2. Get validation rule
    from pyconvexity.validation.rules import get_validation_rule, validate_static_value

    rule = get_validation_rule(conn, component_type, attribute_name)

    # 3. Check if static values are allowed
    if not rule.allows_static:
        raise ValidationError(
            f"Attribute '{attribute_name}' for {component_type} does not allow static values"
        )

    # 4. Validate data type
    validate_static_value(value, rule)

    # 5. Use scenario_id directly (NULL for base network)
    resolved_scenario_id = scenario_id

    # 6. Remove any existing attribute for this scenario
    cursor = conn.cursor()
    if resolved_scenario_id is None:
        cursor.execute(
            "DELETE FROM component_attributes WHERE component_id = ? AND attribute_name = ? AND scenario_id IS NULL",
            (component_id, attribute_name),
        )
    else:
        cursor.execute(
            "DELETE FROM component_attributes WHERE component_id = ? AND attribute_name = ? AND scenario_id = ?",
            (component_id, attribute_name, resolved_scenario_id),
        )

    # 7. Insert new static attribute (store as JSON in static_value TEXT column)
    json_value = value.to_json()

    cursor.execute(
        """INSERT INTO component_attributes 
           (component_id, attribute_name, scenario_id, storage_type, static_value, data_type, unit, is_input) 
           VALUES (?, ?, ?, 'static', ?, ?, ?, ?)""",
        (
            component_id,
            attribute_name,
            resolved_scenario_id,
            json_value,
            rule.data_type,
            rule.unit,
            rule.is_input,
        ),
    )


def set_timeseries_attribute(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
    timeseries: Union[Timeseries, List[float]],
    scenario_id: Optional[int] = None,
) -> None:
    """
    Set a timeseries attribute value for a component in a specific scenario.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Name of the attribute
        timeseries: Timeseries object or list of float values
        scenario_id: Scenario ID (uses master scenario if None)

    Raises:
        ComponentNotFound: If component doesn't exist
        ValidationError: If attribute doesn't allow timeseries values
        TimeseriesError: If timeseries serialization fails
    """
    # 1. Get component type
    from pyconvexity.models.components import get_component_type

    component_type = get_component_type(conn, component_id)

    # 2. Get validation rule
    from pyconvexity.validation.rules import get_validation_rule

    rule = get_validation_rule(conn, component_type, attribute_name)

    # 3. Check if timeseries values are allowed
    if not rule.allows_timeseries:
        raise ValidationError(
            f"Attribute '{attribute_name}' for {component_type} does not allow timeseries values"
        )

    # 4. Convert input to values array
    if isinstance(timeseries, Timeseries):
        values = timeseries.values
    elif isinstance(timeseries, list) and all(
        isinstance(v, (int, float)) for v in timeseries
    ):
        # Direct values array
        values = [float(v) for v in timeseries]
    else:
        raise ValueError("timeseries must be Timeseries or List[float]")

    # 5. Serialize to binary format (ultra-fast, matches Rust exactly)
    binary_data = serialize_values_to_binary(values)

    # 6. Use scenario_id directly (NULL for base network)
    resolved_scenario_id = scenario_id

    # 7. Remove any existing attribute for this scenario
    cursor = conn.cursor()
    if resolved_scenario_id is None:
        cursor.execute(
            "DELETE FROM component_attributes WHERE component_id = ? AND attribute_name = ? AND scenario_id IS NULL",
            (component_id, attribute_name),
        )
    else:
        cursor.execute(
            "DELETE FROM component_attributes WHERE component_id = ? AND attribute_name = ? AND scenario_id = ?",
            (component_id, attribute_name, resolved_scenario_id),
        )

    # 8. Insert new timeseries attribute
    cursor.execute(
        """INSERT INTO component_attributes 
           (component_id, attribute_name, scenario_id, storage_type, timeseries_data, data_type, unit, is_input) 
           VALUES (?, ?, ?, 'timeseries', ?, ?, ?, ?)""",
        (
            component_id,
            attribute_name,
            resolved_scenario_id,
            binary_data,
            rule.data_type,
            rule.unit,
            rule.is_input,
        ),
    )


def get_attribute(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
    scenario_id: Optional[int] = None,
) -> AttributeValue:
    """
    Get an attribute value with scenario fallback logic.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Name of the attribute
        scenario_id: Scenario ID (uses master scenario if None)

    Returns:
        AttributeValue containing either static or timeseries data

    Raises:
        ComponentNotFound: If component doesn't exist
        AttributeNotFound: If attribute doesn't exist
    """
    cursor = conn.cursor()

    # Determine which scenario to check first
    current_scenario_id = scenario_id

    # First try to get the attribute from the current scenario
    if current_scenario_id is None:
        cursor.execute(
            """SELECT storage_type, static_value, timeseries_data, data_type, unit
               FROM component_attributes 
               WHERE component_id = ? AND attribute_name = ? AND scenario_id IS NULL""",
            (component_id, attribute_name),
        )
    else:
        cursor.execute(
            """SELECT storage_type, static_value, timeseries_data, data_type, unit
               FROM component_attributes 
               WHERE component_id = ? AND attribute_name = ? AND scenario_id = ?""",
            (component_id, attribute_name, current_scenario_id),
        )
    result = cursor.fetchone()

    # If not found in current scenario and current scenario is not base (NULL), try base scenario as fallback
    if not result and current_scenario_id is not None:
        cursor.execute(
            """SELECT storage_type, static_value, timeseries_data, data_type, unit
               FROM component_attributes 
               WHERE component_id = ? AND attribute_name = ? AND scenario_id IS NULL""",
            (component_id, attribute_name),
        )
        result = cursor.fetchone()

    if not result:
        raise AttributeNotFound(component_id, attribute_name)

    storage_type, static_value_json, timeseries_data, data_type, unit = result

    # Handle the deserialization based on storage type
    if storage_type == "static":
        if not static_value_json:
            raise ValidationError("Static attribute missing value")

        # Parse JSON value
        json_value = json.loads(static_value_json)

        # Convert based on data type
        if data_type == "float":
            if isinstance(json_value, (int, float)):
                static_value = StaticValue(float(json_value))
            else:
                raise ValidationError("Expected float value")
        elif data_type == "int":
            if isinstance(json_value, (int, float)):
                static_value = StaticValue(int(json_value))
            else:
                raise ValidationError("Expected integer value")
        elif data_type == "boolean":
            if isinstance(json_value, bool):
                static_value = StaticValue(json_value)
            else:
                raise ValidationError("Expected boolean value")
        elif data_type == "string":
            if isinstance(json_value, str):
                static_value = StaticValue(json_value)
            else:
                raise ValidationError("Expected string value")
        else:
            raise ValidationError(f"Unknown data type: {data_type}")

        return AttributeValue.static(static_value)

    elif storage_type == "timeseries":
        if not timeseries_data:
            raise ValidationError("Timeseries attribute missing data")

        # Deserialize from binary format to new efficient Timeseries format
        values = deserialize_values_from_binary(timeseries_data)

        timeseries = Timeseries(
            values=values,
            length=len(values),
            start_index=0,
            data_type=data_type,
            unit=unit,
            is_input=True,  # Default, could be enhanced with actual is_input from DB
        )

        return AttributeValue.timeseries(timeseries)

    else:
        raise ValidationError(f"Unknown storage type: {storage_type}")


def delete_attribute(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
    scenario_id: Optional[int] = None,
) -> None:
    """
    Delete an attribute from a specific scenario.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Name of the attribute
        scenario_id: Scenario ID (uses master scenario if None)

    Raises:
        AttributeNotFound: If attribute doesn't exist
    """
    # Use scenario_id directly (NULL for base network)
    resolved_scenario_id = scenario_id

    cursor = conn.cursor()
    if resolved_scenario_id is None:
        cursor.execute(
            "DELETE FROM component_attributes WHERE component_id = ? AND attribute_name = ? AND scenario_id IS NULL",
            (component_id, attribute_name),
        )
    else:
        cursor.execute(
            "DELETE FROM component_attributes WHERE component_id = ? AND attribute_name = ? AND scenario_id = ?",
            (component_id, attribute_name, resolved_scenario_id),
        )

    if cursor.rowcount == 0:
        raise AttributeNotFound(component_id, attribute_name)


# ============================================================================
# EFFICIENT TIMESERIES SERIALIZATION - MATCHES RUST IMPLEMENTATION EXACTLY
# ============================================================================


def serialize_values_to_binary(values: List[float]) -> bytes:
    """
    Serialize f32 values to binary format - EXACT MATCH WITH RUST.

    Ultra-fast binary format: just raw Float32 array, little-endian.
    """
    if not values:
        return b""

    import struct

    buffer = bytearray(len(values) * 4)  # 4 bytes per Float32

    for i, value in enumerate(values):
        # Pack as little-endian Float32 to match Rust exactly
        struct.pack_into("<f", buffer, i * 4, float(value))

    return bytes(buffer)


def deserialize_values_from_binary(data: bytes) -> List[float]:
    """
    Deserialize f32 values from binary format - EXACT MATCH WITH RUST.

    Ultra-fast deserialization: read raw Float32 values only.
    """
    if not data:
        return []

    # Ensure data length is multiple of 4 (Float32 size)
    if len(data) % 4 != 0:
        raise ValueError("Invalid binary data length - must be multiple of 4 bytes")

    import struct

    values = []

    # Ultra-fast deserialization: read raw Float32 values
    for i in range(0, len(data), 4):
        value = struct.unpack("<f", data[i : i + 4])[0]  # Little-endian Float32
        values.append(value)

    return values


def get_timeseries_length_from_binary(data: bytes) -> int:
    """Get the length of a timeseries without deserializing the full data."""
    if not data:
        return 0

    # Ultra-fast: just divide by 4 bytes per Float32
    if len(data) % 4 != 0:
        raise ValueError("Invalid binary data length - must be multiple of 4 bytes")

    return len(data) // 4


# ============================================================================
# UNIFIED TIMESERIES FUNCTIONS - MATCH RUST API
# ============================================================================


def get_timeseries(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
    scenario_id: Optional[int] = None,
    start_index: Optional[int] = None,
    end_index: Optional[int] = None,
    max_points: Optional[int] = None,
) -> Timeseries:
    """
    Get timeseries data with unified interface matching Rust implementation.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Name of the attribute
        scenario_id: Scenario ID (uses master scenario if None)
        start_index: Start index for range queries
        end_index: End index for range queries
        max_points: Maximum number of points (for sampling)

    Returns:
        Timeseries object with efficient array-based data

    Raises:
        ComponentNotFound: If component doesn't exist
        AttributeNotFound: If attribute doesn't exist
    """
    # Get the attribute value
    attr_value = get_attribute(conn, component_id, attribute_name, scenario_id)

    if not attr_value.is_timeseries():
        raise ValueError(f"Attribute '{attribute_name}' is not a timeseries")

    timeseries = attr_value.as_timeseries()
    if not timeseries:
        raise ValueError("Failed to get timeseries data")

    # Apply range filtering if requested
    if start_index is not None and end_index is not None:
        timeseries = timeseries.slice(start_index, end_index)

    # Apply sampling if requested
    if max_points is not None:
        timeseries = timeseries.sample(max_points)

    return timeseries


# ============================================================================
# ACTUAL VALUE FUNCTIONS
# ============================================================================


def set_actual_static_value(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
    value: StaticValue,
) -> None:
    """
    Set an actual (measured/true) static value for a component attribute.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Attribute name
        value: Static value to set
    """
    from pyconvexity.models.scenarios import get_or_create_actual_scenario

    actual_scenario_id = get_or_create_actual_scenario(conn)
    set_static_attribute(conn, component_id, attribute_name, value, actual_scenario_id)


def set_actual_timeseries_value(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
    timeseries: Union[Timeseries, List[float]],
) -> None:
    """
    Set an actual (measured/true) timeseries value for a component attribute.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Attribute name
        timeseries: Timeseries object or list of float values
    """
    from pyconvexity.models.scenarios import get_or_create_actual_scenario

    actual_scenario_id = get_or_create_actual_scenario(conn)
    set_timeseries_attribute(
        conn, component_id, attribute_name, timeseries, actual_scenario_id
    )


def get_actual_value(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
) -> Optional[AttributeValue]:
    """
    Get the actual value for a component attribute (if it exists).

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Attribute name

    Returns:
        AttributeValue or None if no actual value exists
    """
    from pyconvexity.models.scenarios import get_actual_scenario_id

    actual_scenario_id = get_actual_scenario_id(conn)
    if actual_scenario_id is None:
        return None

    try:
        return get_attribute_direct(conn, component_id, attribute_name, actual_scenario_id)
    except AttributeNotFound:
        return None


def get_attribute_direct(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
    scenario_id: Optional[int] = None,
) -> AttributeValue:
    """
    Get an attribute value directly for a specific scenario (no fallback logic).

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Attribute name
        scenario_id: Scenario ID (NULL for base network)

    Returns:
        AttributeValue

    Raises:
        AttributeNotFound: If attribute doesn't exist in the specified scenario
    """
    cursor = conn.cursor()

    if scenario_id is None:
        cursor.execute(
            """SELECT storage_type, static_value, timeseries_data, data_type, unit
               FROM component_attributes 
               WHERE component_id = ? AND attribute_name = ? AND scenario_id IS NULL""",
            (component_id, attribute_name),
        )
    else:
        cursor.execute(
            """SELECT storage_type, static_value, timeseries_data, data_type, unit
               FROM component_attributes 
               WHERE component_id = ? AND attribute_name = ? AND scenario_id = ?""",
            (component_id, attribute_name, scenario_id),
        )

    result = cursor.fetchone()
    if not result:
        raise AttributeNotFound(component_id, attribute_name)

    storage_type, static_value_json, timeseries_data, data_type, unit = result

    # Handle deserialization based on storage type
    if storage_type == "static":
        if not static_value_json:
            raise ValidationError("Static attribute missing value")

        import json

        json_value = json.loads(static_value_json)

        if data_type == "float":
            static_value = StaticValue(float(json_value))
        elif data_type == "int":
            static_value = StaticValue(int(json_value))
        elif data_type == "boolean":
            static_value = StaticValue(bool(json_value))
        elif data_type == "string":
            static_value = StaticValue(str(json_value))
        else:
            raise ValidationError(f"Unknown data type: {data_type}")

        return AttributeValue.static(static_value)

    elif storage_type == "timeseries":
        if not timeseries_data:
            raise ValidationError("Timeseries attribute missing data")

        values = deserialize_values_from_binary(timeseries_data)

        timeseries = Timeseries(
            values=values,
            length=len(values),
            start_index=0,
            data_type=data_type,
            unit=unit,
            is_input=True,
        )

        return AttributeValue.timeseries(timeseries)

    else:
        raise ValidationError(f"Unknown storage type: {storage_type}")


def clear_actual_value(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
) -> None:
    """
    Clear (delete) the actual value for a component attribute.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Attribute name
    """
    from pyconvexity.models.scenarios import get_actual_scenario_id

    actual_scenario_id = get_actual_scenario_id(conn)
    if actual_scenario_id is None:
        return  # No actual scenario, nothing to clear

    try:
        delete_attribute(conn, component_id, attribute_name, actual_scenario_id)
    except AttributeNotFound:
        pass  # Already doesn't exist


def get_timeseries_metadata(
    conn: sqlite3.Connection,
    component_id: int,
    attribute_name: str,
    scenario_id: Optional[int] = None,
) -> TimeseriesMetadata:
    """
    Get timeseries metadata without loading the full data.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Name of the attribute
        scenario_id: Scenario ID (uses master scenario if None)

    Returns:
        TimeseriesMetadata with length and type information
    """
    # Get basic attribute info without loading full data
    cursor = conn.cursor()

    # Get current scenario ID
    current_scenario_id = scenario_id

    # Get timeseries metadata
    if current_scenario_id is None:
        cursor.execute(
            """SELECT timeseries_data, data_type, unit, is_input
               FROM component_attributes 
               WHERE component_id = ? AND attribute_name = ? AND storage_type = 'timeseries' AND scenario_id IS NULL""",
            (component_id, attribute_name),
        )
    else:
        cursor.execute(
            """SELECT timeseries_data, data_type, unit, is_input
               FROM component_attributes 
               WHERE component_id = ? AND attribute_name = ? AND storage_type = 'timeseries' AND scenario_id = ?""",
            (component_id, attribute_name, current_scenario_id),
        )
    result = cursor.fetchone()

    # Try fallback to base scenario if not found in current scenario
    if not result and current_scenario_id is not None:
        cursor.execute(
            """SELECT timeseries_data, data_type, unit, is_input
               FROM component_attributes 
               WHERE component_id = ? AND attribute_name = ? AND storage_type = 'timeseries' AND scenario_id IS NULL""",
            (component_id, attribute_name),
        )
        result = cursor.fetchone()

    if not result:
        raise AttributeNotFound(component_id, attribute_name)

    timeseries_data, data_type, unit, is_input = result

    # Get length without full deserialization
    length = get_timeseries_length_from_binary(timeseries_data)

    # Get time range from network time periods
    try:
        from pyconvexity.models.network import get_network_time_periods

        time_periods = get_network_time_periods(conn)
        start_time = time_periods[0].timestamp if time_periods else 0
        end_time = time_periods[-1].timestamp if time_periods else 0
    except Exception:
        start_time = 0
        end_time = length - 1

    return TimeseriesMetadata(
        length=length,
        start_time=start_time,
        end_time=end_time,
        start_index=0,
        end_index=length,
        data_type=data_type,
        unit=unit,
        is_input=is_input,
    )
