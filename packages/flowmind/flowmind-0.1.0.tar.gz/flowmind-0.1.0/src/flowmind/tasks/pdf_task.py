"""PDF extraction task - extract text and tables from PDFs."""

from typing import Any, Dict

from flowmind.core.task import BaseTask, TaskResult, TaskStatus, TaskFactory
from flowmind.core.context import Context


class PDFTask(BaseTask):
    """Task for PDF extraction (text, tables, metadata).
    
    Operations:
    - extract: Extract text and tables from PDF
    
    Note: This is a basic implementation. For production, use PyPDF2
    or pdfplumber via plugin for advanced features.
    
    Example:
        >>> task = PDFTask(
        ...     name="extract_invoice",
        ...     operation="extract",
        ...     file_path="invoice.pdf"
        ... )
    """
    
    def __init__(self, name: str, **config):
        super().__init__(name, "PDF extraction task", **config)
    
    def execute(self, context: Context) -> TaskResult:
        """Execute the PDF operation."""
        operation = self.config.get("operation", "extract")
        
        try:
            if operation == "extract":
                result = self._extract_pdf(context)
            else:
                return TaskResult(
                    status=TaskStatus.FAILED,
                    error=f"Unknown operation: {operation}"
                )
            
            return TaskResult(status=TaskStatus.SUCCESS, output=result)
            
        except Exception as e:
            return TaskResult(status=TaskStatus.FAILED, error=str(e))
    
    def _extract_pdf(self, context: Context) -> Dict[str, Any]:
        """Extract content from PDF.
        
        Note: This is a placeholder. For real PDF extraction,
        install PyPDF2 or pdfplumber and use via plugin.
        """
        file_path = context.resolve_variables(self.config.get("file_path"))
        extract_types = self.config.get("extract", ["text"])
        
        # Placeholder response
        result = {
            "file_path": file_path,
            "extracted": extract_types,
            "note": "PDF task placeholder - install PyPDF2/pdfplumber for real extraction"
        }
        
        # Try to use PyPDF2 if available
        try:
            import PyPDF2
            
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                result["text"] = text
                result["num_pages"] = len(reader.pages)
                result["has_library"] = True
                
        except ImportError:
            result["text"] = ""
            result["has_library"] = False
        
        return result


# Register task type
TaskFactory.register("pdf", PDFTask)
TaskFactory.register("extract_pdf", PDFTask)
