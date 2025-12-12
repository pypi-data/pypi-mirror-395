# Job Execution Time Guide

## Overview

The scheduler supports 5 different frequency types for job execution. Here's how to set the time for each type:

---

## 1. **ONCE** - Run a job one time only

Run a job at a specific date and time, then never again.

### Syntax:
```bash
python3 cli.py add --name "job_name" --time "YYYY-MM-DDTHH:MM:SS" --freq once
```

### Examples:
```bash
# Run job on December 5, 2025 at 3:30 PM
python3 cli.py add --name "backup_full" --time "2025-12-05T15:30:00" --freq once

# Run job on December 1, 2025 at 9:00 AM
python3 cli.py add --name "morning_report" --time "2025-12-01T09:00:00" --freq once

# Run job on December 31, 2025 at 11:59 PM
python3 cli.py add --name "year_end" --time "2025-12-31T23:59:00" --freq once
```

---

## 2. **DAILY** - Run a job every day at a specific time

Run a job every day at the same time.

### Syntax:
```bash
python3 cli.py add --name "job_name" --time "YYYY-MM-DDTHH:MM:SS" --freq daily
```

### Examples:
```bash
# Run job every day at 2:00 AM (starting Dec 2, 2025)
python3 cli.py add --name "daily_cleanup" --time "2025-12-02T02:00:00" --freq daily

# Run job every day at 6:00 PM (starting Dec 1, 2025)
python3 cli.py add --name "daily_sync" --time "2025-12-01T18:00:00" --freq daily

# Run job every day at 12:00 PM (noon)
python3 cli.py add --name "lunch_reminder" --time "2025-12-01T12:00:00" --freq daily
```

---

## 3. **WEEKLY** - Run a job every week at a specific time

Run a job once per week on the same day and time.

### Syntax:
```bash
python3 cli.py add --name "job_name" --time "YYYY-MM-DDTHH:MM:SS" --freq weekly
```

### Examples:
```bash
# Run job every Monday at 9:00 AM
python3 cli.py add --name "weekly_report" --time "2025-12-01T09:00:00" --freq weekly

# Run job every Friday at 5:00 PM
python3 cli.py add --name "weekly_meeting" --time "2025-12-05T17:00:00" --freq weekly

# Run job every Sunday at 8:00 PM
python3 cli.py add --name "weekly_backup" --time "2025-12-07T20:00:00" --freq weekly
```

---

## 4. **HOURLY** - Run a job every hour at a specific minute

Run a job every hour at the same minute.

### Syntax:
```bash
python3 cli.py add --name "job_name" --time "YYYY-MM-DDTHH:MM:SS" --freq hourly
```

### Examples:
```bash
# Run job every hour at :00 (top of the hour)
python3 cli.py add --name "health_check" --time "2025-12-01T00:00:00" --freq hourly

# Run job every hour at :30
python3 cli.py add --name "data_sync" --time "2025-12-01T12:30:00" --freq hourly

# Run job every hour at :15
python3 cli.py add --name "status_update" --time "2025-12-01T10:15:00" --freq hourly
```

---

## 5. **INTERVAL** - Run a job every X seconds

Run a job repeatedly at a fixed interval (in seconds).

### Syntax:
```bash
python3 cli.py add --name "job_name" --freq interval --seconds NUM
```

### Examples:
```bash
# Run job every 30 seconds
python3 cli.py add --name "monitor" --freq interval --seconds 30

# Run job every 5 minutes (300 seconds)
python3 cli.py add --name "quick_check" --freq interval --seconds 300

# Run job every 1 minute (60 seconds)
python3 cli.py add --name "heartbeat" --freq interval --seconds 60

# Run job every 1 hour (3600 seconds)
python3 cli.py add --name "hourly_task" --freq interval --seconds 3600
```

---

## Time Format Reference

### ISO 8601 Format:
```
YYYY-MM-DDTHH:MM:SS
```

