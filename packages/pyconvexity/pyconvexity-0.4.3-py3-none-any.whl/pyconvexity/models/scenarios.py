"""
Scenario management operations for PyConvexity.

Provides operations for listing, querying, and managing scenarios.
"""

import sqlite3
import logging
from typing import List, Optional
from dataclasses import dataclass

from pyconvexity.core.errors import ValidationError

logger = logging.getLogger(__name__)


@dataclass
class Scenario:
    """Represents a scenario (single network per database)."""

    id: int
    name: str
    description: Optional[str]
    probability: Optional[float]  # For stochastic optimization
    is_system_scenario: bool = False  # System-reserved scenarios (like "Actual")
    system_purpose: Optional[str] = None  # 'actual' for actual/measured values
    created_at: str = ""


# System scenario constants
ACTUAL_SCENARIO_PURPOSE = "actual"


def list_scenarios(
    conn: sqlite3.Connection, include_system: bool = False
) -> List[Scenario]:
    """
    List scenarios (single network per database).

    Args:
        conn: Database connection
        include_system: If True, include system scenarios (like "Actual")

    Returns:
        List of Scenario objects ordered by creation date
    """
    if include_system:
        query = """
            SELECT id, name, description, probability, is_system_scenario, system_purpose, created_at
            FROM scenarios
            ORDER BY is_system_scenario ASC, created_at ASC
        """
    else:
        query = """
            SELECT id, name, description, probability, is_system_scenario, system_purpose, created_at
            FROM scenarios
            WHERE is_system_scenario = 0
            ORDER BY created_at ASC
        """

    cursor = conn.execute(query)

    scenarios = []
    for row in cursor.fetchall():
        scenarios.append(
            Scenario(
                id=row[0],
                name=row[1],
                description=row[2],
                probability=row[3],
                is_system_scenario=bool(row[4]),
                system_purpose=row[5],
                created_at=row[6],
            )
        )

    return scenarios


def get_scenario_by_name(conn: sqlite3.Connection, name: str) -> Scenario:
    """
    Get a scenario by name (single network per database).

    Args:
        conn: Database connection
        name: Scenario name

    Returns:
        Scenario object

    Raises:
        ValidationError: If scenario doesn't exist
    """
    cursor = conn.execute(
        """
        SELECT id, name, description, probability, is_system_scenario, system_purpose, created_at
        FROM scenarios
        WHERE name = ?
    """,
        (name,),
    )

    row = cursor.fetchone()
    if not row:
        raise ValidationError(f"Scenario '{name}' not found")

    return Scenario(
        id=row[0],
        name=row[1],
        description=row[2],
        probability=row[3],
        is_system_scenario=bool(row[4]),
        system_purpose=row[5],
        created_at=row[6],
    )


def get_scenario_by_id(conn: sqlite3.Connection, scenario_id: int) -> Scenario:
    """
    Get a scenario by ID.

    Args:
        conn: Database connection
        scenario_id: Scenario ID

    Returns:
        Scenario object

    Raises:
        ValidationError: If scenario doesn't exist
    """
    cursor = conn.execute(
        """
        SELECT id, name, description, probability, is_system_scenario, system_purpose, created_at
        FROM scenarios
        WHERE id = ?
    """,
        (scenario_id,),
    )

    row = cursor.fetchone()
    if not row:
        raise ValidationError(f"Scenario with ID {scenario_id} not found")

    return Scenario(
        id=row[0],
        name=row[1],
        description=row[2],
        probability=row[3],
        is_system_scenario=bool(row[4]),
        system_purpose=row[5],
        created_at=row[6],
    )


# ============================================================================
# ACTUAL SCENARIO FUNCTIONS
# ============================================================================


def get_actual_scenario_id(conn: sqlite3.Connection) -> Optional[int]:
    """
    Get the Actual scenario ID (if it exists).

    Args:
        conn: Database connection

    Returns:
        Actual scenario ID or None if not found
    """
    cursor = conn.execute(
        """
        SELECT id FROM scenarios WHERE system_purpose = ?
    """,
        (ACTUAL_SCENARIO_PURPOSE,),
    )

    row = cursor.fetchone()
    return row[0] if row else None


def get_or_create_actual_scenario(conn: sqlite3.Connection) -> int:
    """
    Get the Actual scenario ID, creating it if it doesn't exist.

    Args:
        conn: Database connection

    Returns:
        Actual scenario ID
    """
    scenario_id = get_actual_scenario_id(conn)
    if scenario_id is not None:
        return scenario_id

    # Create the actual scenario
    cursor = conn.execute(
        """
        INSERT INTO scenarios (name, description, is_system_scenario, system_purpose, created_at)
        VALUES ('Actual', 'Actual/measured values for validation and comparison', 1, ?, datetime('now'))
    """,
        (ACTUAL_SCENARIO_PURPOSE,),
    )

    return cursor.lastrowid


def has_actual_value(
    conn: sqlite3.Connection, component_id: int, attribute_name: str
) -> bool:
    """
    Check if an actual value exists for a component attribute.

    Args:
        conn: Database connection
        component_id: Component ID
        attribute_name: Attribute name

    Returns:
        True if actual value exists
    """
    scenario_id = get_actual_scenario_id(conn)
    if scenario_id is None:
        return False

    cursor = conn.execute(
        """
        SELECT COUNT(*) > 0 FROM component_attributes
        WHERE component_id = ? AND attribute_name = ? AND scenario_id = ?
    """,
        (component_id, attribute_name, scenario_id),
    )

    return bool(cursor.fetchone()[0])
