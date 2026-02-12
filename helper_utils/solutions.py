#!/usr/bin/env python3
"""
SQL CTF: Kernel Module Detective - SOLUTIONS
⚠️  SPOILER WARNING: This file contains complete solutions!
Only consult if you're truly stuck on a challenge.
"""

import sqlite3

# Connect to database
conn = sqlite3.connect('kernel_logs.db')
cursor = conn.cursor()

print("=" * 70)
print("SQL CTF SOLUTIONS - SPOILER WARNING!")
print("=" * 70)
print()

# ============================================================================
# TIER 1: RECONNAISSANCE
# ============================================================================
print("TIER 1: RECONNAISSANCE")
print("-" * 70)

print("\nChallenge 1.1: Table Discovery")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"Tables found: {[t[0] for t in tables]}")

print("\nChallenge 1.2: Boot Session Analysis")
cursor.execute("""
    SELECT DISTINCT boot_session
    FROM boot_logs
    WHERE log_level IN ('ERROR', 'CRIT')
    ORDER BY boot_session
""")
sessions = cursor.fetchall()
print(f"Boot sessions with errors: {[s[0] for s in sessions]}")

# ============================================================================
# TIER 2: PATTERN RECOGNITION
# ============================================================================
print("\n" + "=" * 70)
print("TIER 2: PATTERN RECOGNITION")
print("-" * 70)

print("\nChallenge 2.1: Failed Module Loads")
cursor.execute("""
    SELECT 
        module_name,
        COUNT(*) AS failure_count
    FROM module_events
    WHERE status = 'FAILED'
    GROUP BY module_name
    HAVING COUNT(*) > 0
    ORDER BY failure_count DESC
    LIMIT 10
""")
results = cursor.fetchall()
print(f"{'Module':<25} {'Failures':>10}")
print("-" * 40)
for module, count in results:
    print(f"{module:<25} {count:>10}")

print("\nChallenge 2.2: Cross-Table Investigation")
cursor.execute("""
    SELECT DISTINCT me.module_name
    FROM module_events AS me
    INNER JOIN error_codes AS ec
        ON me.module_name = ec.affected_module
    WHERE me.status = 'FAILED'
        AND ec.severity IN ('HIGH', 'CRITICAL')
    ORDER BY me.module_name
""")
results = cursor.fetchall()
print(f"Modules with both failed loads and critical errors:")
for (module,) in results:
    print(f"  • {module}")

# ============================================================================
# TIER 3: ADVANCED CORRELATION
# ============================================================================
print("\n" + "=" * 70)
print("TIER 3: ADVANCED CORRELATION")
print("-" * 70)

print("\nChallenge 3.1: The Triple Threat")
cursor.execute("""
    SELECT 
        me.module_name,
        COUNT(DISTINCT me.event_id) AS failed_loads,
        COUNT(DISTINCT ec.error_id) AS critical_errors,
        COUNT(DISTINCT mem.mem_id) AS memory_failures
    FROM module_events AS me
    INNER JOIN error_codes AS ec
        ON me.module_name = ec.affected_module
        AND ec.severity = 'CRITICAL'
    INNER JOIN memory_events AS mem
        ON me.module_name = mem.requesting_module
        AND mem.allocation_success = 0
    WHERE me.status = 'FAILED'
    GROUP BY me.module_name
    HAVING COUNT(DISTINCT me.event_id) > 0
        AND COUNT(DISTINCT ec.error_id) > 0
        AND COUNT(DISTINCT mem.mem_id) > 0
    ORDER BY (COUNT(DISTINCT me.event_id) + 
              COUNT(DISTINCT ec.error_id) + 
              COUNT(DISTINCT mem.mem_id)) DESC
""")
results = cursor.fetchall()
print(f"{'Module':<25} {'Failed Loads':>12} {'Crit Errors':>12} {'Mem Fails':>12}")
print("-" * 70)
for module, loads, errors, mem in results:
    print(f"{module:<25} {loads:>12} {errors:>12} {mem:>12}")

