"""
Carrier management operations for PyConvexity.

Provides operations for querying carriers and their properties.
"""

import sqlite3
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

from pyconvexity.core.errors import ValidationError

logger = logging.getLogger(__name__)


@dataclass
class Carrier:
    """Represents an energy carrier in the network (single network per database)."""

    id: int
    name: str
    co2_emissions: float
    color: Optional[str]
    nice_name: Optional[str]


def list_carriers(conn: sqlite3.Connection) -> List[Carrier]:
    """
    List all carriers for the network (single network per database).

    Args:
        conn: Database connection

    Returns:
        List of Carrier objects ordered by name
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
            Carrier(
                id=row[0],
                name=row[1],
                co2_emissions=row[2] or 0.0,
                color=row[3],
                nice_name=row[4],
            )
        )

    return carriers


def get_carrier_by_name(conn: sqlite3.Connection, name: str) -> Carrier:
    """
    Get a carrier by name (single network per database).

    Args:
        conn: Database connection
        name: Carrier name

    Returns:
        Carrier object

    Raises:
        ValidationError: If carrier doesn't exist
    """
    cursor = conn.execute(
        """
        SELECT id, name, co2_emissions, color, nice_name
        FROM carriers
        WHERE name = ?
    """,
        (name,),
    )

    row = cursor.fetchone()
    if not row:
        raise ValidationError(f"Carrier '{name}' not found")

    return Carrier(
        id=row[0],
        name=row[1],
        co2_emissions=row[2] or 0.0,
        color=row[3],
        nice_name=row[4],
    )


def get_carrier_by_id(conn: sqlite3.Connection, carrier_id: int) -> Carrier:
    """
    Get a carrier by ID (single network per database).

    Args:
        conn: Database connection
        carrier_id: Carrier ID

    Returns:
        Carrier object

    Raises:
        ValidationError: If carrier doesn't exist
    """
    cursor = conn.execute(
        """
        SELECT id, name, co2_emissions, color, nice_name
        FROM carriers
        WHERE id = ?
    """,
        (carrier_id,),
    )

    row = cursor.fetchone()
    if not row:
        raise ValidationError(f"Carrier with ID {carrier_id} not found")

    return Carrier(
        id=row[0],
        name=row[1],
        co2_emissions=row[2] or 0.0,
        color=row[3],
        nice_name=row[4],
    )


def get_carrier_colors(conn: sqlite3.Connection) -> Dict[str, str]:
    """
    Get carrier colors for visualization (single network per database).

    Args:
        conn: Database connection

    Returns:
        Dictionary mapping carrier names to color strings
    """
    cursor = conn.execute(
        """
        SELECT name, color
        FROM carriers
    """
    )

    colors = {}
    for row in cursor.fetchall():
        if row[1]:  # Only include if color is defined
            colors[row[0]] = row[1]

    # Add default color for Unmet Load if not present
    if "Unmet Load" not in colors:
        colors["Unmet Load"] = "#FF0000"

    return colors
