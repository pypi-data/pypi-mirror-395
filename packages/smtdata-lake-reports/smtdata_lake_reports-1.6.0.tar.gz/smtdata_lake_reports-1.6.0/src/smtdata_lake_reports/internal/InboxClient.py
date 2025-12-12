from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from smtdata_lake_reports.internal.InboxClientTypes import InboxMessage, AthenaQueryInbox
from smtdata_lake_reports import logger

import boto3


@dataclass(frozen=True)
class InboxClientConfig:
    aws_region: str
    queue_url: str

class InboxClient:
    def __init__(self, cfg: InboxClientConfig, *, sqs_client: Optional[boto3.client] = None) -> None:
        self.cfg = cfg
        self.sqs_client = sqs_client or boto3.client("sqs", region_name=self.cfg.aws_region)

    def publish_athena_query_result(self, report_exec_id: str, athena_query_info: dict) -> None:
        logger.debug(f"Publishing athena query result to queue {self.cfg.queue_url} in region {self.cfg.aws_region}")

        msg = InboxMessage(
            report_exec_id=report_exec_id,
            athena_query=AthenaQueryInbox.from_boto_athena(athena_query_info)
        )

        if self.cfg.queue_url:
            resp = self.sqs_client.send_message(
                QueueUrl=self.cfg.queue_url,
                MessageBody=msg.model_dump_json(by_alias=True),
            )

            logger.debug(f"Published message status: {resp.get('MessageStatus')} with id {resp['MessageId']}")
        else:
            logger.debug("No queue_url provided, dumping stats to log instead")
            logger.info(f"Athena query stats {msg.model_dump(by_alias=True)}")
