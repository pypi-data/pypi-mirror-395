"""
Component management operations for PyConvexity.

Provides CRUD operations for energy system components (buses, generators, loads, etc.)
with proper validation and error handling.
"""

import sqlite3
from typing import Dict, Any, Optional, List

from pyconvexity.core.types import Component, CreateComponentRequest, StaticValue
from pyconvexity.core.errors import ComponentNotFound, ValidationError, DatabaseError


def get_component_type(conn: sqlite3.Connection, component_id: int) -> str:
    """
    Get component type for a component ID.

    Args:
        conn: Database connection
        component_id: ID of the component

    Returns:
        Component type string (e.g., "BUS", "GENERATOR")

    Raises:
        ComponentNotFound: If component doesn't exist
    """
    cursor = conn.execute(
        "SELECT component_type FROM components WHERE id = ?", (component_id,)
    )
    row = cursor.fetchone()
    if not row:
        raise ComponentNotFound(component_id)
    return row[0]


def get_component(conn: sqlite3.Connection, component_id: int) -> Component:
    """
    Get component by ID (single network per database).

    Args:
        conn: Database connection
        component_id: ID of the component

    Returns:
        Component object with all fields populated

    Raises:
        ComponentNotFound: If component doesn't exist
    """
    cursor = conn.execute(
        """
        SELECT id, component_type, name, longitude, latitude, 
               carrier_id, bus_id, bus0_id, bus1_id
        FROM components WHERE id = ?
    """,
        (component_id,),
    )

    row = cursor.fetchone()
    if not row:
        raise ComponentNotFound(component_id)

    return Component(
        id=row[0],
        component_type=row[1],
        name=row[2],
        longitude=row[3],
        latitude=row[4],
        carrier_id=row[5],
        bus_id=row[6],
        bus0_id=row[7],
        bus1_id=row[8],
    )


def list_components_by_type(
    conn: sqlite3.Connection, component_type: Optional[str] = None
) -> List[Component]:
    """
    List components by type (single network per database).

    Args:
        conn: Database connection
        component_type: Optional component type filter (e.g., "BUS", "GENERATOR")

    Returns:
        List of Component objects
    """
    if component_type:
        cursor = conn.execute(
            """
            SELECT id, component_type, name, longitude, latitude, 
                   carrier_id, bus_id, bus0_id, bus1_id
            FROM components 
            WHERE component_type = ?
            ORDER BY name
        """,
            (component_type.upper(),),
        )
    else:
        cursor = conn.execute(
            """
            SELECT id, component_type, name, longitude, latitude, 
                   carrier_id, bus_id, bus0_id, bus1_id
            FROM components 
            ORDER BY component_type, name
        """
        )

    components = []
    for row in cursor.fetchall():
        components.append(
            Component(
                id=row[0],
                component_type=row[1],
                name=row[2],
                longitude=row[3],
                latitude=row[4],
                carrier_id=row[5],
                bus_id=row[6],
                bus0_id=row[7],
                bus1_id=row[8],
            )
        )

    return components


def insert_component(conn: sqlite3.Connection, request: CreateComponentRequest) -> int:
    """
    Insert a new component (single network per database).

    Args:
        conn: Database connection
        request: Component creation request with all necessary fields

    Returns:
        ID of the newly created component

    Raises:
        DatabaseError: If insertion fails
        ValidationError: If required fields are missing
    """
    # Determine carrier_id - use provided value or auto-assign default
    # CONSTRAINT components must have carrier_id=None per database schema
    carrier_id = request.carrier_id
    if carrier_id is None and request.component_type.upper() != "CONSTRAINT":
        carrier_id = get_default_carrier_id(conn, request.component_type)
    elif request.component_type.upper() == "CONSTRAINT":
        carrier_id = None  # Explicitly keep None for constraints

    # Insert the component
    cursor = conn.execute(
        """
        INSERT INTO components (
            component_type, name, longitude, latitude, 
            carrier_id, bus_id, bus0_id, bus1_id, 
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    """,
        (
            request.component_type,
            request.name,
            request.longitude,
            request.latitude,
            carrier_id,
            request.bus_id,
            request.bus0_id,
            request.bus1_id,
        ),
    )

    component_id = cursor.lastrowid
    if not component_id:
        raise DatabaseError("Failed to create component")

    # If description is provided, store it as an attribute
    if request.description:
        from pyconvexity.models.attributes import set_static_attribute

        set_static_attribute(
            conn, component_id, "description", StaticValue(request.description)
        )

    # If this is a BUS, ensure unmet load exists
    if request.component_type.upper() == "BUS":
        # Get unmet_load_active flag from network config
        from pyconvexity.models.network import get_network_config

        network_config = get_network_config(conn)
        unmet_load_active = network_config.get("unmet_load_active", True)

        ensure_unmet_load_for_bus(conn, component_id, request.name, unmet_load_active)

    return component_id


