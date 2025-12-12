import datetime

def next_run_time(rule, last_run):
    freq = rule["frequency"]

    if freq == "once":
        time_str = rule["time"]
        if "T" not in time_str:  # HH:MM format
            time_str = f"{last_run.date()}T{time_str}:00"
        return datetime.datetime.fromisoformat(time_str)

    if freq == "daily":
        next_run = last_run + datetime.timedelta(days=1)
        # Keep the same time of day
        time_str = rule.get("time")
        if time_str and "T" not in time_str:
            h, m = map(int, time_str.split(":"))
            next_run = next_run.replace(hour=h, minute=m, second=0, microsecond=0)
        return next_run

    if freq == "hourly":
        return last_run + datetime.timedelta(hours=1)

    if freq == "weekly":
        return last_run + datetime.timedelta(weeks=1)

    if freq == "interval":
        return last_run + datetime.timedelta(seconds=rule["seconds"])

    raise ValueError("Unknown recurrence rule")