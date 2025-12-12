from __future__ import annotations

import boto3
from botocore.exceptions import ClientError
from dataclasses import dataclass
from typing import Mapping, Sequence

from smtdata_lake_reports.athena.internal.AthenaClient import AthenaS3Client, AthenaS3Config, QueryResult
from smtdata_lake_reports.athena.internal.safe_sql import render_safe_athena_sql
from smtdata_lake_reports.runtime_context import get_context, ContextSettings

@dataclass(frozen=True)
class AthenaUserspaceConfig:
    aws_region: str
    tenant_id: str
    bucket: str                          # tenant’s bucket to hold userspace data
    db_name: str                         # database name for userspace data
    workgroup: str                       # The workgroup
    # Optional toggles
    use_iceberg: bool = False            # set True when you want INSERT/UPDATE/DELETE
    iceberg_table_format: str = "ICEBERG"  # Athena keyword; keep for clarity

    def resolved_prefix(self) -> str:
        return f"itbi{self.tenant_id}/user/"

    def table_location(self, table_name: str) -> str:
        # s3://<bucket>/<prefix>/<table_name>/
        return f"s3://{self.bucket}/{self.resolved_prefix()}{table_name}/"


class AthenaUserspaceWriter:
    """
    Helpers to materialize Athena results into per-tenant 'userspace' tables.
    Two modes:
      - CTAS + Parquet (default): snapshot/overwrite tables
      - Iceberg: INSERT INTO for append/update workflows
    """

    def __init__(self, cfg: AthenaUserspaceConfig, *, context: ContextSettings | None = None,
                 athena_client: AthenaS3Client | None = None, glue_client=None):
        """
        Initializer for the AthenaUserspaceWriter. You must pass a config, everything else is optional,
        and if not passed they will be automatically instantiated by the initialiser.

        :param cfg: Core configuration for the AthenaUserspaceWriter.
        :param context: ContextSettings instance with settings - or none, current context will be pulled from env
        :param athena_client: AthenaClient instance to use - or none, instance will be created fresh
        :param glue_client: GlueClient instance to use - or none, instance will be created fresh
        """

        self.cfg = cfg
        self._glue = boto3.client("glue", region_name=cfg.aws_region)

        self.ctx = context or get_context()
        self._glue = glue_client or boto3.client("glue", region_name=cfg.aws_region)
        self._athena_client = athena_client or AthenaS3Client(
            AthenaS3Config(
                workgroup=self.ctx.athena.workgroup_name,
                aws_region=self.ctx.aws_region,
                database=self.cfg.db_name,
                log_sql=self.ctx.athena.log_sql_statements,
            )
        )

    # -------- GLUE DB UTILITIES --------
    def table_exists(self, table_name: str) -> bool:
        try:
            self._glue.get_table(DatabaseName=self.cfg.db_name, Name=table_name)
            return True
        except ClientError as e:
            if e.response.get("Error", {}).get("Code") == "EntityNotFoundException":
                return False
            raise

    def ensure_iceberg_table(
        self,
        table_name: str,
        *,
        partition_by: Sequence[str] = (),
        col_definitions: Mapping[str, str],
    ) -> str:
        """
        Creates an Iceberg table if it doesn't exist.
        For schema-on-write, you can let Athena infer schema from a CTAS seed,
        or define columns explicitly (advanced).
        :param table_name: The name of the table to create
        :param partition_by: The column partitioning to apply to the created table
        :param col_definitions: Column definitions for the created table
        """
        if not self.cfg.use_iceberg:
            raise RuntimeError("UserspaceConfig.use_iceberg=False. Enable Iceberg to use INSERT/UPDATE/DELETE.")

        location = self.cfg.table_location(table_name)

        if self.table_exists(table_name):
            return location

        # Basic Iceberg CREATE TABLE with location
        props = dict(col_definitions.items())
        props_sql = ",\n  ".join(f"{k} {v}" for k, v in props.items())
        partition_by_sql = ""
        if partition_by:
            cols = ", ".join(partition_by)
            partition_by_sql = f"PARTITIONED BY ({cols})"

        create_sql = f"""
        CREATE TABLE {self.cfg.db_name}.{table_name} (
          {props_sql}
        )
        {partition_by_sql}
        TBLPROPERTIES ('table_type' = 'ICEBERG')
        LOCATION '{location}'
        """

        final_sql = render_safe_athena_sql(create_sql, {})

        self._athena_client.run_to_s3(final_sql)

        return location


    # -------- CTAS (PARQUET) --------

    def ctas_overwrite(
        self,
        table_name: str,
        select_sql_template: str,
        params: Mapping[str, object],
        *,
        partition_by: Sequence[str] = (),
        compression: str = "SNAPPY",
        additional_tbl_props: Mapping[str, str] = {},
        pretty_sql: bool = True,
    ) -> QueryResult:
        """
        CREATE TABLE userspace.table_name WITH (...) AS <SELECT ...>

        Overwrites the table (drop-and-create semantics).
        Executed against athena
        """
        db = self.cfg.db_name
        self.cfg.table_location(table_name)

        # Build CTAS WITH clause options
        with_kv = {
            "format": "'PARQUET'",
            "parquet_compression": f"'{compression}'",
        }
        if partition_by:
            # Presto-style array literal
            cols = ", ".join(f"'{c}'" for c in partition_by)
            with_kv["partitioned_by"] = f"ARRAY[{cols}]"

        for k, v in additional_tbl_props.items():
            with_kv[k] = v

        with_sql = ",\n  ".join(f"{k} = {v}" for k, v in with_kv.items())

        # Render the SELECT safely
        select_sql = render_safe_athena_sql(select_sql_template, params, pretty=pretty_sql)

        # Drop existing table to ensure a clean overwrite (optional)
        drop_sql =  f'DROP TABLE IF EXISTS {db}.{table_name}'
        self._athena_client.run_to_s3(drop_sql)

        # Final CTAS
        ctas_sql = f"""
        CREATE TABLE "{db}"."{table_name}"
        WITH (
          {with_sql}
        ) AS
        {select_sql}
        """
        result = self._athena_client.run_to_s3(ctas_sql)

        return result

    # -------- ICEBERG (APPEND/UPSERT) --------
    def iceberg_insert_from_select(
        self,
        table_name: str,
        select_sql_template: str,
        params: Mapping[str, object],
        *,
        pretty_sql: bool = True,
    ) -> QueryResult:
        """
        Generate
        INSERT INTO userspace.table_name SELECT ...

        Query and execute it against athena
        """
        if not self.cfg.use_iceberg:
            raise RuntimeError("UserspaceConfig.use_iceberg=False. Enable Iceberg to use INSERT/UPDATE/DELETE.")

        db = self.cfg.db_name
        select_sql = render_safe_athena_sql(select_sql_template, params, pretty=pretty_sql)

        sql = f'INSERT INTO "{db}"."{table_name}" {select_sql}'

        final_sql = render_safe_athena_sql(sql, {})

        result = self._athena_client.run_to_s3(final_sql)
        return result

    def iceberg_merge_from_select(
        self,
        table_name: str,
        select_sql_template: str,
        params: Mapping[str, object],
        *,
        on_clause: str,            # e.g. 't.id = s.id AND t.dt = s.dt'
        when_matched: str,         # e.g. 'UPDATE SET col = s.col'
        when_not_matched: str,     # e.g. 'INSERT (id, dt, col) VALUES (s.id, s.dt, s.col)'
        pretty_sql: bool = True,
    ) -> QueryResult:
        """
        Generate
        MERGE INTO userspace.table_name AS t USING (<select>) AS s
        ON <on_clause> WHEN MATCHED THEN ... WHEN NOT MATCHED THEN ...

        Query and execute it against athena
        """
        if not self.cfg.use_iceberg:
            raise RuntimeError("UserspaceConfig.use_iceberg=False. Enable Iceberg to use MERGE/UPSERT.")

        db = self.cfg.db_name
        select_sql = render_safe_athena_sql(select_sql_template, params, pretty=pretty_sql)

        sql = f"""
        MERGE INTO "{db}"."{table_name}" AS t
        USING ({select_sql}) AS s
        ON {on_clause}
        WHEN MATCHED THEN {when_matched}
        WHEN NOT MATCHED THEN {when_not_matched}
        """

        final_sql = render_safe_athena_sql(sql, {})

        result = self._athena_client.run_to_s3(final_sql)

        return result