import os
from typing import Optional
import uac_api


class UacConnectionError(Exception): 
    """Custom error when connection or configuration fails."""
    pass


class UacClient:
    """
    Responsible for:
    - Reading UAC_URL and UAC_TOKEN from environment variables.
    - Creating a uac_api.UniversalController client.
    """

    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        self.base_url = base_url or os.getenv("UAC_URL") # UAC server URL
        self.token = token or os.getenv("UAC_TOKEN") # UAC API token

        if not self.base_url or not self.token:
            raise UacConnectionError("Missing UAC_URL or UAC_TOKEN environment variables.") # UAC connection error

        try: # Initialize the UAC API client
            self.client = uac_api.UniversalController(
                self.base_url,
                token=self.token,
                log_level="INFO",
            )
        except Exception as ex: # Handle initialization errors
            raise UacConnectionError(f"Failed to connect to UAC: {ex}")

    def get_client(self): # Return the underlying uac_api client
        """
        Return the underlying uac_api client so services can call UAC APIs.
        """
        return self.client
