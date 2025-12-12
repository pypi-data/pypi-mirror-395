import datetime

def now():
    return datetime.datetime.now()

def parse_time(s):
    return datetime.datetime.fromisoformat(s)