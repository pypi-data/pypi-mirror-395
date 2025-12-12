#!/usr/bin/env python3
"""
Demo script to run the scheduler for 10 seconds
"""
import time
import sys
from scheduler.engine import SchedulerEngine

print("\n" + "="*60)
print("🚀 SCHEDULER DEMO RUN (10 seconds)")
print("="*60 + "\n")

engine = SchedulerEngine()
jobs = engine.list_jobs()

print(f"📋 Loaded {len(jobs)} jobs:")
for job in jobs:
    print(f"   • {job['name']} - next run: {job['next_run']}")

print("\n⏱️  Starting scheduler for 10 seconds...\n")

engine.start()

# Run for 10 seconds
for i in range(10):
    time.sleep(1)
    sys.stdout.write(f"\r⏳ Running... {i+1}/10 seconds")
    sys.stdout.flush()

print("\n\n🛑 Stopping scheduler...")
engine.stop()

# Wait a bit for threads to finish
time.sleep(2)

print("\n✅ Demo completed!")
print("\n" + "="*60)
print("📊 Final job state:")
print("="*60)
for job in engine.list_jobs():
    print(f"   • {job['name']}")
    print(f"     Next run: {job['next_run']}")
    print(f"     Running: {job.get('running', False)}\n")
