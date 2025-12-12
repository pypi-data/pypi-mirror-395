from ..context import BaseNotebookContextProviderPlugin, get_fabric_context
from ..utils import is_on_fabric_spark_driver
from . import in_context


class SparkContextProviderPlugin(BaseNotebookContextProviderPlugin):
    _runtime_name = "spark_notebook"

    @classmethod
    def in_context(cls):
        return in_context()

    @property
    def runtime_name(self) -> str:
        """
        spark_notebook_driver
        spark_notebook_executor
        sjd_driver
        sjd_executor
        """
        artifact = (
            self._runtime_name
            if get_fabric_context().get("trident.artifact.type") == "SynapseNotebook"
            else "sjd"
        )
        if is_on_fabric_spark_driver():
            return artifact + "_driver"
        else:
            return artifact + "_executor"
