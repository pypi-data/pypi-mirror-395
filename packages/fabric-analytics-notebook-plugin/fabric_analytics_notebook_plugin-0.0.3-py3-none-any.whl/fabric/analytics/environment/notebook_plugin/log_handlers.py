import logging
import os

from fabric.analytics.environment.base.log_handlers import ILoggingHandlerProviderPlugin


class NotebookLogHandlerProviderPlugin(ILoggingHandlerProviderPlugin):
    @classmethod
    def in_context(cls):
        return os.path.isfile("/home/trusted-service-user/.trident-context")

    def get_handlers(self, **kwargs):
        from synapse.ml.internal_utils.constants import ML_KUSTO_TABLE_NAME
        from synapse.ml.pymds.handler import SynapseHandler

        hdlr = SynapseHandler(
            ML_KUSTO_TABLE_NAME, scrubbers=kwargs.pop("scrubbers", None)
        )
        hdlr.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d:%H:%M:%S",
        )
        hdlr.setFormatter(formatter)
        return [hdlr]
