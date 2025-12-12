#!/usr/bin/env python3
"""
Simple alarm reminder script.
Usage examples:
  python3 simple_alarm.py --time 14:30 --message "Meeting"
  python3 simple_alarm.py --in 10 --message "Take a break"

The script accepts either --time (HH:MM or HH:MM:SS) which schedules for today (or tomorrow if time already passed),
or --in <seconds> to schedule after N seconds.
When alarm time is reached it will play sound and show notifications using the project's notification helpers.
"""
import argparse
import datetime
import time
import sys

from scheduler.notifications import notify_alarm_ringing, show_popup_notification


def parse_args():
    parser = argparse.ArgumentParser(description="Simple alarm reminder")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--time", help="Absolute time (HH:MM or HH:MM:SS)")
    group.add_argument("--in", dest="in_seconds", type=int, help="Relative seconds from now")
    parser.add_argument("--message", help="Optional message to show with the alarm", default="Alarm")
    parser.add_argument("--duration", type=int, default=5, help="Duration of alarm sound in seconds")
    parser.add_argument("--name", default="Alarm", help="Name of the alarm")
    return parser.parse_args()


def seconds_until_time(timestr: str) -> int:
    """
    Compute seconds until the provided HH:MM or HH:MM:SS time today (or tomorrow if passed).
    """
    now = datetime.datetime.now()
    parts = timestr.split(":")
    if len(parts) not in (2,3):
        raise ValueError("Time must be in HH:MM or HH:MM:SS format")
    hour = int(parts[0])
    minute = int(parts[1])
    second = int(parts[2]) if len(parts) == 3 else 0
    target = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
    if target <= now:
        target = target + datetime.timedelta(days=1)
    return int((target - now).total_seconds())


def main():
    args = parse_args()

    if not args.time and args.in_seconds is None:
        print("No time provided; running a quick demo alarm in 5 seconds. Use --time or --in to schedule.")
        wait = 5
    elif args.in_seconds is not None:
        wait = max(0, args.in_seconds)
    else:
        try:
            wait = seconds_until_time(args.time)
        except Exception as e:
            print(f"Invalid time format: {e}")
            sys.exit(1)

    alarm_name = args.name
    message = args.message
    duration = args.duration

    # Notify user scheduling
    show_popup_notification(title="Alarm Scheduled", message=f"{alarm_name} in {wait} seconds\n{message}", timeout=4)
    print(f"Scheduled '{alarm_name}' to run in {wait} seconds\nMessage: {message}")

    try:
        for i in range(wait, 0, -1):
            sys.stdout.write(f"\rWaiting: {i} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        print("\nTime reached — triggering alarm now")

        # Use project helper to play sound and show alert
        notify_alarm_ringing(alarm_name, duration=duration)

        # Also show a popup with the message
        show_popup_notification(title=f"⏰ {alarm_name}", message=message, timeout=duration)
    except KeyboardInterrupt:
        print("\nAlarm cancelled by user")


if __name__ == '__main__':
    main()
