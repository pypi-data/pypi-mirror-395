import logging
from typing import Any, Optional

from fabric.analytics.environment.base.credentials import (
    MwcAccessToken,
    _get_token_expire_time,
)
from fabric.analytics.environment.mwc_credential import (
    BaseMWCTokenCredentialProviderV1,
    BaseMWCTokenCredentialProviderV2,
    MWCTokenRequestPayloadV1,
    MWCTokenRequestPayloadV2,
)

from ..token_service_client import TokenServiceClient
from . import in_context

logger = logging.getLogger(__name__)


class PythonNotebookMWCTokenCredentialV1(BaseMWCTokenCredentialProviderV1):
    priority = 0

    def __init__(
        self,
        payload: Optional[MWCTokenRequestPayloadV1] = None,
    ):
        super().__init__(payload=payload)

    @classmethod
    def in_context(cls):
        return in_context()

    def get_mwc_token(
        self,
        **kwargs: Any,
    ) -> MwcAccessToken:
        payload: MWCTokenRequestPayloadV1 = self.payload or kwargs.pop("payload")
        if payload.workload_type == "SparkCore":
            if not payload.workspace_id or len(payload.artifact_ids) != 1:
                raise RuntimeError(
                    f"Generate SparkCore MWC Token is via token service and you should pass exactly one workspace_id and one artifact_id"
                )

            mwc_token = TokenServiceClient().get_mwc_token(
                workspace_id=payload.workspace_id,
                artifact_id=payload.artifact_ids[0],
                version="1",
            )

            expires_on = _get_token_expire_time(mwc_token.Token)
            return MwcAccessToken(
                token=mwc_token, expires_on=expires_on, refresh_on=expires_on - 60
            )

        else:
            raise RuntimeError(
                f"Getting MWC TOKEN v1 for Workload {payload.workload_type} Not supported!"
            )


class PythonNotebookMWCTokenCredentialV2(BaseMWCTokenCredentialProviderV2):
    priority = 0

    def __init__(
        self,
        payload: Optional[MWCTokenRequestPayloadV2] = None,
    ):
        super().__init__(payload=payload)

    @classmethod
    def in_context(cls):
        return in_context()

    def get_mwc_token(
        self,
        **kwargs: Any,
    ) -> MwcAccessToken:
        payload: MWCTokenRequestPayloadV2 = self.payload or kwargs.pop("payload")
        if payload.workload_type == "SparkCore":
            if not payload.workspace_id or len(payload.artifacts) != 1:
                raise RuntimeError(
                    f"Generate SparkCore MWC Token is via token service and you should pass exactly one workspace_id and one artifact_id"
                )
            mwc_token = TokenServiceClient().get_mwc_token(
                workspace_id=payload.workspace_id,
                artifact_id=payload.artifacts[0].artifactObjectId,
                version="2",
            )

            expires_on = _get_token_expire_time(mwc_token.Token)
            return MwcAccessToken(
                token=mwc_token, expires_on=expires_on, refresh_on=expires_on - 60
            )
        elif payload.workload_type == "ML":
            if len(payload.artifacts) != 0:
                logger.warning(
                    f"MWC Token Provider for workload ML doesn't support artifact"
                )
            return MwcAccessToken.build_from_json(
                TokenServiceClient().get_ml_mwc_token(workspace_id=payload.workspace_id)
            )
        else:
            raise RuntimeError(
                f"Getting MWC TOKEN v2 for Workload {payload.workload_type} Not supported!"
            )
