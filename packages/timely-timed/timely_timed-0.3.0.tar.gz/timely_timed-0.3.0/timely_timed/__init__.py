"""
timely_timed - A Python package for fetching UTC time from multiple time servers with fallback logic
"""

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen


logger = logging.getLogger(__name__)


class TimeServerError(Exception):
    """Base exception for time server related errors."""

    pass


class AllServersFailedError(TimeServerError):
    """Raised when all configured time servers fail to respond."""

    pass


class TimeServerStrategy(ABC):
    """Abstract base class for time server communication strategies."""

    @abstractmethod
    def fetch_time(self, url: str, body: Optional[Dict[str, Any]] = None) -> datetime:
        """
        Fetch time from a server.

        Args:
            url: The server URL
            body: Optional request body

        Returns:
            datetime: The UTC time

        Raises:
            TimeServerError: If the request fails
        """
        pass

    @abstractmethod
    def matches(self, url: str) -> bool:
        """Check if this strategy handles the given URL."""
        pass


class PostJsonStrategy(TimeServerStrategy):
    """Strategy for POST-based JSON time servers."""

    def matches(self, url: str) -> bool:
        return "chanfana.berensmeier-mike.workers.dev" in url

    def fetch_time(self, url: str, body: Optional[Dict[str, Any]] = None) -> datetime:
        body = body or {}
        req_data = json.dumps(body).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Content-Length": str(len(req_data)),
        }

        req = Request(url, data=req_data, headers=headers, method="POST")

        with urlopen(req, timeout=5) as response:
            response_text = response.read().decode("utf-8")
            response_data = json.loads(response_text)

            if not response_data.get("success") or "result" not in response_data:
                raise TimeServerError(f"Invalid response format from {url}")

            utc_time_str = response_data["result"]["utcTime"]
            return self._parse_iso_time(utc_time_str)

    @staticmethod
    def _parse_iso_time(time_str: str) -> datetime:
        """Parse ISO format time string, handling 'Z' suffix."""
        if time_str.endswith("Z"):
            time_str = time_str[:-1] + "+00:00"
        return datetime.fromisoformat(time_str)


class AiSenseApiStrategy(TimeServerStrategy):
    """Strategy for aisenseapi.com time server."""

    def matches(self, url: str) -> bool:
        return "aisenseapi.com" in url

    def fetch_time(self, url: str, body: Optional[Dict[str, Any]] = None) -> datetime:
        req = Request(url, method="GET")

        with urlopen(req, timeout=5) as response:
            response_text = response.read().decode("utf-8")
            response_data = json.loads(response_text)

            if "datetime" not in response_data:
                raise TimeServerError(f"Invalid response format from {url}")

            utc_time_str = response_data["datetime"]
            return self._parse_iso_time(utc_time_str)

    @staticmethod
    def _parse_iso_time(time_str: str) -> datetime:
        """Parse ISO format time string, handling 'Z' suffix."""
        if time_str.endswith("Z"):
            time_str = time_str[:-1] + "+00:00"
        return datetime.fromisoformat(time_str)


class WorldClockApiStrategy(TimeServerStrategy):
    """Strategy for worldclockapi.com time server."""

    def matches(self, url: str) -> bool:
        return "worldclockapi.com" in url

    def fetch_time(self, url: str, body: Optional[Dict[str, Any]] = None) -> datetime:
        req = Request(url, method="GET")

        with urlopen(req, timeout=5) as response:
            response_text = response.read().decode("utf-8")
            response_data = json.loads(response_text)

            if "currentDateTime" not in response_data:
                raise TimeServerError(f"Invalid response format from {url}")

            utc_time_str = response_data["currentDateTime"]
            return self._parse_iso_time(utc_time_str)

    @staticmethod
    def _parse_iso_time(time_str: str) -> datetime:
        """Parse ISO format time string, handling 'Z' suffix."""
        if time_str.endswith("Z"):
            time_str = time_str[:-1] + "+00:00"
        return datetime.fromisoformat(time_str)


