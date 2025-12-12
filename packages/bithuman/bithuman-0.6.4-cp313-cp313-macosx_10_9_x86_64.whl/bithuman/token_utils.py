"""Token utilities for BithumanRuntime."""
from __future__ import annotations

import asyncio
import datetime
import threading
import time
from typing import Any, Callable, Dict, Optional, Union

import aiohttp
import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from bithuman.token_config import (
    TokenRequestConfig,
    TokenRequestError,
    prepare_headers,
    prepare_request_data,
)


def _prepare_session() -> requests.Session:
    """Prepare requests session with retry capability."""
    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


# log_request_debug is now imported from token_config


def _parse_response(
    response_data: Dict[str, Any], status_code: int, response_text: str
) -> str:
    """Parse the response data and extract the token.

    Args:
        response_data: The parsed JSON response data
        status_code: The HTTP status code
        response_text: The raw response text

    Returns:
        str: The extracted token

    Raises:
        TokenRequestError: If the response is invalid or contains an error
    """
    if status_code == 200:
        if response_data.get("status") == "success" and "data" in response_data:
            token = response_data["data"]["token"]
            logger.debug("Successfully obtained token from API")
            return token
        else:
            error_msg = f"API returned error: {response_data}"
            logger.error(error_msg)
            raise TokenRequestError(error_msg, status_code, response_text, "API_ERROR")
    elif status_code == 402:
        # 402 Payment Required - quota exceeded or payment needed
        error_msg = f"Payment Required (402): {response_data.get('message', response_text) if isinstance(response_data, dict) else response_text}"
        logger.error(error_msg)
        logger.error("402 Payment Required: Your quota has been exceeded or payment is required. Please check your account status or upgrade your plan.")
        raise TokenRequestError(error_msg, status_code, response_text, "PAYMENT_REQUIRED")
    elif status_code == 401:
        # 401 Unauthorized - invalid API secret
        error_msg = f"Unauthorized (401): {response_data.get('message', response_text) if isinstance(response_data, dict) else response_text}"
        logger.error(error_msg)
        logger.error("401 Unauthorized: Invalid API secret. Please check your BITHUMAN_API_SECRET configuration.")
        raise TokenRequestError(error_msg, status_code, response_text, "UNAUTHORIZED")
    elif status_code == 403:
        # 403 Forbidden - access denied
        error_msg = f"Forbidden (403): {response_data.get('message', response_text) if isinstance(response_data, dict) else response_text}"
        logger.error(error_msg)
        logger.error("403 Forbidden: Access denied. Please check your API permissions and account status.")
        raise TokenRequestError(error_msg, status_code, response_text, "FORBIDDEN")
    else:
        error_msg = f"Failed to get token. Status code: {status_code}, Response: {response_text}"
        logger.error(error_msg)
        # Infer error type from status code
        error_type = None
        if status_code:
            error_type_map = {
                400: "BAD_REQUEST",
                404: "NOT_FOUND",
                429: "RATE_LIMIT_EXCEEDED",
                500: "INTERNAL_SERVER_ERROR",
                502: "BAD_GATEWAY",
                503: "SERVICE_UNAVAILABLE",
                504: "GATEWAY_TIMEOUT",
            }
            error_type = error_type_map.get(status_code, f"HTTP_{status_code}")
        raise TokenRequestError(error_msg, status_code, response_text, error_type)


