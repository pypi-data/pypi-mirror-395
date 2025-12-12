"""Built-in task types for FlowMind."""

from flowmind.tasks.file_task import FileTask
from flowmind.tasks.web_task import WebTask
from flowmind.tasks.data_task import DataTask
from flowmind.tasks.email_task import EmailTask
from flowmind.tasks.pdf_task import PDFTask
from flowmind.tasks.ml_task import MLTask
from flowmind.tasks.shell_task import ShellTask

__all__ = [
    "FileTask",
    "WebTask",
    "DataTask",
    "EmailTask",
    "PDFTask",
    "MLTask",
    "ShellTask",
]
