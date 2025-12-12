-- ============================================================================
-- CORE ENERGY NETWORK SCHEMA (SIMPLIFIED)
-- Single-network-per-file design for desktop SQLite
-- Optimized for fast timeseries access and simple Rust/Python API
-- Version 3.1.0 - Single network + Sparse scenarios + Raw timeseries
-- ============================================================================

-- ============================================================================
-- NETWORK METADATA
-- ============================================================================

-- Network metadata - single row per database file
CREATE TABLE network_metadata (
    name TEXT NOT NULL,
    description TEXT,
    
    -- Time axis definition (single source of truth)
    time_start DATETIME NOT NULL,
    time_end DATETIME NOT NULL,
    time_interval TEXT NOT NULL,  -- ISO 8601 duration (PT1H, PT30M, PT2H, etc.)
    
    -- Network-level flags
    locked BOOLEAN DEFAULT 0,  -- Prevent accidental edits to base network
    
    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_time_range CHECK (time_end > time_start)
);

-- Network time periods - optimized storage using computed timestamps
CREATE TABLE network_time_periods (
    period_count INTEGER NOT NULL,      -- Total number of periods (e.g., 8760 for hourly year)
    start_timestamp INTEGER NOT NULL,   -- Unix timestamp of first period
    interval_seconds INTEGER NOT NULL,  -- Seconds between periods (3600 for hourly)
    
    CONSTRAINT valid_period_count CHECK (period_count > 0),
    CONSTRAINT valid_interval CHECK (interval_seconds > 0)
);

-- ============================================================================
-- CARRIERS - ENERGY TYPES
-- ============================================================================

-- Carriers table - energy carriers (electricity, gas, heat, etc.)
CREATE TABLE carriers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    
    -- Carrier properties from PyPSA reference
    co2_emissions REAL DEFAULT 0.0,  -- tonnes/MWh
    color TEXT,                      -- Plotting color
    nice_name TEXT,                  -- Display name  
    max_growth REAL DEFAULT NULL,    -- MW - can be infinite
    max_relative_growth REAL DEFAULT 0.0,  -- MW
    curtailable BOOLEAN DEFAULT FALSE, -- Whether the carrier can be curtailed
    
    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- UNIFIED COMPONENT SYSTEM
-- ============================================================================

-- Components table - unified table for all network components
CREATE TABLE components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_type TEXT NOT NULL,  -- 'BUS', 'GENERATOR', 'LOAD', 'LINE', 'LINK', 'STORAGE_UNIT', 'STORE', 'UNMET_LOAD', 'CONSTRAINT', 'TRANSFORMER', 'SHUNT_IMPEDANCE'
    name TEXT NOT NULL UNIQUE,
    
    -- Geographic location (optional)
    latitude REAL,
    longitude REAL,
    geometry TEXT,      -- GeoJSON geometry (Point, LineString, Polygon, etc.)
    
    -- Energy carrier reference
    carrier_id INTEGER,
    
    -- Bus connections
    bus_id INTEGER,     -- Single bus connection
    bus0_id INTEGER,    -- First bus for lines/links
    bus1_id INTEGER,    -- Second bus for lines/links
    
    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_components_carrier 
        FOREIGN KEY (carrier_id) REFERENCES carriers(id),
    CONSTRAINT fk_components_bus 
        FOREIGN KEY (bus_id) REFERENCES components(id),
    CONSTRAINT fk_components_bus0 
        FOREIGN KEY (bus0_id) REFERENCES components(id),
    CONSTRAINT fk_components_bus1 
        FOREIGN KEY (bus1_id) REFERENCES components(id),
    CONSTRAINT valid_component_type 
        CHECK (component_type IN ('BUS', 'GENERATOR', 'LOAD', 'LINE', 'LINK', 'STORAGE_UNIT', 'STORE', 'UNMET_LOAD', 'CONSTRAINT', 'TRANSFORMER', 'SHUNT_IMPEDANCE'))
);

