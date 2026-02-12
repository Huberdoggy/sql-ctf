#!/usr/bin/env python3
"""
SQL CTF: Kernel Module Detective
Generates a SQLite database with simulated dmesg logs
Goal: Find the faulty kernel module across 5 tiers of difficulty
"""

import sqlite3
import random
import string
from datetime import datetime, timedelta

# Database connection
db_path = 'kernel_logs.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS boot_logs")
cursor.execute("DROP TABLE IF EXISTS module_events")
cursor.execute("DROP TABLE IF EXISTS error_codes")
cursor.execute("DROP TABLE IF EXISTS system_calls")
cursor.execute("DROP TABLE IF EXISTS device_drivers")
cursor.execute("DROP TABLE IF EXISTS memory_events")

# Table 1: Boot Logs - Main log entries
cursor.execute("""
CREATE TABLE boot_logs (
    log_id INTEGER PRIMARY KEY,
    timestamp REAL,
    log_level TEXT,
    subsystem TEXT,
    message TEXT,
    boot_session INTEGER
)
""")

# Table 2: Module Events - Module loading/unloading
cursor.execute("""
CREATE TABLE module_events (
    event_id INTEGER PRIMARY KEY,
    timestamp REAL,
    module_name TEXT,
    action TEXT,
    status TEXT,
    load_address TEXT,
    boot_session INTEGER
)
""")

# Table 3: Error Codes - Detailed error information
cursor.execute("""
CREATE TABLE error_codes (
    error_id INTEGER PRIMARY KEY,
    timestamp REAL,
    error_code TEXT,
    severity TEXT,
    subsystem TEXT,
    affected_module TEXT,
    description TEXT
)
""")

# Table 4: System Calls - System call failures
cursor.execute("""
CREATE TABLE system_calls (
    call_id INTEGER PRIMARY KEY,
    timestamp REAL,
    syscall_name TEXT,
    return_code INTEGER,
    caller_module TEXT,
    process_name TEXT
)
""")

# Table 5: Device Drivers - Device initialization
cursor.execute("""
CREATE TABLE device_drivers (
    driver_id INTEGER PRIMARY KEY,
    timestamp REAL,
    driver_name TEXT,
    device_id TEXT,
    initialization_status TEXT,
    parent_module TEXT
)
""")

# Table 6: Memory Events - Memory allocation issues
cursor.execute("""
CREATE TABLE memory_events (
    mem_id INTEGER PRIMARY KEY,
    timestamp REAL,
    event_type TEXT,
    allocated_bytes INTEGER,
    requesting_module TEXT,
    allocation_success BOOLEAN
)
""")

# Kernel modules (the culprit is 'corrupted_netfilter')
legitimate_modules = [
    'e1000e', 'iwlwifi', 'i915', 'snd_hda_intel', 'uvcvideo',
    'bluetooth', 'usb_storage', 'ext4', 'xfs', 'dm_crypt',
    'kvm_intel', 'vboxdrv', 'nvidia', 'radeon', 'nouveau'
]

faulty_module = 'corrupted_netfilter'
suspicious_modules = ['old_netfilter', 'netfilter_legacy', 'compat_netfilter']

all_modules = legitimate_modules + [faulty_module] + suspicious_modules

subsystems = ['network', 'audio', 'video', 'usb', 'pci', 'disk', 'memory', 'cpu']
log_levels = ['INFO', 'WARN', 'ERROR', 'CRIT', 'DEBUG']

# Generate base timestamp
base_time = datetime(2024, 1, 15, 10, 0, 0).timestamp()

# Helper functions
def random_hex_address():
    return '0x' + ''.join(random.choices('0123456789abcdef', k=16))

def random_error_code():
    return f"ERR_{random.randint(1000, 9999)}"

