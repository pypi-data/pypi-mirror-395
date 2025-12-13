"""
SemBicho CLI Auth Module
Handles authentication with SemBicho backend
"""

import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

try:
    import keyring  # type: ignore
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False
    keyring = None  # type: ignore


class _FileKeyring:
    """
    Fallback storage when system keyring is unavailable.
    Tokens are stored in plain text inside ~/.sembicho/token_store.json.
    """

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path

    def _read(self) -> Dict[str, Dict[str, str]]:
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _write(self, data: Dict[str, Dict[str, str]]):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_password(self, service: str, username: str) -> Optional[str]:
        data = self._read()
        return data.get(service, {}).get(username)

    def set_password(self, service: str, username: str, password: str):
        data = self._read()
        data.setdefault(service, {})[username] = password
        self._write(data)

    def delete_password(self, service: str, username: str):
        data = self._read()
        if service in data and username in data[service]:
            del data[service][username]
            if not data[service]:
                del data[service]
            self._write(data)

class SemBichoAuth:
    """Manages authentication for SemBicho CLI"""
    
    def __init__(self):
        self.service_name = "sembicho-cli"
        self.config_dir = Path.home() / ".sembicho"
        self.config_file = self.config_dir / "config.json"
        self.default_api_url = "https://sembichobackend.onrender.com"
        self._token_store = self.config_dir / "token_store.json"
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)

        # Select secure key storage; fall back to file if keyring is missing
        if KEYRING_AVAILABLE:
            self._keyring = keyring  # type: ignore
        else:
            self._keyring = _FileKeyring(self._token_store)
            print(
                f"Warning: 'keyring' not installed. "
                f"Using plain-text token storage at {self._token_store}"
            )
    
    def get_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"api_url": self.default_api_url}
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")
    
    def get_stored_token(self) -> Optional[str]:
        """Get stored authentication token"""
        try:
            config = self.get_config()
            username = config.get("username")
            if username:
                return self._keyring.get_password(self.service_name, username)
        except Exception:
            pass
        return None
    
    def store_token(self, username: str, token: str):
        """Store authentication token securely"""
        try:
            self._keyring.set_password(self.service_name, username, token)
            config = self.get_config()
            config["username"] = username
            config["last_login"] = datetime.now().isoformat()
            self.save_config(config)
        except Exception as e:
            print(f"Warning: Could not store token: {e}")
    
    def clear_token(self):
        """Clear stored authentication token"""
        try:
            config = self.get_config()
            username = config.get("username")
            if username:
                self._keyring.delete_password(self.service_name, username)
            
            # Clear username from config but keep api_url
            config.pop("username", None)
            config.pop("last_login", None)
            self.save_config(config)
        except Exception as e:
            print(f"Warning: Could not clear token: {e}")
    
    def login_with_token(self, token: str, api_url: Optional[str] = None) -> bool:
        """
        Login to SemBicho backend using JWT token
        Token should be obtained from the web dashboard at https://app.sembicho.com
        """
        config = self.get_config()
        base_url = api_url or config.get("api_url", self.default_api_url)
        
        try:
            # Validate token by calling /auth/me endpoint
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{base_url}/auth/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get("email", user_data.get("username", "user"))
                
                # Store valid token
                self.store_token(username, token)
                
                # Update config with API URL if provided
                if api_url and api_url != config.get("api_url"):
                    config["api_url"] = api_url
                    self.save_config(config)
                
                return True
            else:
                print(f"Warning: token validation failed (status {response.status_code})")
                if response.status_code == 401:
                    print("   Token is invalid or expired")
                    print("   Get a new token from: https://app.sembicho.com/settings/tokens")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Warning: network error during token validation: {e}")
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def logout(self) -> bool:
        """Logout from SemBicho"""
        try:
            self.clear_token()
            return True
        except Exception as e:
            print(f"Logout error: {e}")
            return False
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return self.get_stored_token() is not None
    
    def get_auth_status(self) -> Dict[str, Any]:
        """Get detailed authentication status"""
        config = self.get_config()
        token = self.get_stored_token()
        
        status = {
            "authenticated": token is not None,
            "username": config.get("username", "Not logged in"),
            "api_url": config.get("api_url", self.default_api_url),
            "last_login": config.get("last_login", "Never"),
            "config_path": str(self.config_file)
        }
        
        return status
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests"""
        token = self.get_stored_token()
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}
    
    def test_connection(self, api_url: Optional[str] = None) -> bool:
        """Test basic connection to SemBicho backend (without auth)"""
        config = self.get_config()
        base_url = api_url or config.get("api_url", self.default_api_url)
        
        try:
            response = requests.get(f"{base_url}/docs", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def test_authenticated_connection(self, api_url: Optional[str] = None) -> bool:
        """Test authenticated connection to SemBicho backend using stored token"""
        if not self.is_authenticated():
            return False
            
        config = self.get_config()
        base_url = api_url or config.get("api_url", self.default_api_url)
        headers = self.get_auth_headers()
        
        try:
            # Try to access a protected endpoint
            response = requests.get(f"{base_url}/auth/me", headers=headers, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
