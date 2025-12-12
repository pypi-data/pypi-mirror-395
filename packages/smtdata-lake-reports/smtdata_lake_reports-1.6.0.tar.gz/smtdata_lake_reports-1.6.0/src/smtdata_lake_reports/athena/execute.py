from typing import Optional, Mapping, Any, Tuple, Sequence

from pandas import DataFrame
from sqlalchemy.sql.type_api import TypeEngine

from smtdata_lake_reports.athena.internal.AthenaClient import QueryResult
from smtdata_lake_reports.athena.internal.AthenaUserspaceWriter import AthenaUserspaceConfig, AthenaUserspaceWriter

from smtdata_lake_reports.athena.internal.AthenaClient import AthenaS3Config, AthenaS3Client
from smtdata_lake_reports.athena.internal.safe_sql import render_safe_athena_sql
from smtdata_lake_reports.runtime_context import get_context, ContextSettings


def _init(database_name: str = None) -> Tuple[AthenaS3Client, AthenaUserspaceWriter, ContextSettings]:
    ctx = get_context()
    athena_cfg = AthenaS3Config(
        aws_region=ctx.aws_region,
        database=database_name or ctx.athena.database_name,
        workgroup=ctx.athena.workgroup_name,
        log_sql=ctx.athena.log_sql_statements,
    )

    userspace_cfg = AthenaUserspaceConfig(
        aws_region=ctx.aws_region,
        tenant_id=ctx.tenant_id,
        bucket=ctx.s3_bucket_name,
        workgroup=ctx.athena.workgroup_name,
        db_name=ctx.athena.userspace_database_name,
        use_iceberg=True
    )

    return AthenaS3Client(athena_cfg), AthenaUserspaceWriter(userspace_cfg), ctx


def run_athena_query_to_s3(sql: str,
                           params: Optional[Mapping[str, Any]] = None,
                           types: Optional[Mapping[str, TypeEngine]] = None,
                           *,
                           database_name: str = None) -> str:
    """
    Run a query against Athena. Provide an sql with named parameters along with the parameters and it will be
    prepared before execution.

    Waiting for Athena is handled which means that the response from this query is an absolute S3 path to the result
    of the query

    :param sql: The query with parameters to execute
    :param params: Parameters for the query to safely escape and add to the query
    :param types: Optional Type hints for the query parametiser and optimiser
    :param database_name: Optional database name to override the default which is the `_raw` db
    :return: The absolute S3 path to the result
    """
    client, _, _ = _init(database_name)

    final_sql = render_safe_athena_sql(sql, params or {}, types=types)
    result = client.run_to_s3(final_sql)

    return result.s3_file


def run_athena_query_to_dataframe(
        sql: str,
        params: Optional[Mapping[str, Any]] = None,
        types: Optional[Mapping[str, TypeEngine]] = None,
        *,
        database_name: str = None) -> DataFrame:
    """
    Run a query against Athena. Provide an sql with named parameters along with the parameters, and it will be
    prepared before execution.

    Under the hood this method calls `run_athena_query_to_s3` and then streams back the data from s3 into a
    pandas DataFrame.

    :param sql: The query with parameters to execute
    :param params: Parameters for the query to safely escape and add to the query
    :param types: Optional Type hints for the query parametiser and optimiser
    :param database_name: Optional database name to override the default which is the `_raw` db
    :return: A pandas dataframe with the entire query result
    """
    client, _, _ = _init(database_name)

    s3file = run_athena_query_to_s3(sql, params, types=types, database_name=database_name)

    df = client.csv_to_dataframe(s3file)
    return df


def run_athena_query_to_ctas_temp(
        output_table_name: str,
        select_sql: str,
        params: Optional[Mapping[str, Any]] = None,
        partition_by: Sequence[str] = (),
        *,
        database_name: str = None) -> QueryResult:
    """
    Run a query against Athena. Provide an sql with named parameters along with the parameters, and it will be
    prepared before execution.

    The result will be persisted as a CTAS (Create Table As Select) parquet file in your workgroup defined result
    directory. A userspace table binding will be added (see ITBI documentation), however, ITBI applies short lived
    retention rules (days) to data stored here.

    Please note that the target table will be DROPPED before being populated again.

    If you need more persistent storage, consider using `run_athena_query_to_table_with_insert` or
    `run_athena_query_to_table_with_merge`

    :param select_sql: The query with parameters to execute
    :param output_table_name: The name of the target table
    :param params: Parameters for the query to safely escape and add to the query
    :param partition_by: Which columns to partition by - very important for large tables.
    :param database_name: Optional database name to override the default which is the `_raw` db
    :return:
    """
    _, userspace_writer, _ = _init(database_name)

    result = userspace_writer.ctas_overwrite(output_table_name, select_sql, params, partition_by=partition_by,
                                             pretty_sql=False)

    return result


