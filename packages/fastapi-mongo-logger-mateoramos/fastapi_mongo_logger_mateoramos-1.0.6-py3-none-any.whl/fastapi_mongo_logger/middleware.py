import time
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse
from .logger import MongoLogger


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger: MongoLogger, log_request_body: bool = True, log_response_body: bool = False):
        super().__init__(app)
        self.logger = logger
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        # Capture request data
        request_body = None
        if self.log_request_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    request_body = json.loads(body.decode())
            except Exception as e:
                request_body = f"Unable to parse request body: {str(e)}"

        # Process request
        response = await call_next(request)
        
        # Calculate response time
        process_time = (time.time() - start_time) * 1000

        # Capture response data
        response_body = None
        if self.log_response_body:
            try:
                if isinstance(response, StreamingResponse):
                    # Handle streaming responses
                    response_body = "Streaming response - body not captured"
                else:
                    # For regular responses, we need to read the body
                    body_bytes = b""
                    async for chunk in response.body_iterator:
                        body_bytes += chunk
                    
                    if body_bytes:
                        try:
                            response_body = json.loads(body_bytes.decode())
                        except:
                            response_body = body_bytes.decode()
                    
                    # Recreate response with the same body
                    response = Response(
                        content=body_bytes,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.media_type
                    )
            except Exception as e:
                response_body = f"Unable to parse response body: {str(e)}"

        # Log to MongoDB
        await self.logger.log_endpoint(
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            response_time=process_time,
            request_body=request_body,
            response_body=response_body,
            headers=dict(request.headers),
            query_params=dict(request.query_params),
            client_ip=request.client.host if request.client else None
        )

        return response