def create_component(
    conn: sqlite3.Connection,
    component_type: str,
    name: str,
    description: Optional[str] = None,
    longitude: Optional[float] = None,
    latitude: Optional[float] = None,
    carrier_id: Optional[int] = None,
    bus_id: Optional[int] = None,
    bus0_id: Optional[int] = None,
    bus1_id: Optional[int] = None,
) -> int:
    """
    Create a component and return its ID - convenience function (single network per database).

    Args:
        conn: Database connection
        component_type: Type of component (e.g., "BUS", "GENERATOR")
        name: Component name
        description: Optional description
        longitude: Optional longitude coordinate
        latitude: Optional latitude coordinate
        carrier_id: Optional carrier ID
        bus_id: Optional bus ID (for single-bus components)
        bus0_id: Optional first bus ID (for two-bus components)
        bus1_id: Optional second bus ID (for two-bus components)

    Returns:
        ID of the newly created component
    """
    request = CreateComponentRequest(
        component_type=component_type,
        name=name,
        description=description,
        longitude=longitude,
        latitude=latitude,
        carrier_id=carrier_id,
        bus_id=bus_id,
        bus0_id=bus0_id,
        bus1_id=bus1_id,
    )
    return insert_component(conn, request)


def update_component(
    conn: sqlite3.Connection,
    component_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    longitude: Optional[float] = None,
    latitude: Optional[float] = None,
    carrier_id: Optional[int] = None,
    bus_id: Optional[int] = None,
    bus0_id: Optional[int] = None,
    bus1_id: Optional[int] = None,
) -> None:
    """
    Update a component.

    Args:
        conn: Database connection
        component_id: ID of component to update
        name: New name (optional)
        description: New description (optional)
        longitude: New longitude (optional)
        latitude: New latitude (optional)
        carrier_id: New carrier ID (optional)
        bus_id: New bus ID (optional)
        bus0_id: New first bus ID (optional)
        bus1_id: New second bus ID (optional)

    Raises:
        ComponentNotFound: If component doesn't exist
    """
    # Build dynamic SQL based on what fields are being updated
    set_clauses = []
    params = []

    if name is not None:
        set_clauses.append("name = ?")
        params.append(name)
    if longitude is not None:
        set_clauses.append("longitude = ?")
        params.append(longitude)
    if latitude is not None:
        set_clauses.append("latitude = ?")
        params.append(latitude)
    if carrier_id is not None:
        set_clauses.append("carrier_id = ?")
        params.append(carrier_id)
    if bus_id is not None:
        set_clauses.append("bus_id = ?")
        params.append(bus_id)
    if bus0_id is not None:
        set_clauses.append("bus0_id = ?")
        params.append(bus0_id)
    if bus1_id is not None:
        set_clauses.append("bus1_id = ?")
        params.append(bus1_id)

    # Update component table fields if any changes
    if set_clauses:
        set_clauses.append("updated_at = datetime('now')")
        params.append(component_id)

        sql = f"UPDATE components SET {', '.join(set_clauses)} WHERE id = ?"
        cursor = conn.execute(sql, params)

        if cursor.rowcount == 0:
            raise ComponentNotFound(component_id)

    # Handle description as an attribute
    if description is not None:
        from pyconvexity.models.attributes import set_static_attribute, delete_attribute

        if description == "":
            # Remove description attribute if empty
            try:
                delete_attribute(conn, component_id, "description")
            except:  # AttributeNotFound
                pass  # Already doesn't exist
        else:
            # Set description as attribute
            set_static_attribute(
                conn, component_id, "description", StaticValue(description)
            )


