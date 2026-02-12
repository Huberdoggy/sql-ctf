# 🎯 SQL CTF: Kernel Module Detective

## Mission Briefing
A critical production server has been experiencing intermittent kernel panics. System logs have been collected across 3 boot sessions. Your mission: identify the faulty kernel module causing the instability.

**The Flag:** The name of the corrupted kernel module

---

## 🎓 Tier 1: Reconnaissance (EASY)
**Objective:** Get familiar with the database structure and identify boot sessions with issues

### Challenge 1.1: Table Discovery
Query the database to list all tables and understand their structure.

**Hint:** Use SQLite's metadata tables
```python
# Sample Python starter code
import sqlite3
conn = sqlite3.connect('kernel_logs.db')
cursor = conn.cursor()

# Your query here
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(tables)
```

### Challenge 1.2: Boot Session Analysis
Which boot session(s) had ERROR or CRIT level events in the boot_logs table?

**Skills Needed:** 
- Basic SELECT with WHERE clause
- DISTINCT keyword
- Filtering by log_level

**Expected Output:** List of boot_session numbers with errors

---

## ⚙️ Tier 2: Pattern Recognition (MEDIUM)
**Objective:** Identify modules with suspicious failure patterns

### Challenge 2.1: Failed Module Loads
Find all modules that failed to load at least once. Count how many times each module failed.

**Skills Needed:**
- GROUP BY
- COUNT aggregate function
- WHERE with specific conditions
- ORDER BY

**Expected Output:** Module names with failure counts, sorted by failure count (descending)

### Challenge 2.2: Cross-Table Investigation
Find modules that appear in BOTH the module_events table with 'FAILED' status AND the error_codes table with 'HIGH' or 'CRITICAL' severity.

**Skills Needed:**
- INNER JOIN or EXISTS
- Multiple conditions in WHERE
- DISTINCT to avoid duplicates

**Hint:** Look for modules that show up in both failure scenarios

---

## 🔍 Tier 3: Advanced Correlation (HARD)
**Objective:** Correlate failures across multiple tables using joins

### Challenge 3.1: The Triple Threat
Find modules that have:
1. Failed module loads (module_events.status = 'FAILED')
2. Critical errors (error_codes.severity = 'CRITICAL')
3. Memory allocation failures (memory_events.allocation_success = False)

**Skills Needed:**
- Multiple INNER JOINs
- Proper join conditions
- Aggregation to count occurrences
- HAVING clause for filtering aggregated results

**Expected Output:** Modules appearing in all three problem categories

### Challenge 3.2: Temporal Analysis
Find modules where system call failures (return_code < 0) occurred within 100 seconds of a module load event in boot_session 2 or 3.

**Skills Needed:**
- Self-join or correlated subquery
- Time-based filtering (timestamp arithmetic)
- Complex WHERE conditions

**Hint:** The faulty module shows temporal clustering of failures

---

## 🎯 Tier 4: Statistical Anomaly Detection (VERY HARD)
**Objective:** Use aggregation and statistical analysis to pinpoint anomalies

### Challenge 4.1: Memory Allocation Anomaly
Calculate the memory allocation failure rate for each module. Find modules where:
- They requested memory at least 5 times
- Their failure rate is above 40%

**Skills Needed:**
- Subqueries or CTEs (Common Table Expressions)
- CAST for float division
- Calculated columns
- Complex aggregation

**Formula:** failure_rate = (failed_allocations / total_allocations) * 100

### Challenge 4.2: The Network Stack Investigation
Network issues are often the symptom. Find the module that:
- Is the parent_module for network drivers (driver_name IN ('eth0', 'wlan0'))
- Has at least 2 failed device initializations in device_drivers table
- Appears in error_codes with subsystem = 'network'

**Skills Needed:**
- Multiple JOINs across 3+ tables
- IN operator
- Subqueries for filtering
- INTERSECT or multiple EXISTS clauses

---

## 🏆 Tier 5: The Final Proof (EXPERT)
**Objective:** Build a comprehensive evidence report using advanced SQL

### Challenge 5.1: Unified Timeline
Create a unified timeline showing ALL problematic events for your suspect module across all tables. Include:
- Timestamp
- Event type (which table it came from)
- Status/severity
- Boot session

**Skills Needed:**
- UNION or UNION ALL
- Column aliasing for consistency
- Type conversion
- Sorting across heterogeneous data

**Expected Output:** Complete chronological audit trail

### Challenge 5.2: The Smoking Gun
Write a single comprehensive query that proves which module is the culprit by showing:
1. Module name
2. Total failed loads
3. Count of critical errors
4. Memory allocation failure rate
5. Network device initialization failures
6. System call failure count

Filter to show only modules with:
- At least 3 failed loads
- At least 2 critical errors
- Memory failure rate > 35%

**Skills Needed:**
- Multiple CTEs (WITH clauses)
- Complex aggregations
- Multiple JOINs
- Subqueries
- Calculated fields

**This query will reveal the flag!**

---

## 📝 Submission Format

Once you've identified the culprit, verify it by running:

```python
suspect_module = "your_answer_here"

# Verification query
verification = f"""
SELECT 
    module_name,
    COUNT(*) as total_issues
FROM (
    SELECT module_name FROM module_events WHERE status = 'FAILED'
    UNION ALL
    SELECT affected_module FROM error_codes WHERE severity = 'CRITICAL'
    UNION ALL
    SELECT requesting_module FROM memory_events WHERE allocation_success = 0
) AS all_issues
WHERE module_name = '{suspect_module}'
GROUP BY module_name
"""

cursor.execute(verification)
result = cursor.fetchone()
print(f"Module: {result[0]}, Total Issues: {result[1]}")
```

**Flag Format:** `CTF{module_name_here}`

---

## 🎁 Bonus Challenges

### Bonus 1: Operational Precedence Puzzle
Find modules where (failed_loads > 2 OR critical_errors > 1) AND memory_failures > 3

Test your understanding of:
- Parentheses in WHERE clauses
- AND vs OR precedence
- Complex boolean logic

### Bonus 2: The Window Function Challenge
Rank all modules by their "danger score" (weighted sum):
- Failed loads × 3
- Critical errors × 5
- Memory failures × 2
- System call failures × 1

**Skills:** 
- Window functions (RANK, ROW_NUMBER)
- Complex calculations
- OVER clause

---

## 🚨 Important Notes

1. **Multiple Approaches:** Most challenges can be solved multiple ways (JOINs vs subqueries vs CTEs)
2. **Efficiency Matters:** Try to write efficient queries - use EXPLAIN QUERY PLAN
3. **Decoys Present:** There are intentional red herrings in the data
4. **Time Matters:** Some failures only appear in certain boot sessions
5. **Consult Reference:** Use the SQL reference PDF when stuck

---

## 🎯 Success Criteria

You've mastered SQL when you can:
- ✅ Write complex multi-table JOINs
- ✅ Use subqueries and CTEs effectively
- ✅ Apply proper GROUP BY and aggregation
- ✅ Handle boolean logic and operator precedence
- ✅ Combine UNION with complex queries
- ✅ Perform temporal analysis with timestamps

Good luck, detective! 🔍

**Estimated Time:** 2-4 hours depending on SQL experience
**Recommended Tools:** Python sqlite3, DB Browser for SQLite, or command-line sqlite3
