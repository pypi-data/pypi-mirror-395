import logging
from typing import Any, Optional, Tuple

from azure.core.credentials import AccessToken
from fabric.analytics.environment.base.credentials import decode_jwt
from fabric.analytics.environment.credentials import (
    IFabricAnalyticsTokenCredentialProviderPlugin,
)

from ..token_service_client import TokenServiceClient
from ..utils import scopes_to_resource
from . import in_context

logger = logging.getLogger(__name__)


class PythonNotebookCredentialProviderPlugin(
    IFabricAnalyticsTokenCredentialProviderPlugin
):
    @classmethod
    def in_context(cls):
        return in_context()

    def get_token(
        self,
        *scopes: str,
        claims: Optional[str] = None,
        tenant_id: Optional[str] = None,
        enable_cae: bool = False,
        **kwargs: Any,
    ) -> AccessToken:
        if len(scopes) != 1:
            raise ValueError(
                "This credential requires exactly one scope per token request."
            )

        resource = self._scopes_to_resource(scopes, **kwargs)
        token = TokenServiceClient().get_access_token(resource)
        try:
            payload = decode_jwt(token)
            exp_time = payload.get("exp")
            return AccessToken(token=token, expires_on=exp_time)
        except Exception as ex:
            logger.exception(f"invalid {resource} token from token service")
            raise RuntimeError(f"invalid {resource} token from token service") from ex

    def _scopes_to_resource(
        self, scopes: Optional[Tuple[str, ...]], **kwargs: Any
    ) -> str:
        return scopes_to_resource(scopes=scopes, **kwargs)
