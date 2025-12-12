
from contextlib import asynccontextmanager

import typer
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from starlette.exceptions import HTTPException as StarletteHTTPException

from .cache import NDS_CACHE, NDS_CACHE_INIT
from .core import *
from .rdms import *


async def NDP_make_ep(r, body, ep, db, cls):
    obj = await NDP_get(db, cls, ep=ep)
    if not obj:
        raise RuntimeError("❌ API not found")

    table = obj.table.strip()
    func = obj.func

    if not obj.enable:
        raise RuntimeError("❌ API not enabled")

    if func:
        NDP_run_task(NDP_sys.autowire(func), body, table, r)
        return PushOut()

    if not table:
        raise RuntimeError("🛑 Need detail table")

    result = NDS_query_table(table, obj.fields, body)
    return QueryOut(data=InnerData(result=result))

app = typer.Typer()
console = Console()


@app.callback()
def welcome(ctx: typer.Context):
    text = Text("数据中台", style="bold blue on black")
    table = Table(show_header=False, show_lines=True)
    table.add_column("item", style="green")
    table.add_column("value", style="yellow")
    table.add_row("Date", "2025-11")
    panel = Panel(
        table,
        title=Text("EMDM", style="green"),
        subtitle=text,
        expand=False,
        width=200,
        style="blue",
        title_align="center",
    )
    console.print(panel, justify="center")


NDP_CMD = app.command