def _handle_request_error(e: Exception) -> None:
    """Handle different types of request errors.

    Args:
        e: The exception that occurred

    Raises:
        TokenRequestError: With appropriate error message
    """
    if isinstance(e, requests.exceptions.SSLError):
        error_msg = f"SSL Error requesting token: {e}"
        logger.error(error_msg)
        logger.error(
            "This might be fixed by using the --insecure flag if your environment has SSL issues."
        )
        raise TokenRequestError(error_msg, None, None, "SSL_ERROR")
    elif isinstance(e, requests.exceptions.ConnectionError):
        error_msg = f"Connection Error requesting token: {e}"
        logger.error(error_msg)
        logger.error("Please check your network connection and the API URL.")
        raise TokenRequestError(error_msg, None, None, "CONNECTION_ERROR")
    elif isinstance(e, requests.exceptions.Timeout):
        error_msg = f"Timeout Error requesting token: {e}"
        logger.error(error_msg)
        logger.error("The API server took too long to respond.")
        raise TokenRequestError(error_msg, None, None, "TIMEOUT_ERROR")
    elif isinstance(e, requests.exceptions.HTTPError):
        # Handle HTTP status code errors
        status_code = getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        error_type = None
        if status_code in [429, 500, 502, 503, 504]:
            error_msg = f"HTTP {status_code} Error requesting token: {e}"
            logger.error(error_msg)
            if status_code == 502:
                error_type = "BAD_GATEWAY"
                logger.error("502 Bad Gateway: The API server is temporarily unavailable or overloaded.")
            elif status_code == 503:
                error_type = "SERVICE_UNAVAILABLE"
                logger.error("503 Service Unavailable: The API service is temporarily down.")
            elif status_code == 504:
                error_type = "GATEWAY_TIMEOUT"
                logger.error("504 Gateway Timeout: The API gateway timed out waiting for a response.")
            elif status_code == 429:
                error_type = "RATE_LIMIT_EXCEEDED"
                logger.error("429 Too Many Requests: Rate limit exceeded. Please try again later.")
            elif status_code == 500:
                error_type = "INTERNAL_SERVER_ERROR"
                logger.error("500 Internal Server Error: The API server encountered an error.")
        elif status_code == 402:
            error_type = "PAYMENT_REQUIRED"
            error_msg = f"HTTP 402 Payment Required requesting token: {e}"
            logger.error(error_msg)
            logger.error("402 Payment Required: Your quota has been exceeded or payment is required. Please check your account status or upgrade your plan.")
        elif status_code == 401:
            error_type = "UNAUTHORIZED"
            error_msg = f"HTTP 401 Unauthorized requesting token: {e}"
            logger.error(error_msg)
            logger.error("401 Unauthorized: Invalid API secret. Please check your BITHUMAN_API_SECRET configuration.")
        elif status_code == 403:
            error_type = "FORBIDDEN"
            error_msg = f"HTTP 403 Forbidden requesting token: {e}"
            logger.error(error_msg)
            logger.error("403 Forbidden: Access denied. Please check your API permissions and account status.")
        else:
            error_msg = f"HTTP Error requesting token (status {status_code}): {e}"
            logger.error(error_msg)
        
        # Extract response text if available
        response_text = None
        if hasattr(e, 'response') and e.response is not None:
            try:
                response_text = e.response.text
            except Exception:
                pass
        
        raise TokenRequestError(error_msg, status_code, response_text, error_type)
    else:
        error_msg = f"Error requesting token: {e}"
        logger.error(error_msg)
        logger.error(f"Exception type: {type(e)}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        raise TokenRequestError(error_msg, None, None, "UNKNOWN_ERROR")


def _prepare_request(
    fingerprint: str,
    config: Union[TokenRequestConfig, Any],
    model_hash: Optional[str] = None,
) -> tuple[Dict[str, Any], Dict[str, str]]:
    """Prepare request data and headers for token request.

    Args:
        fingerprint: The hardware fingerprint string
        config: The TokenRequestConfig for token requests or argparse.Namespace object
        model_hash: Optional model hash string (if already calculated)

    Returns:
        tuple[Dict[str, Any], Dict[str, str]]: A tuple containing (request_data, headers)
    """
    logger.debug("Preparing token request data and headers")
    
    # Convert namespace to TokenRequestConfig if needed
    if not isinstance(config, TokenRequestConfig):
        logger.debug("Converting namespace to TokenRequestConfig")
        config = TokenRequestConfig.from_namespace(config)

    # Set model hash if provided
    if model_hash:
        config.runtime_model_hash = model_hash
        logger.debug(f"Model hash set in config: {model_hash[:5]}...{model_hash[-5:] if len(model_hash) > 10 else '***'}")

    # Log config details (with masking)
    logger.debug(f"API URL: {config.api_url}")
    logger.debug(f"API secret: {config.api_secret[:5]}...{config.api_secret[-5:] if len(config.api_secret) > 10 else '***'}")
    logger.debug(f"Fingerprint: {fingerprint[:5]}...{fingerprint[-5:] if len(fingerprint) > 10 else '***'}")
    logger.debug(f"Runtime model hash: {config.runtime_model_hash[:5]}...{config.runtime_model_hash[-5:] if config.runtime_model_hash and len(config.runtime_model_hash) > 10 else '***'}")
    logger.debug(f"Tags: {config.tags}")
    logger.debug(f"Insecure: {config.insecure}")
    logger.debug(f"Timeout: {config.timeout}")

    # Prepare request data
    data = prepare_request_data(fingerprint, config)
    logger.debug(f"Request data keys: {list(data.keys())}")

    # Prepare headers
    headers = prepare_headers(config)
    logger.debug(f"Request headers: {list(headers.keys())}")

    return data, headers


def request_token_sync(config: TokenRequestConfig) -> str:
    """Synchronous version of token request.

    Args:
        config: The TokenRequestConfig for token requests

    Returns:
        str: The token string if successful
    """
    try:
        # Extract fingerprint if runtime is an object
        fingerprint = config.fingerprint

        # Prepare request data and headers
        data, headers = _prepare_request(fingerprint, config, config.runtime_model_hash)

        # Create session with retry capability
        session = _prepare_session()

        # Make request
        response = session.post(
            config.api_url, json=data, headers=headers, timeout=config.timeout
        )

        # Log response details
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        logger.debug(f"Response body: {response.text}")

        # Parse response
        return _parse_response(response.json(), response.status_code, response.text)

    except Exception as e:
        _handle_request_error(e)


async def request_token_async(config: TokenRequestConfig) -> str:
    """Asynchronous version of token request.

    Args:
        config: The TokenRequestConfig for token requests

    Returns:
        str: The token string if successful
    """
    try:
        # Extract fingerprint if runtime is an object
        fingerprint = config.fingerprint

        # Prepare request data and headers
        data, headers = _prepare_request(fingerprint, config, config.runtime_model_hash)

        # Configure SSL context if needed
        ssl_context = None if not config.insecure else False

        # Make request with retry logic
        # Retryable status codes (same as sync version)
        retryable_status_codes = {429, 500, 502, 503, 504}
        
        for attempt in range(3):  # Try up to 3 times
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        config.api_url,
                        json=data,
                        headers=headers,
                        ssl=ssl_context,
                        timeout=config.timeout,
                    ) as response:
                        # Log response details
                        logger.debug(f"Response status: {response.status}")
                        logger.debug(f"Response headers: {dict(response.headers)}")
                        response_text = await response.text()
                        logger.debug(f"Response body: {response_text}")

                        # Check if status code is retryable
                        if response.status in retryable_status_codes:
                            if attempt == 2:  # Last attempt
                                # Parse and raise error on last attempt
                                try:
                                    response_data = await response.json()
                                except Exception as json_error:
                                    # If response is not JSON (e.g., HTML error page), create error response
                                    logger.warning(f"Failed to parse JSON response: {json_error}")
                                    response_data = {"error": response_text}
                                return _parse_response(
                                    response_data, response.status, response_text
                                )
                            else:
                                # Retry for retryable status codes
                                logger.warning(
                                    f"Attempt {attempt + 1} failed with status {response.status} "
                                    f"(502 Bad Gateway/503 Service Unavailable/504 Gateway Timeout), "
                                    f"retrying in {attempt + 1} seconds..."
                                )
                                await asyncio.sleep(attempt + 1)  # Exponential backoff: 1s, 2s
                                continue

                        # Parse response for non-retryable status codes or success
                        try:
                            response_data = await response.json()
                        except Exception as json_error:
                            # If response is not JSON, create error response
                            logger.warning(f"Failed to parse JSON response: {json_error}")
                            response_data = {"error": response_text}
                        return _parse_response(
                            response_data, response.status, response_text
                        )

            except aiohttp.ClientError as e:
                if attempt == 2:  # Last attempt
                    error_msg = f"Failed after 3 attempts: {e}"
                    logger.error(error_msg)
                    # Determine error type from exception
                    error_type = "CONNECTION_ERROR"
                    if "timeout" in str(e).lower():
                        error_type = "TIMEOUT_ERROR"
                    elif "ssl" in str(e).lower():
                        error_type = "SSL_ERROR"
                    raise TokenRequestError(error_msg, None, None, error_type)
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(attempt + 1)  # Exponential backoff: 1s, 2s

    except Exception as e:
        _handle_request_error(e)


