from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel
from pydantic.config import ConfigDict


# ---------- casing ----------
def to_pascal_case(s: str) -> str:
    return "".join(p.capitalize() for p in s.split("_"))


# ---------- models ----------
class ResultReuseInformation(BaseModel):
    reused_previous_result: bool = False

    model_config = ConfigDict(
        alias_generator=to_pascal_case,
        populate_by_name=True,
        frozen=True,
    )


class AthenaQueryStatisticsInbox(BaseModel):
    data_scanned_in_bytes: int = 0
    engine_execution_time_in_millis: int = 0
    query_planning_time_in_millis: int = 0
    query_queue_time_in_millis: int = 0
    result_reuse_information: ResultReuseInformation = ResultReuseInformation()
    service_pre_processing_time_in_millis: int = 0
    service_processing_time_in_millis: int = 0
    total_execution_time_in_millis: int = 0

    model_config = ConfigDict(
        alias_generator=to_pascal_case,
        populate_by_name=True,
        frozen=True,
    )

    @staticmethod
    def from_boto_athena(st: dict) -> AthenaQueryStatisticsInbox:
        """
        Convert a Boto3 Athena Client query result QueryExecution.Statistics information into a
        AthenaQueryStatisticsInbox instance
        :param st:  The QueryExecution.Statistics dictionary from the athena query information response
        :return: A AthenaQueryStatisticsInbox instance with the values that were available
        """
        # st is like resp["QueryExecution"]["Statistics"]. Some keys may be missing depending on the query type.
        reuse_info = st.get("ResultReuseInformation", {}) or {}
        return AthenaQueryStatisticsInbox(
            data_scanned_in_bytes=st.get("DataScannedInBytes", 0),
            engine_execution_time_in_millis=st.get("EngineExecutionTimeInMillis", 0),
            query_planning_time_in_millis=st.get("QueryPlanningTimeInMillis", 0),
            query_queue_time_in_millis=st.get("QueryQueueTimeInMillis", 0),
            result_reuse_information=ResultReuseInformation(
                reused_previous_result=reuse_info.get("ReusedPreviousResult", False)
            ),
            service_pre_processing_time_in_millis=st.get("ServicePreProcessingTimeInMillis", 0),
            service_processing_time_in_millis=st.get("ServiceProcessingTimeInMillis", 0),
            total_execution_time_in_millis=st.get("TotalExecutionTimeInMillis", 0),
        )


class AthenaQueryInbox(BaseModel):
    query_id: str
    status: str
    statistics: Optional[AthenaQueryStatisticsInbox] = None

    model_config = ConfigDict(
        alias_generator=to_pascal_case,
        populate_by_name=True,
        frozen=True,
    )

    @staticmethod
    def from_boto_athena(ath: dict) -> AthenaQueryInbox:
        """
        Convert a Boto3 Athena query result QueryExecution dict into a AthenaQueryInbox instance
        :param ath:
        :return:
        """
        query_execution = ath.get("QueryExecution")
        return AthenaQueryInbox(
            query_id=query_execution.get("QueryExecutionId"),
            status=query_execution.get("Status", {}).get("State"),
            statistics=AthenaQueryStatisticsInbox.from_boto_athena(query_execution.get("Statistics", {})),
        )




class InboxMessage(BaseModel):
    type: Literal["LakeReportsInbox"] = "LakeReportsInbox"
    report_exec_id: str
    athena_query: Optional[AthenaQueryInbox] = None

    model_config = ConfigDict(
        alias_generator=to_pascal_case,
        populate_by_name=True,
        frozen=True,
    )