**Breakdown:**
- `YYYY` = 4-digit year (e.g., 2025)
- `MM` = 2-digit month (01-12)
- `DD` = 2-digit day (01-31)
- `T` = Time separator (literal 'T')
- `HH` = 2-digit hour (00-23, 24-hour format)
- `MM` = 2-digit minute (00-59)
- `SS` = 2-digit second (00-59)

### Time Examples:
```
2025-12-01T09:00:00    → December 1, 2025 at 9:00:00 AM
2025-12-05T14:30:45    → December 5, 2025 at 2:30:45 PM
2025-12-25T00:00:00    → December 25, 2025 at 12:00:00 AM (midnight)
2025-12-31T23:59:59    → December 31, 2025 at 11:59:59 PM
```

---

## Complete Examples

### Set up multiple jobs with different schedules:

```bash
# One-time backup on Dec 15 at 3 PM
python3 cli.py add --name "one_time_backup" --time "2025-12-15T15:00:00" --freq once

# Daily cleanup at 2 AM every day
python3 cli.py add --name "daily_cleanup" --time "2025-12-02T02:00:00" --freq daily

# Weekly report every Monday at 9 AM
python3 cli.py add --name "weekly_report" --time "2025-12-01T09:00:00" --freq weekly

# Hourly status check at :00 every hour
python3 cli.py add --name "hourly_check" --time "2025-12-01T00:00:00" --freq hourly

# Every 5 minutes continuously
python3 cli.py add --name "continuous_monitor" --freq interval --seconds 300
```

### View all jobs:
```bash
python3 cli.py list
```

Output:
```
- one_time_backup | next run: 2025-12-15T15:00:00
- daily_cleanup | next run: 2025-12-02T02:00:00
- weekly_report | next run: 2025-12-01T09:00:00
- hourly_check | next run: 2025-12-01T00:00:00
- continuous_monitor | next run: 2025-12-01T12:34:56.123456
```

### Start the scheduler:
```bash
python3 cli.py start
```

---

## 24-Hour Time Reference

| Time | Format |
|------|--------|
| 12:00 AM (Midnight) | 00:00:00 |
| 1:00 AM | 01:00:00 |
| 6:00 AM | 06:00:00 |
| 12:00 PM (Noon) | 12:00:00 |
| 1:00 PM | 13:00:00 |
| 3:30 PM | 15:30:00 |
| 6:00 PM | 18:00:00 |
| 11:59 PM | 23:59:00 |

---

## Common Time Intervals (in seconds)

| Interval | Seconds |
|----------|---------|
| 10 seconds | 10 |
| 30 seconds | 30 |
| 1 minute | 60 |
| 5 minutes | 300 |
| 10 minutes | 600 |
| 30 minutes | 1800 |
| 1 hour | 3600 |
| 2 hours | 7200 |
| 6 hours | 21600 |
| 12 hours | 43200 |
| 1 day | 86400 |

---

## Tips & Tricks

1. **For DAILY jobs**: The time you set becomes the "anchor time" - the job will run every 24 hours from that time
2. **For WEEKLY jobs**: The job runs exactly 7 days apart from the initial time
3. **For HOURLY jobs**: Only the minute and second matter; it repeats every hour
4. **For INTERVAL jobs**: Use `--seconds` only (no `--time` needed)
5. **For ONCE jobs**: The job runs once at the specified time, then stops

---

## Error Handling

### Invalid time format:
```bash
# ❌ WRONG
python3 cli.py add --name "bad_time" --time "12/25/2025 3:30 PM" --freq daily

# ✅ CORRECT
python3 cli.py add --name "good_time" --time "2025-12-25T15:30:00" --freq daily
```

### Missing time for non-interval jobs:
```bash
# ❌ WRONG - missing --time
python3 cli.py add --name "task" --freq daily

# ✅ CORRECT
python3 cli.py add --name "task" --time "2025-12-02T09:00:00" --freq daily
```

### Missing seconds for interval jobs:
```bash
# ❌ WRONG - missing --seconds
python3 cli.py add --name "task" --freq interval

# ✅ CORRECT
python3 cli.py add --name "task" --freq interval --seconds 300
```