async def token_refresh_worker_async(
    config: TokenRequestConfig,
    stop_event: asyncio.Event,
    refresh_interval: int = 60,
    error_retry_interval: int = 5,
    on_token_refresh: Optional[Callable[[str], None]] = None,
) -> None:
    """Asynchronous worker that periodically refreshes the token.

    This function handles periodic token refresh in an asynchronous context.
    It uses the provided config to request new tokens and calls the on_token_refresh
    callback when a new token is obtained. The worker will continue running until
    the stop_event is set.

    Args:
        config: Configuration for token requests containing API credentials and parameters.
        stop_event: Event to signal when the worker should stop.
        refresh_interval: Time in seconds between refresh attempts (default: 60).
        error_retry_interval: Time to wait after an error before retrying (default: 5).
        on_token_refresh: Callback function to process the new token when refreshed.
    """
    if not config.api_secret:
        logger.warning("No API secret provided, skipping token refresh")
        return

    if not config.runtime_model_hash:
        logger.warning("Failed to get model hash, skipping token refresh")
        return

    while not stop_event.is_set():
        try:
            # Request a new token using the config
            token = await request_token_async(config)
            if token:
                # Call the callback with the new token if provided
                if on_token_refresh:
                    on_token_refresh(token)
                logger.debug(
                    f"Token refreshed successfully at {datetime.datetime.now()}"
                )
            else:
                logger.error("Failed to refresh token: request returned empty token")

            # Wait for refresh_interval seconds before the next refresh,
            # checking for stop event every second
            for _ in range(refresh_interval):
                if stop_event.is_set():
                    break
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Error in token refresh worker: {e}")
            # Wait a shorter interval before retrying after an error
            await asyncio.sleep(error_retry_interval)


