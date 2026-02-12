#!/usr/bin/env python3
"""
SQL CTF: Query Starter Template
Use this template to start working on the challenges
"""

import sqlite3
from typing import List, Tuple

# ============================================================================
# DATABASE CONNECTION
# ============================================================================
def get_connection(db_path: str = 'kernel_logs.db') -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(db_path)
    # Enable foreign keys if needed
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def run_query(query: str, params: tuple = ()) -> List[Tuple]:
    """
    Execute a query and return all results.
    
    Args:
        query: SQL query string
        params: Query parameters (for parameterized queries)
    
    Returns:
        List of result tuples
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def print_results(results: List[Tuple], headers: List[str] = None):
    """
    Pretty print query results.
    
    Args:
        results: List of result tuples
        headers: Optional column headers
    """
    if not results:
        print("No results found.")
        return
    
    # Calculate column widths
    col_widths = [max(len(str(val)) for val in col) for col in zip(*results)]
    
    if headers:
        col_widths = [max(w, len(h)) for w, h in zip(col_widths, headers)]
        # Print headers
        header_row = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
        print(header_row)
        print("-" * len(header_row))
    
    # Print rows
    for row in results:
        print(" | ".join(str(val).ljust(w) for val, w in zip(row, col_widths)))
    
    print(f"\n({len(results)} rows)")

# ============================================================================
# EXPLORATION QUERIES
# ============================================================================
def explore_schema():
    """Print database schema information."""
    print("=" * 70)
    print("DATABASE SCHEMA")
    print("=" * 70)
    
    # Get all tables
    tables = run_query("SELECT name FROM sqlite_master WHERE type='table'")
    
    for (table_name,) in tables:
        print(f"\n📊 Table: {table_name}")
        print("-" * 70)
        
        # Get column info
        schema = run_query(f"PRAGMA table_info({table_name})")
        print(f"{'Column':<20} {'Type':<15} {'Not Null':<10} {'Default':<15}")
        print("-" * 70)
        for col in schema:
            cid, name, type_, notnull, default, pk = col
            print(f"{name:<20} {type_:<15} {bool(notnull)!s:<10} {str(default):<15}")
        
        # Get row count
        count = run_query(f"SELECT COUNT(*) FROM {table_name}")[0][0]
        print(f"\nTotal rows: {count}")

def sample_data(table_name: str, limit: int = 5):
    """Show sample data from a table."""
    print(f"\n📋 Sample data from {table_name}:")
    print("=" * 70)
    results = run_query(f"SELECT * FROM {table_name} LIMIT {limit}")
    
    # Get column names
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    headers = [desc[0] for desc in cursor.description]
    conn.close()
    
    print_results(results, headers)

# ============================================================================
# YOUR CHALLENGE QUERIES GO HERE
# ============================================================================

# Tier 1: Reconnaissance
# ----------------------
def tier1_challenge1():
    """Challenge 1.1: Table Discovery"""
    query = """
    -- Your query here
    SELECT name FROM sqlite_master WHERE type='table'
    """
    results = run_query(query)
    print("\n🎯 Tier 1.1 - Tables in database:")
    print_results(results, ["Table Name"])

def tier1_challenge2():
    """Challenge 1.2: Boot Session Analysis"""
    query = """
    -- TODO: Find boot sessions with ERROR or CRIT level events
    -- Your query here
    """
    # results = run_query(query)
    # print_results(results, ["Boot Session"])
    print("TODO: Implement this query")

# Tier 2: Pattern Recognition
# ---------------------------
def tier2_challenge1():
    """Challenge 2.1: Failed Module Loads"""
    query = """
    -- TODO: Find modules that failed to load, count failures
    -- Your query here
    """
    print("TODO: Implement this query")

def tier2_challenge2():
    """Challenge 2.2: Cross-Table Investigation"""
    query = """
    -- TODO: Find modules in BOTH failed loads AND critical errors
    -- Your query here
    """
    print("TODO: Implement this query")

# Tier 3: Advanced Correlation
# ----------------------------
def tier3_challenge1():
    """Challenge 3.1: The Triple Threat"""
    query = """
    -- TODO: Find modules with failed loads, critical errors, AND memory failures
    -- Hint: Use multiple JOINs
    """
    print("TODO: Implement this query")

def tier3_challenge2():
    """Challenge 3.2: Temporal Analysis"""
    query = """
    -- TODO: Find modules with syscall failures within 100s of module load
    -- Hint: Use timestamp arithmetic
    """
    print("TODO: Implement this query")

# Tier 4: Statistical Anomaly Detection
# -------------------------------------
def tier4_challenge1():
    """Challenge 4.1: Memory Allocation Anomaly"""
    query = """
    -- TODO: Calculate memory allocation failure rate
    -- Filter: >= 5 requests, >40% failure rate
    """
    print("TODO: Implement this query")

def tier4_challenge2():
    """Challenge 4.2: Network Stack Investigation"""
    query = """
    -- TODO: Find module causing network driver failures
    """
    print("TODO: Implement this query")

# Tier 5: The Final Proof
# -----------------------
def tier5_challenge1():
    """Challenge 5.1: Unified Timeline"""
    query = """
    -- TODO: Create unified timeline using UNION
    """
    print("TODO: Implement this query")

def tier5_challenge2():
    """Challenge 5.2: The Smoking Gun"""
    query = """
    -- TODO: Comprehensive analysis with CTEs
    -- This is the big one!
    """
    print("TODO: Implement this query")

# ============================================================================
# CUSTOM QUERIES
# ============================================================================
def my_custom_query():
    """Your own experimental queries go here."""
    query = """
    -- Experiment here
    SELECT * FROM module_events LIMIT 10
    """
    results = run_query(query)
    print_results(results)

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("🎯 SQL CTF: Kernel Module Detective")
    print("=" * 70)
    
    # Uncomment what you want to run:
    
    # Explore the database
    # explore_schema()
    
    # View sample data
    # sample_data('boot_logs')
    # sample_data('module_events')
    # sample_data('error_codes')
    
    # Run challenge queries
    tier1_challenge1()
    # tier1_challenge2()
    # tier2_challenge1()
    # tier2_challenge2()
    # tier3_challenge1()
    # tier3_challenge2()
    # tier4_challenge1()
    # tier4_challenge2()
    # tier5_challenge1()
    # tier5_challenge2()
    
    # Custom queries
    # my_custom_query()
    
    print("\n✅ Query execution complete!")
    print("💡 Edit this file to add your own queries")
    print("📖 Consult sql_reference.pdf for syntax help")
