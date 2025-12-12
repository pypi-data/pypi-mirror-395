"""
KeyNexus Client - Main SDK class
"""

import requests
import uuid
import platform
import hashlib
from typing import Optional, Dict, Any
from .exceptions import (
    KeyNexusError,
    InvalidLicenseError,
    HWIDMismatchError,
    ExpiredLicenseError,
    NetworkError
)


class KeyNexusClient:
    """
    KeyNexus Python SDK Client
    
    Example:
        client = KeyNexusClient(
            app_id="app_xxxxxxxxxxxx",
            secret_key="sk_xxxxxxxxxxxxxxxxxxxx",
            api_url="https://keynexus.es/api"
        )
        
        # Validate license
        result = client.validate_license("XXXXX-XXXXX-XXXXX-XXXXX")
        if result['success']:
            print(f"Welcome! License valid until: {result['license']['expiresAt']}")
    """
    
    def __init__(
        self,
        app_id: str,
        secret_key: str,
        api_url: str = "https://keynexus.es/api",
        auto_hwid: bool = True
    ):
        """
        Initialize KeyNexus client
        
        Args:
            app_id: Your application ID from KeyNexus dashboard
            secret_key: Your secret key (keep this secure!)
            api_url: API base URL (default: https://keynexus.es/api)
            auto_hwid: Automatically generate HWID (default: True)
        """
        self.app_id = app_id
        self.secret_key = secret_key
        self.api_url = api_url.rstrip('/')
        self.session_token = None
        self.hwid = self._generate_hwid() if auto_hwid else None
        
    def _generate_hwid(self) -> str:
        """Generate a unique hardware ID for this machine"""
        try:
            # Get machine-specific info
            machine_id = f"{platform.node()}-{platform.machine()}-{platform.system()}"
            
            # Try to get MAC address
            mac = uuid.getnode()
            machine_id += f"-{mac}"
            
            # Create hash
            hwid = hashlib.sha256(machine_id.encode()).hexdigest()
            return hwid
        except Exception:
            # Fallback to random UUID
            return str(uuid.uuid4())
    
    def _make_request(
        self,
        endpoint: str,
        data: Dict[str, Any],
        method: str = "POST"
    ) -> Dict[str, Any]:
        """Make HTTP request to KeyNexus API"""
        url = f"{self.api_url}{endpoint}"
        
        try:
            if method == "POST":
                response = requests.post(url, json=data, timeout=10)
            else:
                response = requests.get(url, params=data, timeout=10)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def initialize(self, version: str = "1.0.0") -> Dict[str, Any]:
        """
        Initialize application and verify it's active
        
        Args:
            version: Your application version
            
        Returns:
            dict: Response with application info
        """
        data = {
            "action": "init",
            "appId": self.app_id,
            "secretKey": self.secret_key,
            "version": version
        }
        
        result = self._make_request("/client", data)
        
        if not result.get("success"):
            raise KeyNexusError(result.get("message", "Initialization failed"))
        
        return result
    
    def validate_license(
        self,
        license_key: str,
        hwid: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate a license key
        
        Args:
            license_key: The license key to validate
            hwid: Hardware ID (uses auto-generated if not provided)
            
        Returns:
            dict: Validation result with license info
            
        Raises:
            InvalidLicenseError: If license is invalid
            HWIDMismatchError: If HWID doesn't match
            ExpiredLicenseError: If license has expired
        """
        data = {
            "action": "license",
            "appId": self.app_id,
            "secretKey": self.secret_key,
            "key": license_key,
            "hwid": hwid or self.hwid
        }
        
        result = self._make_request("/client", data)
        
        if not result.get("success"):
            message = result.get("message", "Unknown error")
            
            if "HWID" in message:
                raise HWIDMismatchError(message)
            elif "expirada" in message or "expired" in message.lower():
                raise ExpiredLicenseError(message)
            else:
                raise InvalidLicenseError(message)
        
        # Store session token if provided
        if "sessionToken" in result:
            self.session_token = result["sessionToken"]
        
        return result
    
    def login_with_password(
        self,
        username: str,
        password: str,
        hwid: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Login with username/password
        
        Args:
            username: User's username or email
            password: User's password
            hwid: Hardware ID (uses auto-generated if not provided)
            
        Returns:
            dict: Login result with user info and session token
        """
        data = {
            "action": "login",
            "appId": self.app_id,
            "secretKey": self.secret_key,
            "username": username,
            "password": password,
            "hwid": hwid or self.hwid
        }
        
        result = self._make_request("/client/auth", data)
        
        if not result.get("success"):
            raise KeyNexusError(result.get("message", "Login failed"))
        
        # Store session token
        if "token" in result:
            self.session_token = result["token"]
        
        return result
    
    def get_user_info(self, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current user information
        
        Args:
            token: Session token (uses stored token if not provided)
            
        Returns:
            dict: User information
        """
        headers = {
            "Authorization": f"Bearer {token or self.session_token}"
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/client/me",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if not result.get("success"):
                raise KeyNexusError(result.get("message", "Failed to get user info"))
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def logout(self) -> Dict[str, Any]:
        """
        Logout current session
        
        Returns:
            dict: Logout result
        """
        if not self.session_token:
            raise KeyNexusError("No active session")
        
        headers = {
            "Authorization": f"Bearer {self.session_token}"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/client/logout",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            # Clear session token
            self.session_token = None
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def get_sessions(self) -> Dict[str, Any]:
        """
        Get all active sessions for current user
        
        Returns:
            dict: List of sessions
        """
        if not self.session_token:
            raise KeyNexusError("No active session")
        
        headers = {
            "Authorization": f"Bearer {self.session_token}"
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/client/sessions",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def set_hwid(self, hwid: str) -> None:
        """
        Manually set the hardware ID
        
        Args:
            hwid: Hardware ID to use
        """
        self.hwid = hwid
    
    def get_hwid(self) -> str:
        """
        Get the current hardware ID
        
        Returns:
            str: Current HWID
        """
        return self.hwid or self._generate_hwid()