def token_refresh_worker_sync(
    config: TokenRequestConfig,
    stop_event: threading.Event,
    refresh_interval: int = 60,
    error_retry_interval: int = 5,
    on_token_refresh: Optional[Callable[[str], None]] = None,
) -> None:
    """Synchronous worker that periodically refreshes the token.

    This function handles periodic token refresh in a synchronous context.
    It uses the provided config to request new tokens and calls the on_token_refresh
    callback when a new token is obtained. The worker will continue running until
    the stop_event is set.

    Args:
        config: Configuration for token requests containing API credentials and parameters.
        stop_event: Event to signal when the worker should stop.
        refresh_interval: Time in seconds between refresh attempts (default: 60).
        error_retry_interval: Time to wait after an error before retrying (default: 5).
        on_token_refresh: Callback function to process the new token when refreshed.
    """
    while not stop_event.is_set():
        try:
            # Request a new token using the config
            token = request_token_sync(config)
            if token:
                # Call the callback with the new token if provided
                if on_token_refresh:
                    on_token_refresh(token)
                logger.debug(
                    f"Token refreshed successfully at {datetime.datetime.now()}"
                )
            else:
                logger.error("Failed to refresh token: request returned empty token")

            # Wait for refresh_interval seconds before the next refresh,
            # checking for stop event every second
            for _ in range(refresh_interval):
                if stop_event.is_set():
                    break
                time.sleep(1)

        except Exception as e:
            logger.error(f"Error in token refresh worker: {e}")
            # Wait a shorter interval before retrying after an error
            time.sleep(error_retry_interval)
