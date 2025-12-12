from ..context import BaseNotebookContextProviderPlugin
from . import in_context


class PythonContextProviderPlugin(BaseNotebookContextProviderPlugin):
    _runtime_name = "python_notebook"

    @classmethod
    def in_context(cls):
        return in_context()
