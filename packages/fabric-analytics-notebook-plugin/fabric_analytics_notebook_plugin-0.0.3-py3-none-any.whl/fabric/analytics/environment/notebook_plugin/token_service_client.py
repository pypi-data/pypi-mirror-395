import json
import logging
import re
import socket
import uuid
from typing import Dict
from urllib.parse import urlparse

import psutil
import requests  # type: ignore
from fabric.analytics.environment.base.credentials import MwcToken
from fabric.analytics.environment.context import FabricContext
from fabric.analytics.environment.utils.singleton import Singleton
from fabric.analytics.rest.fabric_client import FabricRestClient

from .context import get_fabric_context
from .utils import _shortforms

logger = logging.getLogger(__name__)


class TokenServiceClient(metaclass=Singleton):
    TOKEN_SERVICE_FILE_PATH = "/opt/token-service/tokenservice.config.json"

    def __init__(self):
        self.hostname = socket.gethostname()
        self.process_name = psutil.Process().name()
        self.session_token = get_fabric_context().get("trident.session.token")
        self.sparkcore_tokenservice_endpoint = get_fabric_context().get(
            "trident.lakehouse.tokenservice.endpoint"
        )
        try:
            with open(self.TOKEN_SERVICE_FILE_PATH, "r") as f:
                file_content = f.read()
                token_service_config_dict: Dict[str, str] = {}
                try:
                    token_service_config_dict = json.loads(file_content)
                except json.decoder.JSONDecodeError:
                    token_service_config_dict = json.loads(
                        self._clean_json(file_content)
                    )

                self.synapse_tokenservice_endpoint = token_service_config_dict[
                    "tokenServiceEndpoint"
                ]
                self.cluster_identifier = token_service_config_dict["clusterName"]
        except Exception:
            logger.warning("Error reading token service config file")

    def get_access_token(
        self,
        resource_param: str,
    ) -> str:
        resource_param = _shortforms.get(resource_param, resource_param)

        rid = str(uuid.uuid4())
        _target_url = urlparse(self.sparkcore_tokenservice_endpoint)
        headers = {
            "x-ms-cluster-identifier": self.cluster_identifier,
            "x-ms-workload-resource-moniker": self.cluster_identifier,
            "Content-Type": "application/json;charset=utf-8",
            "x-ms-proxy-host": f"{_target_url.scheme}://{_target_url.hostname}",
            "x-ms-partner-token": self.session_token,
            "User-Agent": f"SynapseML Token Library - HostName:{self.hostname}, ProcessName:{self.process_name}",
            "x-ms-client-request-id": rid,
        }
        url = f"{self.synapse_tokenservice_endpoint}/api/v1/proxy{_target_url.path}/access?resource={resource_param}"
        logger.debug(
            f"fetch access token, raid: {rid},  url: {url}, headers: {headers}"
        )
        resp = requests.get(url=url, headers=headers)

        logger.debug(
            f"fetch access token, {rid} status code: {resp.status_code}, content: {resp.content}"
        )
        if resp.status_code != 200 or not resp.content:
            logger.error(
                f"fetch access token error, {rid} status code: {resp.status_code}, content: {resp.content}"
            )
            raise Exception("Fetch access token error")

        return resp.content.decode("utf-8")

    def get_mwc_token(
        self, workspace_id: str, artifact_id: str, version: str = "2"
    ) -> MwcToken:
        rid = str(uuid.uuid4())
        _target_url = urlparse(self.sparkcore_tokenservice_endpoint)
        headers = {
            "x-ms-cluster-identifier": self.cluster_identifier,
            "x-ms-workload-resource-moniker": self.cluster_identifier,
            "Content-Type": "application/json;charset=utf-8",
            "x-ms-proxy-host": f"{_target_url.scheme}://{_target_url.hostname}",
            "x-ms-partner-token": self.session_token,
            "User-Agent": f"SynapseML Token Library - HostName:{self.hostname}, ProcessName:{self.process_name}",
            "x-ms-client-request-id": rid,
        }
        url = f"{self.synapse_tokenservice_endpoint}/api/v1/proxy{_target_url.path}/mwc/v{version}?workspaceId={workspace_id}&artifactId={artifact_id}"
        logger.debug(f"fetch mwc token, {rid} url: {url}, headers: {headers}")
        resp = requests.get(url=url, headers=headers)

        logger.debug(
            f"fetch mwc token, {rid} status code: {resp.status_code}, content: {resp.content}"
        )
        if resp.status_code != 200 or not resp.content:
            logger.error(
                f"fetch access token error, {rid} status code: {resp.status_code}, content: {resp.content}"
            )
            raise Exception("Fetch access token error")

        return MwcToken(Token=resp.content.decode("utf-8"))

    def get_ml_mwc_token(self, workspace_id: str):
        ctx = FabricContext(workspace_id=workspace_id)

        url = (
            f"{ctx.mwc_workload_host}/webapi/capacities/{ctx.capacity_id}/workloads/"
            + f"ML/MLAdmin/Automatic/workspaceid/{ctx.workspace_id}/"
        )
        url = url + 'token/generatemwctokenv2'

        resp = FabricRestClient().get(
            url=url, headers={'x-ms-workload-resource-moniker': str(uuid.uuid4())}
        )
        resp.raise_for_status()

        return resp.json()

    @classmethod
    def _clean_json(cls, s: str):
        s = re.sub(",[ \t\r\n]+}", "}", s)
        return s