def delete_component(conn: sqlite3.Connection, component_id: int) -> None:
    """
    Delete a component and all its attributes.

    Args:
        conn: Database connection
        component_id: ID of component to delete

    Raises:
        ComponentNotFound: If component doesn't exist
    """
    # First delete all component attributes
    conn.execute(
        "DELETE FROM component_attributes WHERE component_id = ?", (component_id,)
    )

    # Then delete the component itself
    cursor = conn.execute("DELETE FROM components WHERE id = ?", (component_id,))

    if cursor.rowcount == 0:
        raise ComponentNotFound(component_id)


def list_component_attributes(conn: sqlite3.Connection, component_id: int) -> List[str]:
    """
    List all attribute names for a component.

    Args:
        conn: Database connection
        component_id: Component ID

    Returns:
        List of attribute names
    """
    cursor = conn.execute(
        """
        SELECT attribute_name FROM component_attributes 
        WHERE component_id = ? ORDER BY attribute_name
    """,
        (component_id,),
    )

    return [row[0] for row in cursor.fetchall()]


def get_component_by_name(conn: sqlite3.Connection, name: str) -> Component:
    """
    Get a component by name (single network per database).

    Args:
        conn: Database connection
        name: Component name

    Returns:
        Component object

    Raises:
        ComponentNotFound: If component doesn't exist
    """
    cursor = conn.execute(
        """
        SELECT id, component_type, name, longitude, latitude, 
               carrier_id, bus_id, bus0_id, bus1_id
        FROM components 
        WHERE name = ?
    """,
        (name,),
    )

    row = cursor.fetchone()
    if not row:
        raise ComponentNotFound(f"Component '{name}' not found")

    return Component(
        id=row[0],
        component_type=row[1],
        name=row[2],
        longitude=row[3],
        latitude=row[4],
        carrier_id=row[5],
        bus_id=row[6],
        bus0_id=row[7],
        bus1_id=row[8],
    )


def get_component_id(conn: sqlite3.Connection, name: str) -> int:
    """
    Get component ID by name (single network per database).

    Args:
        conn: Database connection
        name: Component name

    Returns:
        Component ID

    Raises:
        ComponentNotFound: If component doesn't exist
    """
    component = get_component_by_name(conn, name)
    return component.id


def component_exists(conn: sqlite3.Connection, name: str) -> bool:
    """
    Check if a component exists (single network per database).

    Args:
        conn: Database connection
        name: Component name

    Returns:
        True if component exists, False otherwise
    """
    cursor = conn.execute(
        """
        SELECT 1 FROM components WHERE name = ?
    """,
        (name,),
    )

    return cursor.fetchone() is not None


def get_component_carrier_map(
    conn: sqlite3.Connection, component_type: Optional[str] = None
) -> Dict[str, str]:
    """
    Get mapping from component names to carrier names (single network per database).

    Args:
        conn: Database connection
        component_type: Optional component type filter

    Returns:
        Dictionary mapping component names to carrier names
    """
    if component_type:
        cursor = conn.execute(
            """
            SELECT c.name,
                   CASE 
                       WHEN c.component_type = 'UNMET_LOAD' THEN 'Unmet Load'
                       ELSE carr.name
                   END as carrier_name
            FROM components c
            LEFT JOIN carriers carr ON c.carrier_id = carr.id
            WHERE c.component_type = ?
        """,
            (component_type.upper(),),
        )
    else:
        cursor = conn.execute(
            """
            SELECT c.name,
                   CASE 
                       WHEN c.component_type = 'UNMET_LOAD' THEN 'Unmet Load'
                       ELSE carr.name
                   END as carrier_name
            FROM components c
            LEFT JOIN carriers carr ON c.carrier_id = carr.id
        """
        )

    return {row[0]: row[1] for row in cursor.fetchall()}