-- Essential indexes only
CREATE INDEX idx_components_type ON components(component_type);
CREATE INDEX idx_components_name ON components(name);
CREATE INDEX idx_components_bus ON components(bus_id);
CREATE INDEX idx_components_bus0 ON components(bus0_id);
CREATE INDEX idx_components_bus1 ON components(bus1_id);

-- ============================================================================
-- ATTRIBUTE VALIDATION SYSTEM
-- ============================================================================

-- Attribute validation rules table
CREATE TABLE attribute_validation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_type TEXT NOT NULL,
    attribute_name TEXT NOT NULL,
    display_name TEXT,
    
    -- Validation rules
    data_type TEXT NOT NULL,           -- 'float', 'boolean', 'string', 'int'
    unit TEXT,
    default_value TEXT,
    allowed_storage_types TEXT NOT NULL, -- 'static', 'timeseries', 'static_or_timeseries'
    is_required BOOLEAN DEFAULT FALSE,
    is_input BOOLEAN DEFAULT TRUE,
    description TEXT,
    
    -- Constraints
    min_value REAL,
    max_value REAL,
    allowed_values TEXT,  -- JSON array
    
    -- Grouping
    group_name TEXT DEFAULT 'other',
    to_save BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT uq_validation_rule 
        UNIQUE (component_type, attribute_name),
    CONSTRAINT valid_component_type_validation 
        CHECK (component_type IN ('BUS', 'GENERATOR', 'LOAD', 'LINE', 'LINK', 'STORAGE_UNIT', 'STORE', 'UNMET_LOAD', 'CONSTRAINT', 'TRANSFORMER', 'SHUNT_IMPEDANCE')),
    CONSTRAINT valid_data_type 
        CHECK (data_type IN ('float', 'boolean', 'string', 'int')),
    CONSTRAINT valid_allowed_storage_types 
        CHECK (allowed_storage_types IN ('static', 'timeseries', 'static_or_timeseries')),
    CONSTRAINT valid_group_name 
        CHECK (group_name IN ('basic', 'capacity', 'power_limits', 'energy', 'unit_commitment', 'ramping', 'costs', 'electrical'))
);

-- Essential indexes only
CREATE INDEX idx_validation_component_type ON attribute_validation_rules(component_type);
CREATE INDEX idx_validation_lookup ON attribute_validation_rules(component_type, attribute_name);

-- ============================================================================
-- SCENARIOS - SPARSE OVERRIDE APPROACH
-- ============================================================================

-- Scenarios table - represents alternative scenarios
-- Base network has NO scenario (scenario_id = NULL in attributes)
-- Supports both deterministic what-if scenarios (probability = NULL) and stochastic scenarios (probability set)
-- System scenarios (is_system_scenario = TRUE) are reserved for special purposes like "Actual" values
CREATE TABLE scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    probability REAL DEFAULT NULL,  -- For stochastic optimization (NULL = deterministic what-if)
    
    -- System scenario flags
    is_system_scenario BOOLEAN DEFAULT FALSE,  -- TRUE = system-reserved, cannot delete, excluded from solves
    system_purpose TEXT DEFAULT NULL,  -- 'actual' for actual/measured values, NULL for user scenarios
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_probability 
        CHECK (probability IS NULL OR (probability >= 0 AND probability <= 1)),
    CONSTRAINT valid_system_purpose
        CHECK (system_purpose IS NULL OR system_purpose IN ('actual'))
);

-- ============================================================================
-- SYSTEM SCENARIO MANAGEMENT
-- ============================================================================

-- Trigger to auto-create the "Actual" system scenario when network_metadata is created
CREATE TRIGGER create_actual_scenario_on_network_create
    AFTER INSERT ON network_metadata
    FOR EACH ROW
    WHEN NOT EXISTS (SELECT 1 FROM scenarios WHERE system_purpose = 'actual')
