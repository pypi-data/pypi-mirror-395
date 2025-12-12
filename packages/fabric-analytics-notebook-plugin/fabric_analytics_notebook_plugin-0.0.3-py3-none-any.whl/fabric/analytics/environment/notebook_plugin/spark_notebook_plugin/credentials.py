import logging
from typing import Any, Dict, Optional, Tuple

from azure.core.credentials import AccessToken
from fabric.analytics.environment.base.credentials import (
    IFabricAnalyticsTokenCredentialProviderPlugin,
    decode_jwt,
)

from ..token_service_client import TokenServiceClient
from ..utils import cache_aud_to_key, is_on_fabric_spark_driver, scopes_to_resource
from . import in_context

logger = logging.getLogger(__name__)


class SparkNotebookCredentialProviderPlugin(
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
        from trident_token_library_wrapper import PyTridentTokenLibrary  # type: ignore

        if len(scopes) != 1:
            raise ValueError(
                "This credential requires exactly one scope per token request."
            )

        scope = self._scopes_to_resource(scopes, **kwargs)
        token: str = ""
        try:
            # This is only used in spark notbook, thus only need to make sure only access cache when it is not in driver
            if scope in cache_aud_to_key.keys() and not is_on_fabric_spark_driver():
                logger.debug(f"getting token {scope} from trident token library cache")
                # Make sure this is only used in spark executor, since token cache is created async and unreliable
                token = PyTridentTokenLibrary.get_access_token_from_cache(scope)
            else:
                logger.debug(f"getting token {scope} from trident token library")
                token = PyTridentTokenLibrary.get_access_token(scope)
        except:
            logger.debug(
                f"Error getting token {scope} from trident token library, try direct call..."
            )

        if not token:
            try:
                token = TokenServiceClient().get_access_token(scope)
            except:
                logger.exception(
                    f"Error getting token {scope} via calling token service directly..."
                )
                raise

        payload = decode_jwt(token)
        exp_time = int(payload.get("exp"))

        return AccessToken(token=token, expires_on=exp_time)

    def _scopes_to_resource(
        self, scopes: Optional[Tuple[str, ...]], **kwargs: Any
    ) -> str:
        return scopes_to_resource(scopes=scopes, **kwargs)
