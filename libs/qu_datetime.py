import time

def now(): return int(time.time())

def seconds_to_form(seconds):
    minutes = seconds // 60
    hours = seconds // (60*60)
    days = seconds // (60*60*24)

    if days:
        return f"{days}d, {hours - days*24}h"
    elif hours:
        return f"{hours}h, {minutes - hours*60}min"
    elif minutes:
        return f"{minutes}min, {seconds - minutes*60}sec"
    else:
        return f"{seconds}sec"

def form_to_seconds(days = 0, hours = 0, minutes = 0, secs = 0):
    return ((((days) * 24 + hours) * 60 + minutes) * 60 + secs)
