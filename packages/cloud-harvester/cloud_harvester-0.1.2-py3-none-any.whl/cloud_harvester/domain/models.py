from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Resource:
    """Unified cloud resource representation."""

    id: str
    provider: str
    kind: str
    resource: Optional[str] = None
    name: Optional[str] = None
    region: Optional[str] = None
    network_id: Optional[str] = None
    subnetwork_id: Optional[str] = None
    status: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dict for serialization or logging."""
        return {
            "id": self.id,
            "provider": self.provider,
            "kind": self.kind,
            "resource": self.resource,
            "name": self.name,
            "region": self.region,
            "network_id": self.network_id,
            "subnetwork_id": self.subnetwork_id,
            "status": self.status,
            "tags": self.tags,
            "raw": self.raw,
        }