print("\nChallenge 3.2: Temporal Analysis")
cursor.execute("""
    SELECT DISTINCT me.module_name
    FROM module_events AS me
    INNER JOIN system_calls AS sc
        ON me.module_name = sc.caller_module
    WHERE me.boot_session IN (2, 3)
        AND sc.return_code < 0
        AND ABS(me.timestamp - sc.timestamp) < 100
    ORDER BY me.module_name
""")
results = cursor.fetchall()
print("Modules with syscall failures within 100s of module load:")
for (module,) in results:
    print(f"  • {module}")

# ============================================================================
# TIER 4: STATISTICAL ANOMALY DETECTION
# ============================================================================
print("\n" + "=" * 70)
print("TIER 4: STATISTICAL ANOMALY DETECTION")
print("-" * 70)

print("\nChallenge 4.1: Memory Allocation Anomaly")
cursor.execute("""
    SELECT 
        requesting_module,
        COUNT(*) AS total_requests,
        SUM(CASE WHEN allocation_success = 0 THEN 1 ELSE 0 END) AS failures,
        ROUND(
            CAST(SUM(CASE WHEN allocation_success = 0 THEN 1 ELSE 0 END) AS REAL) / 
            COUNT(*) * 100, 
            2
        ) AS failure_rate_pct
    FROM memory_events
    GROUP BY requesting_module
    HAVING COUNT(*) >= 5
        AND failure_rate_pct > 40
    ORDER BY failure_rate_pct DESC
""")
results = cursor.fetchall()
print(f"{'Module':<25} {'Total Req':>10} {'Failures':>10} {'Rate %':>10}")
print("-" * 70)
for module, total, failures, rate in results:
    print(f"{module:<25} {total:>10} {failures:>10} {rate:>10.1f}")

print("\nChallenge 4.2: The Network Stack Investigation")
cursor.execute("""
    SELECT DISTINCT dd.parent_module
    FROM device_drivers AS dd
    INNER JOIN error_codes AS ec
        ON dd.parent_module = ec.affected_module
    WHERE dd.driver_name IN ('eth0', 'wlan0')
        AND dd.initialization_status = 'FAILED'
        AND ec.subsystem = 'network'
    GROUP BY dd.parent_module
    HAVING COUNT(DISTINCT dd.driver_id) >= 2
""")
results = cursor.fetchall()
print("Modules causing network driver failures:")
for (module,) in results:
    print(f"  • {module}")

# ============================================================================
# TIER 5: THE FINAL PROOF
# ============================================================================
print("\n" + "=" * 70)
print("TIER 5: THE FINAL PROOF")
print("-" * 70)

print("\nChallenge 5.1: Unified Timeline (sample for one module)")
# This shows timeline for the faulty module
cursor.execute("""
    SELECT 
        timestamp,
        'MODULE_EVENT' AS event_type,
        status AS detail,
        boot_session
    FROM module_events
    WHERE module_name = 'corrupted_netfilter'
    
    UNION ALL
    
    SELECT 
        timestamp,
        'ERROR_CODE' AS event_type,
        severity AS detail,
        NULL AS boot_session
    FROM error_codes
    WHERE affected_module = 'corrupted_netfilter'
    
    UNION ALL
    
    SELECT 
        timestamp,
        'MEMORY_EVENT' AS event_type,
        CASE WHEN allocation_success = 0 THEN 'FAILED' ELSE 'SUCCESS' END AS detail,
        NULL AS boot_session
    FROM memory_events
    WHERE requesting_module = 'corrupted_netfilter'
    
    ORDER BY timestamp
    LIMIT 20
""")
results = cursor.fetchall()
print(f"{'Timestamp':<15} {'Event Type':<15} {'Detail':<15} {'Session':<10}")
print("-" * 70)
for ts, evt_type, detail, session in results:
    session_str = str(int(session)) if session else 'N/A'
    print(f"{ts:<15.2f} {evt_type:<15} {detail:<15} {session_str:<10}")

