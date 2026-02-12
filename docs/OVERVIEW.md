# 🎯 SQL CTF: Kernel Module Detective

Welcome to the **Kernel Module Detective** SQL Capture The Flag challenge! Hunt down a faulty kernel module through progressively difficult SQL queries.

## 📦 What's Included

```
sql-ctf/
├── kernel_logs.db          # SQLite database (~1500 records)
├── docs
    ├── challenges.md       # 5 tiers of SQL challenges
    ├── OVERVIEW.md         # This file
    └── sql_reference.pdf   # Comprehensive SQL syntax guide
├── helper_utils
    ├── generate_ctf_db.py  # Database generator script
    ├── query_starter.py    # Feel free to reference this, or remix my original pandas implementation
    └── solutions.py        # Sample solutions (spoiler warning!)
├── solutions/
    ├── challenge_n.py      # User solutions/working attempts
    └── __init.py__
```

## 🎮 Quick Start

### Option 1: Python (Recommended)

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('kernel_logs.db')
cursor = conn.cursor()

# Example query
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(tables)

# Your CTF queries here...
```

### Option 2: Command Line

```bash
# Open database in CLI
sqlite3 kernel_logs.db

# List tables
.tables

# Run queries
SELECT * FROM boot_logs LIMIT 5;

# Enable formatted output
.mode column
.headers on
```

### Option 3: DB Browser (GUI)

Download [DB Browser for SQLite](https://sqlitebrowser.org/) for a visual interface.

## 📊 Database Schema

### Table Overview

| Table | Records | Description |
|-------|---------|-------------|
| `boot_logs` | ~600 | Main kernel log entries with timestamps and messages |
| `module_events` | ~150 | Module loading/unloading events |
| `error_codes` | ~90 | Detailed error information with severity levels |
| `system_calls` | ~120 | System call failures and return codes |
| `device_drivers` | ~75 | Device initialization status |
| `memory_events` | ~105 | Memory allocation successes/failures |

### Key Relationships

```
module_events.module_name ←→ error_codes.affected_module
module_events.module_name ←→ system_calls.caller_module  
module_events.module_name ←→ device_drivers.parent_module
module_events.module_name ←→ memory_events.requesting_module
```

## 🎯 Challenge Structure

### Tier 1: Reconnaissance (EASY)
- Basic SELECT and filtering
- Understanding the schema
- Simple aggregations
- **Estimated time:** 15-20 minutes

### Tier 2: Pattern Recognition (MEDIUM)
- GROUP BY and aggregate functions
- Multiple conditions
- INNER JOINs
- **Estimated time:** 30-40 minutes

### Tier 3: Advanced Correlation (HARD)
- Multiple JOINs across 3+ tables
- Temporal analysis
- Subqueries
- **Estimated time:** 45-60 minutes

### Tier 4: Statistical Anomaly Detection (VERY HARD)
- CTEs (Common Table Expressions)
- Calculated fields
- Complex aggregations
- **Estimated time:** 45-60 minutes

### Tier 5: The Final Proof (EXPERT)
- UNION operations
- Comprehensive multi-table analysis
- Window functions (bonus)
- **Estimated time:** 30-45 minutes

**Total estimated time:** 2.5-4 hours

## 🔍 The Mission

A production server is experiencing kernel panics. Your job:

1. **Analyze** logs across 3 boot sessions
2. **Correlate** failures across multiple subsystems
3. **Identify** the faulty kernel module
4. **Prove** it with SQL evidence

**The flag:** The name of the corrupted module (format: `CTF{module_name}`)

## 💡 Tips

- Read `challenges.md` for detailed tier descriptions
- Consult `sql_reference.pdf` when stuck on syntax
- Build queries incrementally - test as you go
- Most challenges have multiple valid solutions
- Look for patterns across boot sessions 2 and 3
- The faulty module leaves traces in multiple tables

## 🚨 Spoiler Warning

The `solutions.py` file contains complete answers. Only peek if you're truly stuck!

## 📚 Learning Objectives

By completing this CTF, you'll master:

✅ Complex multi-table JOINs  
✅ Subqueries and CTEs  
✅ Aggregate functions with GROUP BY  
✅ HAVING vs WHERE clauses  
✅ Set operations (UNION, INTERSECT)  
✅ Boolean logic and operator precedence  
✅ Temporal data analysis  
✅ Window functions (advanced)  

## 🏆 Validation

Once you think you've found the culprit:

```python
suspect = "your_module_name_here"

# Run comprehensive verification
cursor.execute(f"""
    SELECT 
        module_name,
        COUNT(*) as total_issues
    FROM (
        SELECT module_name FROM module_events WHERE status = 'FAILED'
        UNION ALL
        SELECT affected_module FROM error_codes WHERE severity = 'CRITICAL'
        UNION ALL
        SELECT requesting_module FROM memory_events WHERE allocation_success = 0
    )
    WHERE module_name = '{suspect}'
    GROUP BY module_name
""")

result = cursor.fetchone()
if result and result[1] > 15:  # High issue count
    print(f"✅ Likely culprit: {result[0]} with {result[1]} critical issues")
else:
    print("❌ Keep searching...")
```

## 🎓 Additional Resources

- [SQLite Documentation](https://www.sqlite.org/lang.html)
- [SQL Tutorial](https://www.sqltutorial.org/)
- [Window Functions Explained](https://www.sqlite.org/windowfunctions.html)

## 🐛 Regenerating the Database

If you want to start fresh or create a new challenge:

```bash
python3 generate_ctf_db.py
```

This will regenerate `kernel_logs.db` with randomized data (but the same culprit).

## 📝 License

This CTF challenge is provided for educational purposes. Feel free to modify and share!

---

**Good luck, detective!** 🔍🎯

*Remember: The truth is in the data, but you need the right query to find it.*
