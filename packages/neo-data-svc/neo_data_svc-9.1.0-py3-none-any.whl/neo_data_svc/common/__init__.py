import re
import time

import httpx
from dynaconf import Dynaconf

from . import job as NDP_job
from . import system as NDP_sys
from .log import NDS_log

_settings = Dynaconf(envvar_prefix="NDS")


def _call_m(m, f, **kw):
    if m == "get":
        kw.pop("json", None)
    return f(**kw)


def NDP_send(url, params=None, json=None, headers=None, timeout=None, *, m="post"):
    with httpx.Client(verify=False, timeout=timeout) as c:
        resp = _call_m(m, getattr(c, m.lower()), url=url,
                       params=params, json=json, headers=headers)
        if resp.status_code == 200:
            return resp.json()
    resp.raise_for_status()


def NDP_sleep():
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass


def NDS_get_v(k, v=None):
    v = _settings.get(k, v)
    if v is None:
        raise ValueError(f"❌ Need {k}")
    return v


def NDS_split_url(url):
    m = re.match(r'(.+://)\{([^}]+)\}:\{([^}]+)\}@(.+)', NDS_get_v(url))
    if not m:
        raise ValueError(f"❌ Wrong {url}")
    return f"{m.group(1)}{m.group(4)}", m.group(2), m.group(3)
