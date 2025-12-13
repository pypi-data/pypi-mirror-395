import logging
import uuid
from functools import wraps

from delta.tables import *
from pyspark.sql import SparkSession as _s
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

from .common import *

_APP = "NDS"
_NDS_PREFIX = "spark"
_HADOOP = f"{_NDS_PREFIX}.hadoop"
_SQL = f"{_NDS_PREFIX}.sql"
_BRICKS = f"{_NDS_PREFIX}.databricks"
_FMT = "delta"
_SCHEMA = "overwriteSchema"
_builder = _s.builder
_instance = None
_sql = None
_sc = None


def NDS_inner_table(table):
    table = table.strip()
    if not table or "." in table:
        raise ValueError(f"❌ Wrong table: {table}")
    return f"{table}"


def NDS_extern_call(f):
    logger = logging.getLogger(f.__module__)

    @wraps(f)
    def _deco(*k, **kw):
        logger.debug(f"🔄 {k[0]}")

        try:
            return f(*k, **kw)
        except Exception as e:
            logger.exception(f"{f.__name__} => {e}")
            raise
    return _deco


def NDS_import_data(data):
    assert _instance is not None
    return (
        data if hasattr(data, "schema") else _instance.createDataFrame(data)
    )


def _exist_table(table):
    assert _instance is not None
    try:
        _instance.table(table)
        return True
    except:
        return False


def NDS_list_tables():
    assert _instance is not None
    return [t.name for t in _instance.catalog.listTables()]


@NDS_extern_call
def NDS_describe_table(table):
    assert _instance is not None
    data = _instance.table(table)
    return [{
        "col_name": f.name,
        "data_type": str(f.dataType),
    } for f in data.schema.fields]


def NDS_temp_view(table):
    return f"{table}_{uuid.uuid4().hex[:8]}"


def NDS_check_sql(statement):
    if ";" in statement or "drop" in statement.lower():
        raise ValueError(f"Illegal statement: {statement}")


def _write(table, data, mode="overwrite", schema="true"):
    assert _sql is not None
    _sql(f"DROP TABLE IF EXISTS {table}")
    data.write.mode(mode) .option(
        _SCHEMA, schema).format(_FMT).saveAsTable(table)


def NDS_refresh(table, data, keys=None):
    assert _instance is not None
    if isinstance(data, dict):
        data = [data]

    data = NDS_import_data(data)

    if not (keys and _exist_table(table)):
        _write(table, data)
        return

    if not isinstance(keys, (list, tuple)):
        keys = [keys]

    _cond = " AND ".join([f"d.{k}=s.{k}" for k in keys])
    _table = DeltaTable.forName(_instance, table)  # type:ignore
    (_table.alias("d")
        .merge(data.alias("s"), _cond)
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
     )


def NDS_sql(sql):
    assert _instance is not None
    NDS_check_sql(sql)
    return [
        r.asDict() for r in _instance.sql(sql).collect()
    ]


def _setup(b):
    url, username, password = NDS_split_url("URL")
    ep, ak, sk = NDS_split_url("EP")

    return (b
            .appName(_APP)
            .config(f"{_HADOOP}.fs.s3a.endpoint", ep)
            .config(f"{_HADOOP}.fs.s3a.access.key", ak)
            .config(f"{_HADOOP}.fs.s3a.secret.key", sk)
            .config(f"{_HADOOP}.fs.s3a.path.style.access", "true")
            .config(f"{_SQL}.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config(f"{_SQL}.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .config(f"{_SQL}.warehouse.dir", "s3a://emdm/project")
            .config(f"{_SQL}.sources.default", _FMT)
            .config(f"{_HADOOP}.fs.defaultFS", "s3a://emdm")
            .config(f"{_HADOOP}.javax.jdo.option.ConnectionDriverName", "org.postgresql.Driver")
            .config(f"{_HADOOP}.javax.jdo.option.ConnectionURL", url)
            .config(f"{_HADOOP}.javax.jdo.option.ConnectionUserName", username)
            .config(f"{_HADOOP}.javax.jdo.option.ConnectionPassword", password)
            .config(f"{_HADOOP}.datanucleus.schema.autoCreateTables", "true")
            .config(f"{_BRICKS}.hive.metastore.schema.syncOnWrite", "true")
            .config(f"{_BRICKS}.delta.logRetentionDuration", "interval 1 days")
            .config(f"{_BRICKS}.delta.schema.autoMerge.enabled", "true")
            .config(f"{_BRICKS}.delta.schema.overwrite.mode", "true")
            .config(f"{_BRICKS}.delta.properties.defaults.columnMapping.mode", "name")
            .enableHiveSupport()
            .getOrCreate()
            )


_instance = _setup(_builder)
NDS_instance = _instance
_sc = _instance.sparkContext
_sql = _instance.sql
