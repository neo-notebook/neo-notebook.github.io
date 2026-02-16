"""Safe HTTP client with timeouts and retries."""

import time
from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .logger import get_logger

logger = get_logger(__name__)


class SafeHTTPClient:
    """HTTP client with safety features (timeout, retries, user-agent)."""

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """
        Initialize HTTP client.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries on failure
        """
        self.timeout = timeout
        self.headers = {
            "User-Agent": "AI-Security-Intelligence-Bot/1.0 (Educational; +https://github.com/USERNAME/neo-notebook.github.io)"
        }

        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def fetch(self, url: str, headers: Optional[dict] = None) -> requests.Response:
        """
        Fetch URL with timeout and retries.

        Args:
            url: URL to fetch
            headers: Additional headers (optional)

        Returns:
            Response object

        Raises:
            requests.RequestException: On fetch failure
        """
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)

        logger.debug(f"Fetching: {url}")
        response = self.session.get(
            url,
            headers=request_headers,
            timeout=self.timeout,
            verify=True  # SSL verification
        )
        response.raise_for_status()

        return response
