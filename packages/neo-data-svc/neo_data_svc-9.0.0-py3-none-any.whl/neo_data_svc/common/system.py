import base64
import datetime as dt
import hashlib
import importlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Union

import uvicorn

tz = 'Asia/Shanghai'
tz_info = timezone(timedelta(hours=8))


def run(app, host="0.0.0.0", port=8001):
    uvicorn.run(app,
                host=host,
                port=port,
                workers=1,
                access_log=True,
                )


def autowire(file="push", pre="emdm.rest.ext.", f="process"):
    _m = pre + file.strip()
    m = importlib.import_module(_m)
    return getattr(m, f)


def F(filename):
    return Path(filename)


def time_str(now, fmt='%Y%m%d%H%M%S'):
    return now.strftime(fmt)


def get_now():
    return datetime.now(tz_info)


def T(now=None):
    if not now:
        now = get_now()
    return time_str(now, '%Y-%m-%d %H:%M:%S')


def get_today(now=None):
    if not now:
        now = get_now()
    today = datetime(now.year, now.month, now.day, 0, 0, 0)
    return time_str(today, '%Y-%m-%d %H:%M:%S')


def timestamp_ms(now=None):
    if not now:
        now = get_now()
    return int(now.timestamp() * 1000)


def digest(s, algorithm='MD5'):
    m = hashlib.new(algorithm)
    m.update(s.encode())
    return m.hexdigest()


def to_base64(s):
    return base64.b64encode(s.encode()).decode('ascii')
