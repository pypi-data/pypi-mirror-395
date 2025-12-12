"""
Async API Connector using httpx.AsyncClient with bounded concurrency.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx

from apilinker.core.connector import EndpointConfig
from apilinker.core.error_handling import ApiLinkerError, ErrorCategory
from apilinker.core.validation import (
    is_validator_available,
    pretty_print_diffs,
    validate_payload_against_schema,
)

logger = logging.getLogger(__name__)


class AsyncApiConnector:
    """
    Asynchronous API connector that mirrors the sync connector API.

    Supports bounded concurrency for sending batched payloads.
    """

    def __init__(
        self,
        connector_type: str,
        base_url: str,
        endpoints: Optional[Dict[str, Dict[str, Any]]] = None,
        timeout: int = 30,
        default_headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        self.connector_type = connector_type
        self.base_url = base_url
        self.timeout = timeout

        # Default headers (may be provided via explicit parameter or legacy 'headers' kwarg)
        if default_headers is None and "headers" in kwargs:
            try:
                default_headers = dict(kwargs.pop("headers"))
            except Exception:
                default_headers = None
        self.default_headers: Dict[str, str] = default_headers or {}
        self.headers: Dict[str, str] = self.default_headers

        # Parse and store endpoint configurations
        self.endpoints: Dict[str, EndpointConfig] = {}
        if endpoints:
            for name, config in endpoints.items():
                self.endpoints[name] = EndpointConfig(**config)

        self.settings: Dict[str, Any] = kwargs

        # Async HTTP client with increased limits for concurrency
        limits = httpx.Limits(max_connections=512, max_keepalive_connections=128)
        self.client = httpx.AsyncClient(
            base_url=self.base_url, timeout=self.timeout, limits=limits
        )

        logger.debug(f"Initialized async {connector_type} connector for {base_url}")

    async def aclose(self) -> None:
        await self.client.aclose()

    def _prepare_request(
        self, endpoint_name: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint '{endpoint_name}' not found in configuration")

        endpoint = self.endpoints[endpoint_name]

        # Combine params from endpoint config and provided params
        request_params = endpoint.params.copy()
        if params:
            request_params.update(params)

        # Prepare headers (merge default headers and endpoint-specific headers)
        headers = {**(self.default_headers or {}), **endpoint.headers}

        request: Dict[str, Any] = {
            "url": endpoint.path,
            "method": endpoint.method,
            "headers": headers,
            "params": request_params,
        }
        if endpoint.body_template:
            request["json"] = endpoint.body_template
        return request

    def _process_response(
        self, response: httpx.Response, endpoint_name: str
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        response.raise_for_status()
        data: Any = response.json()

        # Extract data from response path if configured
        endpoint = self.endpoints[endpoint_name]
        if endpoint.response_path and isinstance(data, dict):
            path_parts = endpoint.response_path.split(".")
            current_data: Any = data
            for part in path_parts:
                if isinstance(current_data, dict) and part in current_data:
                    current_data = current_data[part]
                else:
                    logger.warning(
                        f"Response path '{endpoint.response_path}' not found in response"
                    )
                    break
            if current_data is not data:
                data = current_data

        # Validate against response schema if provided
        endpoint = self.endpoints[endpoint_name]
        if endpoint.response_schema and is_validator_available():
            valid, diffs = validate_payload_against_schema(
                data, endpoint.response_schema
            )
            if not valid:
                logger.warning(
                    "Response schema validation failed for %s\n%s",
                    endpoint_name,
                    pretty_print_diffs(diffs),
                )

        if isinstance(data, (dict, list)):
            return data
        return {"value": data}

    async def fetch_data(
        self, endpoint_name: str, params: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint '{endpoint_name}' not found in configuration")

        endpoint = self.endpoints[endpoint_name]
        logger.info(
            f"[async] Fetching data from endpoint: {endpoint_name} ({endpoint.method} {endpoint.path})"
        )

        request = self._prepare_request(endpoint_name, params)
        try:
            response = await self.client.request(
                request["method"],
                request["url"],
                headers=request["headers"],
                params=request["params"],
                json=request.get("json"),
            )
            result = self._process_response(response, endpoint_name)
            return result
        except Exception as e:
            error_category, status_code = self._categorize_error(e)
            response_body = None
            if hasattr(e, "response"):
                try:
                    response_body = e.response.text[:1000]
                except Exception:
                    response_body = "<Unable to read response body>"
            raise ApiLinkerError(
                message=f"Failed to fetch data from {endpoint_name}: {str(e)}",
                error_category=error_category,
                status_code=status_code,
                response_body=response_body,
                request_url=str(request["url"]),
                request_method=request["method"],
                additional_context={"endpoint": endpoint_name, "params": params},
            )

    async def send_data(
        self,
        endpoint_name: str,
        data: Union[Dict[str, Any], List[Dict[str, Any]]],
        concurrency_limit: int = 10,
        batch_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint '{endpoint_name}' not found in configuration")

        endpoint = self.endpoints[endpoint_name]
        logger.info(
            f"[async] Sending data to endpoint: {endpoint_name} ({endpoint.method} {endpoint.path})"
        )

        request = self._prepare_request(endpoint_name)

        # Validate request schema if provided
        if endpoint.request_schema and is_validator_available():

            def _validate_item(item: Any) -> None:
                valid, diffs = validate_payload_against_schema(
                    item, endpoint.request_schema
                )
                if not valid:
                    logger.error(
                        "Request schema validation failed for %s\n%s",
                        endpoint_name,
                        pretty_print_diffs(diffs),
                    )
                    raise ApiLinkerError(
                        message="Request failed schema validation",
                        error_category=ErrorCategory.VALIDATION,
                        status_code=0,
                        additional_context={"endpoint": endpoint_name, "diffs": diffs},
                    )

            if isinstance(data, list):
                for item in data:
                    _validate_item(item)
            else:
                _validate_item(data)

        if not isinstance(data, list) or (batch_size and batch_size <= 1):
            try:
                response = await self.client.request(
                    request["method"],
                    request["url"],
                    headers=request["headers"],
                    params=request["params"],
                    json=data if not isinstance(data, list) else data[:1][0],
                )
                response.raise_for_status()
                result = response.json() if response.content else {}
                return {"success": True, "result": result}
            except Exception as e:
                error_category, status_code = self._categorize_error(e)
                response_body = None
                if hasattr(e, "response"):
                    try:
                        response_body = e.response.text[:1000]
                    except Exception:
                        response_body = "<Unable to read response body>"
                raise ApiLinkerError(
                    message=f"Failed to send data to {endpoint_name}: {str(e)}",
                    error_category=error_category,
                    status_code=status_code,
                    response_body=response_body,
                    request_url=str(request["url"]),
                    request_method=request["method"],
                    additional_context={"endpoint": endpoint_name},
                )

        # Batched list with bounded concurrency
        semaphore = asyncio.Semaphore(max(1, int(concurrency_limit)))
        results: List[Dict[str, Any]] = []
        failures: List[Dict[str, Any]] = []

        async def _send_one(item_index: int, item: Any) -> None:
            async with semaphore:
                try:
                    response = await self.client.request(
                        request["method"],
                        request["url"],
                        headers=request["headers"],
                        params=request["params"],
                        json=item,
                    )
                    response.raise_for_status()
                    result = response.json() if response.content else {}
                    results.append(result)
                except Exception as e:
                    error_category, status_code = self._categorize_error(e)
                    response_body = None
                    if hasattr(e, "response"):
                        try:
                            response_body = e.response.text[:1000]
                        except Exception:
                            response_body = "<Unable to read response body>"
                    error = ApiLinkerError(
                        message=f"Failed to send data item {item_index} to {endpoint_name}: {str(e)}",
                        error_category=error_category,
                        status_code=status_code,
                        response_body=response_body,
                        request_url=str(request["url"]),
                        request_method=request["method"],
                        additional_context={
                            "endpoint": endpoint_name,
                            "item_index": item_index,
                        },
                    )
                    failures.append(error.to_dict())
                    logger.error(f"Error sending data item {item_index}: {error}")

        async def _send_chunk(chunk_index: int, chunk: List[Any]) -> None:
            async with semaphore:
                try:
                    response = await self.client.request(
                        request["method"],
                        request["url"],
                        headers=request["headers"],
                        params=request["params"],
                        json=chunk,
                    )
                    response.raise_for_status()
                    result = response.json() if response.content else {}
                    results.append(result)
                except Exception as e:
                    error_category, status_code = self._categorize_error(e)
                    response_body = None
                    if hasattr(e, "response"):
                        try:
                            response_body = e.response.text[:1000]
                        except Exception:
                            response_body = "<Unable to read response body>"
                    error = ApiLinkerError(
                        message=f"Failed to send batch {chunk_index} (size={len(chunk)}) to {endpoint_name}: {str(e)}",
                        error_category=error_category,
                        status_code=status_code,
                        response_body=response_body,
                        request_url=str(request["url"]),
                        request_method=request["method"],
                        additional_context={
                            "endpoint": endpoint_name,
                            "batch_size": len(chunk),
                        },
                    )
                    failures.append(error.to_dict())
                    logger.error(f"Error sending batch {chunk_index}: {error}")

        # Use a task pool to avoid overwhelming the event loop with too many tasks
        tasks: List[asyncio.Task] = []
        if batch_size and batch_size > 1:
            chunk_index = 0
            for i in range(0, len(data), batch_size):
                chunk = data[i : i + batch_size]
                tasks.append(asyncio.create_task(_send_chunk(chunk_index, chunk)))
                chunk_index += 1
                if len(tasks) >= concurrency_limit * 5:
                    await asyncio.gather(*tasks)
                    tasks.clear()
            if tasks:
                await asyncio.gather(*tasks)
            successful = len(results) * (batch_size or 1)
        else:
            for i, item in enumerate(data):
                tasks.append(asyncio.create_task(_send_one(i, item)))
                if len(tasks) >= concurrency_limit * 5:
                    await asyncio.gather(*tasks)
                    tasks.clear()
            if tasks:
                await asyncio.gather(*tasks)
            successful = len(results)
        failed = len(failures)
        return {
            "success": successful > 0 and failed == 0,
            "sent_count": successful,
            "failed_count": failed,
            "results": results,
            "failures": failures,
        }

    def _categorize_error(self, exc: Exception) -> Tuple[ErrorCategory, int]:
        category = ErrorCategory.UNKNOWN
        status_code = None
        if isinstance(exc, httpx.TimeoutException):
            category = ErrorCategory.TIMEOUT
            status_code = 0
        elif isinstance(exc, httpx.TransportError) or isinstance(
            exc, httpx.RequestError
        ):
            category = ErrorCategory.NETWORK
            status_code = 0
        elif isinstance(exc, httpx.HTTPStatusError):
            status_code = exc.response.status_code
            if status_code == 401 or status_code == 403:
                category = ErrorCategory.AUTHENTICATION
            elif status_code == 422 or status_code == 400:
                category = ErrorCategory.VALIDATION
            elif status_code == 429:
                category = ErrorCategory.RATE_LIMIT
            elif status_code >= 500:
                category = ErrorCategory.SERVER
            elif status_code >= 400:
                category = ErrorCategory.CLIENT
        return category, status_code
