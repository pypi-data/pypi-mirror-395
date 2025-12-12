"""Web operations task for HTTP requests and web scraping."""

import json
from typing import Any, Dict, Optional
from urllib import request, parse
from urllib.error import HTTPError, URLError

from flowmind.core.task import BaseTask, TaskResult, TaskStatus
from flowmind.core.context import Context
from flowmind.utils.validator import Validator


class WebTask(BaseTask):
    """Task for web operations (HTTP requests, scraping).
    
    Operations:
    - get: HTTP GET request
    - post: HTTP POST request
    - download: Download file from URL
    - scrape: Extract data from HTML (basic)
    
    Example:
        >>> task = WebTask(
        ...     name="fetch_api",
        ...     operation="get",
        ...     url="https://api.example.com/data"
        ... )
    """
    
    def __init__(self, name: str, **config):
        super().__init__(name, "Web operations task", **config)
    
    def validate(self) -> bool:
        """Validate task configuration."""
        try:
            Validator.require_fields(self.config, "operation", "url")
            Validator.validate_choice(
                self.config["operation"],
                ["get", "post", "download", "scrape"],
                "operation"
            )
            Validator.validate_url(self.config["url"])
            return True
        except (ValueError, TypeError):
            return False
    
    def execute(self, context: Context) -> TaskResult:
        """Execute the web operation."""
        operation = self.config["operation"]
        
        try:
            if operation == "get":
                result = self._http_get(context)
            elif operation == "post":
                result = self._http_post(context)
            elif operation == "download":
                result = self._download_file(context)
            elif operation == "scrape":
                result = self._scrape_page(context)
            else:
                return TaskResult(
                    status=TaskStatus.FAILED,
                    error=f"Unknown operation: {operation}"
                )
            
            return TaskResult(status=TaskStatus.SUCCESS, output=result)
            
        except Exception as e:
            return TaskResult(status=TaskStatus.FAILED, error=str(e))
    
    def _http_get(self, context: Context) -> Dict[str, Any]:
        """Perform HTTP GET request."""
        url = context.resolve_variables(self.config["url"])
        headers = self.config.get("headers", {})
        
        req = request.Request(url, headers=headers)
        
        try:
            with request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                status_code = response.getcode()
                
                # Parse JSON if requested
                if self.config.get("parse_json", True):
                    try:
                        content = json.loads(content)
                    except json.JSONDecodeError:
                        pass
                
                return {
                    "status_code": status_code,
                    "content": content,
                    "url": url
                }
        except HTTPError as e:
            return {
                "status_code": e.code,
                "error": str(e),
                "url": url
            }
    
    def _http_post(self, context: Context) -> Dict[str, Any]:
        """Perform HTTP POST request."""
        url = context.resolve_variables(self.config["url"])
        data = context.resolve_variables(self.config.get("data", {}))
        headers = self.config.get("headers", {})
        
        # Convert data to JSON if it's a dict
        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        elif isinstance(data, str):
            data = data.encode('utf-8')
        
        req = request.Request(url, data=data, headers=headers, method='POST')
        
        try:
            with request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                status_code = response.getcode()
                
                if self.config.get("parse_json", True):
                    try:
                        content = json.loads(content)
                    except json.JSONDecodeError:
                        pass
                
                return {
                    "status_code": status_code,
                    "content": content,
                    "url": url
                }
        except HTTPError as e:
            return {
                "status_code": e.code,
                "error": str(e),
                "url": url
            }
    
    def _download_file(self, context: Context) -> Dict[str, Any]:
        """Download file from URL."""
        url = context.resolve_variables(self.config["url"])
        output_path = context.resolve_variables(self.config.get("output", "downloaded_file"))
        
        request.urlretrieve(url, output_path)
        
        import os
        return {
            "url": url,
            "file_path": output_path,
            "size": os.path.getsize(output_path)
        }
    
    def _scrape_page(self, context: Context) -> Dict[str, Any]:
        """Basic HTML scraping (extract text).
        
        Note: For advanced scraping, use a proper library like BeautifulSoup
        in a custom plugin.
        """
        url = context.resolve_variables(self.config["url"])
        selector = self.config.get("selector")
        
        # Simple text extraction without external dependencies
        with request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        
        # Very basic extraction - just get all text
        # For real use cases, recommend BeautifulSoup plugin
        import re
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return {
            "url": url,
            "text": text[:1000],  # First 1000 chars
            "length": len(text)
        }


# Register task type
from flowmind.core.task import TaskFactory
TaskFactory.register("web", WebTask)
TaskFactory.register("download", WebTask)
TaskFactory.register("http", WebTask)
