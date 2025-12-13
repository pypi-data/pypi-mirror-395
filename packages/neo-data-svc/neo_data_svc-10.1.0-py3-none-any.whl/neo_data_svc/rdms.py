from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import field_validator
from sqlalchemy import Boolean, Column, DateTime, func, text
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlmodel import Field, SQLModel, select

from .common import NDS_get_v

_executor = ThreadPoolExecutor(100)


class NDPModel(SQLModel):
    __abstract__ = True


T = TypeVar("T")
M = TypeVar("M", bound=NDPModel)


class ProjectListRequest(NDPModel):
    path: str


class ProjectDescribeRequest(NDPModel):
    table: str


class ProjectBase(NDPModel, Generic[T]):
    table: str
    fields: str = Field("")
    where: T


class ProjectWhere(NDPModel):
    sqlwhere: Optional[str] = Field("")
    pageNo: int = Field(1, ge=1)
    pageSize: int = Field(10, ge=0)

    @field_validator('pageNo', 'pageSize', mode='before')
    @classmethod
    def convert(cls, v):
        if v is None:
            return v
        try:
            return int(v)
        except (ValueError, TypeError):
            return v


class ProjectQuery(ProjectBase[ProjectWhere]):
    pass


class BaseResponse(NDPModel, Generic[T]):
    code: int = 100
    data: T


class InnerData(NDPModel):
    statusCode: int = 200
    result: List[dict]


class QueryOut(BaseResponse[InnerData]):
    pass


class PushData(NDPModel):
    data: Union[dict, List[dict]]
    pk: Optional[str] = None

    @field_validator("data", mode="before")
    @classmethod
    def _ensure_list(cls, v):
        return v if isinstance(v, list) else [v]


class PushOut(NDPModel):
    statusCode: int = 200
    description: str = "success"


class FuckData(NDPModel):
    tablename: str
    primarykey: str
    primaryvalue: str
    fields: Dict[str, Any] = {}
    childdata: List["FuckData"] = []

    def walk(self) -> List[List]:
        return (
            [[self.tablename, {**self.fields, self.primarykey: self.primaryvalue}, self.primarykey]] +
            [item for child in self.childdata for item in child.walk()]
        )


_url = NDS_get_v("DB")
assert _url is not None

async_engine = create_async_engine(
    f"postgresql+asyncpg://{_url}",
    pool_pre_ping=True,
    pool_recycle=600,
    future=True
)
async_AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def NDP_run_task(*k):
    _executor.submit(*k)


async def NDP_init_db():
    assert async_engine is not None
    async with async_engine.begin() as c:
        await c.run_sync(NDPModel.metadata.create_all)


async def NDP_get_db():
    assert async_AsyncSessionLocal is not None
    async with async_AsyncSessionLocal() as s:
        yield s


async def NDP_get(
    db: AsyncSession,
    model: Type[M],
    **filters
):
    stmt = select(model).filter_by(**filters)
    result = await db.execute(stmt)
    return result.scalars().first()


async def NDP_all(
    db: AsyncSession,
    model: Type[M],
    **filters
):
    stmt = select(model).filter_by(**filters)
    result = await db.execute(stmt)
    return result.scalars().all()


async def NDP_add(
        db: AsyncSession,
        model: Type[M],
        **kwargs
):
    obj = model(**kwargs)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def NDP_patch(
    db: AsyncSession,
    instance: M,
    **kwargs
) -> M:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance


async def NDP_delete(
    db: AsyncSession,
    instance: M
) -> M | None:
    await db.delete(instance)
    await db.commit()


async def NDP_sql(
    db: AsyncSession,
    sql: str = "",
    file: str = ""
):
    if sql:
        await db.execute(text(sql))
        await db.commit()

    if not file:
        return

    with open(file, "r") as f:
        sql = f.read()
        await db.execute(text(sql))
        await db.commit()
