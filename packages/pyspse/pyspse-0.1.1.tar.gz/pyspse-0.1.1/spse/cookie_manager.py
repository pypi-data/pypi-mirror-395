"""
SPSE Cookie Manager
Handles cookie retrieval and session management for SPSE
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from .config import (
    SPSE_BASE_URL,
    SPSE_HEADERS,
    SPSE_DEFAULT_COOKIES,
    RETRY_CONFIG,
    REQUEST_TIMEOUT,
    build_paths,
    DEFAULT_CATEGORY
)


class SPSECookieManager:
    """Manages SPSE session cookies"""
    
    def __init__(self):
        self.base_url = SPSE_BASE_URL
        self.session = self._create_session()
        self.spse_session_cookie = None
    
    def _create_session(self):
        """Create session with retry strategy"""
        session = requests.Session()
        
        # Retry strategy from config
        retry = Retry(**RETRY_CONFIG)
        
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Set headers from config, allowing UA override via env var
        headers = SPSE_HEADERS.copy()
        user_agent_override = os.getenv("SPSE_USER_AGENT")
        if user_agent_override:
            headers["User-Agent"] = user_agent_override
        session.headers.update(headers)
        
        # Set any default cookies if provided
        if SPSE_DEFAULT_COOKIES:
            session.cookies.update(SPSE_DEFAULT_COOKIES)
        
        return session
    
    def get_spse_session_cookie(self, endpoint_type='tender', category=None):
        """
        Request to SPSE page to get SPSE_SESSION cookie
        
        Args:
            endpoint_type: The endpoint type to request (default: 'tender')
                          Can be 'tender' or 'nontender'
        
        Returns:
            bool: True if cookie was successfully obtained, False otherwise
        """
        paths = build_paths(category or DEFAULT_CATEGORY)
        endpoint_map = {
            'tender': paths["tender_path"],
            'nontender': paths["nontender_path"],
        }
        endpoint = endpoint_map.get(endpoint_type, paths["tender_path"])
        
        try:
            url = f"{self.base_url}{endpoint}"
            print(f"Requesting: {url}")
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            
            # Check if request was successful
            response.raise_for_status()
            
            # Get SPSE_SESSION cookie
            if 'SPSE_SESSION' in self.session.cookies:
                self.spse_session_cookie = self.session.cookies['SPSE_SESSION']
                return True
            else:
                print("✗ SPSE_SESSION cookie not found")
                print(f"Available cookies: {list(self.session.cookies.keys())}")
                return False
                
        except requests.exceptions.RequestException:
            return False
    
    def get_cookies(self):
        """Get all cookies from session"""
        return dict(self.session.cookies)
    
    def is_spse_session_set(self):
        """Check if SPSE_SESSION cookie is set"""
        return self.spse_session_cookie is not None
    
    def get_session(self):
        """Get the requests session object"""
        return self.session