# Generate data for 3 boot sessions
for boot_session in range(1, 4):
    session_offset = (boot_session - 1) * 3600  # 1 hour apart
    
    # Generate boot logs (200 per session)
    for i in range(200):
        timestamp = base_time + session_offset + i * 2.5
        log_level = random.choice(log_levels) if random.random() > 0.3 else 'INFO'
        subsystem = random.choice(subsystems)
        
        messages = [
            f"Initializing {subsystem} subsystem",
            f"{subsystem.upper()} device detected",
            f"Loading {subsystem} configuration",
            f"{subsystem} ready",
            f"Processing {subsystem} requests"
        ]
        
        # Inject anomalies for the faulty module in session 2 and 3
        if boot_session >= 2 and random.random() < 0.05 and subsystem == 'network':
            messages.append(f"Unusual activity in network stack")
            log_level = 'WARN'
        
        message = random.choice(messages)
        
        cursor.execute("""
            INSERT INTO boot_logs (timestamp, log_level, subsystem, message, boot_session)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, log_level, subsystem, message, boot_session))
    
    # Generate module events (50 per session)
    for i in range(50):
        timestamp = base_time + session_offset + i * 10
        module_name = random.choice(all_modules)
        action = random.choice(['LOAD', 'LOAD', 'LOAD', 'UNLOAD'])  # More loads than unloads
        
        # The faulty module has issues in sessions 2 and 3
        if module_name == faulty_module and boot_session >= 2:
            status = 'FAILED' if random.random() < 0.4 else 'SUCCESS'
        else:
            status = 'SUCCESS' if random.random() > 0.05 else 'FAILED'
        
        load_address = random_hex_address()
        
        cursor.execute("""
            INSERT INTO module_events (timestamp, module_name, action, status, load_address, boot_session)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, module_name, action, status, load_address, boot_session))
    
    # Generate error codes (30 per session)
    for i in range(30):
        timestamp = base_time + session_offset + random.uniform(0, 3600)
        error_code = random_error_code()
        severity = random.choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])
        subsystem = random.choice(subsystems)
        affected_module = random.choice(all_modules)
        
        descriptions = [
            "Resource temporarily unavailable",
            "Invalid memory access",
            "Timeout waiting for resource",
            "Buffer overflow detected",
            "Null pointer dereference",
            "Segmentation fault",
            "Permission denied",
            "Device not responding"
        ]
        
        # Faulty module generates more critical errors
        if affected_module == faulty_module and boot_session >= 2:
            severity = random.choice(['HIGH', 'CRITICAL'])
            descriptions.append("Kernel panic avoided")
            descriptions.append("Stack corruption detected")
            descriptions.append("Memory leak pattern detected")
        
        description = random.choice(descriptions)
        
        cursor.execute("""
            INSERT INTO error_codes (timestamp, error_code, severity, subsystem, affected_module, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, error_code, severity, subsystem, affected_module, description))
    
    # Generate system calls (40 per session)
    for i in range(40):
        timestamp = base_time + session_offset + random.uniform(0, 3600)
        syscalls = ['open', 'read', 'write', 'ioctl', 'mmap', 'socket', 'connect', 'bind']
        syscall_name = random.choice(syscalls)
        return_code = 0 if random.random() > 0.2 else random.choice([-1, -2, -11, -22])
        caller_module = random.choice(all_modules)
        
        processes = ['systemd', 'NetworkManager', 'pulseaudio', 'Xorg', 'firefox', 'chrome']
        process_name = random.choice(processes)
        
        # Faulty module causes syscall failures
        if caller_module == faulty_module and boot_session >= 2:
            return_code = random.choice([-1, -11, -22])
        
        cursor.execute("""
            INSERT INTO system_calls (timestamp, syscall_name, return_code, caller_module, process_name)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, syscall_name, return_code, caller_module, process_name))
    
    # Generate device drivers (25 per session)
    for i in range(25):
        timestamp = base_time + session_offset + i * 20
        drivers = ['eth0', 'wlan0', 'sda', 'nvidia0', 'audio0', 'usb1', 'bluetooth0']
        driver_name = random.choice(drivers)
        device_id = f"{random.randint(1000, 9999)}:{random.randint(1000, 9999)}"
        initialization_status = 'SUCCESS' if random.random() > 0.1 else 'FAILED'
        parent_module = random.choice(all_modules)
        
        # Network devices fail when faulty module is involved
        if parent_module == faulty_module and driver_name in ['eth0', 'wlan0'] and boot_session >= 2:
            initialization_status = 'FAILED'
        
        cursor.execute("""
            INSERT INTO device_drivers (timestamp, driver_name, device_id, initialization_status, parent_module)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, driver_name, device_id, initialization_status, parent_module))
    
    # Generate memory events (35 per session)
    for i in range(35):
        timestamp = base_time + session_offset + random.uniform(0, 3600)
        event_types = ['ALLOC', 'FREE', 'REALLOC', 'MMAP']
        event_type = random.choice(event_types)
        allocated_bytes = random.randint(1024, 1048576)
        requesting_module = random.choice(all_modules)
        allocation_success = True if random.random() > 0.15 else False
        
        # Faulty module has memory allocation issues
        if requesting_module == faulty_module and boot_session >= 2:
            allocation_success = False if random.random() < 0.5 else True
            allocated_bytes = random.randint(10485760, 104857600)  # Larger allocations
        
        cursor.execute("""
            INSERT INTO memory_events (timestamp, event_type, allocated_bytes, requesting_module, allocation_success)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, event_type, allocated_bytes, requesting_module, allocation_success))

# Create indices for better query performance
cursor.execute("CREATE INDEX idx_boot_logs_session ON boot_logs(boot_session)")
cursor.execute("CREATE INDEX idx_module_events_module ON module_events(module_name)")
cursor.execute("CREATE INDEX idx_error_codes_module ON error_codes(affected_module)")
cursor.execute("CREATE INDEX idx_system_calls_module ON system_calls(caller_module)")
cursor.execute("CREATE INDEX idx_device_drivers_module ON device_drivers(parent_module)")
cursor.execute("CREATE INDEX idx_memory_events_module ON memory_events(requesting_module)")

conn.commit()
conn.close()

print(f"✅ Database '{db_path}' generated successfully!")
print(f"📊 Total records: ~1500 across 6 tables")
print(f"🎯 Hidden faulty module: '{faulty_module}'")
print(f"🔍 Decoy modules: {suspicious_modules}")
print(f"\n🚀 Ready to start the CTF challenge!")
print(f"\nTo begin:")
print(f"1. python3 generate_ctf_db.py  # (you just did this)")
print(f"2. Read challenges.md for the 5 tiers")
print(f"3. Consult sql_reference.pdf when needed")
print(f"4. Query the database using Python sqlite3 or CLI")
