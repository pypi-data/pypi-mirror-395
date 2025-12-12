#!/usr/bin/env python3
"""
Demo script to test the new alert notification feature
"""
import time
import sys
from scheduler.engine import SchedulerEngine

print("\n" + "="*70)
print("🔔 ALERT NOTIFICATION DEMO (5 seconds)")
print("="*70 + "\n")

engine = SchedulerEngine()
jobs = engine.list_jobs()

print(f"📋 Running job: {jobs[0]['name']}")
print("   Expected: Alert dialog + alarm sound + popup notification\n")

engine.start()

# Run for 5 seconds
for i in range(5):
    time.sleep(1)
    sys.stdout.write(f"\r⏳ Running... {i+1}/5 seconds")
    sys.stdout.flush()

print("\n\n🛑 Stopping scheduler...")
engine.stop()
time.sleep(1)

print("\n✅ Alert demo completed!")
print("\n" + "="*70)
print("📊 Features demonstrated:")
print("   ✓ Alert dialog box (macOS)")
print("   ✓ Alarm sound playing")
print("   ✓ Popup notification")
print("   ✓ Job execution tracking")
print("="*70 + "\n")
