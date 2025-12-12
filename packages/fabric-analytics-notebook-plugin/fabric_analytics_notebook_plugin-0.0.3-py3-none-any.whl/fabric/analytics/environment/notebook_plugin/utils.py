import logging
import os
import threading
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

_shortforms = {
    "https://storage.azure.com": "storage",
    "storage": "storage",
    "https://analysis.windows.net/powerbi/api": "pbi",
    "pbi": "pbi",
    "https://vault.azure.net": "keyvault",
    "keyvault": "keyvault",
    "https://kusto.kusto.windows.net": "kusto",
    "kusto": "kusto",
    "ml": "ml",
    "sql": "sql",
}

# This is aud can be read from cache
cache_aud_to_key = {
    "https://storage.azure.com": "storage",
    "storage": "storage",
    "https://analysis.windows.net/powerbi/api": "pbi",
    "pbi": "pbi",
    "https://vault.azure.net": "keyvault",
    "keyvault": "keyvault",
    "ml": "ml",
}

_ml_1p_token_audience = [
    "https://analysis.windows.net/powerbi/api",
    "pbi",
    "https://api.fabric.microsoft.com",
    "https://analysis.windows-int.net/powerbi/api",
]


def scopes_to_resource(scopes: Optional[Tuple[str, ...]], **kwargs: Any):
    scopes_list = list(scopes) if scopes else []

    if len(scopes_list) != 1:
        raise ValueError(
            "This credential requires exactly one scope per token request."
        )

    resource = scopes_list[0]
    if resource.endswith("/.default"):
        resource = resource[: -len("/.default")]

    if kwargs.pop("use_ml_1p", True):
        # Use ML 1P for pbi audience by default
        if resource in _ml_1p_token_audience:
            logger.debug("Using ML 1P token for pbi audience")
            resource = "ml"

    return resource


def is_pure_python_env() -> bool:
    return os.environ.get("MSNOTEBOOKUTILS_RUNTIME_TYPE", "").lower() == "jupyter"


def is_fabric_spark() -> bool:
    return (
        os.path.isfile("/home/trusted-service-user/.trident-context")
        and not is_pure_python_env()
    )


def is_on_fabric_spark_driver() -> bool:
    if is_fabric_spark():
        from pyspark.sql import SparkSession

        return SparkSession.getActiveSession() is not None
    return False


def safe_get_spark_context():
    """This function returns spark context only when on fabric spark driver

    Returns:
        SparkContext
    """
    if is_pure_python_env():
        return None
    try:
        if not is_on_fabric_spark_driver():
            logger.debug("Not in fabric spark driver")
            return None

        from pyspark.sql import SparkSession

        spark = SparkSession.getActiveSession()
        sc = spark.sparkContext
        logger.debug("On driver now")
        return sc
    except Exception:
        logger.debug("Not in fabric spark driver")
    return None