def run_athena_query_to_table_with_insert(
        output_table_name: str,
        select_sql: str,
        params: Optional[Mapping[str, Any]] = None,
        partition_by: Sequence[str] = (),
        *,
        col_definitions: Mapping[str, str],
        pretty_sql: bool = False,
        database_name: str = None) -> QueryResult:
    """
    Run a query against Athena. Provide an sql with named parameters along with the parameters, and it will be
    prepared before execution.

    The result will be persisted in the given table inside your userspace tables (see ITBI documentation).

    Please note that an Iceberg table will be created for you, and that INSERTS are being performed. Hence
    if there are duplicate keys the process will likely fail. This method is good for time-series data with only new
    events since last time - since no updates can or will be applied back in time in the target table.

    Use run_athena_query_to_table_with_merge to deal with inserting with update/delete/insert logic

    :param output_table_name: The name of the target / output table to write into
    :param select_sql: The select query finding data to insert
    :param params: Named parameter map for the select query
    :param partition_by: Which columns to partition by - very important for large tables.
    :param database_name: Optional database name to override the default which is the `_raw` db
    :param col_definitions: Column definitions to use for the underlying Iceberg table
    :param pretty_sql: Whether to format the SQL pretty
    :return:
    """
    _, userspace_writer, _ = _init(database_name)

    userspace_writer.ensure_iceberg_table(
        output_table_name,
        partition_by=partition_by,
        col_definitions=col_definitions
    )

    result = userspace_writer.iceberg_insert_from_select(output_table_name, select_sql, params, pretty_sql=pretty_sql)

    return result


def run_athena_query_to_table_with_merge(
        output_table_name: str,
        select_sql: str,
        params: Optional[Mapping[str, Any]] = None,
        partition_by: Sequence[str] = (),
        *,
        col_definitions: Mapping[str, str],
        on_clause: str,  # e.g. 't.id = s.id AND t.dt = s.dt'
        when_matched: str,  # e.g. 'UPDATE SET col = s.col'
        when_not_matched: str,  # e.g. 'INSERT (id, dt, col) VALUES (s.id, s.dt, s.col)'
        pretty_sql: bool = False,
        database_name: str = None) -> QueryResult:
    """
    Run a query against Athena. Provide an sql with named parameters along with the parameters, and it will be
    prepared before execution.

    The result will be persisted in the given table inside your userspace tables (see ITBI documentation).

    Please note that an Iceberg table will be created for you. Using this method allows for advanced used of Iceberg
    by using the MERGE INTO syntax. This allows for updating/deleteing and inserting data in one go.

    See https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg-merge-into.html

    :param col_definitions: Table column definitions to add to the underlying table
    :param output_table_name: The name of the target table
    :param select_sql: The query with parameters to execute that selects data for the target table
    :param params: parameters for the query to safely escape and add to the query
    :param partition_by: Which columns to partition by - very important for large tables.
    :param on_clause: clause for the ON part of the merge statement - e.g. 't.id = s.id AND t.dt = s.dt'
    :param when_matched: clause for the WHEN MATCHED part of the statement -  e.g. 'UPDATE SET col = s.col'
    :param when_not_matched: clause for the WHEN NOT MATCHED part of the statement - e.g. 'INSERT (id, dt, col)
            VALUES (s.id, s.dt, s.col)'
    :param pretty_sql: Whether to pretty format the rendered SQL
    :param database_name: Optional database name to override the default which is the `_raw` db

    :return: A QueryResult instance
    """

    _, userspace_writer, _ = _init(database_name)

    userspace_writer.ensure_iceberg_table(output_table_name, partition_by=partition_by, col_definitions=col_definitions)

    result = userspace_writer.iceberg_merge_from_select(
        output_table_name,
        select_sql,
        params,
        on_clause=on_clause,
        when_matched=when_matched,
        when_not_matched=when_not_matched,
        pretty_sql=pretty_sql
    )

    return result
