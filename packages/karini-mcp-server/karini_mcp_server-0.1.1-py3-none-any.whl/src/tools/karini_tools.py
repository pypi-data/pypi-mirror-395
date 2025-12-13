from typing import Optional, Dict
import json
from fastmcp import FastMCP
from src.services.client import KariniClient
from src.services.config import Config

config = Config.from_env()

class KariniTools:
    def __init__(self):
        self.config = config
        self.karini_client = KariniClient()

    def register_copilot_tools(self, mcp: FastMCP):        
        if not self.config.validate_copilot_config():
            return
        
        @mcp.tool()
        async def ask_karini_copilot(
            question: str,
            files: list = None
        ) -> str:
            """Ask a question to the Karini AI copilot and get an answer.
            
            This tool allows you to interact with your configured Karini copilot by sending
            natural language questions and receiving AI-generated responses. The copilot
            maintains conversation context through threads and can optionally process files.
            
            Args:
                question: The question or message to send to the copilot
                files: Optional list of S3 file paths to process with the question
                    Example: ["s3://bucket/path/file1.txt", "s3://bucket/path/file2.pdf"]
            """
            try:
                response = await self.karini_client.ask_copilot(
                    question=question,
                    suggest_followup_questions=False,
                    files=files
                )
                return json.dumps(response, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to ask copilot: {str(e)}"
                })

    def register_webhook_tools(self, mcp: FastMCP):        
        if not self.config.validate_webhook_config():
            return
        
        @mcp.tool()
        async def invoke_webhook_recipe(
            question: str = None,
            files: list = None,
            metadata: dict = None
        ) -> str:
            """Invoke a Karini webhook recipe to process data asynchronously.
            
            This tool triggers a webhook recipe that can process text queries, files, and 
            metadata. The webhook executes asynchronously and returns a request_id that 
            can be used to check the processing status later.
            
            Args:
                question: Optional input message or query to process
                files: Optional list of S3 file paths. Content type is automatically detected.
                    Example: ["s3://bucket/file.pdf", "s3://bucket/image.jpg"]
                metadata: Optional dictionary of key-value pairs for additional context
            """
            try:
                response = await self.karini_client.invoke_webhook(
                    input_message=question,
                    files=files,
                    metadata=metadata
                )
                return json.dumps(response, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to invoke webhook: {str(e)}"
                })
                
        @mcp.tool()
        async def get_webhook_status(
            request_id: str = None,
            limit: int = 5
        ) -> str:
            """Check the status of webhook recipe executions.
            
            This tool allows you to monitor webhook processing status. You can either check
            a specific request by ID or retrieve the status of recent webhook executions.
            
            Args:
                request_id: Optional specific request ID returned from invoke_webhook_recipe.
                            If provided, returns detailed status for that specific request.
                            If not provided, returns a list of recent webhook executions.
                limit: Number of recent requests to return when request_id is not specified.
                Default is 5.
            """
            try:
                response = await self.karini_client.get_webhook_status(
                    request_id=request_id,
                    limit=limit
                )
                return json.dumps(response, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to get webhook status: {str(e)}"
                })

    def register_dataset_tools(self, mcp: FastMCP):
        if not self.config.validate_dataset_config():
            return
        
        @mcp.tool()
        async def query_karini_dataset(
            text: str,
            top_k: int = 5
        ) -> str:
            """Search and retrieve information from the Karini knowledge base.
            
            This tool performs semantic search across your configured Karini dataset
            to find relevant documents and information based on the query text.
            
            Args:
                text: The search query or question to find relevant information
                top_k: Number of most relevant results to return (default: 5, max: 20)
            """
            try:
                response = await self.karini_client.query_dataset(
                    text=text,
                    top_k=top_k
                )
                return json.dumps(response, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to query dataset: {str(e)}"
                })

    def register_tracing_tools(self, mcp: FastMCP):
        if not self.config.validate_tracing_config():
            return
        
        @mcp.tool()
        async def get_traces(
            request_id: str,
        ) -> str:
            """Trace a Karini event by request ID.
            
            This tool allows you to trace and retrieve detailed information about
            a specific Karini event using its request ID.
            
            Args:
                request_id: The unique identifier of the Karini event to trace
            """
            try:
                response = await self.karini_client.get_traces(
                    request_id=request_id,
                )
                return json.dumps(response, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to trace event: {str(e)}"
                })