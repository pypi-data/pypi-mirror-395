from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, List
import boto3
import pandas as pd
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

from smtdata_lake_reports.runtime_context import ContextSettings, get_context


@dataclass(frozen=True)
class S3ClientConfig:
    aws_region: str
    bucket: str


class S3Client:
    """
    Minimal, testable S3 helper for a tenant-owned bucket.
    - Upload local files or bytes
    - Download to local or bytes
    - Move within the same bucket (copy + delete)

    Defaults (region & bucket) come from ContextSettings, but you can pass an explicit S3ClientConfig.
    """

    def __init__(
            self,
            cfg: S3ClientConfig,
            *,
            s3_client: Optional[BaseClient] = None,
            context: Optional[ContextSettings] = None
    ) -> None:
        self.context = context or get_context()

        self.cfg = cfg
        self.s3: BaseClient = s3_client or boto3.client("s3", region_name=self.cfg.aws_region)

    @staticmethod
    def create_instance() -> S3Client:
        """
        Static method to create a default instance of the S3Client with settings and credentials loaded from the
        environment
        :return: A ready to use instance
        """

        ctx = get_context()
        cfg = S3ClientConfig(ctx.aws_region, ctx.s3_bucket_name)
        return S3Client(cfg)

    # ---------- public API ----------

    def upload_file(
            self,
            local_path: str,
            key: str,
            *,
            extra_args: Optional[Dict] = None,
    ) -> None:
        """Upload a local file to s3://bucket/(base_prefix/)key"""
        try:
            self.s3.upload_file(
                Filename=local_path,
                Bucket=self.cfg.bucket,
                Key=self._sanitize_key(key),
                ExtraArgs=extra_args or {},
            )
        except ClientError as e:
            raise RuntimeError(
                f"Upload failed for {local_path} -> s3://{self.cfg.bucket}/{self._sanitize_key(key)}: {e}") from e

    def put_bytes(
            self,
            data: bytes,
            key: str,
            *,
            content_type: Optional[str] = None,
            extra_args: Optional[Dict] = None,
    ) -> None:
        """Upload in-memory bytes to S3."""
        args = {"Bucket": self.cfg.bucket, "Key": self._sanitize_key(key), "Body": data}
        if content_type:
            args["ContentType"] = content_type
        if extra_args:
            args.update(extra_args)
        try:
            self.s3.put_object(**args)
        except ClientError as e:
            raise RuntimeError(f"put_bytes failed for key {key}: {e}") from e

    def download_file(self, key: str, local_path: str) -> None:
        """Download S3 object to a local path."""
        try:
            self.s3.download_file(
                Bucket=self.cfg.bucket,
                Key=self._sanitize_key(key),
                Filename=local_path,
            )
        except ClientError as e:
            raise RuntimeError(f"Download failed for s3://{self.cfg.bucket}/{self._sanitize_key(key)}: {e}") from e

    def get_bytes(self, key: str) -> bytes:
        """Download S3 object content as bytes."""
        try:
            resp = self.s3.get_object(Bucket=self.cfg.bucket, Key=self._sanitize_key(key))
            return resp["Body"].read()
        except ClientError as e:
            raise RuntimeError(f"get_bytes failed for key {key}: {e}") from e

    def stream_bytes(self, key: str) -> StreamingBody:
        """
        Return the underlying S3 streaming body for the given key.

        The caller is responsible for consuming and closing the stream
        (e.g. via read(), iter_chunks(), iter_lines(), or .close()).

        :param key: Either a full s3 bucket url with key and file, or just a relative path+file within the bucket
        :return: An iterator of bytes
        """
        full_key = self._sanitize_key(key)

        try:
            resp = self.s3.get_object(Bucket=self.cfg.bucket, Key=full_key)
        except ClientError as e:
            raise RuntimeError(f"get_object failed for key {full_key}: {e}") from e

        return resp["Body"]

    def move(self, src_key_or_full_src: str, dst_key: str, *, extra_copy_args: Optional[Dict] = None) -> None:
        """
        Move within the same bucket: copy to new key, then delete old key.
        Not atomic—wrap in higher-level logic if you need stronger guarantees.

        :param src_key_or_full_src: Either a full s3 bucket url with key and file, or just a relative path+file within the bucket
        :param dst_key: The destination key to move the file to
        :param extra_copy_args:
        :return: Nothing
        """

        full_src = self._sanitize_key(src_key_or_full_src)
        full_dst = self._sanitize_key(dst_key)

        try:
            self.s3.copy(
                CopySource={"Bucket": self.cfg.bucket, "Key": full_src},
                Bucket=self.cfg.bucket,
                Key=full_dst,
                ExtraArgs=extra_copy_args or {},
            )
            self.delete_file(full_src)
        except ClientError as e:
            raise RuntimeError(f"Move failed {full_src} -> {full_dst}: {e}") from e

    def delete_file(self, key: str) -> None:
        full_src = self._sanitize_key(key)
        try:
            self.s3.delete_object(Bucket=self.cfg.bucket, Key=full_src)
        except ClientError as e:
            raise RuntimeError(f"Delete failed {full_src}: {e}") from e

    def dataframe_to_csv_streaming(self, df, key: str, *, index=False, header=True):
        """
        Write out a Pandas DataFrame as a CSV file stream stored in the bucket on the given key.

        It is a streaming write meaning that only slighly more memory is required, and no files are created locally

        :param df: The DataFrame to write out, using the built in `to_csv` function
        :param key: The key (path + filename) to write the DataFrame to
        :param index: If True, add row names
        :param header: If True add headers to the resulting CSV
        :return:
        """
        full_key = f"s3://{self.cfg.bucket}/{self._sanitize_key(key)}"
        df.to_csv(full_key, index=index, header=header, lineterminator="\n")

    def read_csv_to_dataframe(self, key: str, **read_csv_kwargs) -> pd.DataFrame:
        """
        Download a CSV from S3 and load it into a Pandas DataFrame without using the filesystem.

        :param key: The key of the CSV file in the bucket
        :param read_csv_kwargs: Extra keyword args passed to pandas.read_csv (e.g. delimiter, dtype)
        :return: Pandas DataFrame
        """
        try:
            full_s3_key = f"s3://{self.cfg.bucket}/{self._sanitize_key(key)}"
            return pd.read_csv(full_s3_key, **read_csv_kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to read CSV {key} into DataFrame: {e}") from e

    def dataframe_to_parquet_streaming(self, df: pd.DataFrame, key: str, **to_parquet_kwargs):
        full_s3_key = f"s3://{self.cfg.bucket}/{self._sanitize_key(key)}"
        return df.to_parquet(full_s3_key, **to_parquet_kwargs)


    def read_parquet_to_dataframe(self, key: str, **read_parquet_kwargs):
        try:
            full_s3_key = f"s3://{self.cfg.bucket}/{self._sanitize_key(key)}"
            return pd.read_parquet(full_s3_key, **read_parquet_kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to read Parquet {key} into DataFrame: {e}") from e

    def list_files(self, prefix: Optional[str] = None, max_keys: int = 1000) -> List[str]:
        """
        List object keys in the configured bucket.

        Add a prefix to filter objects starting with that given prefix. This effectively results in what would be
        considered a "recursive file listing" on a file system

        :param prefix: Optional prefix to filter keys (e.g. "reports/")
        :param max_keys: Maximum number of keys to return per page (default 1000)
        :return: List of object keys
        """
        kwargs = {
            "Bucket": self.cfg.bucket,
            "MaxKeys": max_keys,
        }
        if prefix:
            kwargs["Prefix"] = self._sanitize_key(prefix)

        keys: List[str] = []
        continuation_token = None

        try:
            while True:
                if continuation_token:
                    kwargs["ContinuationToken"] = continuation_token
                resp = self.s3.list_objects_v2(**kwargs)

                for obj in resp.get("Contents", []):
                    keys.append(obj["Key"])

                if resp.get("IsTruncated"):  # more pages
                    continuation_token = resp["NextContinuationToken"]
                else:
                    break
        except ClientError as e:
            raise RuntimeError(f"Failed to list files in s3://{self.cfg.bucket}/{prefix or ''}: {e}") from e

        return keys

    def _sanitize_key(self, key_or_bucket_with_key: str) -> str:
        """
        Sanitize the given key such that:
        1. If it leads with a `/` remove it as it creates wonky folders in s3
        2. If it is a full bucket URI within the configured tenant-bucket strip it out

        :param key_or_bucket_with_key:
        :return:
        """
        if key_or_bucket_with_key.startswith(f"s3://{self.cfg.bucket}/"):
            key_or_bucket_with_key = key_or_bucket_with_key[len(f"s3://{self.cfg.bucket}/"):]

        return key_or_bucket_with_key.lstrip("/")
