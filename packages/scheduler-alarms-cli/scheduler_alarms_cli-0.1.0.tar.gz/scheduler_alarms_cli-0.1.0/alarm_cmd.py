#!/usr/bin/env python3
"""
Ultra-simple one-line alarm command.

Usage:
  python3 alarm_cmd.py 7am
  python3 alarm_cmd.py 2:30pm "take medicine"
  python3 alarm_cmd.py "in 5 minutes" "break time"
  python3 alarm_cmd.py 10s
  python3 alarm_cmd.py 3m "reminder message"

Format: alarm_cmd.py <time> [message]
  Time: 7am, 2:30pm, in 5 minutes, 10s, 3m, etc.
  Message: Optional custom reminder text (in quotes)
"""
import sys
import re
import datetime
import time

from scheduler.notifications import notify_alarm_ringing, show_popup_notification


def parse_time(time_input: str) -> int:
    """Parse time input and return seconds until alarm. Supports multiple formats."""
    time_input = time_input.lower().strip()
    
    # Pattern 1: "Xs", "Xm", "Xh" (shorthand: 10s, 5m, 2h)
    match = re.match(r'^(\d+)([smh])$', time_input)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        multiplier = {'s': 1, 'm': 60, 'h': 3600}[unit]
        return value * multiplier
    
    # Pattern 2: "in Xs/Xm/Xh"
    match = re.search(r'in\s+(\d+)\s*([smh])', time_input)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        multiplier = {'s': 1, 'm': 60, 'h': 3600}[unit]
        return value * multiplier
    
    # Pattern 3: "in X seconds/minutes/hours"
    match = re.search(r'in\s+(\d+)\s+(second|minute|hour)s?', time_input)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        multiplier = {'second': 1, 'minute': 60, 'hour': 3600}[unit]
        return value * multiplier
    
    # Pattern 4: "Xam/Xpm" or "X:XXam/pm"
    match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)', time_input)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        ampm = match.group(3)
        
        # Convert to 24-hour format
        if ampm == 'pm' and hour != 12:
            hour += 12
        elif ampm == 'am' and hour == 12:
            hour = 0
        
        if hour > 23 or minute > 59:
            raise ValueError(f"Invalid time: {hour}:{minute:02d}")
        
        # Calculate seconds
        now = datetime.datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if target <= now:
            target += datetime.timedelta(days=1)
        
        return int((target - now).total_seconds())
    
    raise ValueError(f"Invalid time format: '{time_input}'")


def format_time_desc(seconds: int) -> str:
    """Convert seconds to human-readable format."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hours}h {mins}m"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 alarm_cmd.py <time> [message]")
        print("\nExamples:")
        print("  python3 alarm_cmd.py 7am")
        print("  python3 alarm_cmd.py 2:30pm \"take medicine\"")
        print("  python3 alarm_cmd.py 10s")
        print("  python3 alarm_cmd.py 5m \"break reminder\"")
        print("  python3 alarm_cmd.py \"in 10 minutes\"")
        sys.exit(0)
    
    time_input = sys.argv[1]
    message = sys.argv[2] if len(sys.argv) > 2 else "Alarm"
    
    try:
        # Parse time
        seconds = parse_time(time_input)
        time_desc = format_time_desc(seconds)
        
        # Show scheduled message
        alarm_name = f"Alarm in {time_desc}"
        print(f"\n⏰ Alarm scheduled: {alarm_name}")
        print(f"📝 Message: {message}")
        print(f"⏳ Waiting {seconds} seconds...\n")
        
        # Show notification
        show_popup_notification(
            title="Alarm Scheduled",
            message=f"{alarm_name}\n{message}",
            timeout=3
        )
        
        # Count down
        for i in range(seconds, 0, -1):
            mins = i // 60
            secs = i % 60
            sys.stdout.write(f"\r⏳ {mins:02d}:{secs:02d} remaining...")
            sys.stdout.flush()
            time.sleep(1)
        
        # Trigger alarm
        print("\n\n" + "="*60)
        print("🔔🔔🔔 ALARM TRIGGERED! 🔔🔔🔔")
        print("="*60 + "\n")

        notify_alarm_ringing(alarm_name, duration=5)
        show_popup_notification(
            title=f"⏰ {alarm_name}",
            message=message,
            timeout=5
        )


        # Play loud alarm sound (Sosumi or Basso) for 5 seconds after notification
        from scheduler.notifications import play_notification_sound
        import time as time_mod
        for _ in range(5):
            play_notification_sound("alert")  # 'alert' maps to Sosumi.aiff (loud)
            time_mod.sleep(1)

        print(f"\n✓ Alarm: {message}")
        print("="*60 + "\n")
        
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Alarm cancelled by user")
        sys.exit(0)


if __name__ == '__main__':
    main()
