"""
Onwords API Client - Connect to Onwords Gate Control API
https://ostapi.onwords.in/api-documentation
"""

import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass

# Config paths
CONFIG_DIR = Path.home() / ".onwords"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Onwords API Base URL
API_BASE_URL = "https://ostapi.onwords.in"


@dataclass
class Product:
    """Represents an Onwords product/device."""
    product_id: str
    gate_type: Optional[str] = None
    
    @classmethod
    def from_api(cls, product_id: str, gate_type: str = None) -> "Product":
        """Create Product from API response."""
        return cls(product_id=product_id, gate_type=gate_type)


class OnwordsAPI:
    """
    Onwords Gate Control API client.
    
    API Documentation: https://ostapi.onwords.in/api-documentation
    
    Usage:
        from onwords import OnwordsAPI
        
        api = OnwordsAPI("your-api-key")
        products = api.get_device_list()
        api.control_device("product_id", "open")
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or self._load_api_key()
        if not self.api_key:
            raise ValueError(
                "API key required!\n\n"
                "Get your API key from: https://ostapi.onwords.in\n"
                "Then configure it using:\n"
                "  onwords.configure('your-api-key')\n"
                "  or CLI: onwords-config --api-key YOUR_KEY"
            )
    
    def _load_api_key(self) -> Optional[str]:
        """Load API key from config file."""
        if CONFIG_FILE.exists():
            try:
                config = json.loads(CONFIG_FILE.read_text())
                return config.get("api_key")
            except (json.JSONDecodeError, IOError):
                pass
        return None
    
    def _request(self, endpoint: str, method: str = "POST", data: dict = None) -> dict:
        """Make API request to Onwords API."""
        url = f"{API_BASE_URL}/{endpoint}"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "onwords-python/0.2.0"
        }
        
        req_data = json.dumps(data).encode() if data else None
        request = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            try:
                error_json = json.loads(error_body)
                detail = error_json.get("detail", error_body)
            except json.JSONDecodeError:
                detail = error_body
                
            if e.code == 401:
                raise ValueError("Invalid API key. Please check your credentials.")
            elif e.code == 403:
                raise ValueError(f"Access denied: {detail}")
            elif e.code == 404:
                raise ValueError(f"Not found: {detail}")
            elif e.code == 400:
                raise ValueError(f"Invalid request: {detail}")
            else:
                raise ConnectionError(f"API error {e.code}: {detail}")
        except urllib.error.URLError as e:
            raise ConnectionError(f"Connection failed: {e.reason}")
    
    def get_device_list(self) -> List[str]:
        """
        Fetch all device/product IDs linked to your API key.
        
        Endpoint: POST /get_device_list
        
        Returns:
            List of product IDs
        """
        response = self._request("get_device_list")
        return response.get("product_ids", [])
    
    def control_device(self, product_id: str, action: str) -> dict:
        """
        Send control command to a device.
        
        Endpoint: POST /control-device/
        
        Supported Actions by Gate Type:
        
        Sliding Gate (3chsg):
            - open: Open the gate
            - close: Close the gate  
            - pause: Pause/stop the gate
            
        Sliding Gate Advanced (3chsgsl):
            - open: Open the gate
            - close: Close the gate
            - pause: Pause/stop the gate
            - partial_open: Pedestrian/partial opening
            
        Arm Gate (3chag):
            - open_single_gate: Open single arm
            - close_single_gate: Close single arm
            - pause_single_gate: Pause single arm
            - open_double_gate: Open both arms
            - close_double_gate: Close both arms
            - pause_double_gate: Pause both arms
        
        Args:
            product_id: Target product ID
            action: Command action
            
        Returns:
            API response with status, product_id, and gate_type
        """
        data = {
            "product_id": product_id,
            "action": action
        }
        return self._request("control-device/", method="POST", data=data)


def _ensure_config_dir():
    """Ensure config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def save_config(api_key: str = None, **kwargs):
    """Save configuration to file."""
    _ensure_config_dir()
    
    config = {}
    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    
    if api_key:
        config["api_key"] = api_key
    config.update(kwargs)
    
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def load_config() -> dict:
    """Load configuration from file."""
    _ensure_config_dir()
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def configure(api_key: str):
    """
    Configure Onwords with your API key.
    
    Get your API key from: https://ostapi.onwords.in
    
    Usage:
        import onwords
        onwords.configure("your-api-key-here")
    
    Args:
        api_key: Your Onwords API key
    """
    save_config(api_key=api_key)
    print(f"[Onwords] API key configured successfully!")
    print(f"[Onwords] Config saved to: {CONFIG_FILE}")


def get_products() -> List[str]:
    """
    Fetch all product IDs from your Onwords account.
    
    Usage:
        import onwords
        
        onwords.configure("your-api-key")  # First time only
        products = onwords.get_products()
        
        for product_id in products:
            print(product_id)
    
    Returns:
        List of product IDs
    """
    api = OnwordsAPI()
    return api.get_device_list()
