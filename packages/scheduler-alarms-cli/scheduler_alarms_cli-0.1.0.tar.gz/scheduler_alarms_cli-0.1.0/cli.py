import argparse
from scheduler.engine import SchedulerEngine

engine = SchedulerEngine()

parser = argparse.ArgumentParser(description="Scheduler & Alarms CLI")
sub = parser.add_subparsers(dest="command")

# add job
add = sub.add_parser("add")
add.add_argument("--name", required=True)
add.add_argument("--time")
add.add_argument("--freq", choices=["once", "daily", "weekly", "hourly", "interval"], default="once")
add.add_argument("--seconds", type=int)

# start
sub.add_parser("start")

# list jobs
sub.add_parser("list")

args = parser.parse_args()

if args.command == "add":
    rule = {"frequency": args.freq}

    if args.freq == "interval":
        if not args.seconds:
            print("Error: --seconds is required for interval jobs")
            exit(1)
        rule["seconds"] = args.seconds
    else:
        if not args.time:
            print(f"Error: --time is required for {args.freq} jobs (format: HH:MM)")
            exit(1)
        rule["time"] = args.time

    try:
        engine.add_job(args.name, "echo task", rule)
        print("Job added successfully.")
    except Exception as e:
        print(f"Error adding job: {e}")
        exit(1)

elif args.command == "list":
    jobs = engine.list_jobs()
    if not jobs:
        print("No jobs scheduled.")
    else:
        for job in jobs:
            print(f"- {job['name']} | next run: {job['next_run']}")

elif args.command == "start":
    print("Starting scheduler... (Ctrl+C to stop)")
    try:
        engine.start()
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        engine.stop()