BEGIN
    INSERT INTO scenarios (name, description, is_system_scenario, system_purpose)
    VALUES ('Actual', 'Actual/measured values for validation and comparison', TRUE, 'actual');
END;

-- Trigger to prevent deletion of system scenarios
CREATE TRIGGER prevent_system_scenario_deletion
    BEFORE DELETE ON scenarios
    FOR EACH ROW
    WHEN OLD.is_system_scenario = TRUE
BEGIN
    SELECT RAISE(ABORT, 'Cannot delete system scenarios');
END;

-- Trigger to prevent modification of system scenario flags
CREATE TRIGGER prevent_system_scenario_modification
    BEFORE UPDATE ON scenarios
    FOR EACH ROW
    WHEN OLD.is_system_scenario = TRUE AND (
        NEW.is_system_scenario != OLD.is_system_scenario OR 
        NEW.system_purpose != OLD.system_purpose
    )
BEGIN
    SELECT RAISE(ABORT, 'Cannot modify system scenario flags');
END;

-- ============================================================================
-- UNIFIED COMPONENT ATTRIBUTES - SPARSE SCENARIOS + RAW TIMESERIES
-- ============================================================================

-- Component attributes - sparse scenario overrides
-- scenario_id = NULL → Base network (editable)
-- scenario_id = 1    → Scenario 1 (overrides base, read-only)
CREATE TABLE component_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_id INTEGER NOT NULL,
    attribute_name TEXT NOT NULL,
    
    -- Scenario support - NULL = base network, non-NULL = scenario override
    scenario_id INTEGER,  -- NULLABLE!
    
    -- Storage type
    storage_type TEXT NOT NULL CHECK (storage_type IN ('static', 'timeseries')),
    
    -- Value storage
    static_value TEXT,      -- JSON-encoded static value (all data types)
    timeseries_data BLOB,   -- Raw f32 array (NOT Parquet!)
    
    -- Cached metadata
    data_type TEXT NOT NULL,
    unit TEXT,
    is_input BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_attributes_component 
        FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE,
    CONSTRAINT fk_attributes_scenario 
        FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE,
    
    -- Storage validation
    CONSTRAINT check_exactly_one_storage_type CHECK (
        (storage_type = 'static' AND static_value IS NOT NULL AND timeseries_data IS NULL) OR
        (storage_type = 'timeseries' AND static_value IS NULL AND timeseries_data IS NOT NULL)
    ),
    
    -- Unique per component/attribute/scenario (NULL scenario counts as unique value)
    CONSTRAINT uq_component_attribute_scenario 
        UNIQUE (component_id, attribute_name, scenario_id)
);

-- Essential indexes only
CREATE INDEX idx_attributes_lookup ON component_attributes(
    component_id, attribute_name, scenario_id
);
CREATE INDEX idx_attributes_scenario ON component_attributes(scenario_id);

-- ============================================================================
-- SCENARIO CACHE - MATERIALIZED VIEW FOR FAST SCENARIO COUNTING
-- ============================================================================

-- Scenario cache - stores precomputed scenario counts and details
-- This is a materialized view that's kept in sync via application code
-- Updated transactionally whenever attribute values change
CREATE TABLE IF NOT EXISTS attribute_scenario_cache (
    component_id INTEGER NOT NULL,
    attribute_name TEXT NOT NULL,
    
    -- Cached computed values
    scenario_count INTEGER NOT NULL DEFAULT 1,      -- Display count (includes synthetic base)
    has_base_value BOOLEAN NOT NULL DEFAULT FALSE,  -- TRUE if base network has value
    has_scenario_values BOOLEAN NOT NULL DEFAULT FALSE, -- TRUE if any scenarios have values
    
    -- Scenario details for dropdown (JSON array)
    -- Format: [{scenario_id: 0, scenario_name: "Base", value: "123", has_value: true}, ...]
    scenario_details TEXT,
    
    -- Metadata
    last_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (component_id, attribute_name),
    CONSTRAINT fk_scenario_cache_component 
        FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
);

