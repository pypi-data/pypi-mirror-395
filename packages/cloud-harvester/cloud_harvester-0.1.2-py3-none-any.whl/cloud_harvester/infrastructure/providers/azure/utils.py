from __future__ import annotations

from typing import Any, Optional, Tuple


def extract_network_info(payload: Any) -> Tuple[Optional[str], Optional[str]]:
    """
    Best-effort extraction of virtual network and subnet identifiers from Azure payloads.

    Traverses dict/list structures and looks for keys containing "virtualnetwork",
    "vnet", or "subnet".
    """
    network_id: Optional[str] = None
    subnet_id: Optional[str] = None
    stack = [payload]
    seen = set()

    while stack and (network_id is None or subnet_id is None):
        current = stack.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))

        if isinstance(current, dict):
            for key, value in current.items():
                key_lower = key.lower()
                if network_id is None and (
                    "virtualnetwork" in key_lower
                    or key_lower == "vnet"
                    or "vnet" in key_lower
                ):
                    network_id = _pick_identifier(value)
                if subnet_id is None and "subnet" in key_lower:
                    subnet_id = _pick_identifier(value)

                if isinstance(value, (dict, list, tuple, set)):
                    stack.append(value)

        elif isinstance(current, (list, tuple, set)):
            stack.extend(current)

    return network_id, subnet_id


def _pick_identifier(value: Any) -> Optional[str]:
    """Normalize a candidate identifier from strings or collections."""
    if isinstance(value, str):
        return value or None

    if isinstance(value, (list, tuple, set)):
        for item in value:
            candidate = _pick_identifier(item)
            if candidate:
                return candidate
        return None

    if isinstance(value, dict):
        for candidate_key in ("id", "Id", "identifier", "Identifier", "resourceId"):
            if candidate_key in value:
                candidate = _pick_identifier(value[candidate_key])
                if candidate:
                    return candidate
        for nested_value in value.values():
            candidate = _pick_identifier(nested_value)
            if candidate:
                return candidate
        return None

    return None
