"""
API Key Validation for CAILculator MCP
Communicates with hosted auth server to validate subscriptions
"""

import httpx
import logging
from typing import Tuple

from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def validate_api_key(api_key: str) -> Tuple[bool, str]:
    """
    Validate API key against CAILculator auth server.

    Args:
        api_key: User's API key from environment

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    # Development mode: accept keys starting with "dev_"
    if settings.enable_dev_mode and api_key.startswith("dev_"):
        logger.info("Development mode: API key accepted")
        return True, ""

    # Production: validate with auth server
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                settings.auth_endpoint,
                json={"api_key": api_key},
                headers={"User-Agent": "CAILculator-MCP/0.1.0"}
            )

            if response.status_code == 200:
                data = response.json()

                if data.get("valid", False):
                    # Log usage info
                    usage = data.get("usage", "?")
                    limit = data.get("limit", "?")
                    logger.info(f"API key valid. Usage: {usage}/{limit}")
                    return True, ""
                else:
                    error = data.get("error", "Unknown error")
                    logger.warning(f"API key invalid: {error}")
                    return False, error
            else:
                logger.error(f"Auth server returned {response.status_code}")
                # Fallback to offline mode if server is having issues (5xx errors)
                if response.status_code >= 500 and settings.enable_offline_fallback:
                    logger.warning(f"Auth server error {response.status_code}, falling back to offline mode")
                    return True, ""
                return False, f"Auth server error (HTTP {response.status_code})"

    except httpx.TimeoutException:
        logger.error("Auth request timed out")
        # Fail open in development to avoid blocking users if server is down
        if settings.enable_offline_fallback:
            logger.warning("Falling back to offline mode due to timeout")
            return True, ""
        return False, "Auth server timeout"

    except httpx.RequestError as e:
        logger.error(f"Auth request failed: {e}")
        if settings.enable_offline_fallback:
            logger.warning("Falling back to offline mode due to connection error")
            return True, ""
        return False, f"Cannot reach auth server: {str(e)}"

    except Exception as e:
        logger.error(f"Unexpected auth error: {e}")
        return False, f"Validation error: {str(e)}"
