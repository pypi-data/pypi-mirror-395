
from .rdms import ProjectQuery, ProjectWhere
from .repo import *


@NDS_extern_call
def NDS_query_table(table, fields, body):

    q = ProjectQuery(
        table=table,
        fields=fields,
        where=ProjectWhere.model_validate(body))

    where_clause = f"WHERE {q.where.sqlwhere}" if q.where.sqlwhere else ""
    sql = f"SELECT {q.fields} FROM {table} {where_clause}"
    offset, limit = (q.where.pageNo - 1) * q.where.pageSize, q.where.pageSize
    return NDS_sql(f""" {sql} LIMIT {limit} OFFSET {offset} """)


@NDS_extern_call
def NDS_refresh_table(table, data, keys=None):

    if not data:
        return

    NDS_refresh(table, data, keys)