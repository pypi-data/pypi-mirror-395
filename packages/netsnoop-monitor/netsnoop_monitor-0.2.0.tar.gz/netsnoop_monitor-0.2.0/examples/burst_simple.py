#!/usr/bin/env python3
"""
Test Process Burst Anomaly
This script will trigger a HIGH burst alert (>10 processes in 10s)
"""

import subprocess
import sys

print("⚠️  Process Burst Test - Spawning multiple processes...")
print("   This will create 15 new Python processes")
print("   Your monitor should show a HIGH BURST alert immediately")

processes = []

for i in range(15):
    # Spawn a process that sleeps for 10 seconds
    proc = subprocess.Popen(
        [sys.executable, '-c', 'import time; time.sleep(10)'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    processes.append(proc)
    print(f"   Spawned process {i+1}/15 (PID: {proc.pid})")

print("\n✅ All processes spawned!")
print("   Your monitor should show a BURST alert now")
print("\n⏳ Waiting for processes to finish...")

# Wait for all processes to complete
for proc in processes:
    proc.wait()

print("👋 Test complete!")