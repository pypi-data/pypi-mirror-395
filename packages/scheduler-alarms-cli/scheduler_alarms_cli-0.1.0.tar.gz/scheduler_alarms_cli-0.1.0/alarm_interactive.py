#!/usr/bin/env python3
"""
Interactive alarm reminder with natural language input.
Accepts simple commands like:
  - "add alarm for 7 am"
  - "remind me at 2:30 pm"
  - "alarm at 09:15"
  - "notify me in 30 seconds"
  - "set alarm for 3 pm with message take medicine"
"""
import re
import datetime
import time
import sys

from scheduler.notifications import notify_alarm_ringing, show_popup_notification


def parse_natural_time(text: str) -> tuple[int, str]:
    """
    Parse natural language time input and return (seconds_until, description).
    
    Examples:
      "7am" or "7 am" or "at 7am" -> (secs until 7 AM, "7:00 AM")
      "2:30pm" or "2:30 pm" -> (secs until 2:30 PM, "2:30 PM")
      "in 30 seconds" or "30 seconds" -> (30, "in 30 seconds")
      "in 5 minutes" or "5 minutes" -> (300, "in 5 minutes")
      "in 2 hours" or "2 hours" -> (7200, "in 2 hours")
    """
    text = text.lower().strip()
    # Remove leading words like "add alarm", "remind", "set alarm", "alarm"
    text = re.sub(r'^(add\s+alarm|remind\s+me|set\s+alarm|alarm|for|at|in)\s+', '', text)
    text = text.strip()
    
    # Pattern 1: "X seconds/minutes/hours" (with or without "in")
    match = re.search(r'(\d+)\s*(second|minute|hour)s?(?:\s+with)?', text)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        multiplier = {"second": 1, "minute": 60, "hour": 3600}[unit]
        seconds = value * multiplier
        unit_name = f"{unit}{'s' if value > 1 else ''}"
        return seconds, f"in {value} {unit_name}"
    
    # Pattern 2: "HH:MM am/pm" or "H am/pm" (with optional "at")
    match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)', text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        ampm = match.group(3)
        
        # Convert 12-hour to 24-hour format
        if ampm == 'pm' and hour != 12:
            hour += 12
        elif ampm == 'am' and hour == 12:
            hour = 0
        
        # Validate hour/minute
        if hour > 23 or minute > 59:
            raise ValueError(f"Invalid time: {hour}:{minute:02d}")
        
        # Calculate seconds until that time
        now = datetime.datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If time has passed, schedule for tomorrow
        if target <= now:
            target += datetime.timedelta(days=1)
        
        seconds = int((target - now).total_seconds())
        time_str = f"{hour % 12 or 12}:{minute:02d} {'AM' if hour < 12 else 'PM'}"
        return seconds, time_str
    
    raise ValueError(f"Could not parse time from: '{text}'")


def extract_message(text: str) -> str:
    """Extract optional message from input (after 'with message' or 'with')."""
    # Look for content after "with" keyword
    match = re.search(r'with\s+(.+?)$', text, re.IGNORECASE)
    if match:
        msg = match.group(1).strip()
        if msg and len(msg) > 2:
            return msg
    return "Alarm"


def interactive_mode():
    """Run in interactive mode, accepting user input until 'quit' or 'exit'."""
    print("\n" + "="*70)
    print("🔔 INTERACTIVE ALARM REMINDER")
    print("="*70)
    print("\n📝 Simple commands to try:")
    print("  7am               (set alarm for 7 AM today or tomorrow)")
    print("  2:30pm            (set alarm for 2:30 PM)")
    print("  9:15am with meds  (alarm at 9:15 AM with reminder text)")
    print("  in 30 seconds     (set alarm 30 seconds from now)")
    print("  5 minutes         (set alarm in 5 minutes)")
    print("  2 hours           (set alarm in 2 hours)")
    print("  quit or exit      (stop the program)")
    print("-"*70 + "\n")
    
    while True:
        try:
            user_input = input("🕐 Enter alarm command: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ('quit', 'exit'):
                print("👋 Goodbye!")
                break
            
            # Parse the input
            try:
                wait_seconds, time_desc = parse_natural_time(user_input)
                message = extract_message(user_input)
                alarm_name = f"Alarm at {time_desc}"
                
                # Show scheduling message
                print(f"\n✅ Scheduled: {alarm_name} | Message: {message}")
                print(f"   Waiting: {wait_seconds} seconds ({time_desc})")
                
                # Show notification
                show_popup_notification(
                    title="Alarm Scheduled",
                    message=f"{alarm_name}\n{message}",
                    timeout=3
                )
                
                # Run the alarm
                print()
                for i in range(wait_seconds, 0, -1):
                    sys.stdout.write(f"\r⏳ {i:3d}s remaining...")
                    sys.stdout.flush()
                    time.sleep(1)
                
                print("\n\n🚨 ALARM TIME REACHED!")
                notify_alarm_ringing(alarm_name, duration=5)
                show_popup_notification(
                    title=f"⏰ {alarm_name}",
                    message=message,
                    timeout=5
                )
                print(f"✓ Alarm completed: {alarm_name}\n")
                
            except ValueError as e:
                print(f"❌ Error: {e}")
                print("   Try formats like: '7 am', '2:30 pm', 'in 30 seconds'\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Alarm interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"⚠️  Unexpected error: {e}")


def batch_mode(args):
    """Run a single alarm from command-line arguments."""
    command = " ".join(args)
    try:
        wait_seconds, time_desc = parse_natural_time(command)
        message = extract_message(command)
        alarm_name = f"Alarm at {time_desc}"
        
        print(f"Scheduled: {alarm_name} | Message: {message}")
        print(f"Waiting: {wait_seconds} seconds\n")
        
        for i in range(wait_seconds, 0, -1):
            sys.stdout.write(f"\r⏳ {i:3d}s remaining...")
            sys.stdout.flush()
            time.sleep(1)
        
        print("\n\n🚨 ALARM TIME REACHED!")
        notify_alarm_ringing(alarm_name, duration=5)
        show_popup_notification(
            title=f"⏰ {alarm_name}",
            message=message,
            timeout=5
        )
        print(f"✓ Alarm completed\n")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) > 1:
        # Batch mode: process command line arguments
        batch_mode(sys.argv[1:])
    else:
        # Interactive mode
        interactive_mode()


if __name__ == '__main__':
    main()
