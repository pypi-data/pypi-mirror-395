"""
Notification and alarm module for scheduler jobs.
Provides pop-up notifications, system notifications, and alarm sounds.
"""

import os
import sys
import threading
import warnings
from pathlib import Path

# Suppress plyer-related warnings
warnings.filterwarnings('ignore')

try:
    from plyer import notification
except (ImportError, ModuleNotFoundError):
    notification = None


# Available system sounds on macOS
MACOS_SOUNDS = {
    "alarm": "/System/Library/Sounds/Sosumi.aiff",  # Loud buzzer
    "buzzer": "/System/Library/Sounds/Basso.aiff",  # Extra buzzer
    "bell": "/System/Library/Sounds/Glass.aiff",
    "notification": "/System/Library/Sounds/Ping.aiff",
    "alert": "/System/Library/Sounds/Sosumi.aiff",
    "beep": "/System/Library/Sounds/Beep.aiff",
    "pop": "/System/Library/Sounds/Pop.aiff",
    "success": "/System/Library/Sounds/Tink.aiff",
}


def play_notification_sound(sound_type="notification"):
    """
    Play a notification sound based on type.
    
    Args:
        sound_type (str): Type of sound - 'alarm', 'notification', 'alert', etc.
    """
    try:
        if sys.platform == "darwin":  # macOS
            sound_file = MACOS_SOUNDS.get(sound_type, MACOS_SOUNDS["notification"])
            # Play loud buzzer effect for alarm
            if sound_type == "alarm":
                import time as time_mod
                for _ in range(6):
                    os.system(f"afplay {sound_file} > /dev/null 2>&1 &")
                    time_mod.sleep(0.2)
                # Also play Basso for extra buzzer
                for _ in range(2):
                    os.system(f"afplay {MACOS_SOUNDS['buzzer']} > /dev/null 2>&1 &")
                    time_mod.sleep(0.2)
            else:
                os.system(f"afplay {sound_file} > /dev/null 2>&1 &")
        elif sys.platform == "win32":  # Windows
            import winsound
            # Play default Windows sound
            winsound.MessageBeep()
        elif sys.platform == "linux":  # Linux
            # Use paplay or aplay if available
            os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null &")
    except Exception as e:
        pass  # Silently fail if sound unavailable


def play_alarm_sound(duration=3):
    """
    Play a system beep/alarm sound for the specified duration.
    
    Args:
        duration (int): Duration of the alarm in seconds
    """
    try:
        if sys.platform == "darwin":  # macOS
                # Play a simple double "beep beep" pattern using the system Beep sound
                # This will play two quick beeps repeatedly for the requested duration
                import time as time_mod
                beep_file = MACOS_SOUNDS.get("beep", "/System/Library/Sounds/Beep.aiff")
                # For each second, play two short beeps
                end_time = time_mod.time() + max(0, int(duration))
                while time_mod.time() < end_time:
                    # first beep
                    os.system(f"afplay {beep_file} > /dev/null 2>&1")
                    time_mod.sleep(0.18)
                    # second beep
                    os.system(f"afplay {beep_file} > /dev/null 2>&1")
                    # short pause before next pair
                    time_mod.sleep(0.32)
        elif sys.platform == "win32":  # Windows
            # Use Windows beep
            import winsound
            winsound.Beep(1000, int(duration * 1000))
        elif sys.platform == "linux":  # Linux
            # Use beep command or speaker-test
            os.system(f"(speaker-test -t sine -f 1000 -l 1 2>/dev/null || beep) &")
    except Exception as e:
        pass  # Silently fail if sound unavailable


def show_popup_notification(title, message, timeout=10):
    """
    Show a system pop-up notification.
    
    Args:
        title (str): Title of the notification
        message (str): Message content
        timeout (int): Timeout in seconds (default 10)
    """
    try:
        if sys.platform == "darwin":
            # Always use osascript for macOS notification popups
            safe_message = message.replace('"', '\"')
            safe_title = title.replace('"', '\"')
            script = f'display notification "{safe_message}" with title "{safe_title}"'
            os.system(f"osascript -e '{script}' &")
        elif notification:
            notification.notify(
                title=title,
                message=message,
                timeout=timeout,
                app_name="Scheduler",
            )
        else:
            print(f"\n🔔 {title}")
            print(f"   {message}")
    except Exception as e:
        # Silently fail for notification popup
        pass


def show_popup_window(title, message):
    """
    Show a pop-up dialog window (macOS).
    Falls back to terminal display on other systems.
    
    Args:
        title (str): Title of the dialog
        message (str): Message content
    """
    try:
        if sys.platform == "darwin":  # macOS
            # Use osascript for native macOS notification
            # Escape quotes in the message
            safe_message = message.replace('"', '\\"')
            safe_title = title.replace('"', '\\"')
            script = f'display notification "{safe_message}" with title "{safe_title}"'
            os.system(f'osascript -e \'{script}\' &')
        else:
            # Show notification through plyer
            show_popup_notification(title, message)
    except Exception as e:
        print(f"Could not show pop-up: {e}")


