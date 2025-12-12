from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from cloud_harvester.domain.enums import AzureResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.azure.clients import query_resource_graph
from cloud_harvester.infrastructure.providers.azure.utils import extract_network_info


def collect_from_resource_graph(
    resource_types: Iterable[str],
    azure_resource: AzureResource,
    resource_kind: ResourceKind,
    credential=None,
    subscription_id: Optional[str] = None,
    extra_filter: Optional[str] = None,
) -> List[Resource]:
    """Generic helper to collect Azure resources via Resource Graph."""

    types_clause = ", ".join(
        f"'{resource_type.lower()}'" for resource_type in resource_types
    )
    query = ["Resources", f"| where tolower(type) in~ ({types_clause})"]
    if extra_filter:
        query.append(extra_filter)
    query.append(
        "| project id, name, type, location, tags, kind, resourceGroup, properties"
    )
    records = query_resource_graph(
        "\n".join(query), credential=credential, subscription_id=subscription_id
    )

    resources: List[Resource] = []
    for record in records:
        tags_raw = record.get("tags") or {}
        tags: Dict[str, str] = {str(k): str(v) for k, v in tags_raw.items()}
        props: Dict[str, Any] = record.get("properties") or {}
        status = _status_from_properties(props)
        network_id, subnetwork_id = extract_network_info(record)
        resources.append(
            Resource(
                id=str(record.get("id") or ""),
                provider=Provider.AZURE.value,
                kind=resource_kind.value,
                resource=azure_resource.value,
                name=str(record.get("name") or ""),
                region=str(record.get("location") or ""),
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=status,
                tags=tags,
                raw=dict(record),
            )
        )
    return resources


def _status_from_properties(props) -> Optional[str]:
    if isinstance(props, dict):
        for key in ("provisioningState", "status", "state", "powerState", "stateCode"):
            value = props.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, dict):
                for nested_key in ("code", "displayStatus", "value"):
                    nested_value = value.get(nested_key)
                    if isinstance(nested_value, str):
                        return nested_value
    return None
