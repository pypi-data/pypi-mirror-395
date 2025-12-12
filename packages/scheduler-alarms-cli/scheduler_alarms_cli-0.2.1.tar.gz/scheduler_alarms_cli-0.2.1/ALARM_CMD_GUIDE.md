# One-Line Alarm Command

Ultra-simple alarm command for quick terminal use. Set alarms in one line with customizable messages.

## Quick Examples

```bash
# 5 seconds
python3 alarm_cmd.py 5s

# 5 seconds with message
python3 alarm_cmd.py 5s "break time"

# 3 minutes
python3 alarm_cmd.py 3m

# 3 minutes with message
python3 alarm_cmd.py 3m "take medicine"

# 1 hour
python3 alarm_cmd.py 1h

# 7 AM (absolute time)
python3 alarm_cmd.py 7am

# 2:30 PM with message
python3 alarm_cmd.py 2:30pm "meeting reminder"

# Verbose format
python3 alarm_cmd.py "in 10 minutes" "check the oven"
```

## Time Formats Supported

### Shorthand (quickest)
| Format | Meaning |
|--------|---------|
| `5s` | 5 seconds |
| `3m` | 3 minutes |
| `1h` | 1 hour |
| `90s` | 90 seconds |
| `15m` | 15 minutes |

### Absolute Time (24-hour today or tomorrow)
| Format | Meaning |
|--------|---------|
| `7am` | 7:00 AM |
| `2:30pm` | 2:30 PM |
| `9:15am` | 9:15 AM |
| `14:30` | 2:30 PM (military) |

### Verbose Relative
| Format | Meaning |
|--------|---------|
| `in 10 seconds` | 10 seconds from now |
| `in 5 minutes` | 5 minutes from now |
| `in 2 hours` | 2 hours from now |

## Features

✅ **One-line usage** — Simple, fast, no configuration  
✅ **Alarm sound** — System beep with alarm sound  
✅ **Visual alert** — Alert dialog box on macOS  
✅ **Notification popup** — Desktop notification  
✅ **Custom message** — Add reminder text (optional)  
✅ **Countdown display** — Shows time remaining (MM:SS)  
✅ **Multiple formats** — Flexible time input  

## Examples by Use Case

### Morning Routine
```bash
# Remind at 7 AM to take vitamins
python3 alarm_cmd.py 7am "take vitamins"

# Alarm in 10 minutes to get ready
python3 alarm_cmd.py 10m "get ready"
```

### Work Reminders
```bash
# 30-minute break reminder
python3 alarm_cmd.py 30m "time for a break"

# 2 PM meeting reminder
python3 alarm_cmd.py 2pm "team standup meeting"

# 1-hour quick task timer
python3 alarm_cmd.py 1h "review emails"
```

### Quick Testing
```bash
# Test alarm in 5 seconds
python3 alarm_cmd.py 5s

# Test with message
python3 alarm_cmd.py 3s "test notification"
```

## Behavior

1. **Scheduling** — Script displays the scheduled time and message
2. **Waiting** — Shows countdown timer (MM:SS format)
3. **Alert** — When time is reached:
   - Prints large ALARM message
   - Plays system alarm sound
   - Shows alert dialog (macOS)
   - Shows desktop notification
   - Displays custom message
4. **Complete** — Shows "Alarm: {message}" and exits

## Notes

- If time has already passed (e.g., `7am` at 8 PM), alarm is scheduled for tomorrow
- Press `Ctrl+C` to cancel the alarm
- Optional `pyobjus` module suppresses macOS notification warnings; not required
- Non-fatal errors from plyer will be silently handled

## Comparison with Other Scripts

| Feature | alarm_cmd.py | alarm_interactive.py | cli.py (scheduler) |
|---------|:-----:|:-----:|:-----:|
| One-line usage | ✅ | ❌ | ❌ |
| Interactive mode | ❌ | ✅ | ✅ |
| Multiple jobs | ❌ | ❌ | ✅ |
| Job persistence | ❌ | ❌ | ✅ |
| Simplicity | ⭐⭐⭐ | ⭐⭐ | ⭐ |

## Quick Aliases (Optional)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias alarm='python3 /Users/iamjam01/Desktop/Alarm\ OJT/alarm_cmd.py'
```

Then use:
```bash
alarm 5m "break"
alarm 7am "wake up"
alarm 30s
```

## Installation

Already included! Just run:
```bash
cd "/Users/iamjam01/Desktop/Alarm OJT"
python3 alarm_cmd.py 5s
```
