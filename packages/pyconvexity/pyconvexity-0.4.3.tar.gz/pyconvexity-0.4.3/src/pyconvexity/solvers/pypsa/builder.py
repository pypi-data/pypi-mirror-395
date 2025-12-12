"""
Network building functionality for PyPSA solver integration.

Simplified to always use MultiIndex format for consistent multi-period optimization.
"""

import logging
import json
import pandas as pd
from typing import Dict, Any, Optional, Callable

from pyconvexity.models import (
    list_components_by_type,
    get_network_time_periods,
    get_network_info,
)

logger = logging.getLogger(__name__)


class NetworkBuilder:
    """
    Builds PyPSA networks from database data.

    Simplified to always create MultiIndex snapshots for consistent multi-period optimization,
    even for single-year models.
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize NetworkBuilder.

        Args:
            verbose: Enable detailed logging output
        """
        self.verbose = verbose

        # Import PyPSA with error handling
        try:
            import pypsa

            self.pypsa = pypsa
        except ImportError as e:
            raise ImportError(
                "PyPSA is not installed or could not be imported. "
                "Please ensure it is installed correctly in the environment."
            ) from e

        # Import batch loader for efficient data loading
        from pyconvexity.solvers.pypsa.batch_loader import PyPSABatchLoader

        self.batch_loader = PyPSABatchLoader()

    def build_network(
        self,
        conn,
        scenario_id: Optional[int] = None,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        include_unmet_loads: bool = True,
    ) -> "pypsa.Network":
        """
        Build complete PyPSA network from database (single network per database).

        Args:
            conn: Database connection
            scenario_id: Optional scenario ID
            progress_callback: Optional progress callback
            include_unmet_loads: Whether to include unmet load components (default: True)

        Returns:
            Configured PyPSA Network object
        """
        if progress_callback:
            progress_callback(0, "Loading network metadata...")

        # Load network info
        network_info = self._load_network_info(conn)

        if progress_callback:
            progress_callback(5, f"Building network: {network_info['name']}")

        # Create PyPSA network
        network = self.pypsa.Network(name=network_info["name"])

        # Set time index
        self._set_time_index(conn, network)

        if progress_callback:
            progress_callback(15, "Loading carriers...")

        # Load carriers
        self._load_carriers(conn, network)

        if progress_callback:
            progress_callback(20, "Loading components...")

        # Load all components using efficient batch loader
        self._load_components(
            conn, network, scenario_id, progress_callback, include_unmet_loads
        )

        # NOTE: Snapshot weightings will be set AFTER multi-period optimization setup
        # in the solver, not here. This matches the old code's approach where PyPSA's
        # multi-period setup can reset snapshot weightings to 1.0

        if progress_callback:
            progress_callback(95, "Network build complete")

        return network

    def load_network_data(
        self, conn, scenario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Load network data as structured dictionary without building PyPSA network (single network per database).

        Args:
            conn: Database connection
            scenario_id: Optional scenario ID

        Returns:
            Dictionary with all network data
        """
        data = {
            "network_info": self._load_network_info(conn),
            "carriers": self._load_carriers_data(conn),
            "components": {},
            "time_periods": [],
        }

        # Load time periods
        try:
            time_periods = get_network_time_periods(conn)
            data["time_periods"] = [
                {
                    "timestamp": tp.formatted_time,
                    "period_index": tp.period_index,
                    "weight": getattr(tp, "weight", 1.0),  # Weight not in new schema
                }
                for tp in time_periods
            ]
        except Exception as e:
            logger.warning(f"Failed to load time periods: {e}")

        # Load all component types
        component_types = [
            "BUS",
            "GENERATOR",
            "UNMET_LOAD",
            "LOAD",
            "LINE",
            "LINK",
            "STORAGE_UNIT",
            "STORE",
        ]

        for comp_type in component_types:
            try:
                components = list_components_by_type(conn, comp_type)
                if components:
                    data["components"][comp_type.lower()] = [
                        {
                            "id": comp.id,
                            "name": comp.name,
                            "component_type": comp.component_type,
                            "longitude": comp.longitude,
                            "latitude": comp.latitude,
                            "carrier_id": comp.carrier_id,
                            "bus_id": comp.bus_id,
                            "bus0_id": comp.bus0_id,
                            "bus1_id": comp.bus1_id,
                        }
                        for comp in components
                    ]
            except Exception as e:
                logger.warning(f"Failed to load {comp_type} components: {e}")

        return data

    def _load_network_info(self, conn) -> Dict[str, Any]:
        """Load network metadata (single network per database)."""
        from pyconvexity.models import get_network_info

        return get_network_info(conn)

    def _set_time_index(self, conn, network: "pypsa.Network"):
        """Set time index from network time periods - always create MultiIndex for consistency."""
        try:
            time_periods = get_network_time_periods(conn)
            if not time_periods:
                logger.error("No time periods found for network")
                return

            # Convert to pandas DatetimeIndex
            timestamps = [pd.Timestamp(tp.formatted_time) for tp in time_periods]

            # Extract unique years for investment periods
            years = sorted(list(set([ts.year for ts in timestamps])))

            # Always create MultiIndex following PyPSA multi-investment tutorial format
            # First level: investment periods (years), Second level: timesteps
            multi_snapshots = []
            for ts in timestamps:
                multi_snapshots.append((ts.year, ts))

            multi_index = pd.MultiIndex.from_tuples(
                multi_snapshots, names=["period", "timestep"]
            )

            # Verify MultiIndex is unique (should always be true now with UTC timestamps)
            if not multi_index.is_unique:
                raise ValueError(
                    f"Created MultiIndex is not unique! Check timestamp generation."
                )

            network.set_snapshots(multi_index)

            # Set investment periods for multi-period optimization
            network.investment_periods = years

            # Store years for statistics
            network._available_years = years

            logger.info(
                f"Time index: {len(multi_index)} snapshots across {len(years)} investment periods: {years}"
            )

        except Exception as e:
            logger.error(f"Failed to set time index: {e}")
            network._available_years = []

    def _load_carriers(self, conn, network: "pypsa.Network"):
        """Load carriers into PyPSA network (single network per database)."""
        carriers = self._load_carriers_data(conn)
        for carrier in carriers:
            filtered_attrs = self._filter_carrier_attrs(carrier)
            network.add("Carrier", carrier["name"], **filtered_attrs)

    def _load_carriers_data(self, conn) -> list:
        """Load carrier data from database (single network per database)."""
        cursor = conn.execute(
            """
            SELECT name, co2_emissions, nice_name, color
            FROM carriers 
            ORDER BY name
        """
        )

        carriers = []
        for row in cursor.fetchall():
            carriers.append(
                {
                    "name": row[0],
                    "co2_emissions": row[1],
                    "nice_name": row[2],
                    "color": row[3],
                }
            )

        return carriers

    def _filter_carrier_attrs(self, carrier: Dict[str, Any]) -> Dict[str, Any]:
        """Filter carrier attributes for PyPSA compatibility."""
        filtered = {}
        for key, value in carrier.items():
            if key != "name" and value is not None:
                filtered[key] = value
        return filtered

    def _load_components(
        self,
        conn,
        network: "pypsa.Network",
        scenario_id: Optional[int],
        progress_callback: Optional[Callable[[int, str], None]] = None,
        include_unmet_loads: bool = True,
    ):
        """Load all network components using batch loader (single network per database)."""
        # Load component connections
        connections = self.batch_loader.batch_load_component_connections(conn)
        bus_id_to_name = connections["bus_id_to_name"]
        carrier_id_to_name = connections["carrier_id_to_name"]

        # Component type mapping for later identification
        component_type_map = {}

        # Load buses
        if progress_callback:
            progress_callback(25, "Loading buses...")
        self._load_buses(conn, network, scenario_id, component_type_map)

        # Load generators (including unmet loads if requested)
        if progress_callback:
            progress_callback(35, "Loading generators...")
        self._load_generators(
            conn,
            network,
            scenario_id,
            bus_id_to_name,
            carrier_id_to_name,
            component_type_map,
            include_unmet_loads,
        )

        # Load loads
        if progress_callback:
            progress_callback(50, "Loading loads...")
        self._load_loads(conn, network, scenario_id, bus_id_to_name, carrier_id_to_name)

        # Load lines
        if progress_callback:
            progress_callback(65, "Loading lines...")
        self._load_lines(conn, network, scenario_id, bus_id_to_name, carrier_id_to_name)

        # Load links
        if progress_callback:
            progress_callback(75, "Loading links...")
        self._load_links(conn, network, scenario_id, bus_id_to_name, carrier_id_to_name)

        # Load storage units
        if progress_callback:
            progress_callback(85, "Loading storage...")
        self._load_storage_units(
            conn, network, scenario_id, bus_id_to_name, carrier_id_to_name
        )
        self._load_stores(
            conn, network, scenario_id, bus_id_to_name, carrier_id_to_name
        )

        # Store component type mapping on network
        network._component_type_map = component_type_map

    def _load_buses(
        self,
        conn,
        network: "pypsa.Network",
        scenario_id: Optional[int],
        component_type_map: Dict[str, str],
    ):
        """Load bus components (single network per database)."""
        buses = list_components_by_type(conn, "BUS")
        bus_ids = [bus.id for bus in buses]

        bus_attributes = self.batch_loader.batch_load_component_attributes(
            conn, bus_ids, scenario_id
        )
        bus_timeseries = self.batch_loader.batch_load_component_timeseries(
            conn, bus_ids, scenario_id
        )

        for bus in buses:
            attrs = bus_attributes.get(bus.id, {})
            timeseries = bus_timeseries.get(bus.id, {})

            # Add coordinate data from components table (PyPSA uses 'x' for longitude, 'y' for latitude)
            if bus.longitude is not None:
                attrs["x"] = bus.longitude
            if bus.latitude is not None:
                attrs["y"] = bus.latitude

            # Merge timeseries into attributes
            attrs.update(timeseries)

            network.add("Bus", bus.name, **attrs)
            component_type_map[bus.name] = bus.component_type

    def _load_generators(
        self,
        conn,
        network: "pypsa.Network",
        scenario_id: Optional[int],
        bus_id_to_name: Dict[int, str],
        carrier_id_to_name: Dict[int, str],
        component_type_map: Dict[str, str],
        include_unmet_loads: bool = True,
    ):
        """Load generator and unmet load components (single network per database)."""
        generators = list_components_by_type(conn, "GENERATOR")

        # Conditionally load unmet loads based on parameter
        if include_unmet_loads:
            unmet_loads = list_components_by_type(conn, "UNMET_LOAD")
            all_generators = generators + unmet_loads
            if self.verbose:
                logger.info(
                    f"Loading {len(generators)} generators and {len(unmet_loads)} unmet loads"
                )
        else:
            all_generators = generators
            if self.verbose:
                logger.info(f"Loading {len(generators)} generators (unmet loads disabled)")

        generator_ids = [gen.id for gen in all_generators]

        generator_attributes = self.batch_loader.batch_load_component_attributes(
            conn, generator_ids, scenario_id
        )
        generator_timeseries = self.batch_loader.batch_load_component_timeseries(
            conn, generator_ids, scenario_id
        )

        for gen in all_generators:
            attrs = generator_attributes.get(gen.id, {})
            timeseries = generator_timeseries.get(gen.id, {})

            # Set bus connection
            if gen.bus_id:
                bus_name = bus_id_to_name.get(gen.bus_id, f"bus_{gen.bus_id}")
                attrs["bus"] = bus_name

            # Set carrier
            if gen.carrier_id:
                carrier_name = carrier_id_to_name.get(gen.carrier_id, "-")
                attrs["carrier"] = carrier_name
            else:
                attrs["carrier"] = "-"

            # Merge timeseries into attributes
            attrs.update(timeseries)

            component_type_map[gen.name] = gen.component_type
            network.add("Generator", gen.name, **attrs)

    def _load_loads(
        self,
        conn,
        network: "pypsa.Network",
        scenario_id: Optional[int],
        bus_id_to_name: Dict[int, str],
        carrier_id_to_name: Dict[int, str],
    ):
        """Load load components (single network per database)."""
        loads = list_components_by_type(conn, "LOAD")
        load_ids = [load.id for load in loads]

        load_attributes = self.batch_loader.batch_load_component_attributes(
            conn, load_ids, scenario_id
        )
        load_timeseries = self.batch_loader.batch_load_component_timeseries(
            conn, load_ids, scenario_id
        )

        for load in loads:
            attrs = load_attributes.get(load.id, {})
            timeseries = load_timeseries.get(load.id, {})

            if load.bus_id:
                bus_name = bus_id_to_name.get(load.bus_id, f"bus_{load.bus_id}")
                attrs["bus"] = bus_name

            if load.carrier_id:
                carrier_name = carrier_id_to_name.get(load.carrier_id, "-")
                attrs["carrier"] = carrier_name
            else:
                attrs["carrier"] = "-"

            # Merge timeseries into attributes
            attrs.update(timeseries)

            network.add("Load", load.name, **attrs)

    def _load_lines(
        self,
        conn,
        network: "pypsa.Network",
        scenario_id: Optional[int],
        bus_id_to_name: Dict[int, str],
        carrier_id_to_name: Dict[int, str],
    ):
        """Load line components (single network per database)."""
        lines = list_components_by_type(conn, "LINE")
        line_ids = [line.id for line in lines]

        line_attributes = self.batch_loader.batch_load_component_attributes(
            conn, line_ids, scenario_id
        )
        line_timeseries = self.batch_loader.batch_load_component_timeseries(
            conn, line_ids, scenario_id
        )

        for line in lines:
            attrs = line_attributes.get(line.id, {})
            timeseries = line_timeseries.get(line.id, {})

            if line.bus0_id and line.bus1_id:
                bus0_name = bus_id_to_name.get(line.bus0_id, f"bus_{line.bus0_id}")
                bus1_name = bus_id_to_name.get(line.bus1_id, f"bus_{line.bus1_id}")
                attrs["bus0"] = bus0_name
                attrs["bus1"] = bus1_name

            if line.carrier_id:
                carrier_name = carrier_id_to_name.get(line.carrier_id, "AC")
                attrs["carrier"] = carrier_name
            else:
                attrs["carrier"] = "AC"

            # Merge timeseries into attributes
            attrs.update(timeseries)

            network.add("Line", line.name, **attrs)

    def _load_links(
        self,
        conn,
        network: "pypsa.Network",
        scenario_id: Optional[int],
        bus_id_to_name: Dict[int, str],
        carrier_id_to_name: Dict[int, str],
    ):
        """Load link components (single network per database)."""
        links = list_components_by_type(conn, "LINK")
        link_ids = [link.id for link in links]

        link_attributes = self.batch_loader.batch_load_component_attributes(
            conn, link_ids, scenario_id
        )
        link_timeseries = self.batch_loader.batch_load_component_timeseries(
            conn, link_ids, scenario_id
        )

        for link in links:
            attrs = link_attributes.get(link.id, {})
            timeseries = link_timeseries.get(link.id, {})

            if link.bus0_id and link.bus1_id:
                bus0_name = bus_id_to_name.get(link.bus0_id, f"bus_{link.bus0_id}")
                bus1_name = bus_id_to_name.get(link.bus1_id, f"bus_{link.bus1_id}")
                attrs["bus0"] = bus0_name
                attrs["bus1"] = bus1_name

            if link.carrier_id:
                carrier_name = carrier_id_to_name.get(link.carrier_id, "DC")
                attrs["carrier"] = carrier_name
            else:
                attrs["carrier"] = "DC"

            # Merge timeseries into attributes
            attrs.update(timeseries)

            network.add("Link", link.name, **attrs)

    def _load_storage_units(
        self,
        conn,
        network: "pypsa.Network",
        scenario_id: Optional[int],
        bus_id_to_name: Dict[int, str],
        carrier_id_to_name: Dict[int, str],
    ):
        """Load storage unit components (single network per database)."""
        storage_units = list_components_by_type(conn, "STORAGE_UNIT")
        storage_ids = [storage.id for storage in storage_units]

        storage_attributes = self.batch_loader.batch_load_component_attributes(
            conn, storage_ids, scenario_id
        )
        storage_timeseries = self.batch_loader.batch_load_component_timeseries(
            conn, storage_ids, scenario_id
        )

        for storage in storage_units:
            attrs = storage_attributes.get(storage.id, {})
            timeseries = storage_timeseries.get(storage.id, {})

            if storage.bus_id:
                bus_name = bus_id_to_name.get(storage.bus_id, f"bus_{storage.bus_id}")
                attrs["bus"] = bus_name

            if storage.carrier_id:
                carrier_name = carrier_id_to_name.get(storage.carrier_id, "-")
                attrs["carrier"] = carrier_name
            else:
                attrs["carrier"] = "-"

            # Merge timeseries into attributes
            attrs.update(timeseries)

            network.add("StorageUnit", storage.name, **attrs)

    def _load_stores(
        self,
        conn,
        network: "pypsa.Network",
        scenario_id: Optional[int],
        bus_id_to_name: Dict[int, str],
        carrier_id_to_name: Dict[int, str],
    ):
        """Load store components (single network per database)."""
        stores = list_components_by_type(conn, "STORE")
        store_ids = [store.id for store in stores]

        store_attributes = self.batch_loader.batch_load_component_attributes(
            conn, store_ids, scenario_id
        )
        store_timeseries = self.batch_loader.batch_load_component_timeseries(
            conn, store_ids, scenario_id
        )

        for store in stores:
            attrs = store_attributes.get(store.id, {})
            timeseries = store_timeseries.get(store.id, {})

            if store.bus_id:
                bus_name = bus_id_to_name.get(store.bus_id, f"bus_{store.bus_id}")
                attrs["bus"] = bus_name

            if store.carrier_id:
                carrier_name = carrier_id_to_name.get(store.carrier_id, "-")
                attrs["carrier"] = carrier_name
            else:
                attrs["carrier"] = "-"

            # Merge timeseries into attributes
            attrs.update(timeseries)

            network.add("Store", store.name, **attrs)

    def _set_snapshot_weightings(self, conn, network: "pypsa.Network"):
        """Set snapshot weightings from time periods (single network per database)."""
        try:
            time_periods = get_network_time_periods(conn)
            if time_periods and len(network.snapshots) > 0:
                # Get network info to determine time interval
                network_info = get_network_info(conn)
                time_interval = network_info.get("time_interval", "PT1H")
                weight = self._parse_time_interval(time_interval)
                if weight is None:
                    weight = 1.0

                # Create weightings array - all periods get same weight
                weightings = [weight] * len(time_periods)

                if len(weightings) == len(network.snapshots):
                    # Set all three columns like the old code - critical for proper objective calculation
                    network.snapshot_weightings.loc[:, "objective"] = weightings
                    network.snapshot_weightings.loc[:, "generators"] = weightings
                    network.snapshot_weightings.loc[:, "stores"] = weightings
                else:
                    logger.warning(
                        f"Mismatch between weightings ({len(weightings)}) and snapshots ({len(network.snapshots)})"
                    )
        except Exception as e:
            logger.warning(f"Failed to set snapshot weightings: {e}")

    def _parse_time_interval(self, time_interval: str) -> Optional[float]:
        """Parse time interval string to hours."""
        if not time_interval:
            return None

        try:
            # Handle pandas frequency strings
            if time_interval.endswith("H"):
                return float(time_interval[:-1])
            elif time_interval.endswith("D"):
                return float(time_interval[:-1]) * 24
            elif time_interval.endswith("M"):
                return float(time_interval[:-1]) / 60
            elif time_interval.endswith("S"):
                return float(time_interval[:-1]) / 3600
            else:
                # Try to parse as float (assume hours)
                return float(time_interval)
        except (ValueError, TypeError):
            logger.warning(f"Could not parse time interval: {time_interval}")
            return None

    def _build_bus_id_to_name_map(self, conn) -> Dict[int, str]:
        """Build mapping from bus IDs to names (single network per database)."""
        buses = list_components_by_type(conn, "BUS")
        return {bus.id: bus.name for bus in buses}

    def _build_carrier_id_to_name_map(self, conn) -> Dict[int, str]:
        """Build mapping from carrier IDs to names (single network per database)."""
        cursor = conn.execute("SELECT id, name FROM carriers")
        return {row[0]: row[1] for row in cursor.fetchall()}
