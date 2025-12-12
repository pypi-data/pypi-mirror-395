"""Token configuration utilities for BithumanRuntime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from loguru import logger


@dataclass
class TokenRequestConfig:
    """Configuration for token requests."""

    api_url: str
    api_secret: str
    fingerprint: Optional[str] = None
    client_id: Optional[str] = None
    figure_id: Optional[str] = None
    transaction_id: Optional[str] = None
    runtime_model_hash: Optional[str] = None
    tags: Optional[str] = None
    insecure: bool = False
    timeout: float = 30.0

    @classmethod
    def from_namespace(cls, namespace) -> "TokenRequestConfig":
        """Create a TokenRequestConfig from an argparse.Namespace object.

        Args:
            namespace: An argparse.Namespace object containing the configuration

        Returns:
            TokenRequestConfig: A new TokenRequestConfig instance
        """
        # Get required parameters
        api_url = getattr(namespace, "api_url", None)
        api_secret = getattr(namespace, "api_secret", None)

        if not api_url or not api_secret:
            raise ValueError("api_url and api_secret are required parameters")

        # Get optional parameters with defaults
        return cls(
            api_url=api_url,
            api_secret=api_secret,
            fingerprint=getattr(namespace, "fingerprint", None),
            client_id=getattr(namespace, "client_id", None),
            figure_id=getattr(namespace, "figure_id", None),
            transaction_id=getattr(namespace, "transaction_id", None),
            runtime_model_hash=getattr(namespace, "runtime_model_hash", None),
            tags=getattr(namespace, "tags", None),
            insecure=getattr(namespace, "insecure", False),
            timeout=getattr(namespace, "timeout", 30.0),
        )


def prepare_request_data(
    fingerprint: str, config: TokenRequestConfig
) -> Dict[str, Any]:
    """Prepare request data for token request."""
    data = {"fingerprint": fingerprint}

    if config.client_id:
        data["client_id"] = config.client_id

    if config.figure_id:
        data["figure_id"] = config.figure_id

    if config.runtime_model_hash:
        data["runtime_model_hash"] = config.runtime_model_hash

    if config.transaction_id:
        data["transaction_id"] = config.transaction_id

    if config.tags:
        data["tags"] = config.tags

    return data


def prepare_headers(config: TokenRequestConfig) -> Dict[str, str]:
    """Prepare headers for token request."""
    headers = {"Content-Type": "application/json"}

    if config.api_secret:
        headers["api-secret"] = config.api_secret
        logger.debug("API secret provided")
    else:
        logger.warning("No api-secret provided, authentication may fail")

    return headers


def log_request_debug(headers: Dict[str, str], data: Dict[str, Any], api_url: str):
    """Log request debug information."""
    debug_headers = headers.copy()
    if "api-secret" in debug_headers:
        secret_val = debug_headers["api-secret"]
        debug_headers["api-secret"] = (
            secret_val[:4] + "..." + secret_val[-4:] if len(secret_val) > 8 else "***"
        )

    logger.debug(f"Request headers: {debug_headers}")
    logger.debug(f"Request data: {data}")
    logger.debug(f"Using API URL: {api_url}")


class TokenRequestError(Exception):
    """Custom exception for token request errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
        error_type: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response_text = response_text
        self.error_type = error_type or self._infer_error_type(status_code)
        super().__init__(self.message)
    
    def _infer_error_type(self, status_code: Optional[int]) -> str:
        """Infer error type from status code."""
        if status_code is None:
            return "UNKNOWN_ERROR"
        
        error_type_map = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            402: "PAYMENT_REQUIRED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            429: "RATE_LIMIT_EXCEEDED",
            500: "INTERNAL_SERVER_ERROR",
            502: "BAD_GATEWAY",
            503: "SERVICE_UNAVAILABLE",
            504: "GATEWAY_TIMEOUT",
        }
        return error_type_map.get(status_code, f"HTTP_{status_code}")
    
    def __str__(self) -> str:
        """Return formatted error message."""
        parts = [f"[{self.error_type}]"]
        if self.status_code:
            parts.append(f"HTTP {self.status_code}")
        parts.append(self.message)
        if self.response_text and len(self.response_text) < 200:
            parts.append(f"(Response: {self.response_text})")
        return " ".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        return {
            "error_type": self.error_type,
            "status_code": self.status_code,
            "message": self.message,
            "response_text": self.response_text[:500] if self.response_text else None,  # Limit length
        }
