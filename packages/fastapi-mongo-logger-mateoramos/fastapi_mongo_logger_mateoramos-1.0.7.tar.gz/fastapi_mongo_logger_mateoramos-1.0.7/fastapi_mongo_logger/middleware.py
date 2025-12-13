import time
import json
import jwt
from typing import Callable, Optional, Dict, Any, List
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse
from .logger import MongoLogger


def _decode_jwt_from_header(auth_header: str, jwt_secret: Optional[str] = None, jwt_algorithms: List[str] = ["HS256"]) -> Optional[Dict]:
    """Decode JWT token from Authorization header."""
    try:
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header[7:]  # Remove "Bearer " prefix

        if jwt_secret:
            decoded = jwt.decode(token, jwt_secret, algorithms=jwt_algorithms)
        else:
            # Decode without verification
            decoded = jwt.decode(token, options={"verify_signature": False})

        return decoded
    except jwt.ExpiredSignatureError:
        return {"jwt_error": "Token expired"}
    except jwt.InvalidTokenError as e:
        return {"jwt_error": f"Invalid token: {str(e)}"}
    except Exception:
        return None


async def _parse_request_body(request: Request) -> Optional[Any]:
    """Parse request body based on content type."""
    content_type = request.headers.get("content-type", "")

    try:
        body = await request.body()
        if not body:
            return None

        # Handle JSON content
        if "application/json" in content_type:
            return json.loads(body.decode())

        # Handle form data (application/x-www-form-urlencoded)
        elif "application/x-www-form-urlencoded" in content_type:
            form_data = {}
            decoded = body.decode()
            for pair in decoded.split("&"):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    form_data[key] = value
            return {"form_data": form_data}

        # Handle multipart/form-data (file uploads)
        elif "multipart/form-data" in content_type:
            # We can't easily re-parse multipart data from raw bytes
            # Log metadata about the request instead
            return {
                "content_type": "multipart/form-data",
                "body_size_bytes": len(body),
                "note": "File upload request - body not parsed to avoid consuming stream"
            }

        # Handle plain text
        elif "text/plain" in content_type:
            return {"text": body.decode()}

        # Unknown content type - try JSON first, then raw
        else:
            try:
                return json.loads(body.decode())
            except json.JSONDecodeError:
                return {"raw_body": body.decode()[:1000]}  # Limit size

    except Exception as e:
        return {"parse_error": str(e)}


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        logger: MongoLogger,
        log_request_body: bool = True,
        log_response_body: bool = False,
        jwt_secret: Optional[str] = None,
        jwt_algorithms: List[str] = ["HS256"],
        decode_jwt: bool = True
    ):
        super().__init__(app)
        self.logger = logger
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.jwt_secret = jwt_secret
        self.jwt_algorithms = jwt_algorithms
        self.decode_jwt = decode_jwt

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()

        # Capture request data
        request_body = None
        if self.log_request_body and request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            request_body = await _parse_request_body(request)

        # Extract JWT user info if enabled
        authenticated_user = None
        if self.decode_jwt:
            auth_header = request.headers.get("authorization", "")
            authenticated_user = _decode_jwt_from_header(auth_header, self.jwt_secret, self.jwt_algorithms)

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

        # Prepare headers (exclude sensitive auth token from raw headers if JWT is decoded)
        headers = dict(request.headers)

        # Log to MongoDB
        log_kwargs = {
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "response_time": process_time,
            "request_body": request_body,
            "response_body": response_body,
            "headers": headers,
            "query_params": dict(request.query_params),
            "client_ip": request.client.host if request.client else None,
        }

        # Add authenticated user info if available
        if authenticated_user:
            log_kwargs["authenticated_user"] = authenticated_user

        await self.logger.log_endpoint(**log_kwargs)

        return response