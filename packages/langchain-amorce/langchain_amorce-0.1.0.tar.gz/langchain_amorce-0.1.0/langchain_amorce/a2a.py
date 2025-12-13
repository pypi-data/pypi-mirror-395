"""
A2A Protocol compatibility layer
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class A2AEnvelope:
    """
    A2A-compatible message envelope with Amorce signatures.
    
    Combines A2A Protocol messaging with Amorce security.
    """
    
    sender_id: str
    message: str
    signature: str
    protocol_version: str = "a2a/1.0"
    security_layer: str = "amorce/3.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to A2A message format."""
        return {
            "protocol": self.protocol_version,
            "security": {
                "layer": self.security_layer,
                "sender_id": self.sender_id,
                "signature": self.signature,
                "algorithm": "ed25519"
            },
            "payload": {
                "message": self.message
            },
            "metadata": {
                "timestamp": self._get_timestamp(),
                "version": "1.0"
            }
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'A2AEnvelope':
        """Parse A2A message with Amorce signature."""
        return cls(
            sender_id=data['security']['sender_id'],
            message=data['payload']['message'],
            signature=data['security']['signature'],
            protocol_version=data.get('protocol', 'a2a/1.0'),
            security_layer=data['security'].get('layer', 'amorce/3.0')
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'A2AEnvelope':
        """Parse from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
