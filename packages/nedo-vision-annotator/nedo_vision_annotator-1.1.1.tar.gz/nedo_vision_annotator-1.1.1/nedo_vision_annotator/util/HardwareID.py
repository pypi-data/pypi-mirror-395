"""
Utility to get unique hardware ID for the annotator
"""
import platform
import uuid
import hashlib


def get_hardware_id() -> str:
    """
    Generate a unique hardware ID based on MAC address and hostname.
    
    Returns:
        str: Unique hardware identifier
    """
    try:
        # Get MAC address
        mac = uuid.getnode()
        mac_str = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
        
        # Get hostname
        hostname = platform.node()
        
        # Combine and hash
        combined = f"{mac_str}-{hostname}"
        hardware_id = hashlib.sha256(combined.encode()).hexdigest()[:16]
        
        return hardware_id.upper()
    except Exception:
        # Fallback to random UUID if hardware detection fails
        return uuid.uuid4().hex[:16].upper()