def notify_job_execution(job_name, with_sound=True, with_popup=True):
    """
    Comprehensive notification when a job is executed.
    
    Args:
        job_name (str): Name of the job being executed
        with_sound (bool): Whether to play alarm sound
        with_popup (bool): Whether to show pop-up notification
    """
    print(f"\n⏰ JOB ALERT: {job_name}")
    
    if with_sound:
        # Play notification sound in background thread so it doesn't block execution
        sound_thread = threading.Thread(
            target=play_notification_sound, 
            args=("alarm",),
            daemon=True
        )
        sound_thread.start()
    
    if with_popup:
        notification_thread = threading.Thread(
            target=show_popup_window,
            args=(f"Job Execution", f"Job '{job_name}' is now running"),
            daemon=True
        )
        notification_thread.start()


def notify_job_completed(job_name, next_run_time):
    """
    Notification when a job completes.
    
    Args:
        job_name (str): Name of the job
        next_run_time (str): Time of next run
    """
    message = f"Job completed. Next run: {next_run_time}"
    show_popup_notification(
        title=f"✓ {job_name} Completed",
        message=message,
        timeout=5
    )
    
    # Play a success/completion sound in background
    sound_thread = threading.Thread(
        target=play_notification_sound,
        args=("success",),
        daemon=True
    )
    sound_thread.start()


def show_alert_dialog(job_name, message=""):
    """
    Show an alert dialog box during alarm execution (macOS specific).
    Falls back to terminal display on other systems.
    
    Args:
        job_name (str): Name of the job triggering the alert
        message (str): Additional alert message
    """
    try:
        if sys.platform == "darwin":  # macOS
            # Create an interactive alert dialog
            alert_text = f"🚨 ALARM: {job_name}"
            if message:
                alert_text += f"\n\n{message}"
            
            safe_text = alert_text.replace('"', '\\"').replace("'", "\\'")
            
            # Use AppleScript to show an alert dialog
            script = f'''
            tell application "System Events"
                display alert "{job_name}" message "{message}" buttons {{"Dismiss", "Snooze"}} default button 1 with icon caution
            end tell
            '''
            os.system(f"osascript -e '{script}' > /dev/null 2>&1 &")
        else:
            # Fallback for Windows/Linux
            print(f"\n🚨 ALERT: {job_name}")
            if message:
                print(f"   {message}")
    except Exception as e:
        print(f"\n🚨 ALERT: {job_name}")
        if message:
            print(f"   {message}")


def notify_alarm_ringing(job_name, duration=5):
    """
    Comprehensive alarm notification with sound, visual alert, and popup.
    Called when an alarm job is triggered.
    
    Args:
        job_name (str): Name of the alarm job
        duration (int): Duration to play alarm sound (seconds)
    """
    print(f"\n🔔🔔🔔 ALARM RINGING: {job_name} 🔔🔔🔔")
    
    # Show alert dialog in background thread
    alert_thread = threading.Thread(
        target=show_alert_dialog,
        args=(job_name, "Your scheduled alarm has been triggered!"),
        daemon=True
    )
    alert_thread.start()
    
    # Play alarm sound in background thread
    alarm_thread = threading.Thread(
        target=play_alarm_sound,
        args=(duration,),
        daemon=True
    )
    alarm_thread.start()
    
    # Show popup notification
    popup_thread = threading.Thread(
        target=show_popup_notification,
        args=(f"⏰ {job_name}", "Alarm is ringing!", duration),
        daemon=True
    )
    popup_thread.start()


def notify_scheduler_started(job_count: int):
    """
    Notify that the scheduler has started.

    Args:
        job_count (int): Number of jobs loaded
    """
    try:
        title = "Scheduler Started"
        message = f"Scheduler is running with {job_count} jobs."
        # Short popup and a light sound
        threading.Thread(target=show_popup_notification, args=(title, message, 4), daemon=True).start()
        threading.Thread(target=play_notification_sound, args=("pop",), daemon=True).start()
    except Exception:
        pass


def notify_scheduler_status(job_count: int):
    """
    Periodic status notification while the scheduler is running.

    Args:
        job_count (int): Number of jobs currently scheduled
    """
    try:
        title = "Scheduler Status"
        message = f"Running — {job_count} jobs scheduled."
        # Use a subtle popup to avoid being too noisy
        threading.Thread(target=show_popup_notification, args=(title, message, 3), daemon=True).start()
    except Exception:
        pass


def notify_scheduler_stopped():
    """
    Notify that the scheduler has stopped.
    """
    try:
        title = "Scheduler Stopped"
        message = "Scheduler has been stopped."
        threading.Thread(target=show_popup_notification, args=(title, message, 4), daemon=True).start()
        threading.Thread(target=play_notification_sound, args=("success",), daemon=True).start()
    except Exception:
        pass
