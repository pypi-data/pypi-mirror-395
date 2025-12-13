import httpx
from typing import Dict, Any, Optional
from bson import ObjectId
from src.services.config import Config
import json
import mimetypes

class KariniClient:    
    def __init__(
        self,
        api_base: Optional[str] = None,
        copilot_id: Optional[str] = None,
        karini_api_key: Optional[str] = None,
        webhook_api_key: Optional[str] = None,
        webhook_recipe_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
    ):
        """Initialize Karini client."""
        config = Config.from_env()
        self.api_base = api_base or config.api_base
        self.copilot_id = copilot_id or config.copilot_id
        self.karini_api_key = karini_api_key or config.karini_api_key
        self.webhook_api_key = webhook_api_key or config.webhook_api_key
        self.webhook_recipe_id = webhook_recipe_id or config.webhook_recipe_id
        self.dataset_id = dataset_id or config.karini_dataset_id
    
    async def ask_copilot(
        self,
        question: str,
        suggest_followup_questions: bool = False,
        files: list = None,
    ):
        """Send a question to the copilot."""
        url = f"{self.api_base}/api/copilot/{self.copilot_id}"
        thread = "68f1efc97c30caba4676f6a0"
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.karini_api_key,
            "x-client-type": "swagger",
        }
        
        payload = {
            "request_id": str(ObjectId()),
            "question": question,
            "suggest_followup_questions": suggest_followup_questions,
            "thread": thread,
        }
        
        if files:
            payload["files"] = {
                "documents": files,
                "metadata": {}
            }
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                response.raise_for_status()
                
                full_response = ""
                async for chunk in response.aiter_text():
                    full_response += chunk
                
                if "#%&response&%#" in full_response:
                    response_part = full_response.split("#%&response&%#")[1]
                    response_part = json.loads(response_part)
                    if "response" in response_part:
                        return response_part.get("response")
                    return response_part
                
                return full_response

    async def invoke_webhook(
        self,
        input_message: str = None,
        files: list = None,
        metadata: dict = None,
    ) -> Dict[str, Any]:
        """Invoke webhook recipe."""
        url = f"{self.api_base}/api/webhook/recipe/{self.webhook_recipe_id}"
        
        headers = {
            "Content-Type": "application/json",
            "x-api-token": self.webhook_api_key,
        }
        
        formatted_files = []
        if files:
            for file_path in files:
                content_type, _ = mimetypes.guess_type(file_path)
                formatted_files.append({
                    "content_type": content_type or "application/octet-stream",
                    "file_path": file_path
                })
        
        payload = {
            "files": formatted_files,
            "input_message": input_message or "",
            "metadata": metadata or {},
        }
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def get_webhook_status(
        self,
        request_id: str = None,
        limit: int = 5
    ) -> Dict[str, Any]:
        """Get webhook request status - single request or recent requests."""
        
        if request_id:
            # Get single request by ID
            url = f"{self.api_base}/api/webhook/request/{request_id}"
        else:
            # Get recent requests for recipe
            url = f"{self.api_base}/api/webhook/recipe/{self.webhook_recipe_id}?limit={limit}"
        
        headers = {
            "accept": "application/json",
            "x-api-token": self.webhook_api_key,
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def query_dataset(
        self,
        text: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """Query karini dataset."""
        url = f"{self.api_base}/api/search"
        
        headers = {
            "accept": "application/json",
            "x-api-key": self.karini_api_key,
            "Content-Type": "application/json",
            "x-client-type": "swagger",
        }
        
        payload = {
            "datasetId": self.dataset_id,
            "query": {
                "mode": "text",
                "text": text,
                "top_k": top_k
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        
    async def get_traces(
        self,
        request_id: str
    ) -> Dict[str, Any]:
        """Get tracing information for a specific request."""
        url = f"{self.api_base}/api/trace/{request_id}"

        headers = {
            "accept": "application/json",
            "x-api-key": self.karini_api_key,
            "x-client-type": "swagger",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            traces_result = response.json()

            data_list = traces_result.get("data", [])

            for idx, item in enumerate(data_list):
                process = item.get("process", "")

                details = item.get("details", {})
                prompt = details.get("prompt", {})

                if process == "generate_embeddings":
                    if isinstance(prompt.get("output"), dict):
                        prompt["output"]["vector"] = []
                    elif isinstance(prompt.get("output"), list):
                        prompt["output"] = []

                elif process == "search_vector_index":

                    raw_input = prompt.get("input", {})

                    if isinstance(raw_input, str):
                        try:
                            raw_input = json.loads(raw_input)
                        except Exception:
                            raw_input = {}

                    query = raw_input.get("query", {})

                    if "hybrid" in query:
                        for q in query["hybrid"].get("queries", []):
                            knn_query = q.get("knn", {})
                            embedding_data = knn_query.get("embedding")
                            if isinstance(embedding_data, dict) and "vector" in embedding_data:
                                embedding_data["vector"] = []

                    elif "script_score" in query:
                        params = query["script_score"].get("script", {}).get("params", {})
                        if "query_value" in params:
                            params["query_value"] = []

                    elif "bool" in query:
                        must_list = query["bool"].get("must", [])
                        if must_list:
                            condition_query = must_list[-1]
                            if "knn" in condition_query:
                                embeddings = condition_query["knn"].get("embedding", {})
                                if isinstance(embeddings, dict) and "vector" in embeddings:
                                    embeddings["vector"] = []

                    prompt["input"] = raw_input

                details["prompt"] = prompt
                item["details"] = details

            traces_result["data"] = data_list
            return traces_result
