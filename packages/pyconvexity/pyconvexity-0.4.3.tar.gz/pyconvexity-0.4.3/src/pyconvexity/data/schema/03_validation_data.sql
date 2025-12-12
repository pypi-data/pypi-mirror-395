-- ============================================================================
-- PYPSA ATTRIBUTE VALIDATION RULES
-- Complete set of validation rules for all component types
-- Based on PyPSA component attribute definitions
-- Updated to use new 10-group system: basic, capacity, power_limits, energy, unit_commitment, ramping, costs, electrical, energy, outputs
-- Version 2.2.0
-- ============================================================================

-- Clear any existing validation rules
DELETE FROM attribute_validation_rules;

-- ============================================================================
-- BUS ATTRIBUTES
-- ============================================================================

-- BUS attributes from buses.csv (PyPSA reference) - Updated to new 10-group system
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name, to_save) VALUES
-- Input attributes for BUS
('BUS', 'v_nom', 'Nominal Voltage', 'float', 'kV', '1', 'static', TRUE, TRUE, 'The standard or average voltage of a bus in the network.', 0, NULL, 'electrical', FALSE),
('BUS', 'type', 'Type', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Placeholder. Not yet implemented.', NULL, NULL, 'basic', FALSE),
('BUS', 'x', 'Longitude', 'float', 'n/a', '0', 'static', TRUE, TRUE, 'Longitude; A measurement of angular distance, expressed in degrees, east or west of the Prime Meridian.', NULL, NULL, 'basic', FALSE),
('BUS', 'y', 'Latitude', 'float', 'n/a', '0', 'static', TRUE, TRUE, 'Latitude; A measurement of angular distance, expressed in degrees, north or south of the Equator.', NULL, NULL, 'basic', FALSE),
('BUS', 'carrier', 'Carrier', 'string', 'n/a', 'AC', 'static', TRUE, TRUE, 'Carrier: can be "AC" or "DC" for electrical buses, or "heat" or "gas" for thermal buses.', NULL, NULL, 'basic', FALSE),
('BUS', 'unit', 'Unit', 'string', 'n/a', 'None', 'static', FALSE, TRUE, 'Unit of the bus'' carrier if the implicitly assumed unit ("MW") is inappropriate (e.g. "t/h", "MWh_th/h"). Only descriptive. Does not influence any functions.', NULL, NULL, 'basic', FALSE),
('BUS', 'v_mag_pu_set', 'Voltage Magnitude Setpoint', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'Voltage magnitude set point, per unit of the nominal voltage (v_nom).', 0, NULL, 'electrical', FALSE),
('BUS', 'v_mag_pu_min', 'Min Voltage Magnitude', 'float', 'per unit', '0', 'static', FALSE, TRUE, 'Minimum desired voltage, per unit of the nominal voltage (v_nom). This is a placeholder attribute and is not currently used by any functions.', 0, NULL, 'electrical', FALSE),
('BUS', 'v_mag_pu_max', 'Max Voltage Magnitude', 'float', 'per unit', 'inf', 'static', FALSE, TRUE, 'Maximum desired voltage, per unit of the nominal voltage (v_nom). This is a placeholder attribute and is not currently used by any functions.', 0, NULL, 'electrical', FALSE),
-- Output attributes for BUS
('BUS', 'control', 'Control Strategy', 'string', 'n/a', 'PQ', 'static', FALSE, FALSE, 'P,Q,V control strategy for PF, must be "PQ", "PV" or "Slack". Note that this attribute is an output inherited from the controls of the generators attached to the bus; setting it directly on the bus will not have any effect.', NULL, NULL, 'electrical', FALSE),
('BUS', 'generator', 'Slack Generator', 'string', 'n/a', 'n/a', 'static', FALSE, FALSE, 'Name of slack generator attached to slack bus.', NULL, NULL, 'electrical', FALSE),
('BUS', 'sub_network', 'Sub-Network', 'string', 'n/a', 'n/a', 'static', FALSE, FALSE, 'Name of connected sub-network to which bus belongs. This attribute is set by PyPSA in the function network.determine_network_topology(); do not set it directly by hand.', NULL, NULL, 'basic', FALSE),
('BUS', 'p', 'Active Power', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power at bus (positive if net generation at bus)', NULL, NULL, 'electrical', TRUE),
('BUS', 'q', 'Reactive Power', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'reactive power (positive if net generation at bus)', NULL, NULL, 'electrical', TRUE),
('BUS', 'v_mag_pu', 'Voltage Magnitude', 'float', 'per unit', '1', 'timeseries', FALSE, FALSE, 'Voltage magnitude, per unit of v_nom', NULL, NULL, 'electrical', TRUE),
('BUS', 'v_ang', 'Voltage Angle', 'float', 'radians', '0', 'timeseries', FALSE, FALSE, 'Voltage angle', NULL, NULL, 'electrical', TRUE),
('BUS', 'marginal_price', 'Marginal Price', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Locational marginal price from LOPF from power balance constraint', NULL, NULL, 'costs', TRUE);

-- ============================================================================
-- GENERATOR ATTRIBUTES  
-- ============================================================================

-- GENERATOR attributes from generators.csv (PyPSA reference) - Updated to new 10-group system
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for GENERATOR
('GENERATOR', 'control', 'Control Strategy', 'string', 'n/a', 'PQ', 'static', FALSE, TRUE, 'Power flow control mode: "PQ" (fixed active and reactive power), "PV" (fixed active power and voltage magnitude), or "Slack" (balances system power, typically one per network).', NULL, NULL, 'electrical'),
('GENERATOR', 'type', 'Type', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Placeholder for generator type. Not yet implemented.', NULL, NULL, 'basic'),
('GENERATOR', 'p_nom', 'Nominal Power', 'float', 'MW', '0', 'static', TRUE, TRUE, 'The maximum rated capacity of the generator in MW. This sets the upper limit for power output in all calculations.', 0, NULL, 'capacity'),
('GENERATOR', 'p_nom_mod', 'Nominal Power Module', 'float', 'MW', '0', 'static', FALSE, TRUE, 'The unit size for capacity expansion. When extending the nominal power (p_nom), it can only be increased in multiples of this module size.', 0, NULL, 'capacity'),
('GENERATOR', 'p_nom_extendable', 'Extendable Capacity', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Switch to allow the nominal power (p_nom) to be extended in optimization.', NULL, NULL, 'capacity'),
('GENERATOR', 'p_nom_min', 'Min Nominal Power', 'float', 'MW', '0', 'static', FALSE, TRUE, 'If the nominal power (p_nom) is extendable in optimization, set its minimum value.', 0, NULL, 'capacity'),
('GENERATOR', 'p_nom_max', 'Max Nominal Power', 'float', 'MW', 'inf', 'static', FALSE, TRUE, 'If the nominal power (p_nom) is extendable in optimization, set its maximum value (e.g. limited by technical potential).', 0, NULL, 'capacity'),
('GENERATOR', 'p_min_pu', 'Min Capacity Factor', 'float', 'per unit', '0', 'static_or_timeseries', FALSE, TRUE, 'The minimum output for each snapshot per unit of the nominal power (p_nom) for the optimization (e.g. for variable renewable generators this can change due to weather conditions and compulsory feed-in; for conventional generators it represents a minimal dispatch). Note that if committable is False and the min capacity factor (p_min_pu) > 0, this represents a must-run condition.', 0, NULL, 'power_limits'),
('GENERATOR', 'p_max_pu', 'Max Capacity Factor', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'The maximum output for each snapshot per unit of the nominal power (p_nom) for the optimization (e.g. for variable renewable generators this can change due to weather conditions; for conventional generators it represents a maximum dispatch).', 0, 1, 'power_limits'),
('GENERATOR', 'p_set', 'Active Power Setpoint', 'float', 'MW', '0', 'static_or_timeseries', FALSE, TRUE, 'Fixed active power output that the generator must produce. Used when the generator output is predetermined rather than optimized.', NULL, NULL, 'power_limits'),
('GENERATOR', 'e_sum_min', 'Min Energy Sum', 'float', 'MWh', '-inf', 'static', FALSE, TRUE, 'The minimum total energy that must be produced over the entire time period being optimized (the optimization horizon).', NULL, NULL, 'energy'),
('GENERATOR', 'e_sum_max', 'Max Energy Sum', 'float', 'MWh', 'inf', 'static', FALSE, TRUE, 'The maximum total energy that can be produced over the entire time period being optimized (the optimization horizon).', NULL, NULL, 'energy'),
('GENERATOR', 'q_set', 'Reactive Power Setpoint', 'float', 'MVar', '0', 'static_or_timeseries', FALSE, TRUE, 'Fixed reactive power output that the generator must produce. Used when the reactive power output is predetermined rather than optimized.', NULL, NULL, 'power_limits'),
('GENERATOR', 'sign', 'Power Sign', 'float', 'n/a', '1', 'static', FALSE, TRUE, 'Power flow direction convention: 1 for generation (positive power flows into the network), -1 for consumption (positive power flows out of the network).', NULL, NULL, 'power_limits'),
('GENERATOR', 'carrier', 'Carrier', 'string', 'n/a', 'n/a', 'static', TRUE, TRUE, 'Prime mover Carrier (e.g. coal, gas, wind, solar); required for global constraints on primary energy in optimization', NULL, NULL, 'basic'),
('GENERATOR', 'marginal_cost', 'Marginal Cost', 'float', 'currency/MWh', '0', 'static_or_timeseries', TRUE, TRUE, 'The variable cost of producing one additional MWh of electricity. Used by the optimizer to determine the economic dispatch order of generators (lower cost generators are dispatched first).', 0, NULL, 'costs'),
('GENERATOR', 'marginal_cost_quadratic', 'Quadratic Marginal Cost', 'float', 'currency/MWh', '0', 'static_or_timeseries', FALSE, TRUE, 'Quadratic term for non-linear cost curves. When set, the total cost includes a quadratic component that increases with the square of output, modeling increasing marginal costs at higher generation levels.', 0, NULL, 'costs'),
('GENERATOR', 'capital_cost', 'Capital Cost', 'float', 'currency/MW', '0', 'static', FALSE, TRUE, 'The cost per MW of adding new capacity. Includes investment costs (spread over the planning period) and fixed operations & maintenance costs. Only relevant when extendable capacity (p_nom_extendable) is True.', 0, NULL, 'costs'),
('GENERATOR', 'active', 'Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether this generator is active and should be included in network calculations. Set to False to temporarily disable the generator without deleting it.', NULL, NULL, 'basic'),
('GENERATOR', 'build_year', 'Build Year', 'int', 'year', '0', 'static', FALSE, TRUE, 'The year when the generator can be built or commissioned. Essential for multi-year capacity expansion planning models, which determine optimal investment timing and generator retirement schedules.', 0, 3000, 'capacity'),
('GENERATOR', 'lifetime', 'Lifetime', 'float', 'years', 'inf', 'static', FALSE, TRUE, 'The operational lifetime of the generator in years. Essential for multi-year capacity expansion planning models, which use this to determine when generators retire (build year (build_year) + lifetime). Set to "inf" for generators that never retire.', 0, NULL, 'capacity'),
('GENERATOR', 'efficiency', 'Efficiency', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'Ratio between primary energy and electrical energy, e.g. takes value 0.4 MWh_elec/MWh_thermal for gas. This is required for global constraints on primary energy in optimization.', 0, 1, 'energy'),
('GENERATOR', 'committable', 'Committable', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Enable unit commitment, allowing the generator to be turned on or off with associated start-up and shutdown costs. Only available when the nominal power (p_nom) is not extendable.', NULL, NULL, 'unit_commitment'),
('GENERATOR', 'start_up_cost', 'Start-up Cost', 'float', 'currency', '0', 'static', FALSE, TRUE, 'Cost to start up the generator. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('GENERATOR', 'shut_down_cost', 'Shutdown Cost', 'float', 'currency', '0', 'static', FALSE, TRUE, 'Cost to shut down the generator. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('GENERATOR', 'stand_by_cost', 'Stand-by Cost', 'float', 'currency/h', '0', 'static_or_timeseries', FALSE, TRUE, 'Stand-by cost for operating the generator at null power output.', 0, NULL, 'unit_commitment'),
('GENERATOR', 'min_up_time', 'Min Up Time', 'int', 'snapshots', '0', 'static', FALSE, TRUE, 'Minimum number of snapshots for status to be 1. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('GENERATOR', 'min_down_time', 'Min Down Time', 'int', 'snapshots', '0', 'static', FALSE, TRUE, 'Minimum number of snapshots for status to be 0. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('GENERATOR', 'up_time_before', 'Up Time Before', 'int', 'snapshots', '1', 'static', FALSE, TRUE, 'Number of snapshots that the generator was online before network.snapshots start. Only read if committable (committable) is True and min up time (min_up_time) is non-zero.', 0, NULL, 'unit_commitment'),
('GENERATOR', 'down_time_before', 'Down Time Before', 'int', 'snapshots', '0', 'static', FALSE, TRUE, 'Number of snapshots that the generator was offline before network.snapshots start. Only read if committable (committable) is True and min down time (min_down_time) is non-zero.', 0, NULL, 'unit_commitment'),
('GENERATOR', 'ramp_limit_up', 'Ramp Up Limit', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'Maximum active power increase from one snapshot to the next, per unit of the nominal power (p_nom). Ignored if 1.', NULL, NULL, 'ramping'),
('GENERATOR', 'ramp_limit_down', 'Ramp Down Limit', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'Maximum active power decrease from one snapshot to the next, per unit of the nominal power (p_nom). Ignored if 1.', NULL, NULL, 'ramping'),
('GENERATOR', 'ramp_limit_start_up', 'Ramp Up at Start', 'float', 'per unit', '1', 'static', FALSE, TRUE, 'Maximum active power increase at start up, per unit of the nominal power (p_nom). Only read if committable (committable) is True.', NULL, NULL, 'ramping'),
('GENERATOR', 'ramp_limit_shut_down', 'Ramp Down at Shutdown', 'float', 'per unit', '1', 'static', FALSE, TRUE, 'Maximum active power decrease at shut down, per unit of the nominal power (p_nom). Only read if committable (committable) is True.', NULL, NULL, 'ramping'),
('GENERATOR', 'weight', 'Weight', 'float', 'n/a', '1', 'static', FALSE, TRUE, 'Weighting factor used when aggregating or clustering multiple generators into representative units. Higher weights indicate generators that should be prioritized in clustering algorithms.', NULL, NULL, 'basic'),
-- Output attributes for GENERATOR (from PyPSA generators.csv lines 38-46)
('GENERATOR', 'p', 'Active Power', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power at bus (positive if net generation)', NULL, NULL, 'electrical'),
('GENERATOR', 'q', 'Reactive Power', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'reactive power (positive if net generation)', NULL, NULL, 'electrical'),
('GENERATOR', 'p_nom_opt', 'Optimised Nominal Power', 'float', 'MW', '0', 'static', FALSE, FALSE, 'Optimised nominal power (p_nom).', 0, NULL, 'capacity'),
('GENERATOR', 'status', 'Status', 'float', 'n/a', '1', 'timeseries', FALSE, FALSE, 'Status (1 is on, 0 is off). Only outputted if committable (committable) is True.', NULL, NULL, 'unit_commitment'),
('GENERATOR', 'mu_upper', 'Shadow Price Upper', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper nominal power (p_nom) limit', NULL, NULL, 'costs'),
('GENERATOR', 'mu_lower', 'Shadow Price Lower', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower nominal power (p_nom) limit', NULL, NULL, 'costs'),
('GENERATOR', 'mu_p_set', 'Shadow Price P Set', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of fixed power generation active power setpoint (p_set)', NULL, NULL, 'costs'),
('GENERATOR', 'mu_ramp_limit_up', 'Shadow Price Ramp Up', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper ramp up limit', NULL, NULL, 'ramping'),
('GENERATOR', 'mu_ramp_limit_down', 'Shadow Price Ramp Down', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower ramp down limit', NULL, NULL, 'ramping');

-- ============================================================================
-- LOAD ATTRIBUTES
-- ============================================================================

-- LOAD attributes from loads.csv (PyPSA reference) - Updated to new 10-group system
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for LOAD
('LOAD', 'carrier', 'Carrier', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Carrier type for the load: "AC" or "DC" for electrical loads, or "heat" or "gas" for thermal loads. Used for categorization and energy balance constraints.', NULL, NULL, 'basic'),
('LOAD', 'type', 'Type', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Placeholder for load type. Not yet implemented.', NULL, NULL, 'basic'),
('LOAD', 'p_set', 'Active Power Demand', 'float', 'MW', '0', 'static_or_timeseries', TRUE, TRUE, 'The active power demand of the load in MW. This is the real power that the load consumes from the network. Can be static or time-varying.', NULL, NULL, 'power_limits'),
('LOAD', 'q_set', 'Reactive Power Demand', 'float', 'MVar', '0', 'static_or_timeseries', FALSE, TRUE, 'The reactive power demand of the load in MVar. Positive values indicate inductive loads (lagging power factor), negative values indicate capacitive loads (leading power factor). Can be static or time-varying.', NULL, NULL, 'power_limits'),
('LOAD', 'sign', 'Power Sign', 'float', 'n/a', '-1', 'static', FALSE, TRUE, 'Power flow direction convention: -1 for loads (positive power flows out of the network), 1 for generation (positive power flows into the network). Typically -1 for loads.', NULL, NULL, 'power_limits'),
('LOAD', 'active', 'Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether this load is active and should be included in network calculations. Set to False to temporarily disable the load without deleting it.', NULL, NULL, 'basic'),
-- Output attributes for LOAD (PyPSA load outputs)
('LOAD', 'p', 'Active Power', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power consumption (positive if consuming)', NULL, NULL, 'electrical'),
('LOAD', 'q', 'Reactive Power', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'reactive power consumption (positive if consuming)', NULL, NULL, 'electrical');

-- ============================================================================
-- LINE ATTRIBUTES
-- ============================================================================

-- LINE attributes from lines.csv (PyPSA reference) - Updated to new 10-group system
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for LINE
('LINE', 'type', 'Type', 'string', 'n/a', '', 'static', FALSE, TRUE, 'Name of a predefined line standard type. If set, the line standard impedance parameters are automatically calculated from the line length (length) and number of parallel lines (num_parallel), overriding any manually set values for series reactance (x), series resistance (r), and shunt susceptance (b). Leave empty to manually specify impedance parameters.', NULL, NULL, 'basic'),
('LINE', 'x', 'Series Reactance', 'float', 'Ohm', '0', 'static', TRUE, TRUE, 'The series reactance of the line in Ohms. Must be non-zero for AC lines in power flow calculations. If the line has series inductance L in Henries, then x = 2πfL where f is the frequency in Hertz. The series impedance is z = r + jx. Ignored if line type (type) is set.', 0, NULL, 'electrical'),
('LINE', 'r', 'Series Resistance', 'float', 'Ohm', '0', 'static', FALSE, TRUE, 'The series resistance of the line in Ohms. Must be non-zero for DC lines in power flow calculations. The series impedance is z = r + jx. Ignored if line type (type) is set.', 0, NULL, 'electrical'),
('LINE', 'g', 'Shunt Conductance', 'float', 'Siemens', '0', 'static', FALSE, TRUE, 'The shunt conductance of the line in Siemens. The shunt admittance is y = g + jb, where b is the shunt susceptance (b).', 0, NULL, 'electrical'),
('LINE', 'b', 'Shunt Susceptance', 'float', 'Siemens', '0', 'static', FALSE, TRUE, 'The shunt susceptance of the line in Siemens. If the line has shunt capacitance C in Farads, then b = 2πfC where f is the frequency in Hertz. The shunt admittance is y = g + jb, where g is the shunt conductance (g). Ignored if line type (type) is set.', NULL, NULL, 'electrical'),
('LINE', 's_nom', 'Nominal Apparent Power', 'float', 'MVA', '0', 'static', TRUE, TRUE, 'The maximum apparent power capacity of the line in MVA. This sets the thermal limit for power flow through the line.', 0, NULL, 'capacity'),
('LINE', 's_nom_mod', 'Nominal Power Module', 'float', 'MVA', '0', 'static', FALSE, TRUE, 'The unit size for capacity expansion. When extending the nominal apparent power (s_nom), it can only be increased in multiples of this module size.', 0, NULL, 'capacity'),
('LINE', 's_nom_extendable', 'Extendable Capacity', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Switch to allow the nominal apparent power (s_nom) to be extended in optimization.', NULL, NULL, 'capacity'),
('LINE', 's_nom_min', 'Min Nominal Power', 'float', 'MVA', '0', 'static', FALSE, TRUE, 'If the nominal apparent power (s_nom) is extendable in optimization, set its minimum value.', 0, NULL, 'capacity'),
('LINE', 's_nom_max', 'Max Nominal Power', 'float', 'MVA', 'inf', 'static', FALSE, TRUE, 'If the nominal apparent power (s_nom) is extendable in optimization, set its maximum value (e.g. limited by technical potential or right-of-way constraints).', 0, NULL, 'capacity'),
('LINE', 's_max_pu', 'Max Power Factor', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'The maximum allowed absolute flow per unit of the nominal apparent power (s_nom). Can be set less than 1 to account for security margins (e.g., n-1 contingency), or can be time-varying to represent weather-dependent dynamic line rating for overhead lines.', 0, 1, 'power_limits'),
('LINE', 'capital_cost', 'Capital Cost', 'float', 'currency/MVA', '0', 'static', FALSE, TRUE, 'The cost per MVA of adding new line capacity. Includes investment costs (spread over the planning period) and fixed operations & maintenance costs. Only relevant when extendable capacity (s_nom_extendable) is True.', 0, NULL, 'costs'),
('LINE', 'active', 'Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether this line is active and should be included in network calculations. Set to False to temporarily disable the line without deleting it.', NULL, NULL, 'basic'),
('LINE', 'build_year', 'Build Year', 'int', 'year', '0', 'static', FALSE, TRUE, 'The year when the line can be built or commissioned. Essential for multi-year capacity expansion planning models, which determine optimal investment timing and line retirement schedules.', 0, 3000, 'capacity'),
('LINE', 'lifetime', 'Lifetime', 'float', 'years', 'inf', 'static', FALSE, TRUE, 'The operational lifetime of the line in years. Essential for multi-year capacity expansion planning models, which use this to determine when lines retire (build year (build_year) + lifetime). Set to "inf" for lines that never retire.', 0, NULL, 'capacity'),
('LINE', 'length', 'Line Length', 'float', 'km', '0', 'static', FALSE, TRUE, 'The physical length of the line in kilometers. Required when line type (type) is set to calculate impedance parameters automatically. Also used for calculating capital costs.', 0, NULL, 'electrical'),
('LINE', 'carrier', 'Carrier', 'string', 'n/a', '', 'static', FALSE, TRUE, 'Carrier type for the line. Must be "AC" (alternating current) as lines only support AC transmission.', NULL, NULL, 'basic'),
('LINE', 'terrain_factor', 'Terrain Factor', 'float', 'per unit', '1', 'static', FALSE, TRUE, 'Multiplier for capital cost to account for difficult terrain. Values greater than 1 increase the capital cost (capital_cost) to reflect higher construction costs in challenging terrain (e.g., mountains, water crossings).', 0, NULL, 'electrical'),
('LINE', 'num_parallel', 'Number of Parallel Lines', 'float', 'n/a', '1', 'static', FALSE, TRUE, 'The number of parallel transmission circuits (can be fractional). When line type (type) is set, this is used to calculate the total impedance (more parallel lines reduce effective impedance). If line type (type) is empty, this value is ignored.', 1, NULL, 'electrical'),
('LINE', 'v_ang_min', 'Min Voltage Angle Diff', 'float', 'Degrees', '-inf', 'static', FALSE, TRUE, 'Minimum voltage angle difference across the line in degrees. This is a placeholder attribute and is not currently used by any functions.', NULL, NULL, 'electrical'),
('LINE', 'v_ang_max', 'Max Voltage Angle Diff', 'float', 'Degrees', 'inf', 'static', FALSE, TRUE, 'Maximum voltage angle difference across the line in degrees. This is a placeholder attribute and is not currently used by any functions.', NULL, NULL, 'electrical'),
-- Output attributes for LINE (PyPSA line outputs)
('LINE', 'p0', 'Active Power Bus0', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power at bus0 (positive if power flows from bus0 to bus1)', NULL, NULL, 'electrical'),
('LINE', 'p1', 'Active Power Bus1', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power at bus1 (positive if power flows from bus1 to bus0)', NULL, NULL, 'electrical'),
('LINE', 'q0', 'Reactive Power Bus0', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'reactive power at bus0', NULL, NULL, 'electrical'),
('LINE', 'q1', 'Reactive Power Bus1', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'reactive power at bus1', NULL, NULL, 'electrical'),
('LINE', 's_nom_opt', 'Optimised Apparent Power', 'float', 'MVA', '0', 'static', FALSE, FALSE, 'Optimised nominal apparent power (s_nom) from capacity expansion optimization.', 0, NULL, 'capacity'),
('LINE', 'mu_upper', 'Shadow Price Upper', 'float', 'currency/MVA', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper nominal apparent power (s_nom) limit', NULL, NULL, 'costs'),
('LINE', 'mu_lower', 'Shadow Price Lower', 'float', 'currency/MVA', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower nominal apparent power (s_nom) limit', NULL, NULL, 'costs'),
('LINE', 'sub_network', 'Sub-Network', 'string', 'n/a', 'n/a', 'static', FALSE, FALSE, 'Name of connected sub-network to which line belongs. This attribute is set by PyPSA.', NULL, NULL, 'basic'),
('LINE', 'x_pu', 'Per Unit Reactance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit series reactance calculated from the series reactance (x) and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('LINE', 'r_pu', 'Per Unit Resistance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit series resistance calculated from the series resistance (r) and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('LINE', 'g_pu', 'Per Unit Conductance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit shunt conductance calculated from the shunt conductance (g) and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('LINE', 'b_pu', 'Per Unit Susceptance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit shunt susceptance calculated from the shunt susceptance (b) and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('LINE', 'x_pu_eff', 'Effective Per Unit Reactance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Effective per unit series reactance for linear power flow', NULL, NULL, 'electrical'),
('LINE', 'r_pu_eff', 'Effective Per Unit Resistance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Effective per unit series resistance for linear power flow', NULL, NULL, 'electrical');

-- ============================================================================
-- LINK ATTRIBUTES
-- ============================================================================

-- LINK attributes from links.csv (PyPSA reference) - Updated to new 10-group system
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for LINK
('LINK', 'type', 'Type', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Placeholder for link type. Not yet implemented.', NULL, NULL, 'basic'),
('LINK', 'carrier', 'Carrier', 'string', 'n/a', '', 'static', FALSE, TRUE, 'Carrier type transported by the link: "DC" for electrical HVDC links, or "heat" or "gas" for thermal links. Used for categorization and energy balance constraints.', NULL, NULL, 'basic'),
('LINK', 'efficiency', 'Transfer Efficiency', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'The efficiency of power transfer from bus0 to bus1. A value of 1.0 means no losses, while lower values represent transmission losses. Can be time-varying to model temperature-dependent performance (e.g., heat pump Coefficient of Performance).', 0, 1, 'energy'),
('LINK', 'active', 'Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether this link is active and should be included in network calculations. Set to False to temporarily disable the link without deleting it.', NULL, NULL, 'basic'),
('LINK', 'build_year', 'Build Year', 'int', 'year', '0', 'static', FALSE, TRUE, 'The year when the link can be built or commissioned. Essential for multi-year capacity expansion planning models, which determine optimal investment timing and link retirement schedules.', 0, 3000, 'capacity'),
('LINK', 'lifetime', 'Lifetime', 'float', 'years', 'inf', 'static', FALSE, TRUE, 'The operational lifetime of the link in years. Essential for multi-year capacity expansion planning models, which use this to determine when links retire (build year (build_year) + lifetime). Set to "inf" for links that never retire.', 0, NULL, 'capacity'),
('LINK', 'p_nom', 'Nominal Power', 'float', 'MW', '0', 'static', TRUE, TRUE, 'The maximum active power capacity of the link in MW. This sets the limit for power flow through the link.', 0, NULL, 'capacity'),
('LINK', 'p_nom_mod', 'Nominal Power Module', 'float', 'MW', '0', 'static', FALSE, TRUE, 'The unit size for capacity expansion. When extending the nominal power (p_nom), it can only be increased in multiples of this module size.', 0, NULL, 'capacity'),
('LINK', 'p_nom_extendable', 'Extendable Capacity', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Switch to allow the nominal power (p_nom) to be extended in optimization.', NULL, NULL, 'capacity'),
('LINK', 'p_nom_min', 'Min Nominal Power', 'float', 'MW', '0', 'static', FALSE, TRUE, 'If the nominal power (p_nom) is extendable in optimization, set its minimum value.', 0, NULL, 'capacity'),
('LINK', 'p_nom_max', 'Max Nominal Power', 'float', 'MW', 'inf', 'static', FALSE, TRUE, 'If the nominal power (p_nom) is extendable in optimization, set its maximum value (e.g. limited by technical potential or right-of-way constraints).', 0, NULL, 'capacity'),
('LINK', 'p_set', 'Power Setpoint', 'float', 'MW', '0', 'static_or_timeseries', FALSE, TRUE, 'Fixed active power flow that the link must transfer from bus0 to bus1. Used when the link power flow is predetermined rather than optimized.', NULL, NULL, 'power_limits'),
('LINK', 'p_min_pu', 'Min Capacity Factor', 'float', 'per unit of p_nom', '0', 'static_or_timeseries', FALSE, TRUE, 'The minimum power flow per unit of the nominal power (p_nom). Negative values allow reverse flow (from bus1 to bus0). Can be static or time-varying.', NULL, NULL, 'power_limits'),
('LINK', 'p_max_pu', 'Max Capacity Factor', 'float', 'per unit of p_nom', '1', 'static_or_timeseries', FALSE, TRUE, 'The maximum power flow per unit of the nominal power (p_nom). Negative values allow reverse flow (from bus1 to bus0). Can be static or time-varying.', NULL, NULL, 'power_limits'),
('LINK', 'capital_cost', 'Capital Cost', 'float', 'currency/MW', '0', 'static', FALSE, TRUE, 'The cost per MW of adding new link capacity. Includes investment costs (spread over the planning period) and fixed operations & maintenance costs. Only relevant when extendable capacity (p_nom_extendable) is True.', 0, NULL, 'costs'),
('LINK', 'marginal_cost', 'Marginal Cost', 'float', 'currency/MWh', '0', 'static_or_timeseries', FALSE, TRUE, 'The variable cost of transferring 1 MWh from bus0 to bus1 (before efficiency losses). Used by the optimizer to determine economic dispatch. Only meaningful if the max capacity factor (p_max_pu) >= 0 (unidirectional flow).', 0, NULL, 'costs'),
('LINK', 'marginal_cost_quadratic', 'Quadratic Marginal Cost', 'float', 'currency/MWh', '0', 'static_or_timeseries', FALSE, TRUE, 'Quadratic term for non-linear cost curves. When set, the total cost includes a quadratic component that increases with the square of power flow, modeling increasing marginal costs at higher transfer levels.', 0, NULL, 'costs'),
('LINK', 'stand_by_cost', 'Stand-by Cost', 'float', 'currency/h', '0', 'static_or_timeseries', FALSE, TRUE, 'Stand-by cost for operating the link at null power flow.', 0, NULL, 'unit_commitment'),
('LINK', 'length', 'Link Length', 'float', 'km', '0', 'static', FALSE, TRUE, 'The physical length of the link in kilometers. Used for calculating capital costs, especially for transmission lines or pipelines.', 0, NULL, 'electrical'),
('LINK', 'terrain_factor', 'Terrain Factor', 'float', 'per unit', '1', 'static', FALSE, TRUE, 'Multiplier for capital cost to account for difficult terrain. Values greater than 1 increase the capital cost (capital_cost) to reflect higher construction costs in challenging terrain (e.g., mountains, water crossings).', 0, NULL, 'electrical'),
('LINK', 'committable', 'Committable', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Enable unit commitment, allowing the link to be turned on or off with associated start-up and shutdown costs. Only available when the nominal power (p_nom) is not extendable.', NULL, NULL, 'unit_commitment'),
('LINK', 'start_up_cost', 'Start-up Cost', 'float', 'currency', '0', 'static', FALSE, TRUE, 'Cost to start up the link. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('LINK', 'shut_down_cost', 'Shutdown Cost', 'float', 'currency', '0', 'static', FALSE, TRUE, 'Cost to shut down the link. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('LINK', 'min_up_time', 'Min Up Time', 'int', 'snapshots', '0', 'static', FALSE, TRUE, 'Minimum number of snapshots for status to be 1. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('LINK', 'min_down_time', 'Min Down Time', 'int', 'snapshots', '0', 'static', FALSE, TRUE, 'Minimum number of snapshots for status to be 0. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('LINK', 'up_time_before', 'Up Time Before', 'int', 'snapshots', '1', 'static', FALSE, TRUE, 'Number of snapshots that the link was online before network.snapshots start. Only read if committable (committable) is True and min up time (min_up_time) is non-zero.', 0, NULL, 'unit_commitment'),
('LINK', 'down_time_before', 'Down Time Before', 'int', 'snapshots', '0', 'static', FALSE, TRUE, 'Number of snapshots that the link was offline before network.snapshots start. Only read if committable (committable) is True and min down time (min_down_time) is non-zero.', 0, NULL, 'unit_commitment'),
('LINK', 'ramp_limit_up', 'Ramp Up Limit', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'Maximum power flow increase from one snapshot to the next, per unit of the nominal power (p_nom). Ignored if 1.', NULL, NULL, 'ramping'),
('LINK', 'ramp_limit_down', 'Ramp Down Limit', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'Maximum power flow decrease from one snapshot to the next, per unit of the nominal power (p_nom). Ignored if 1.', NULL, NULL, 'ramping'),
('LINK', 'ramp_limit_start_up', 'Ramp Up at Start', 'float', 'per unit', '1', 'static', FALSE, TRUE, 'Maximum power flow increase at start up, per unit of the nominal power (p_nom). Only read if committable (committable) is True.', NULL, NULL, 'ramping'),
-- Output attributes for LINK (PyPSA link outputs)
('LINK', 'p0', 'Active Power Bus0', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power at bus0 (positive if power flows from bus0 to bus1)', NULL, NULL, 'electrical'),
('LINK', 'p1', 'Active Power Bus1', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power at bus1 (positive if power flows from bus1 to bus0)', NULL, NULL, 'electrical'),
('LINK', 'p_nom_opt', 'Optimised Nominal Power', 'float', 'MW', '0', 'static', FALSE, FALSE, 'Optimised nominal power (p_nom) from capacity expansion optimization.', 0, NULL, 'capacity'),
('LINK', 'status', 'Status', 'float', 'n/a', '1', 'timeseries', FALSE, FALSE, 'Status (1 is on, 0 is off). Only outputted if committable (committable) is True.', NULL, NULL, 'unit_commitment'),
('LINK', 'mu_upper', 'Shadow Price Upper', 'float', 'currency/MW', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper nominal power (p_nom) limit', NULL, NULL, 'costs'),
('LINK', 'mu_lower', 'Shadow Price Lower', 'float', 'currency/MW', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower nominal power (p_nom) limit', NULL, NULL, 'costs'),
('LINK', 'mu_p_set', 'Shadow Price P Set', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of fixed power transmission power setpoint (p_set)', NULL, NULL, 'costs'),
('LINK', 'mu_ramp_limit_up', 'Shadow Price Ramp Up', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper ramp up limit', NULL, NULL, 'ramping'),
('LINK', 'mu_ramp_limit_down', 'Shadow Price Ramp Down', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower ramp down limit', NULL, NULL, 'ramping');

-- ============================================================================
-- UNMET_LOAD ATTRIBUTES  
-- ============================================================================

-- UNMET_LOAD attributes - same as GENERATOR but with specific defaults and restrictions - Updated to simplified groups
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for UNMET_LOAD (same as GENERATOR)
('UNMET_LOAD', 'control', 'Control Strategy', 'string', 'n/a', 'PQ', 'static', FALSE, TRUE, 'Power flow control mode: "PQ" (fixed active and reactive power), "PV" (fixed active power and voltage magnitude), or "Slack" (balances system power, typically one per network).', NULL, NULL, 'electrical'),
('UNMET_LOAD', 'type', 'Type', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Placeholder for unmet load type. Not yet implemented.', NULL, NULL, 'basic'),
('UNMET_LOAD', 'p_nom', 'Nominal Power', 'float', 'MW', '10000000', 'static', FALSE, TRUE, 'The maximum rated capacity in MW. For unmet load, this is typically set very high (e.g., 10000000 MW) to allow the optimizer to serve any unmet demand. This sets the upper limit for power output in all calculations.', 0, NULL, 'capacity'),
('UNMET_LOAD', 'p_nom_extendable', 'Extendable Capacity', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Switch to allow the nominal power (p_nom) to be extended in optimization.', NULL, NULL, 'capacity'),
('UNMET_LOAD', 'p_nom_min', 'Min Nominal Power', 'float', 'MW', '0', 'static', FALSE, TRUE, 'If the nominal power (p_nom) is extendable in optimization, set its minimum value.', 0, NULL, 'capacity'),
('UNMET_LOAD', 'p_nom_max', 'Max Nominal Power', 'float', 'MW', 'inf', 'static', FALSE, TRUE, 'If the nominal power (p_nom) is extendable in optimization, set its maximum value (e.g. limited by technical potential).', 0, NULL, 'capacity'),
('UNMET_LOAD', 'p_min_pu', 'Min Capacity Factor', 'float', 'per unit', '0', 'static_or_timeseries', FALSE, TRUE, 'The minimum output for each snapshot per unit of the nominal power (p_nom) for the optimization. Note that if committable (committable) is False and the min capacity factor (p_min_pu) > 0, this represents a must-run condition.', 0, 1, 'power_limits'),
('UNMET_LOAD', 'p_max_pu', 'Max Capacity Factor', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'The maximum output for each snapshot per unit of the nominal power (p_nom) for the optimization.', 0, 1, 'power_limits'),
('UNMET_LOAD', 'p_set', 'Active Power Setpoint', 'float', 'MW', '0', 'static_or_timeseries', FALSE, TRUE, 'Fixed active power output that the unmet load generator must produce. Used when the output is predetermined rather than optimized.', NULL, NULL, 'power_limits'),
('UNMET_LOAD', 'q_set', 'Reactive Power Setpoint', 'float', 'MVar', '0', 'static_or_timeseries', FALSE, TRUE, 'Fixed reactive power output that the unmet load generator must produce. Used when the reactive power output is predetermined rather than optimized.', NULL, NULL, 'power_limits'),
('UNMET_LOAD', 'sign', 'Power Sign', 'float', 'n/a', '1', 'static', FALSE, TRUE, 'Power flow direction convention: 1 for generation (positive power flows into the network), -1 for consumption (positive power flows out of the network).', NULL, NULL, 'power_limits'),
('UNMET_LOAD', 'carrier', 'Carrier', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Prime mover Carrier (e.g. coal, gas, wind, solar); required for global constraints on primary energy in optimization', NULL, NULL, 'basic'),
('UNMET_LOAD', 'marginal_cost', 'Marginal Cost (Penalty)', 'float', 'currency/MWh', '100000000', 'static_or_timeseries', FALSE, TRUE, 'The variable cost of producing one additional MWh of electricity. For unmet load, this is typically set very high (e.g., 100000000 currency/MWh) as a penalty cost to discourage the optimizer from using this generator unless absolutely necessary. Used by the optimizer to determine the economic dispatch order (lower cost generators are dispatched first).', 0, NULL, 'costs'),
('UNMET_LOAD', 'build_year', 'Build Year', 'int', 'year', '0', 'static', FALSE, TRUE, 'The year when the unmet load generator can be built or commissioned. Essential for multi-year capacity expansion planning models, which determine optimal investment timing and generator retirement schedules.', 0, 3000, 'capacity'),
('UNMET_LOAD', 'lifetime', 'Lifetime', 'float', 'years', 'inf', 'static', FALSE, TRUE, 'The operational lifetime of the unmet load generator in years. Essential for multi-year capacity expansion planning models, which use this to determine when generators retire (build year (build_year) + lifetime). Set to "inf" for generators that never retire.', 0, NULL, 'capacity'),
('UNMET_LOAD', 'capital_cost', 'Capital Cost', 'float', 'currency/MW', '0', 'static_or_timeseries', FALSE, TRUE, 'The cost per MW of adding new capacity. Includes investment costs (spread over the planning period) and fixed operations & maintenance costs. Only relevant when extendable capacity (p_nom_extendable) is True.', 0, NULL, 'costs'),
('UNMET_LOAD', 'efficiency', 'Efficiency', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'Ratio between primary energy and electrical energy, e.g. takes value 0.4 MWh_elec/MWh_thermal for gas. This is required for global constraints on primary energy in optimization.', 0, 1, 'energy'),
('UNMET_LOAD', 'committable', 'Committable', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Enable unit commitment, allowing the unmet load generator to be turned on or off with associated start-up and shutdown costs. Only available when the nominal power (p_nom) is not extendable.', NULL, NULL, 'unit_commitment'),
('UNMET_LOAD', 'start_up_cost', 'Start-up Cost', 'float', 'currency', '0', 'static', FALSE, TRUE, 'Cost to start up the unmet load generator. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('UNMET_LOAD', 'shut_down_cost', 'Shutdown Cost', 'float', 'currency', '0', 'static', FALSE, TRUE, 'Cost to shut down the unmet load generator. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('UNMET_LOAD', 'min_up_time', 'Min Up Time', 'int', 'snapshots', '0', 'static', FALSE, TRUE, 'Minimum number of snapshots for status to be 1. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('UNMET_LOAD', 'min_down_time', 'Min Down Time', 'int', 'snapshots', '0', 'static', FALSE, TRUE, 'Minimum number of snapshots for status to be 0. Only read if committable (committable) is True.', 0, NULL, 'unit_commitment'),
('UNMET_LOAD', 'up_time_before', 'Up Time Before', 'int', 'snapshots', '1', 'static', FALSE, TRUE, 'Number of snapshots that the unmet load generator was online before network.snapshots start. Only read if committable (committable) is True and min up time (min_up_time) is non-zero.', 0, NULL, 'unit_commitment'),
('UNMET_LOAD', 'down_time_before', 'Down Time Before', 'int', 'snapshots', '0', 'static', FALSE, TRUE, 'Number of snapshots that the unmet load generator was offline before network.snapshots start. Only read if committable (committable) is True and min down time (min_down_time) is non-zero.', 0, NULL, 'unit_commitment'),
('UNMET_LOAD', 'ramp_limit_up', 'Ramp Up Limit', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'Maximum active power increase from one snapshot to the next, per unit of the nominal power (p_nom). Ignored if 1.', NULL, NULL, 'ramping'),
('UNMET_LOAD', 'ramp_limit_down', 'Ramp Down Limit', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'Maximum active power decrease from one snapshot to the next, per unit of the nominal power (p_nom). Ignored if 1.', NULL, NULL, 'ramping'),
('UNMET_LOAD', 'ramp_limit_start_up', 'Ramp Up at Start', 'float', 'per unit', '1', 'static', FALSE, TRUE, 'Maximum active power increase at start up, per unit of the nominal power (p_nom). Only read if committable (committable) is True.', NULL, NULL, 'ramping'),
('UNMET_LOAD', 'ramp_limit_shut_down', 'Ramp Down at Shutdown', 'float', 'per unit', '1', 'static', FALSE, TRUE, 'Maximum active power decrease at shut down, per unit of the nominal power (p_nom). Only read if committable (committable) is True.', NULL, NULL, 'ramping'),
('UNMET_LOAD', 'active', 'Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether this unmet load generator is active and should be included in network calculations. Set to False to temporarily disable the generator without deleting it.', NULL, NULL, 'basic'),
-- Output attributes for UNMET_LOAD (same as GENERATOR since PyPSA treats them as generators)
('UNMET_LOAD', 'p', 'Active Power', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power at bus (positive if net generation)', NULL, NULL, 'electrical'),
('UNMET_LOAD', 'q', 'Reactive Power', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'reactive power (positive if net generation)', NULL, NULL, 'electrical'),
('UNMET_LOAD', 'p_nom_opt', 'Optimised Nominal Power', 'float', 'MW', '0', 'static', FALSE, FALSE, 'Optimised nominal power (p_nom) from capacity expansion optimization.', 0, NULL, 'capacity'),
('UNMET_LOAD', 'status', 'Status', 'float', 'n/a', '1', 'timeseries', FALSE, FALSE, 'Status (1 is on, 0 is off). Only outputted if committable (committable) is True.', NULL, NULL, 'unit_commitment'),
('UNMET_LOAD', 'mu_upper', 'Shadow Price Upper', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper nominal power (p_nom) limit', NULL, NULL, 'costs'),
('UNMET_LOAD', 'mu_lower', 'Shadow Price Lower', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower nominal power (p_nom) limit', NULL, NULL, 'costs'),
('UNMET_LOAD', 'mu_p_set', 'Shadow Price P Set', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of fixed power generation active power setpoint (p_set)', NULL, NULL, 'costs'),
('UNMET_LOAD', 'mu_ramp_limit_up', 'Shadow Price Ramp Up', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper ramp up limit', NULL, NULL, 'ramping'),
('UNMET_LOAD', 'mu_ramp_limit_down', 'Shadow Price Ramp Down', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower ramp down limit', NULL, NULL, 'ramping');

-- ============================================================================
-- STORAGE_UNIT ATTRIBUTES
-- ============================================================================

-- STORAGE_UNIT attributes from storage_units.csv (PyPSA reference) - Updated to simplified groups
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for STORAGE_UNIT
('STORAGE_UNIT', 'control', 'Control Strategy', 'string', 'n/a', 'PQ', 'static', FALSE, TRUE, 'Power flow control mode: "PQ" (fixed active and reactive power), "PV" (fixed active power and voltage magnitude), or "Slack" (balances system power, typically one per network).', NULL, NULL, 'electrical'),
('STORAGE_UNIT', 'type', 'Type', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Placeholder for storage unit type. Not yet implemented.', NULL, NULL, 'basic'),
('STORAGE_UNIT', 'p_nom', 'Nominal Power', 'float', 'MW', '0', 'static', TRUE, TRUE, 'The maximum rated power capacity of the storage unit in MW. This sets the limit for both charging (negative power) and discharging (positive power) in all calculations.', 0, NULL, 'capacity'),
('STORAGE_UNIT', 'p_nom_mod', 'Nominal Power Module', 'float', 'MW', '0', 'static', FALSE, TRUE, 'The unit size for capacity expansion. When extending the nominal power (p_nom), it can only be increased in multiples of this module size.', 0, NULL, 'capacity'),
('STORAGE_UNIT', 'p_nom_extendable', 'Extendable Capacity', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Switch to allow the nominal power (p_nom) to be extended in optimization.', NULL, NULL, 'capacity'),
('STORAGE_UNIT', 'p_nom_min', 'Min Nominal Power', 'float', 'MW', '0', 'static', FALSE, TRUE, 'If the nominal power (p_nom) is extendable in optimization, set its minimum value.', 0, NULL, 'capacity'),
('STORAGE_UNIT', 'p_nom_max', 'Max Nominal Power', 'float', 'MW', 'inf', 'static', FALSE, TRUE, 'If the nominal power (p_nom) is extendable in optimization, set its maximum value (e.g. limited by technical potential).', 0, NULL, 'capacity'),
('STORAGE_UNIT', 'p_min_pu', 'Min Capacity Factor', 'float', 'per unit', '-1', 'static_or_timeseries', FALSE, TRUE, 'The minimum power flow per unit of the nominal power (p_nom). Negative values represent charging (withdrawing power from the bus), positive values represent discharging. Can be static or time-varying.', -1, 1, 'power_limits'),
('STORAGE_UNIT', 'p_max_pu', 'Max Capacity Factor', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'The maximum power flow per unit of the nominal power (p_nom). Positive values represent discharging (injecting power into the bus), negative values represent charging. Can be static or time-varying.', -1, 1, 'power_limits'),
('STORAGE_UNIT', 'p_set', 'Active Power Setpoint', 'float', 'MW', '0', 'static_or_timeseries', FALSE, TRUE, 'Fixed active power output that the storage unit must produce (positive for discharging, negative for charging). Used when the power output is predetermined rather than optimized.', NULL, NULL, 'power_limits'),
('STORAGE_UNIT', 'q_set', 'Reactive Power Setpoint', 'float', 'MVar', '0', 'static_or_timeseries', FALSE, TRUE, 'Fixed reactive power output that the storage unit must produce. Used when the reactive power output is predetermined rather than optimized.', NULL, NULL, 'power_limits'),
('STORAGE_UNIT', 'sign', 'Power Sign', 'float', 'n/a', '1', 'static', FALSE, TRUE, 'Power flow direction convention: 1 for generation/discharging (positive power flows into the network), -1 for consumption/charging (positive power flows out of the network).', NULL, NULL, 'power_limits'),
('STORAGE_UNIT', 'carrier', 'Carrier', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Carrier type for the storage unit (e.g. battery, hydro, hydrogen); required for global constraints on primary energy in optimization', NULL, NULL, 'basic'),
('STORAGE_UNIT', 'spill_cost', 'Spill Cost', 'float', 'currency/MWh', '0', 'static_or_timeseries', FALSE, TRUE, 'The cost of spilling 1 MWh of energy that cannot be stored (e.g., water spillage from a hydro reservoir when the reservoir is full).', 0, NULL, 'costs'),
('STORAGE_UNIT', 'marginal_cost', 'Marginal Cost', 'float', 'currency/MWh', '0', 'static_or_timeseries', FALSE, TRUE, 'The variable cost of discharging one additional MWh of electricity. Used by the optimizer to determine the economic dispatch order (lower cost storage units are dispatched first).', 0, NULL, 'costs'),
('STORAGE_UNIT', 'marginal_cost_quadratic', 'Quadratic Marginal Cost', 'float', 'currency/MWh', '0', 'static_or_timeseries', FALSE, TRUE, 'Quadratic term for non-linear cost curves. When set, the total discharge cost includes a quadratic component that increases with the square of discharge power, modeling increasing marginal costs at higher discharge levels.', 0, NULL, 'costs'),
('STORAGE_UNIT', 'marginal_cost_storage', 'Storage Marginal Cost', 'float', 'currency/MWh/h', '0', 'static_or_timeseries', FALSE, TRUE, 'The variable cost of storing 1 MWh of energy for one hour. This represents the opportunity cost or wear-and-tear cost associated with storing energy in the storage unit.', 0, NULL, 'costs'),
('STORAGE_UNIT', 'capital_cost', 'Capital Cost', 'float', 'currency/MW', '0', 'static', FALSE, TRUE, 'The cost per MW of adding new storage capacity. Includes investment costs (spread over the planning period) and fixed operations & maintenance costs. Only relevant when extendable capacity (p_nom_extendable) is True.', 0, NULL, 'costs'),
('STORAGE_UNIT', 'active', 'Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether this storage unit is active and should be included in network calculations. Set to False to temporarily disable the storage unit without deleting it.', NULL, NULL, 'basic'),
('STORAGE_UNIT', 'build_year', 'Build Year', 'int', 'year', '0', 'static', FALSE, TRUE, 'The year when the storage unit can be built or commissioned. Essential for multi-year capacity expansion planning models, which determine optimal investment timing and storage unit retirement schedules.', 0, 3000, 'capacity'),
('STORAGE_UNIT', 'lifetime', 'Lifetime', 'float', 'years', 'inf', 'static', FALSE, TRUE, 'The operational lifetime of the storage unit in years. Essential for multi-year capacity expansion planning models, which use this to determine when storage units retire (build year (build_year) + lifetime). Set to "inf" for storage units that never retire.', 0, NULL, 'capacity'),
('STORAGE_UNIT', 'state_of_charge_initial', 'Initial State of Charge', 'float', 'MWh', '0', 'static', FALSE, TRUE, 'The state of charge (energy stored) at the beginning of the optimization period, before the first snapshot. Ignored if cyclic state of charge (cyclic_state_of_charge) is True.', 0, NULL, 'energy'),
('STORAGE_UNIT', 'state_of_charge_initial_per_period', 'Initial SOC per Period', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'If True, the initial state of charge (state_of_charge_initial) is applied at the beginning of each investment period separately, rather than only at the start of the entire optimization horizon.', NULL, NULL, 'energy'),
('STORAGE_UNIT', 'state_of_charge_set', 'State of Charge Setpoint', 'float', 'MWh', '1', 'static_or_timeseries', FALSE, TRUE, 'Fixed state of charge values that the storage unit must maintain at specific snapshots. Used when the state of charge is predetermined rather than optimized. Can be static or time-varying.', NULL, NULL, 'energy'),
('STORAGE_UNIT', 'cyclic_state_of_charge', 'Cyclic State of Charge', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'If True, the initial state of charge (state_of_charge_initial) is ignored and the storage unit must end with the same state of charge as it started (cyclic constraint). This ensures the storage unit returns to its initial state at the end of the optimization period.', NULL, NULL, 'energy'),
('STORAGE_UNIT', 'cyclic_state_of_charge_per_period', 'Cyclic SOC per Period', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'If True, the cyclic state of charge constraint (cyclic_state_of_charge) is applied to each investment period separately, rather than only to the entire optimization horizon.', NULL, NULL, 'energy'),
('STORAGE_UNIT', 'max_hours', 'Max Storage Hours', 'float', 'hours', '1', 'static', FALSE, TRUE, 'The maximum energy storage capacity expressed as the number of hours the storage unit can discharge at full nominal power (p_nom). The maximum state of charge in MWh equals max hours (max_hours) × nominal power (p_nom).', 0, NULL, 'energy'),
('STORAGE_UNIT', 'efficiency_store', 'Storage Efficiency', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'The round-trip efficiency for charging (storing energy). A value of 1.0 means no losses, while lower values represent energy losses during charging. Can be time-varying to model temperature-dependent performance.', 0, 1, 'energy'),
('STORAGE_UNIT', 'efficiency_dispatch', 'Dispatch Efficiency', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'The round-trip efficiency for discharging (releasing stored energy). A value of 1.0 means no losses, while lower values represent energy losses during discharging. Can be time-varying to model temperature-dependent performance.', 0, 1, 'energy'),
('STORAGE_UNIT', 'standing_loss', 'Standing Loss', 'float', 'per unit', '0', 'static_or_timeseries', FALSE, TRUE, 'The self-discharge rate per hour, expressed as a fraction of the current state of charge. Represents energy losses that occur even when the storage unit is idle (e.g., battery self-discharge, reservoir evaporation). Can be time-varying.', 0, 1, 'energy'),
('STORAGE_UNIT', 'inflow', 'Inflow', 'float', 'MW', '0', 'static_or_timeseries', FALSE, TRUE, 'Natural inflow of energy to the state of charge (e.g., river inflow to a hydro reservoir, solar charging for a battery). Positive values increase the stored energy without drawing power from the bus. Can be static or time-varying.', NULL, NULL, 'energy'),
-- Output attributes for STORAGE_UNIT (PyPSA storage unit outputs)
('STORAGE_UNIT', 'p', 'Active Power', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power at bus (positive if discharging)', NULL, NULL, 'electrical'),
('STORAGE_UNIT', 'q', 'Reactive Power', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'reactive power at bus', NULL, NULL, 'electrical'),
('STORAGE_UNIT', 'state_of_charge', 'State of Charge', 'float', 'MWh', '0', 'timeseries', FALSE, FALSE, 'State of charge of storage unit', 0, NULL, 'energy'),
('STORAGE_UNIT', 'p_nom_opt', 'Optimised Nominal Power', 'float', 'MW', '0', 'static', FALSE, FALSE, 'Optimised nominal power (p_nom) from capacity expansion optimization.', 0, NULL, 'capacity'),
('STORAGE_UNIT', 'spill', 'Spill', 'float', 'MWh', '0', 'timeseries', FALSE, FALSE, 'Spillage of storage unit', 0, NULL, 'electrical'),
('STORAGE_UNIT', 'status', 'Status', 'float', 'n/a', '1', 'timeseries', FALSE, FALSE, 'Status (1 is on, 0 is off). Only outputted if committable (committable) is True.', NULL, NULL, 'unit_commitment'),
('STORAGE_UNIT', 'mu_upper', 'Shadow Price Upper', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper nominal power (p_nom) limit', NULL, NULL, 'costs'),
('STORAGE_UNIT', 'mu_lower', 'Shadow Price Lower', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower nominal power (p_nom) limit', NULL, NULL, 'costs'),
('STORAGE_UNIT', 'p_dispatch', 'Active Power Dispatch', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power dispatch at bus', NULL, NULL, 'electrical'),
('STORAGE_UNIT', 'p_store', 'Active Power Charging', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power charging at bus', NULL, NULL, 'electrical'),
('STORAGE_UNIT', 'mu_state_of_charge_set', 'Shadow Price SOC Set', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of fixed state of charge setpoint (state_of_charge_set)', NULL, NULL, 'costs'),
('STORAGE_UNIT', 'mu_energy_balance', 'Shadow Price Energy Balance', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of storage consistency equations', NULL, NULL, 'costs');

-- ============================================================================
-- STORE ATTRIBUTES
-- ============================================================================

-- STORE attributes from stores.csv (PyPSA reference) - Updated to simplified groups
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for STORE
('STORE', 'type', 'Type', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Placeholder for store type. Not yet implemented.', NULL, NULL, 'basic'),
('STORE', 'carrier', 'Carrier', 'string', 'n/a', '', 'static', FALSE, TRUE, 'Carrier type for the store (e.g. heat, gas, hydrogen). Used for categorization and energy balance constraints.', NULL, NULL, 'basic'),
('STORE', 'e_nom', 'Nominal Energy Capacity', 'float', 'MWh', '0', 'static', TRUE, TRUE, 'The maximum energy storage capacity of the store in MWh. This sets the upper limit for the amount of energy that can be stored.', 0, NULL, 'capacity'),
('STORE', 'e_nom_mod', 'Nominal Energy Module', 'float', 'MWh', '0', 'static', FALSE, TRUE, 'The unit size for capacity expansion. When extending the nominal energy capacity (e_nom), it can only be increased in multiples of this module size.', 0, NULL, 'capacity'),
('STORE', 'e_nom_extendable', 'Extendable Energy Capacity', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Switch to allow the nominal energy capacity (e_nom) to be extended in optimization.', NULL, NULL, 'capacity'),
('STORE', 'e_nom_min', 'Min Energy Capacity', 'float', 'MWh', '0', 'static', FALSE, TRUE, 'If the nominal energy capacity (e_nom) is extendable in optimization, set its minimum value.', 0, NULL, 'capacity'),
('STORE', 'e_nom_max', 'Max Energy Capacity', 'float', 'MWh', 'inf', 'static', FALSE, TRUE, 'If the nominal energy capacity (e_nom) is extendable in optimization, set its maximum value (e.g. limited by technical potential).', 0, NULL, 'capacity'),
('STORE', 'e_min_pu', 'Min Energy Factor', 'float', 'per unit', '0', 'static_or_timeseries', FALSE, TRUE, 'The minimum stored energy per unit of the nominal energy capacity (e_nom). Can be static or time-varying.', 0, 1, 'energy'),
('STORE', 'e_max_pu', 'Max Energy Factor', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'The maximum stored energy per unit of the nominal energy capacity (e_nom). Can be static or time-varying.', 0, 1, 'energy'),
('STORE', 'e_initial', 'Initial Energy', 'float', 'MWh', '0', 'static', FALSE, TRUE, 'The energy stored at the beginning of the optimization period, before the first snapshot. Ignored if cyclic energy (e_cyclic) is True.', 0, NULL, 'energy'),
('STORE', 'e_initial_per_period', 'Initial Energy per Period', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'If True, the initial energy (e_initial) is applied at the beginning of each investment period separately, rather than only at the start of the entire optimization horizon.', NULL, NULL, 'energy'),
('STORE', 'e_cyclic', 'Cyclic Energy', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'If True, the initial energy (e_initial) is ignored and the store must end with the same energy as it started (cyclic constraint). This ensures the store returns to its initial state at the end of the optimization period.', NULL, NULL, 'energy'),
('STORE', 'e_cyclic_per_period', 'Cyclic Energy per Period', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'If True, the cyclic energy constraint (e_cyclic) is applied to each investment period separately, rather than only to the entire optimization horizon.', NULL, NULL, 'energy'),
('STORE', 'p_set', 'Active Power Setpoint', 'float', 'MW', '0', 'static_or_timeseries', FALSE, TRUE, 'Fixed active power flow that the store must maintain (positive for withdrawing energy from the bus, negative for injecting energy into the bus). Used when the power flow is predetermined rather than optimized.', NULL, NULL, 'power_limits'),
('STORE', 'q_set', 'Reactive Power Setpoint', 'float', 'MVar', '0', 'static_or_timeseries', FALSE, TRUE, 'Fixed reactive power flow that the store must maintain. Used when the reactive power flow is predetermined rather than optimized.', NULL, NULL, 'power_limits'),
('STORE', 'sign', 'Power Sign', 'float', 'n/a', '1', 'static', FALSE, TRUE, 'Power flow direction convention: 1 for generation/discharging (positive power flows into the network), -1 for consumption/charging (positive power flows out of the network).', NULL, NULL, 'power_limits'),
('STORE', 'marginal_cost', 'Marginal Cost', 'float', 'currency/MWh', '0', 'static_or_timeseries', FALSE, TRUE, 'The variable cost applied to both charging and discharging 1 MWh of energy. Used by the optimizer to determine the economic dispatch order.', 0, NULL, 'costs'),
('STORE', 'marginal_cost_quadratic', 'Quadratic Marginal Cost', 'float', 'currency/MWh', '0', 'static_or_timeseries', FALSE, TRUE, 'Quadratic term for non-linear cost curves. When set, the total cost includes a quadratic component that increases with the square of energy flow, modeling increasing marginal costs at higher flow levels.', 0, NULL, 'costs'),
('STORE', 'marginal_cost_storage', 'Storage Marginal Cost', 'float', 'currency/MWh/h', '0', 'static_or_timeseries', FALSE, TRUE, 'The variable cost of storing 1 MWh of energy for one hour. This represents the opportunity cost or wear-and-tear cost associated with storing energy in the store.', 0, NULL, 'costs'),
('STORE', 'capital_cost', 'Capital Cost', 'float', 'currency/MWh', '0', 'static', FALSE, TRUE, 'The cost per MWh of adding new storage capacity. Includes investment costs (spread over the planning period) and fixed operations & maintenance costs. Only relevant when extendable capacity (e_nom_extendable) is True.', 0, NULL, 'costs'),
('STORE', 'standing_loss', 'Standing Loss', 'float', 'per unit', '0', 'static_or_timeseries', FALSE, TRUE, 'The self-discharge rate per hour, expressed as a fraction of the current stored energy. Represents energy losses that occur even when the store is idle (e.g., thermal losses, leakage). Can be time-varying.', 0, 1, 'energy'),
('STORE', 'active', 'Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether this store is active and should be included in network calculations. Set to False to temporarily disable the store without deleting it.', NULL, NULL, 'basic'),
('STORE', 'build_year', 'Build Year', 'int', 'year', '0', 'static', FALSE, TRUE, 'The year when the store can be built or commissioned. Essential for multi-year capacity expansion planning models, which determine optimal investment timing and store retirement schedules.', 0, 3000, 'capacity'),
('STORE', 'lifetime', 'Lifetime', 'float', 'years', 'inf', 'static', FALSE, TRUE, 'The operational lifetime of the store in years. Essential for multi-year capacity expansion planning models, which use this to determine when stores retire (build year (build_year) + lifetime). Set to "inf" for stores that never retire.', 0, NULL, 'capacity'),
-- Output attributes for STORE (PyPSA store outputs)
('STORE', 'p', 'Active Power', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'active power at bus (positive if withdrawing energy)', NULL, NULL, 'electrical'),
('STORE', 'q', 'Reactive Power', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'reactive power at bus', NULL, NULL, 'electrical'),
('STORE', 'e', 'Energy', 'float', 'MWh', '0', 'timeseries', FALSE, FALSE, 'Energy stored in store', 0, NULL, 'electrical'),
('STORE', 'e_nom_opt', 'Optimised Energy Capacity', 'float', 'MWh', '0', 'static', FALSE, FALSE, 'Optimised nominal energy capacity (e_nom) from capacity expansion optimization.', 0, NULL, 'capacity'),
('STORE', 'mu_upper', 'Shadow Price Upper', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper energy limit (e_max_pu × e_nom)', NULL, NULL, 'costs'),
('STORE', 'mu_lower', 'Shadow Price Lower', 'float', 'currency/MWh', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower energy limit (e_min_pu × e_nom)', NULL, NULL, 'costs');

-- ============================================================================
-- TRANSFORMER ATTRIBUTES
-- ============================================================================

-- TRANSFORMER attributes from transformers.csv (PyPSA reference) - Updated to simplified groups
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for TRANSFORMER
('TRANSFORMER', 'bus0', 'Origin Bus', 'string', 'n/a', 'n/a', 'static', TRUE, TRUE, 'Name of the origin bus (typically higher voltage) to which the transformer is attached.', NULL, NULL, 'basic'),
('TRANSFORMER', 'bus1', 'Destination Bus', 'string', 'n/a', 'n/a', 'static', TRUE, TRUE, 'Name of the destination bus (typically lower voltage) to which the transformer is attached.', NULL, NULL, 'basic'),
('TRANSFORMER', 'type', 'Type', 'string', 'n/a', 'n/a', 'static', FALSE, TRUE, 'Name of a predefined transformer standard type. If set, the transformer type impedance parameters are automatically calculated, overriding any manually set values for series reactance (x), series resistance (r), shunt susceptance (b), nominal apparent power (s_nom), tap ratio (tap_ratio), tap side (tap_side), and phase shift (phase_shift). Leave empty to manually specify impedance parameters.', NULL, NULL, 'basic'),
('TRANSFORMER', 'model', 'Transformer Model', 'string', 'n/a', 't', 'static', TRUE, TRUE, 'Model used for admittance matrix: "t" or "pi". Defaults to "t" following physics and DIgSILENT PowerFactory conventions.', NULL, NULL, 'basic'),
('TRANSFORMER', 'x', 'Series Reactance', 'float', 'per unit', '0', 'static', TRUE, TRUE, 'The series reactance in per unit (using nominal apparent power (s_nom) as base power). Must be non-zero for AC transformers in linear power flow. The series impedance is z = r + jx. Ignored if transformer type (type) is set.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'r', 'Series Resistance', 'float', 'per unit', '0', 'static', TRUE, TRUE, 'The series resistance in per unit (using nominal apparent power (s_nom) as base power). Must be non-zero for DC transformers in linear power flow. The series impedance is z = r + jx. Ignored if transformer type (type) is set.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'g', 'Shunt Conductance', 'float', 'per unit', '0', 'static', FALSE, TRUE, 'The shunt conductance in per unit (using nominal apparent power (s_nom) as base power). The shunt admittance is y = g + jb, where b is the shunt susceptance (b). Ignored if transformer type (type) is set.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'b', 'Shunt Susceptance', 'float', 'per unit', '0', 'static', FALSE, TRUE, 'The shunt susceptance in per unit (using nominal apparent power (s_nom) as base power). The shunt admittance is y = g + jb, where g is the shunt conductance (g). Ignored if transformer type (type) is set.', NULL, NULL, 'electrical'),
('TRANSFORMER', 's_nom', 'Nominal Apparent Power', 'float', 'MVA', '0', 'static', FALSE, TRUE, 'The maximum apparent power capacity of the transformer in MVA. This sets the limit for power flow through the transformer in either direction. Ignored if extendable capacity (s_nom_extendable) is True.', 0, NULL, 'capacity'),
('TRANSFORMER', 's_nom_mod', 'Nominal Apparent Power Module', 'float', 'MVA', '0', 'static', FALSE, TRUE, 'The unit size for capacity expansion. When extending the nominal apparent power (s_nom), it can only be increased in multiples of this module size. Introduces integer variables in optimization.', 0, NULL, 'capacity'),
('TRANSFORMER', 's_nom_extendable', 'Extendable Capacity', 'boolean', 'n/a', 'False', 'static', FALSE, TRUE, 'Switch to allow the nominal apparent power (s_nom) to be extended in optimization.', NULL, NULL, 'capacity'),
('TRANSFORMER', 's_nom_min', 'Min Nominal Apparent Power', 'float', 'MVA', '0', 'static', FALSE, TRUE, 'If the nominal apparent power (s_nom) is extendable in optimization, set its minimum value.', 0, NULL, 'capacity'),
('TRANSFORMER', 's_nom_max', 'Max Nominal Apparent Power', 'float', 'MVA', 'inf', 'static', FALSE, TRUE, 'If the nominal apparent power (s_nom) is extendable in optimization, set its maximum value (e.g. limited by technical potential).', 0, NULL, 'capacity'),
('TRANSFORMER', 's_nom_set', 'Nominal Apparent Power Setpoint', 'float', 'MVA', 'n/a', 'static', FALSE, TRUE, 'If the nominal apparent power (s_nom) is extendable in optimization, set the value of the optimized nominal apparent power (s_nom_opt).', 0, NULL, 'capacity'),
('TRANSFORMER', 's_max_pu', 'Max Capacity Factor', 'float', 'per unit', '1', 'static_or_timeseries', FALSE, TRUE, 'The maximum allowed absolute flow per unit of the nominal apparent power (s_nom). Can be set less than 1 to account for security margins (e.g., n-1 contingency), or can be time-varying to represent weather-dependent dynamic rating.', 0, NULL, 'power_limits'),
('TRANSFORMER', 'capital_cost', 'Capital Cost', 'float', 'currency/MVA', '0', 'static', FALSE, TRUE, 'The cost per MVA of adding new transformer capacity. Includes investment costs (spread over the planning period) and fixed operations & maintenance costs. Only relevant when extendable capacity (s_nom_extendable) is True.', 0, NULL, 'costs'),
('TRANSFORMER', 'num_parallel', 'Number of Parallel Transformers', 'float', 'n/a', '1', 'static', FALSE, TRUE, 'The number of parallel transformers (can be fractional). When transformer type (type) is set, this is used to calculate the total impedance (more parallel transformers reduce effective impedance). If transformer type (type) is empty, this value is ignored.', 0, NULL, 'electrical'),
('TRANSFORMER', 'tap_ratio', 'Tap Ratio', 'float', 'per unit', '1', 'static', FALSE, TRUE, 'Ratio of per unit voltages at each bus for tap changer. A value of 1.0 means no voltage transformation. Ignored if transformer type (type) is set.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'tap_side', 'Tap Side', 'int', 'n/a', '0', 'static', FALSE, TRUE, 'Defines if the tap changer is modeled at the primary side (bus0, usually high-voltage, value 0) or the secondary side (bus1, usually low-voltage, value 1). Must be 0 or 1. Ignored if transformer type (type) is set.', 0, 1, 'electrical'),
('TRANSFORMER', 'tap_position', 'Tap Position', 'int', 'n/a', '0', 'static', FALSE, TRUE, 'If the transformer has a transformer type (type), determines the tap position relative to the neutral tap position.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'phase_shift', 'Phase Shift', 'float', 'Degrees', '0', 'static', FALSE, TRUE, 'Voltage phase angle shift in degrees. Used to model phase-shifting transformers. Ignored if transformer type (type) is set.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'active', 'Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether this transformer is active and should be included in network calculations. Set to False to temporarily disable the transformer without deleting it.', NULL, NULL, 'basic'),
('TRANSFORMER', 'build_year', 'Build Year', 'int', 'year', '0', 'static', FALSE, TRUE, 'The year when the transformer can be built or commissioned. Essential for multi-year capacity expansion planning models, which determine optimal investment timing and transformer retirement schedules.', 0, 3000, 'capacity'),
('TRANSFORMER', 'lifetime', 'Lifetime', 'float', 'years', 'inf', 'static', FALSE, TRUE, 'The operational lifetime of the transformer in years. Essential for multi-year capacity expansion planning models, which use this to determine when transformers retire (build year (build_year) + lifetime). Set to "inf" for transformers that never retire.', 0, NULL, 'capacity'),
('TRANSFORMER', 'v_ang_min', 'Min Voltage Angle Difference', 'float', 'Degrees', '-inf', 'static', FALSE, TRUE, 'Minimum voltage angle difference across the transformer in degrees. This is a placeholder attribute and is not currently used by any functions.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'v_ang_max', 'Max Voltage Angle Difference', 'float', 'Degrees', 'inf', 'static', FALSE, TRUE, 'Maximum voltage angle difference across the transformer in degrees. This is a placeholder attribute and is not currently used by any functions.', NULL, NULL, 'electrical'),
-- Output attributes for TRANSFORMER (PyPSA transformer outputs)
('TRANSFORMER', 'sub_network', 'Sub Network', 'string', 'n/a', 'n/a', 'static', FALSE, FALSE, 'Name of connected sub-network to which transformer belongs, as calculated by network topology analysis. Do not set manually.', NULL, NULL, 'basic'),
('TRANSFORMER', 'p0', 'Active Power Bus0', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'Active power at bus0 (positive if branch is withdrawing power from bus0)', NULL, NULL, 'electrical'),
('TRANSFORMER', 'q0', 'Reactive Power Bus0', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'Reactive power at bus0 (positive if branch is withdrawing power from bus0)', NULL, NULL, 'electrical'),
('TRANSFORMER', 'p1', 'Active Power Bus1', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'Active power at bus1 (positive if branch is withdrawing power from bus1)', NULL, NULL, 'electrical'),
('TRANSFORMER', 'q1', 'Reactive Power Bus1', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'Reactive power at bus1 (positive if branch is withdrawing power from bus1)', NULL, NULL, 'electrical'),
('TRANSFORMER', 'x_pu', 'Per Unit Series Reactance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit series reactance calculated from the series reactance (x) and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'r_pu', 'Per Unit Series Resistance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit series resistance calculated from the series resistance (r) and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'g_pu', 'Per Unit Shunt Conductance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit shunt conductance calculated from the shunt conductance (g) and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'b_pu', 'Per Unit Shunt Susceptance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit shunt susceptance calculated from the shunt susceptance (b) and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'x_pu_eff', 'Effective Per Unit Series Reactance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Effective per unit series reactance for linear power flow, calculated from the series reactance (x), tap ratio (tap_ratio), and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('TRANSFORMER', 'r_pu_eff', 'Effective Per Unit Series Resistance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Effective per unit series resistance for linear power flow, calculated from the series resistance (r), tap ratio (tap_ratio), and the nominal voltage (v_nom) of the connected buses.', NULL, NULL, 'electrical'),
('TRANSFORMER', 's_nom_opt', 'Optimised Nominal Apparent Power', 'float', 'MVA', '0', 'static', FALSE, FALSE, 'Optimised nominal apparent power (s_nom) from capacity expansion optimization.', 0, NULL, 'capacity'),
('TRANSFORMER', 'mu_lower', 'Shadow Price Lower', 'float', 'currency/MVA', '0', 'timeseries', FALSE, FALSE, 'Shadow price of lower nominal apparent power (s_nom) limit. Always non-negative.', NULL, NULL, 'costs'),
('TRANSFORMER', 'mu_upper', 'Shadow Price Upper', 'float', 'currency/MVA', '0', 'timeseries', FALSE, FALSE, 'Shadow price of upper nominal apparent power (s_nom) limit. Always non-negative.', NULL, NULL, 'costs');

-- ============================================================================
-- SHUNT_IMPEDANCE ATTRIBUTES
-- ============================================================================

-- SHUNT_IMPEDANCE attributes from shunt_impedances.csv (PyPSA reference) - Updated to simplified groups
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for SHUNT_IMPEDANCE
('SHUNT_IMPEDANCE', 'bus', 'Bus', 'string', 'n/a', 'n/a', 'static', TRUE, TRUE, 'Name of the bus to which the shunt impedance is attached.', NULL, NULL, 'basic'),
('SHUNT_IMPEDANCE', 'g', 'Shunt Conductance', 'float', 'Siemens', '0', 'static', FALSE, TRUE, 'The shunt conductance in Siemens. Positive values withdraw active power from the bus. The shunt admittance is y = g + jb, where b is the shunt susceptance (b).', NULL, NULL, 'electrical'),
('SHUNT_IMPEDANCE', 'b', 'Shunt Susceptance', 'float', 'Siemens', '0', 'static', FALSE, TRUE, 'The shunt susceptance in Siemens. Positive values withdraw reactive power from the bus (inductive). The shunt admittance is y = g + jb, where g is the shunt conductance (g).', NULL, NULL, 'electrical'),
('SHUNT_IMPEDANCE', 'sign', 'Power Sign', 'float', 'n/a', '-1', 'static', FALSE, TRUE, 'Power flow direction convention: -1 means positive conductance (g) withdraws active power (p) from the bus, 1 means positive conductance (g) injects active power (p) into the bus.', NULL, NULL, 'power_limits'),
('SHUNT_IMPEDANCE', 'active', 'Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether this shunt impedance is active and should be included in network calculations. Set to False to temporarily disable the shunt impedance without deleting it.', NULL, NULL, 'basic'),
-- Output attributes for SHUNT_IMPEDANCE (PyPSA shunt impedance outputs)
('SHUNT_IMPEDANCE', 'p', 'Active Power', 'float', 'MW', '0', 'timeseries', FALSE, FALSE, 'Active power at bus (positive if net load)', NULL, NULL, 'electrical'),
('SHUNT_IMPEDANCE', 'q', 'Reactive Power', 'float', 'MVar', '0', 'timeseries', FALSE, FALSE, 'Reactive power at bus (positive if net generation)', NULL, NULL, 'electrical'),
('SHUNT_IMPEDANCE', 'g_pu', 'Per Unit Shunt Conductance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit shunt conductance calculated from the shunt conductance (g) and the nominal voltage (v_nom) of the connected bus.', NULL, NULL, 'electrical'),
('SHUNT_IMPEDANCE', 'b_pu', 'Per Unit Shunt Susceptance', 'float', 'per unit', '0', 'static', FALSE, FALSE, 'Per unit shunt susceptance calculated from the shunt susceptance (b) and the nominal voltage (v_nom) of the connected bus.', NULL, NULL, 'electrical');

-- ============================================================================
-- CONSTRAINT ATTRIBUTES
-- ============================================================================

-- CONSTRAINT attributes for Python code block constraints
INSERT INTO attribute_validation_rules (component_type, attribute_name, display_name, data_type, unit, default_value, allowed_storage_types, is_required, is_input, description, min_value, max_value, group_name) VALUES
-- Input attributes for CONSTRAINT
('CONSTRAINT', 'constraint_code', 'Constraint Code', 'string', 'n/a', '', 'static', TRUE, TRUE, 'Python code block defining constraint logic', NULL, NULL, 'basic'),
('CONSTRAINT', 'description', 'Description', 'string', 'n/a', '', 'static', FALSE, TRUE, 'Human-readable description of the constraint', NULL, NULL, 'basic'),
('CONSTRAINT', 'is_active', 'Is Active', 'boolean', 'n/a', 'True', 'static', FALSE, TRUE, 'Whether constraint is active and should be applied', NULL, NULL, 'basic'),
('CONSTRAINT', 'priority', 'Priority', 'int', 'n/a', '0', 'static', FALSE, TRUE, 'Execution priority (lower numbers execute first)', NULL, NULL, 'basic');

-- ============================================================================
-- COMPONENT CARRIER VALIDATION TRIGGERS
-- ============================================================================

-- Bus carrier validation - buses can only use AC, DC, heat, or gas carriers
CREATE TRIGGER validate_bus_carrier
    BEFORE INSERT ON components
    FOR EACH ROW
    WHEN NEW.component_type = 'BUS' AND NEW.carrier_id IS NOT NULL
BEGIN
    SELECT CASE 
        WHEN NOT EXISTS (
            SELECT 1 FROM carriers 
            WHERE id = NEW.carrier_id 
            AND name IN ('AC', 'DC', 'heat', 'gas')
        ) THEN
            RAISE(ABORT, 'Buses can only use AC, DC, heat, or gas carriers')
    END;
END;

-- Bus carrier validation for updates
CREATE TRIGGER validate_bus_carrier_update
    BEFORE UPDATE OF carrier_id ON components
    FOR EACH ROW
    WHEN NEW.component_type = 'BUS' AND NEW.carrier_id IS NOT NULL AND NEW.carrier_id != OLD.carrier_id
BEGIN
    SELECT CASE 
        WHEN NOT EXISTS (
            SELECT 1 FROM carriers 
            WHERE id = NEW.carrier_id 
            AND name IN ('AC', 'DC', 'heat', 'gas')
        ) THEN
            RAISE(ABORT, 'Buses can only use AC, DC, heat, or gas carriers')
    END;
END;

-- Line carrier validation - lines can only use AC carriers (PyPSA specification)
CREATE TRIGGER validate_line_carrier
    BEFORE INSERT ON components
    FOR EACH ROW
    WHEN NEW.component_type = 'LINE' AND NEW.carrier_id IS NOT NULL
BEGIN
    SELECT CASE 
        WHEN NOT EXISTS (
            SELECT 1 FROM carriers 
            WHERE id = NEW.carrier_id 
            AND name = 'AC'
        ) THEN
            RAISE(ABORT, 'Lines can only use AC carriers')
    END;
END;

-- Line carrier validation for updates
CREATE TRIGGER validate_line_carrier_update
    BEFORE UPDATE OF carrier_id ON components
    FOR EACH ROW
    WHEN NEW.component_type = 'LINE' AND NEW.carrier_id IS NOT NULL AND NEW.carrier_id != OLD.carrier_id
BEGIN
    SELECT CASE 
        WHEN NOT EXISTS (
            SELECT 1 FROM carriers 
            WHERE id = NEW.carrier_id 
            AND name = 'AC'
        ) THEN
            RAISE(ABORT, 'Lines can only use AC carriers')
    END;
END;

-- ============================================================================
-- NOTE: Bus connections are stored in connectivity JSON field, not as attributes
-- PyPSA export will resolve connectivity JSON to bus names during export process
-- ============================================================================

-- ============================================================================
-- VALIDATION COMPLETION
-- ============================================================================

-- Update schema version to indicate validation rules are populated
UPDATE system_metadata 
SET value = '2.2.0', updated_at = CURRENT_TIMESTAMP 
WHERE key = 'schema_version';

INSERT OR REPLACE INTO system_metadata (key, value, description) 
VALUES ('validation_rules_version', '2.2.0', 'PyPSA validation rules version');

INSERT OR REPLACE INTO system_metadata (key, value, description) 
VALUES ('validation_rules_count', (SELECT COUNT(*) FROM attribute_validation_rules), 'Total number of validation rules');

-- Set database user version for tracking
PRAGMA user_version = 3; 