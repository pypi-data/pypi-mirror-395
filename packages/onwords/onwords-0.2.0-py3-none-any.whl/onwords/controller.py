"""
Onwords Controller - Control your gate devices
https://ostapi.onwords.in/api-documentation
"""

from typing import Optional, Dict
from .api import OnwordsAPI


class Controller:
    """
    Controller class for Onwords gate devices.
    
    Supported Device Types:
    
    Sliding Gate (3chsg):
        - open, close, pause
        
    Sliding Gate Advanced (3chsgsl):
        - open, close, pause, partial_open
        
    Arm Gate (3chag):
        - Single: open_single_gate, close_single_gate, pause_single_gate
        - Double: open_double_gate, close_double_gate, pause_double_gate
    
    Usage:
        from onwords import Controller
        
        gate = Controller("my-product-id")
        gate.open()
        gate.close()
        gate.pause()
    """
    
    def __init__(self, product_id: str, api_key: str = None):
        self.product_id = product_id
        self._api = OnwordsAPI(api_key)
        self.gate_type: Optional[str] = None
    
    def _send(self, action: str) -> dict:
        """Send action to device and return response."""
        response = self._api.control_device(self.product_id, action)
        if response.get("gate_type"):
            self.gate_type = response["gate_type"]
        return response
    
    # ─────────────────────────────────────────────
    # Sliding Gate Actions (3chsg, 3chsgsl)
    # ─────────────────────────────────────────────
    
    def open(self) -> dict:
        """
        Open the gate.
        
        Works with: Sliding Gate, Sliding Gate Advanced
        """
        return self._send("open")
    
    def close(self) -> dict:
        """
        Close the gate.
        
        Works with: Sliding Gate, Sliding Gate Advanced
        """
        return self._send("close")
    
    def pause(self) -> dict:
        """
        Pause/stop the gate.
        
        Works with: Sliding Gate, Sliding Gate Advanced
        """
        return self._send("pause")
    
    def partial_open(self) -> dict:
        """
        Partially open the gate (pedestrian mode).
        
        Works with: Sliding Gate Advanced (3chsgsl) only
        """
        return self._send("partial_open")
    
    # Aliases for convenience
    def stop(self) -> dict:
        """Alias for pause()."""
        return self.pause()
    
    def pedestrian(self) -> dict:
        """Alias for partial_open()."""
        return self.partial_open()
    
    # ─────────────────────────────────────────────
    # Arm Gate - Single Gate Actions (3chag)
    # ─────────────────────────────────────────────
    
    def open_single_gate(self) -> dict:
        """
        Open single arm gate.
        
        Works with: Arm Gate (3chag)
        """
        return self._send("open_single_gate")
    
    def close_single_gate(self) -> dict:
        """
        Close single arm gate.
        
        Works with: Arm Gate (3chag)
        """
        return self._send("close_single_gate")
    
    def pause_single_gate(self) -> dict:
        """
        Pause single arm gate.
        
        Works with: Arm Gate (3chag)
        """
        return self._send("pause_single_gate")
    
    # ─────────────────────────────────────────────
    # Arm Gate - Double Gate Actions (3chag)
    # ─────────────────────────────────────────────
    
    def open_double_gate(self) -> dict:
        """
        Open double arm gate (both arms).
        
        Works with: Arm Gate (3chag)
        """
        return self._send("open_double_gate")
    
    def close_double_gate(self) -> dict:
        """
        Close double arm gate (both arms).
        
        Works with: Arm Gate (3chag)
        """
        return self._send("close_double_gate")
    
    def pause_double_gate(self) -> dict:
        """
        Pause double arm gate (both arms).
        
        Works with: Arm Gate (3chag)
        """
        return self._send("pause_double_gate")
    
    # ─────────────────────────────────────────────
    # Generic Action
    # ─────────────────────────────────────────────
    
    def action(self, action_name: str) -> dict:
        """
        Send any action to the device.
        
        Args:
            action_name: Action to perform
            
        Supported actions by gate type:
        
        Sliding Gate (3chsg):
            - open, close, pause
            
        Sliding Gate Advanced (3chsgsl):
            - open, close, pause, partial_open
            
        Arm Gate (3chag):
            - open_single_gate, close_single_gate, pause_single_gate
            - open_double_gate, close_double_gate, pause_double_gate
        """
        return self._send(action_name)
    
    def __repr__(self) -> str:
        gate_info = f", gate_type={self.gate_type!r}" if self.gate_type else ""
        return f"Controller(product_id={self.product_id!r}{gate_info})"


def control(product: str, api_key: str = None) -> Controller:
    """
    Quick control function for Onwords gate devices.
    
    Usage:
        import onwords
        
        onwords.configure("your-api-key")  # First time only
        
        gate = onwords.control("my-product-id")
        gate.open()
        gate.close()
    
    Args:
        product: Product ID to control
        api_key: Optional API key (uses saved key if not provided)
        
    Returns:
        Controller instance for the device
    """
    return Controller(product, api_key)