# Helper functions


def get_default_carrier_id(conn: sqlite3.Connection, component_type: str) -> int:
    """Get default carrier ID for a component type (single network per database)."""
    # Default carrier names based on PyPSA conventions
    default_carrier_name = {
        "BUS": "AC",
        "GENERATOR": "electricity",
        "LOAD": "electricity",
        "STORAGE_UNIT": "electricity",
        "STORE": "electricity",
        "LINE": "AC",
        "LINK": "AC",
    }.get(component_type.upper(), "AC")

    # Try to find the default carrier
    cursor = conn.execute(
        """
        SELECT id FROM carriers WHERE name = ? LIMIT 1
    """,
        (default_carrier_name,),
    )

    row = cursor.fetchone()
    if row:
        return row[0]

    # If not found, try AC
    cursor = conn.execute(
        """
        SELECT id FROM carriers WHERE name = 'AC' LIMIT 1
    """
    )

    row = cursor.fetchone()
    if row:
        return row[0]

    # If still not found, get any carrier
    cursor = conn.execute(
        """
        SELECT id FROM carriers LIMIT 1
    """
    )

    row = cursor.fetchone()
    if row:
        return row[0]

    raise DatabaseError("No carriers found in database")


def ensure_unmet_load_for_bus(
    conn: sqlite3.Connection, bus_id: int, bus_name: str, unmet_load_active: bool
) -> None:
    """Ensure there is exactly one UNMET_LOAD per bus (single network per database)."""
    # Check if unmet load already exists for this bus
    cursor = conn.execute(
        """
        SELECT id FROM components 
        WHERE bus_id = ? AND component_type = 'UNMET_LOAD' 
        LIMIT 1
    """,
        (bus_id,),
    )

    if cursor.fetchone():
        return  # Already exists

    # Get default carrier for generators (unmet loads are treated as generators)
    carrier_id = get_default_carrier_id(conn, "GENERATOR")

    # Insert unmet load component - sanitize bus name for PyPSA compatibility
    # Remove spaces, periods, and other problematic characters
    sanitized_bus_name = bus_name.replace(" ", "_").replace(".", "_").replace("-", "_")
    name = f"unmet_load_{sanitized_bus_name}"
    cursor = conn.execute(
        """
        INSERT INTO components (
            component_type, name, carrier_id, bus_id, 
            created_at, updated_at
        ) VALUES ('UNMET_LOAD', ?, ?, ?, datetime('now'), datetime('now'))
    """,
        (name, carrier_id, bus_id),
    )

    unmet_load_id = cursor.lastrowid

    # Set fixed attributes for unmet load
    from pyconvexity.models.attributes import set_static_attribute

    set_static_attribute(conn, unmet_load_id, "marginal_cost", StaticValue(1e6))
    set_static_attribute(conn, unmet_load_id, "p_nom", StaticValue(1e6))
    set_static_attribute(
        conn, unmet_load_id, "p_max_pu", StaticValue(1.0)
    )  # Can run at full capacity
    set_static_attribute(
        conn, unmet_load_id, "p_min_pu", StaticValue(0.0)
    )  # Can be turned off
    set_static_attribute(
        conn, unmet_load_id, "sign", StaticValue(1.0)
    )  # Positive power sign (generation)
    set_static_attribute(conn, unmet_load_id, "active", StaticValue(unmet_load_active))


def get_bus_name_to_id_map(conn: sqlite3.Connection) -> Dict[str, int]:
    """Get mapping from bus names to component IDs (single network per database)."""
    cursor = conn.execute(
        """
        SELECT name, id FROM components 
        WHERE component_type = 'BUS'
    """
    )

    return {row[0]: row[1] for row in cursor.fetchall()}
