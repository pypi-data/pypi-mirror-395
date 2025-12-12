"""Email operations task - send and receive emails."""

from typing import Any, Dict

from flowmind.core.task import BaseTask, TaskResult, TaskStatus, TaskFactory
from flowmind.core.context import Context


class EmailTask(BaseTask):
    """Task for email operations (send, receive, classify).
    
    Operations:
    - send: Send email (requires SMTP configuration)
    - classify: Classify email content (basic keyword matching)
    
    Note: For production use, configure SMTP settings or use plugins
    for advanced email handling.
    
    Example:
        >>> task = EmailTask(
        ...     name="send_alert",
        ...     operation="send",
        ...     to="admin@example.com",
        ...     subject="Alert",
        ...     body="System alert!"
        ... )
    """
    
    def __init__(self, name: str, **config):
        super().__init__(name, "Email operations task", **config)
    
    def execute(self, context: Context) -> TaskResult:
        """Execute the email operation."""
        operation = self.config.get("operation", "send")
        
        try:
            if operation == "send":
                result = self._send_email(context)
            elif operation == "classify":
                result = self._classify_email(context)
            else:
                return TaskResult(
                    status=TaskStatus.FAILED,
                    error=f"Unknown operation: {operation}"
                )
            
            return TaskResult(status=TaskStatus.SUCCESS, output=result)
            
        except Exception as e:
            return TaskResult(status=TaskStatus.FAILED, error=str(e))
    
    def _send_email(self, context: Context) -> Dict[str, Any]:
        """Send email via SMTP.
        
        Note: This is a placeholder. For real use, configure SMTP
        or use a plugin with proper email library.
        """
        to = context.resolve_variables(self.config.get("to"))
        subject = context.resolve_variables(self.config.get("subject", ""))
        body = context.resolve_variables(self.config.get("body", ""))
        
        # Placeholder - in production, use smtplib
        return {
            "sent": True,
            "to": to,
            "subject": subject,
            "note": "Email task placeholder - configure SMTP for real sending"
        }
    
    def _classify_email(self, context: Context) -> Dict[str, Any]:
        """Classify email using basic keyword matching."""
        content = context.resolve_variables(self.config.get("content", ""))
        categories = self.config.get("categories", ["urgent", "normal", "spam"])
        
        # Simple keyword-based classification
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["urgent", "asap", "immediate", "critical"]):
            category = "urgent"
        elif any(word in content_lower for word in ["spam", "click here", "winner", "prize"]):
            category = "spam"
        else:
            category = "normal"
        
        return {
            "category": category,
            "confidence": 0.8,  # Placeholder confidence
            "content_length": len(content)
        }


# Register task type
TaskFactory.register("email", EmailTask)
