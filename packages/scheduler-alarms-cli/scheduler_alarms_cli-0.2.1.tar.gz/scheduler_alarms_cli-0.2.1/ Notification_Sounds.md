# Notification Sounds Guide

Your scheduler now includes built-in notification sounds for job execution and completion events!

## 🔊 Available Sounds

The following system sounds are available on **macOS**:

| Sound Type | Usage | File |
|-----------|-------|------|
| **alarm** | Job execution alert | Alarm.aiff |
| **bell** | Notification (Glass) | Glass.aiff |
| **notification** | Default notification | Ping.aiff |
| **alert** | Warning alert | Alert.aiff |
| **beep** | Simple beep | Beep.aiff |
| **pop** | Pop sound | Pop.aiff |
| **success** | Job completion (Purr) | Purr.aiff |

## 📢 When Sounds Play

1. **Job Execution Sound** (Alarm)
   - Plays when a job starts running
   - Sound type: "alarm"
   - Plays in background thread (non-blocking)

2. **Job Completion Sound** (Success)
   - Plays when a job finishes
   - Sound type: "success" (Purr sound)
   - Plays in background thread (non-blocking)

## 🛠️ How to Customize Sounds

Edit `scheduler/notifications.py` to change the sound mappings:

```python
MACOS_SOUNDS = {
    "alarm": "/System/Library/Sounds/Alarm.aiff",        # Change this line
    "bell": "/System/Library/Sounds/Glass.aiff",
    "notification": "/System/Library/Sounds/Ping.aiff",
    "alert": "/System/Library/Sounds/Alert.aiff",
    "beep": "/System/Library/Sounds/Beep.aiff",
    "pop": "/System/Library/Sounds/Pop.aiff",
    "success": "/System/Library/Sounds/Purr.aiff",       # Change this line
}
```

## 🎵 Full List of macOS System Sounds

All available sounds are located in `/System/Library/Sounds/`:

- Alarm.aiff
- Alert.aiff
- Beep.aiff
- Boing.aiff
- Bottle.aiff
- Chirp.aiff
- Click.aiff
- Clink.aiff
- Clop.aiff
- Cluck.aiff
- Ding.aiff
- Drip.aiff
- Experience.aiff
- Frog.aiff
- Funk.aiff
- Glass.aiff
- Gong.aiff
- Harp.aiff
- Hero.aiff
- Hindsight.aiff
- Huh.aiff
- Knock.aiff
- Lasso.aiff
- Magnetic.aiff
- Mast.aiff
- Ping.aiff
- Pop.aiff
- Purr.aiff
- Sparkle.aiff
- Submarine.aiff
- Swish.aiff
- Tink.aiff
- Wow.aiff

## 💻 Cross-Platform Support

- **macOS**: Uses native macOS system sounds via `afplay`
- **Windows**: Uses Windows system MessageBeep
- **Linux**: Uses `paplay` or `aplay` with freedesktop sounds

## 🔕 Disable Sounds

To disable notification sounds, modify `runner.py`:

```python
# Change this line in run_job() method:
notify_job_execution(job['name'], with_sound=False, with_popup=True)
```

Or disable for job completion in `execute_and_reschedule()`:
```python
# Comment out or modify the sound thread
```

## ✅ Example Usage

When you run the scheduler with `python3 cli.py start`:

```
Scheduler started...

▶ Running job: daily_backup
⏰ JOB ALERT: daily_backup
[Alarm sound plays]
✔ Completed job: daily_backup
[Success/Purr sound plays]

▶ Running job: daily_backup
⏰ JOB ALERT: daily_backup
[Alarm sound plays]
[Notification popup appears]

## 🖥️ Notification Popups

You can display a notification popup when an alarm or job event occurs. On macOS, use either `osascript` or the `plyer` library:

### Using osascript (macOS)

Add this to your Python code:

```python
import os
def show_popup_notification(title, message):
   os.system(f'''osascript -e 'display notification "{message}" with title "{title}"' ''')
```

### Using plyer (cross-platform)

Install plyer:
```sh
pip install plyer
```

Add this to your Python code:
```python
from plyer import notification
notification.notify(title="Alarm", message="Time's up!", app_name="Scheduler")
```

Both methods will show a notification popup when the alarm rings or a job event occurs.
```
