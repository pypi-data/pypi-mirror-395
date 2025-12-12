import requests
import time
import logging
from typing import Optional
from requests.exceptions import ConnectionError

# Create a library-specific logger
logger = logging.getLogger("hybrid_edge")
logging.basicConfig(level=logging.INFO) # Default to showing info

class HybridLLM:
    """
    A Python Client for connecting to a Hybrid Edge AI Node.
    """
    def __init__(self, username: str, gist_id: str, secret_key: str) -> None:
        self.username = username
        self.gist_id = gist_id
        self.secret_key = secret_key
        self.base_url: Optional[str] = None
        
        # Auto-discover URL
        self.refresh_connection()

    def refresh_connection(self) -> None:
        """Fetches the latest URL from the Gist Phonebook."""
        gist_url = f"https://gist.githubusercontent.com/{self.username}/{self.gist_id}/raw/tunnel.json"
        
        try:
            r = requests.get(f"{gist_url}?t={time.time()}", timeout=10)
            r.raise_for_status()
            data = r.json()
            self.base_url = data.get('url')
            
            if not self.base_url:
                logger.warning("Gist Phonebook is empty.")
            else:
                logger.info(f"Connected to Hybrid Edge Node: {self.base_url}")
            
        except Exception as e:
            logger.error(f"Service Discovery Failed: {e}")
            self.base_url = None

    def generate(self, prompt: str, model: str = "llama3.2") -> str:
        """
        Sends a prompt to the Edge Node.
        """
        if not self.base_url:
            self.refresh_connection()
            if not self.base_url:
                return "Error: Could not find Edge Node URL."

        api_endpoint = f"{self.base_url}/api/generate"

        try:
            response = requests.post(
                api_endpoint,
                json={"model": model, "prompt": prompt, "stream": False},
                headers={"Authorization": f"Bearer {self.secret_key}"},
                timeout=60
            )

            if response.status_code == 200:
                return response.json().get('response', "Error: Empty response")
            elif response.status_code == 403:
                return "Error: Invalid Secret Key (403)"
            elif response.status_code in [530, 502, 503]:
                logger.warning("Tunnel unstable. Refreshing connection...")
                self.refresh_connection()
                return "Error: Tunnel connection died. Try again."
            else:
                return f"Error {response.status_code}: {response.text}"

        except ConnectionError:
            return "Error: Connection Refused (Tunnel Down)"
        except Exception as e:
            return f"Error: {str(e)}"