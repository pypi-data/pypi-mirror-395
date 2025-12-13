import asyncio
from datetime import datetime
from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import json


class MongoLogger:
    def __init__(self, mongo_url: str, database_name: str, collection_name: str = "api_logs"):
        self.mongo_url = mongo_url
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    async def connect(self):
        if not self.client:
            self.client = AsyncIOMotorClient(self.mongo_url)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]

    async def log(self, data: Dict[str, Any]):
        await self.connect()
        log_entry = {
            "timestamp": datetime.utcnow(),
            **data
        }
        await self.collection.insert_one(log_entry)

    async def log_endpoint(
        self,
        method: str,
        path: str,
        status_code: int,
        response_time: float,
        request_body: Optional[Any] = None,
        response_body: Optional[Any] = None,
        headers: Optional[Dict] = None,
        query_params: Optional[Dict] = None,
        user_id: Optional[str] = None,
        **kwargs
    ):
        data = {
            "type": "endpoint",
            "method": method,
            "path": path,
            "status_code": status_code,
            "response_time_ms": response_time,
            "request_body": self._serialize_data(request_body),
            "response_body": self._serialize_data(response_body),
            "headers": headers,
            "query_params": query_params,
            "user_id": user_id,
            **kwargs
        }
        await self.log(data)

    async def log_custom(self, event_type: str, data: Dict[str, Any]):
        log_data = {
            "type": event_type,
            **data
        }
        await self.log(log_data)

    def _serialize_data(self, data: Any) -> Any:
        if data is None:
            return None
        try:
            json.dumps(data)
            return data
        except (TypeError, ValueError):
            return str(data)

    async def close(self):
        if self.client:
            self.client.close()