class TimeServerClient:
    """
    A client for fetching UTC time from multiple time servers with fallback logic.

    This client supports multiple time server formats and automatically falls back
    to alternative servers if one fails.

    Example:
        >>> client = TimeServerClient()
        >>> utc_time = client.get_utc_time()
        >>> print(utc_time)
    """

    DEFAULT_SERVERS = [
        "https://chanfana.berensmeier-mike.workers.dev/get-utc-time",
        "https://aisenseapi.com/services/v1/datetime",
        "http://worldclockapi.com/api/json/utc/now",
    ]

    DEFAULT_STRATEGIES = [
        PostJsonStrategy(),
        AiSenseApiStrategy(),
        WorldClockApiStrategy(),
    ]

    def __init__(
        self,
        custom_servers: Optional[List[str]] = None,
        custom_strategies: Optional[List[TimeServerStrategy]] = None,
        use_default_servers: bool = True,
        excluded_servers: Optional[List[str]] = None,
    ):
        """
        Initialize the client with servers and strategies.

        Args:
            custom_servers: Optional list of custom server URLs. Custom servers
                          take priority over default ones.
            custom_strategies: Optional list of custom strategies for handling
                             different server types.
            use_default_servers: If False, only use custom_servers (no defaults).
            excluded_servers: Optional list of server URLs to exclude from defaults.
                            Supports partial matching (e.g., "worldclockapi" matches
                            "http://worldclockapi.com/api/json/utc/now").
        """
        # Build server list
        default_servers = self.DEFAULT_SERVERS if use_default_servers else []

        # Filter out excluded servers
        if excluded_servers:
            default_servers = [
                server
                for server in default_servers
                if not any(excluded in server for excluded in excluded_servers)
            ]

        self.servers = (custom_servers or []) + default_servers
        self.strategies = (custom_strategies or []) + self.DEFAULT_STRATEGIES

    def remove_server(self, server_pattern: str) -> int:
        """
        Remove servers matching the given pattern.

        Args:
            server_pattern: Pattern to match against server URLs (supports partial matching)

        Returns:
            int: Number of servers removed

        Example:
            >>> client.remove_server("worldclockapi")  # Removes worldclockapi server
            >>> client.remove_server("http://worldclockapi.com/api/json/utc/now")  # Exact match
        """
        original_count = len(self.servers)
        self.servers = [
            server for server in self.servers if server_pattern not in server
        ]
        removed_count = original_count - len(self.servers)

        if removed_count > 0:
            logger.info(
                f"Removed {removed_count} server(s) matching '{server_pattern}'"
            )

        return removed_count

    def add_server(self, server_url: str, priority: bool = True) -> None:
        """
        Add a new server to the list.

        Args:
            server_url: URL of the time server to add
            priority: If True, add at the beginning (highest priority),
                     otherwise append to the end
        """
        if priority:
            self.servers.insert(0, server_url)
        else:
            self.servers.append(server_url)

    def add_strategy(self, strategy: TimeServerStrategy, priority: bool = True) -> None:
        """
        Add a new strategy for handling time servers.

        Args:
            strategy: The strategy instance to add
            priority: If True, add at the beginning (highest priority),
                     otherwise append to the end
        """
        if priority:
            self.strategies.insert(0, strategy)
        else:
            self.strategies.append(strategy)

    def get_utc_time(self, body: Optional[Dict[str, Any]] = None) -> datetime:
        """
        Fetch UTC time from time servers with automatic fallback.

        Args:
            body: Optional dictionary to send as JSON in POST requests.
                  Ignored for GET-based servers.

        Returns:
            datetime: The UTC time as a datetime object

        Raises:
            AllServersFailedError: If all time servers fail to respond with valid time
        """
        errors = []

        for server_url in self.servers:
            strategy = self._find_strategy(server_url)

            if not strategy:
                logger.warning(f"No strategy found for server: {server_url}")
                errors.append((server_url, "No matching strategy"))
                continue

            try:
                utc_time = strategy.fetch_time(server_url, body)
                logger.debug(f"Successfully fetched time from {server_url}")
                return utc_time

            except (
                URLError,
                TimeServerError,
                KeyError,
                ValueError,
                TypeError,
                OSError,
            ) as e:
                logger.warning(f"Failed to fetch time from {server_url}: {e}")
                errors.append((server_url, str(e)))
                continue

        # All servers failed
        error_details = "\n".join([f"  - {url}: {err}" for url, err in errors])
        raise AllServersFailedError(
            f"All {len(self.servers)} time servers failed to respond with valid time:\n{error_details}"
        )

    def _find_strategy(self, url: str) -> Optional[TimeServerStrategy]:
        """Find the appropriate strategy for a given URL."""
        for strategy in self.strategies:
            if strategy.matches(url):
                return strategy
        return None


def get_utc_time(
    body: Optional[Dict[str, Any]] = None,
    custom_servers: Optional[List[str]] = None,
) -> datetime:
    """
    Convenience function to get UTC time from time servers.

    Args:
        body: Optional dictionary to send as JSON in POST requests
        custom_servers: Optional list of custom server URLs

    Returns:
        datetime: The UTC time as a datetime object

    Raises:
        AllServersFailedError: If all time servers fail

    Example:
        >>> from timely_timed import get_utc_time
        >>> current_time = get_utc_time()
        >>> print(f"Current UTC time: {current_time}")
    """
    client = TimeServerClient(custom_servers=custom_servers)
    return client.get_utc_time(body)
