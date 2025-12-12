# athena_s3_client.py
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Optional, Tuple

import boto3
from botocore.response import StreamingBody
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from smtdata_lake_reports.internal.InboxClient import InboxClient, InboxClientConfig
from smtdata_lake_reports.runtime_context import ContextSettings, get_context
from smtdata_lake_reports import logger


@dataclass(frozen=True)
class AthenaS3Config:
    aws_region: str
    database: str
    workgroup: str
    log_sql: bool


@dataclass(frozen=True)
class QueryResult:
    query_id: str
    s3_file: str


class AthenaS3Client:
    """
    Minimal Athena client geared towards writing results to S3.

    Primary API:
        - run_to_s3(sql) -> 's3://bucket/prefix/uuid.csv'
        - run_to_dataframe(sql) -> pandas.DataFrame (reads the S3 CSV)
    """

    def __init__(
            self,
            cfg: AthenaS3Config,
            *,
            athena: Optional[BaseClient] = None,
            s3: Optional[BaseClient] = None,
            inbox_client: Optional[InboxClient] = None,
            context: Optional[ContextSettings] = None) -> None:

        self.cfg = cfg
        self.athena = athena or boto3.client("athena", region_name=cfg.aws_region)
        self.s3 = s3 or boto3.client("s3", region_name=cfg.aws_region)
        self.context = context or get_context()
        self.inbox_client = inbox_client or InboxClient(
            InboxClientConfig(self.cfg.aws_region, self.context.inbox.queue_url))

    # ---------- core helpers ----------

    def _start(self, sql: str, *, client_request_token: Optional[str] = None) -> str:
        token = client_request_token or str(uuid.uuid4())
        try:
            resp = self.athena.start_query_execution(
                QueryString=sql,
                QueryExecutionContext={"Database": self.cfg.database},
                WorkGroup=self.cfg.workgroup,
                ClientRequestToken=token,
            )
        except ClientError as e:
            raise RuntimeError(f"Athena start_query_execution failed: {e}") from e
        return resp["QueryExecutionId"]

    def _wait(
            self,
            qid: str,
            *,
            timeout: float = 300.0,
            poll_initial: float = 1.0,
            poll_max: float = 5.0,
            backoff: float = 1.25,
            cancel_on_timeout: bool = True,
    ) -> None:
        start = time.time()
        delay = poll_initial
        logger.debug(f"Entering wait for query {qid}")
        while True:
            try:
                state = self.athena.get_query_execution(QueryExecutionId=qid)["QueryExecution"]["Status"]["State"]
            except ClientError:
                state = "RUNNING"

            logger.debug(f"Query execution status: {state}")
            if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
                break

            if time.time() - start >= timeout:
                logger.warning(f"Query execution did not complete within set timeout: {state}")
                if cancel_on_timeout:
                    try:
                        self.athena.stop_query_execution(QueryExecutionId=qid)
                    except ClientError:
                        pass
                raise TimeoutError(f"Athena query {qid} timed out after {timeout:.0f}s")

            logger.debug(f"Sleeping for: {delay:.0f}s before retrying status query")
            time.sleep(delay)
            delay = min(delay * backoff, poll_max)

        if state == "FAILED":
            logger.warning("Query execution entered failed state")
            st = self.athena.get_query_execution(QueryExecutionId=qid)["QueryExecution"]["Status"]
            raise RuntimeError(f"Athena query {qid} failed: {st.get('StateChangeReason')}")
        if state == "CANCELLED":
            logger.warning("Query execution was cancelled")
            raise RuntimeError(f"Athena query {qid} was cancelled")

    def _output_s3(self, qid: str) -> str:
        exec_info = self.athena.get_query_execution(QueryExecutionId=qid)["QueryExecution"]
        return exec_info["ResultConfiguration"]["OutputLocation"]  # s3://bucket/key.csv

    @staticmethod
    def _split_s3(uri: str) -> Tuple[str, str]:
        assert uri.startswith("s3://"), f"Not an S3 URI: {uri}"
        rest = uri[5:]
        bucket, _, key = rest.partition("/")
        return bucket, key

    # ---------- public API ----------

    def run_to_s3(self, sql: str, *, timeout_in_seconds: float = 3600.0) -> QueryResult:
        """
        Run a query and return the S3 URI of the CSV Athena wrote.

        :arg sql: The SQL query to run
        :arg timeout_in_seconds: How long to wait for the query to complete in seconds
        """
        query_id = ''
        try:
            if self.cfg.log_sql:
                logger.info(sql)

            query_id = self._start(sql)
            logger.debug(f"Starting query with id {query_id}")
            self._wait(query_id, timeout=timeout_in_seconds)

            return QueryResult(query_id, self._output_s3(query_id))
        finally:
            state = self.athena.get_query_execution(QueryExecutionId=query_id)
            logger.debug(f"Query execution status: {state}")

            self.inbox_client.publish_athena_query_result(self.context.report.exec_id, state)

    def download_bytes(self, s3_uri: str) -> bytes:
        """
        Download an object from S3 (useful if you want the raw CSV bytes).
        """
        bucket, key = self._split_s3(s3_uri)
        try:
            obj = self.s3.get_object(Bucket=bucket, Key=key)
        except ClientError as e:
            raise RuntimeError(f"Unable to fetch {s3_uri}: {e}") from e
        return obj["Body"].read()

    def open_stream(self, s3_uri: str) -> StreamingBody:
        """
        Return a streaming body for an S3 object.
        Callers must consume and close it.
        """
        bucket, key = self._split_s3(s3_uri)
        try:
            obj = self.s3.get_object(Bucket=bucket, Key=key)
        except ClientError as e:
            raise RuntimeError(f"Unable to open stream {s3_uri}: {e}") from e
        return obj["Body"]

    def run_and_download(self, sql: str, *, timeout: float = 3600.0) -> Tuple[str, bytes]:
        """
        Convenience: run_to_s3 + download_bytes. Returns (s3_uri, csv_bytes).
        """
        s3_uri = self.run_to_s3(sql, timeout_in_seconds=timeout)
        return s3_uri, self.download_bytes(s3_uri)

    # ---------- pandas overloads ----------
    def csv_to_dataframe(self, s3_uri: str):
        """
        Read an existing Athena CSV result into pandas.
        """
        import io
        import pandas as pd

        csv_bytes = self.download_bytes(s3_uri)
        return pd.read_csv(io.BytesIO(csv_bytes))
