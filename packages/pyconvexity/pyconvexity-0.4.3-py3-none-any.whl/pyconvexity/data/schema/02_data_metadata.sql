-- ============================================================================
-- DATA STORAGE AND METADATA SCHEMA
-- Essential tables for data storage and solve results
-- Version 3.1.0 - Simplified for single-network-per-file
-- ============================================================================

-- ============================================================================
-- GENERIC DATA STORAGE
-- ============================================================================

-- Generic data store for arbitrary network-level data
CREATE TABLE network_data_store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,          -- 'config', 'results', 'statistics', 'scripts', etc.
    name TEXT NOT NULL,
    data_format TEXT DEFAULT 'json', -- 'json', 'csv', 'binary', 'text'
    data BLOB NOT NULL,
    metadata TEXT,                   -- JSON metadata
    checksum TEXT,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_datastore_category_name 
        UNIQUE (category, name),
    CONSTRAINT valid_data_format 
        CHECK (data_format IN ('json', 'csv', 'binary', 'text', 'yaml', 'toml'))
);

CREATE INDEX idx_datastore_category ON network_data_store(category);

-- ============================================================================
-- DOCUMENTATION AND NOTES
-- ============================================================================

-- Network-level notes
CREATE TABLE network_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    tags TEXT,  -- JSON array
    note_type TEXT DEFAULT 'note',
    priority INTEGER DEFAULT 0,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_note_type 
        CHECK (note_type IN ('note', 'todo', 'warning', 'info', 'doc'))
);

-- Component-specific notes
CREATE TABLE component_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    tags TEXT,
    note_type TEXT DEFAULT 'note',
    priority INTEGER DEFAULT 0,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_component_notes_component 
        FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE,
    CONSTRAINT valid_component_note_type 
        CHECK (note_type IN ('note', 'todo', 'warning', 'info', 'doc'))
);

CREATE INDEX idx_component_notes_component ON component_notes(component_id);

-- ============================================================================
-- SOLVE RESULTS AND STATISTICS
-- ============================================================================

-- Network solve results - stores solver outputs per scenario
CREATE TABLE network_solve_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id INTEGER,  -- NULL for base network, non-NULL for scenario
    
    -- Solve metadata
    solved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    solver_name TEXT NOT NULL,
    solve_type TEXT NOT NULL,
    solve_status TEXT NOT NULL,
    objective_value REAL,
    solve_time_seconds REAL,
    
    -- Results stored as JSON
    results_json TEXT NOT NULL,
    metadata_json TEXT,
    
    -- Only one result per scenario (including NULL for base network)
    UNIQUE (scenario_id),
    
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE
);

CREATE INDEX idx_solve_results_scenario ON network_solve_results(scenario_id);

-- Year-based solve results for capacity expansion analysis
CREATE TABLE network_solve_results_by_year (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id INTEGER,  -- NULL for base network
    year INTEGER NOT NULL,
    
    results_json TEXT NOT NULL,
    metadata_json TEXT,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_solve_results_year_scenario 
        FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE,
    CONSTRAINT uq_solve_results_year_unique 
        UNIQUE (scenario_id, year),
    CONSTRAINT valid_year CHECK (year >= 1900 AND year <= 2100)
);

CREATE INDEX idx_solve_results_year_scenario ON network_solve_results_by_year(scenario_id);
