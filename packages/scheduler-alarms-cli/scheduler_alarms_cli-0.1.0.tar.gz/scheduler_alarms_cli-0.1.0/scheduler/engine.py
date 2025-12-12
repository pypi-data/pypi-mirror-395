import threading
from scheduler.runner import JobRunner
from scheduler.job_store import load_jobs
from scheduler.utils import parse_time, now
from scheduler.recurrence import next_run_time
from scheduler.notifications import notify_scheduler_started, notify_scheduler_status, notify_scheduler_stopped

class SchedulerEngine:
    def __init__(self):
        self.jobs = load_jobs()
        # Keep next_run as ISO format strings in the jobs list

        self.runner = JobRunner(self.jobs)
        self.thread = None
        # Background status notifier
        self._status_thread = None
        self._status_running = False

    def add_job(self, name, command, rule):
        if rule["frequency"] == "interval":
            first_run = now()
        else:
            # Handle HH:MM format by converting to today's date
            time_str = rule.get("time", "00:00")
            if "T" not in time_str:  # HH:MM format
                today = now().date()
                time_str = f"{today}T{time_str}:00"
            first_run = parse_time(time_str)

        job = {
            "name": name,
            "command": command,
            "rule": rule,
            "next_run": first_run.isoformat()
        }
        self.jobs.append(job)

        from scheduler.job_store import save_jobs
        save_jobs(self.jobs)

    def start(self):
        # Start runner thread
        self.thread = threading.Thread(target=self.runner.start)
        self.thread.start()

        # Start status notifier thread
        self._status_running = True
        notify_scheduler_started(len(self.jobs))

        def _status_loop():
            # Periodically notify that scheduler is running (every 5 seconds)
            while self._status_running:
                try:
                    notify_scheduler_status(len(self.jobs))
                except Exception:
                    pass
                threading.Event().wait(5)

        self._status_thread = threading.Thread(target=_status_loop, daemon=True)
        self._status_thread.start()

    def stop(self):
        # Stop runner and the status notifier
        self.runner.stop()
        if self.thread:
            self.thread.join()

        # Stop status thread
        self._status_running = False
        if self._status_thread and self._status_thread.is_alive():
            self._status_thread.join(timeout=2)

        try:
            notify_scheduler_stopped()
        except Exception:
            pass

    def list_jobs(self):
        return self.jobs