-- Index for fast component-based lookups
CREATE INDEX IF NOT EXISTS idx_scenario_cache_component 
    ON attribute_scenario_cache(component_id);

-- Index for bulk table loads
CREATE INDEX IF NOT EXISTS idx_scenario_cache_component_type
    ON attribute_scenario_cache(component_id, attribute_name);

-- NOTES:
-- This cache is maintained by application code (Rust) in the same transaction
-- as attribute writes. This ensures ACID guarantees - the cache can never be
-- stale or inconsistent with the actual data.
--
-- Cache logic:
-- - If has_scenario_values: scenario_count = num_scenarios + 1 (always include base)
-- - If only has_base_value: scenario_count = 1 (no indicator shown)
-- - If neither: scenario_count = 0 (no values at all)

-- ============================================================================
-- VALIDATION TRIGGERS
-- ============================================================================

-- Trigger to validate attributes against rules on insert
CREATE TRIGGER validate_component_attribute_insert
    BEFORE INSERT ON component_attributes
    FOR EACH ROW
    WHEN NOT EXISTS (
        SELECT 1 FROM components c
        JOIN attribute_validation_rules avr ON c.component_type = avr.component_type
        WHERE c.id = NEW.component_id 
        AND avr.attribute_name = NEW.attribute_name
    )
BEGIN
    SELECT RAISE(ABORT, 'Attribute is not defined for this component type');
END;

-- Trigger to validate storage type on insert
CREATE TRIGGER validate_storage_type_insert
    BEFORE INSERT ON component_attributes
    FOR EACH ROW
    WHEN EXISTS (
        SELECT 1 FROM components c
        JOIN attribute_validation_rules avr ON c.component_type = avr.component_type
        WHERE c.id = NEW.component_id
        AND avr.attribute_name = NEW.attribute_name
        AND avr.allowed_storage_types != 'static_or_timeseries'
        AND avr.allowed_storage_types != NEW.storage_type
    )
BEGIN
    SELECT RAISE(ABORT, 'Storage type not allowed for this attribute');
END;

-- Trigger to update timestamps
CREATE TRIGGER update_component_attributes_timestamp
    BEFORE UPDATE ON component_attributes
    FOR EACH ROW
BEGIN
    UPDATE component_attributes 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

-- Trigger to update component timestamps when attributes change
CREATE TRIGGER update_component_timestamp_on_attribute_change
    AFTER INSERT ON component_attributes
    FOR EACH ROW
BEGIN
    UPDATE components 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.component_id;
END;

-- ============================================================================
-- NETWORK CONFIGURATION
-- ============================================================================

-- Network configuration parameters with scenario support
CREATE TABLE network_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id INTEGER, -- NULL for network defaults
    
    param_name TEXT NOT NULL,
    param_type TEXT NOT NULL,
    param_value TEXT NOT NULL,
    param_description TEXT,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_network_config_scenario 
        FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE,
    CONSTRAINT uq_network_config_param 
        UNIQUE (scenario_id, param_name),
    CONSTRAINT valid_param_type 
        CHECK (param_type IN ('boolean', 'real', 'integer', 'string', 'json'))
);

CREATE INDEX idx_network_config_lookup ON network_config(scenario_id, param_name);

-- ============================================================================
-- SYSTEM METADATA
-- ============================================================================

-- System metadata table for schema version tracking and system-level settings
CREATE TABLE system_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_system_metadata_key ON system_metadata(key);

-- Initialize system metadata with schema version
INSERT INTO system_metadata (key, value, description) 
VALUES ('schema_version', '3.1.0', 'Database schema version');

-- ============================================================================
-- SCHEMA VERSION
-- ============================================================================

PRAGMA user_version = 31;  -- Schema version 3.1
