"""Main client class for the SDK."""

from myosdk.assets import Assets
from myosdk.characters import Characters
from myosdk.http import HTTPClient
from myosdk.jobs import Jobs


class Client:
    """Main client for interacting with the MyoSapiens API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://v2m-alb-us-east-1.myolab.ai",
        timeout: float = 30.0,
    ):
        """Initialize the client.

        Args:
            api_key: API key for authentication
            base_url: Base URL of the API (default: https://v2m-alb-us-east-1.myolab.ai)
            timeout: Request timeout in seconds (default: 30.0)
        """
        self._http = HTTPClient(api_key=api_key, base_url=base_url, timeout=timeout)
        self._assets = Assets(self._http)
        self._jobs = Jobs(self._http)
        self._characters = Characters(self._http)

    @property
    def assets(self) -> Assets:
        """Access the assets resource."""
        return self._assets

    @property
    def jobs(self) -> Jobs:
        """Access the jobs resource."""
        return self._jobs

    @property
    def characters(self) -> Characters:
        """Access the characters catalog."""
        return self._characters

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._http.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