print("\nChallenge 5.2: The Smoking Gun - COMPREHENSIVE ANALYSIS")
cursor.execute("""
    WITH 
    failed_loads AS (
        SELECT 
            module_name,
            COUNT(*) AS failed_load_count
        FROM module_events
        WHERE status = 'FAILED'
        GROUP BY module_name
    ),
    critical_errors AS (
        SELECT 
            affected_module,
            COUNT(*) AS critical_error_count
        FROM error_codes
        WHERE severity = 'CRITICAL'
        GROUP BY affected_module
    ),
    memory_stats AS (
        SELECT 
            requesting_module,
            COUNT(*) AS total_allocs,
            SUM(CASE WHEN allocation_success = 0 THEN 1 ELSE 0 END) AS failed_allocs,
            ROUND(
                CAST(SUM(CASE WHEN allocation_success = 0 THEN 1 ELSE 0 END) AS REAL) / 
                COUNT(*) * 100,
                2
            ) AS mem_failure_rate
        FROM memory_events
        GROUP BY requesting_module
    ),
    network_failures AS (
        SELECT 
            parent_module,
            COUNT(*) AS net_init_failures
        FROM device_drivers
        WHERE initialization_status = 'FAILED'
            AND driver_name IN ('eth0', 'wlan0')
        GROUP BY parent_module
    ),
    syscall_failures AS (
        SELECT 
            caller_module,
            COUNT(*) AS syscall_fail_count
        FROM system_calls
        WHERE return_code < 0
        GROUP BY caller_module
    )
    
    SELECT 
        fl.module_name,
        COALESCE(fl.failed_load_count, 0) AS failed_loads,
        COALESCE(ce.critical_error_count, 0) AS critical_errors,
        COALESCE(ms.mem_failure_rate, 0) AS mem_failure_pct,
        COALESCE(nf.net_init_failures, 0) AS network_failures,
        COALESCE(sf.syscall_fail_count, 0) AS syscall_failures,
        -- Danger score (weighted)
        (COALESCE(fl.failed_load_count, 0) * 3 +
         COALESCE(ce.critical_error_count, 0) * 5 +
         COALESCE(nf.net_init_failures, 0) * 4 +
         COALESCE(sf.syscall_fail_count, 0) * 1) AS danger_score
    FROM failed_loads AS fl
    LEFT JOIN critical_errors AS ce ON fl.module_name = ce.affected_module
    LEFT JOIN memory_stats AS ms ON fl.module_name = ms.requesting_module
    LEFT JOIN network_failures AS nf ON fl.module_name = nf.parent_module
    LEFT JOIN syscall_failures AS sf ON fl.module_name = sf.caller_module
    WHERE fl.failed_load_count >= 3
        AND COALESCE(ce.critical_error_count, 0) >= 2
        AND COALESCE(ms.mem_failure_rate, 0) > 35
    ORDER BY danger_score DESC
""")

results = cursor.fetchall()
print(f"\n{'=' * 110}")
print(f"{'Module':<25} {'Failed':>7} {'Crit':>7} {'Mem%':>7} {'Net':>7} {'Sys':>7} {'SCORE':>10}")
print(f"{'':25} {'Loads':>7} {'Errs':>7} {'Fail':>7} {'Fail':>7} {'Fail':>7} {'':>10}")
print(f"{'=' * 110}")
for module, loads, errs, mem_pct, net, sys, score in results:
    print(f"{module:<25} {loads:>7} {errs:>7} {mem_pct:>6.1f}% {net:>7} {sys:>7} {score:>10}")

print(f"{'=' * 110}")

# ============================================================================
# THE FLAG
# ============================================================================
print("\n" + "=" * 70)
print("🎯 THE FLAG")
print("=" * 70)

if results:
    culprit = results[0][0]  # Top result by danger score
    print(f"\n✅ CULPRIT IDENTIFIED: {culprit}")
    print(f"\n🏆 FLAG: CTF{{{culprit}}}")
    print(f"\nCongratulations! You've successfully identified the faulty kernel module!")
else:
    print("\n❌ No module meets all criteria. Review the queries above.")

print("\n" + "=" * 70)

# Close connection
conn.close()

print("\n💡 Key SQL Concepts Used:")
print("  • Multiple CTEs (WITH clauses)")
print("  • LEFT JOINs for optional relationships")
print("  • COALESCE for NULL handling")
print("  • Complex aggregations")
print("  • Calculated fields (danger score)")
print("  • HAVING clause for post-aggregation filtering")
print("  • UNION for combining heterogeneous data")
print("\n🎓 You've mastered advanced SQL! Well done!")
