from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HTMLFetcher:
    """Handles HTTP requests with retry logic and proper error handling."""
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.timeout = timeout
    
    def fetch(self, url: str) -> Optional[str]:
        """Fetch HTML content from URL with error handling."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
