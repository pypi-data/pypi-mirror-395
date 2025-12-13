import asyncio
import time
import jwt
from functools import wraps
from typing import Any, Callable, Dict, Optional, List
from fastapi import Request
from .logger import MongoLogger


def _extract_jwt_user_info(request: Request, jwt_secret: Optional[str] = None, jwt_algorithms: list = ["HS256"]) -> Optional[Dict]:
    """
    Extract and decode JWT token from Authorization header.

    Args:
        request: FastAPI Request object
        jwt_secret: Secret key to verify the token. If None, token is decoded without verification.
        jwt_algorithms: List of algorithms to use for decoding

    Returns:
        Decoded token payload or None if no valid token found
    """
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header[7:]  # Remove "Bearer " prefix

        if jwt_secret:
            # Verify and decode the token
            decoded = jwt.decode(token, jwt_secret, algorithms=jwt_algorithms)
        else:
            # Decode without verification (useful when verification is done elsewhere)
            decoded = jwt.decode(token, options={"verify_signature": False})

        return decoded
    except jwt.ExpiredSignatureError:
        return {"jwt_error": "Token expired"}
    except jwt.InvalidTokenError as e:
        return {"jwt_error": f"Invalid token: {str(e)}"}
    except Exception:
        return None


def _find_request_in_args(args, kwargs) -> Optional[Request]:
    """Find FastAPI Request object in function arguments."""
    # Check kwargs first
    if "request" in kwargs and isinstance(kwargs["request"], Request):
        return kwargs["request"]

    # Check positional args
    for arg in args:
        if isinstance(arg, Request):
            return arg

    return None


def _extract_request_metadata(request: Request) -> Dict[str, Any]:
    """Extract useful metadata from the request object."""
    return {
        "endpoint": str(request.url.path),
        "method": request.method,
        "full_url": str(request.url),
        "query_params": dict(request.query_params) if request.query_params else None,
        "client_ip": request.client.host if request.client else None,
    }


def log_endpoint(logger: MongoLogger, jwt_secret: Optional[str] = None, jwt_algorithms: list = ["HS256"], **log_kwargs):
    """
    Decorator to log endpoint/function calls with optional JWT user extraction.

    Args:
        logger: MongoLogger instance
        jwt_secret: Secret key to verify JWT. If None, decodes without verification.
        jwt_algorithms: List of algorithms for JWT decoding (default: ["HS256"])
        **log_kwargs: Additional fields to include in every log entry
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()

            # Extract request info and JWT user if Request is available
            user_info = None
            request_metadata = {}
            request = _find_request_in_args(args, kwargs)
            if request:
                user_info = _extract_jwt_user_info(request, jwt_secret, jwt_algorithms)
                request_metadata = _extract_request_metadata(request)

            try:
                result = await func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000

                log_data = {
                    "function_name": func.__name__,
                    "success": True,
                    "response_time_ms": response_time,
                    **log_kwargs
                }
                # Add request metadata at the top level
                log_data.update(request_metadata)
                if user_info:
                    log_data["authenticated_user"] = user_info

                await logger.log_custom("function_call", log_data)
                return result
            except Exception as e:
                response_time = (time.time() - start_time) * 1000

                log_data = {
                    "function_name": func.__name__,
                    "success": False,
                    "error": str(e),
                    "response_time_ms": response_time,
                    **log_kwargs
                }
                # Add request metadata at the top level
                log_data.update(request_metadata)
                if user_info:
                    log_data["authenticated_user"] = user_info

                await logger.log_custom("function_call", log_data)
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()

            # Extract request info and JWT user if Request is available
            user_info = None
            request_metadata = {}
            request = _find_request_in_args(args, kwargs)
            if request:
                user_info = _extract_jwt_user_info(request, jwt_secret, jwt_algorithms)
                request_metadata = _extract_request_metadata(request)

            try:
                result = func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000

                log_data = {
                    "function_name": func.__name__,
                    "success": True,
                    "response_time_ms": response_time,
                    **log_kwargs
                }
                # Add request metadata at the top level
                log_data.update(request_metadata)
                if user_info:
                    log_data["authenticated_user"] = user_info

                asyncio.create_task(logger.log_custom("function_call", log_data))
                return result
            except Exception as e:
                response_time = (time.time() - start_time) * 1000

                log_data = {
                    "function_name": func.__name__,
                    "success": False,
                    "error": str(e),
                    "response_time_ms": response_time,
                    **log_kwargs
                }
                # Add request metadata at the top level
                log_data.update(request_metadata)
                if user_info:
                    log_data["authenticated_user"] = user_info

                asyncio.create_task(logger.log_custom("function_call", log_data))
                raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator


def log_function(logger: MongoLogger, event_type: str = "custom_event", **log_kwargs):
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000
                
                await logger.log_custom(event_type, {
                    "function_name": func.__name__,
                    "success": True,
                    "response_time_ms": response_time,
                    **log_kwargs
                })
                return result
            except Exception as e:
                response_time = (time.time() - start_time) * 1000
                await logger.log_custom(event_type, {
                    "function_name": func.__name__,
                    "success": False,
                    "error": str(e),
                    "response_time_ms": response_time,
                    **log_kwargs
                })
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                response_time = (time.time() - start_time) * 1000
                
                asyncio.create_task(logger.log_custom(event_type, {
                    "function_name": func.__name__,
                    "success": True,
                    "response_time_ms": response_time,
                    **log_kwargs
                }))
                return result
            except Exception as e:
                response_time = (time.time() - start_time) * 1000
                asyncio.create_task(logger.log_custom(event_type, {
                    "function_name": func.__name__,
                    "success": False,
                    "error": str(e),
                    "response_time_ms": response_time,
                    **log_kwargs
                }))
                raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator