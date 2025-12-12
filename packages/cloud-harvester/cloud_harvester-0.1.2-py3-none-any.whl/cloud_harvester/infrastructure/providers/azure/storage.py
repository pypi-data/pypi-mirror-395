from __future__ import annotations

from typing import Any, Dict, List, Optional, cast

from cloud_harvester.domain.enums import AzureResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.azure.clients import get_storage_client
from cloud_harvester.infrastructure.providers.azure.resource_graph import (
    collect_from_resource_graph,
)
from cloud_harvester.infrastructure.providers.azure.utils import extract_network_info


def collect_storage_accounts(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.storage/storageaccounts"],
        azure_resource=AzureResource.STORAGE_ACCOUNT,
        resource_kind=ResourceKind.STORAGE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_managed_disks(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.compute/disks"],
        azure_resource=AzureResource.MANAGED_DISK,
        resource_kind=ResourceKind.STORAGE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_file_shares(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    storage_client = get_storage_client(
        credential=credential, subscription_id=subscription_id
    )
    accounts = storage_client.storage_accounts.list()

    resources: List[Resource] = []
    for account in accounts:
        if not account.id or not account.name:
            continue
        rg_name = _resource_group_from_id(account.id)
        try:
            shares = storage_client.file_shares.list(rg_name, account.name)
        except Exception:
            continue
        for share in shares:
            share_id = (
                getattr(share, "id", None)
                or f"{account.id}/fileServices/default/shares/{share.name}"
            )
            metadata: Dict[str, Any] = getattr(share, "metadata", None) or {}
            status = getattr(share, "share_status", None)
            raw_share: Dict[str, Any] = cast(
                Dict[str, Any],
                share.as_dict() if hasattr(share, "as_dict") else dict(share.__dict__),
            )
            network_id, subnetwork_id = extract_network_info(raw_share)
            resources.append(
                Resource(
                    id=share_id,
                    provider=Provider.AZURE.value,
                    kind=ResourceKind.STORAGE.value,
                    resource=AzureResource.STORAGE_FILE_SHARE.value,
                    name=share.name,
                    region=account.location,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=status,
                    tags={str(k): str(v) for k, v in metadata.items()},
                    raw=raw_share,
                )
            )
    return resources


def _resource_group_from_id(resource_id: str) -> str:
    parts = resource_id.split("/")
    for idx, part in enumerate(parts):
        if part.lower() == "resourcegroups" and idx + 1 < len(parts):
            return parts[idx + 1]
    raise ValueError(f"Unable to parse resource group from id: {resource_id}")
