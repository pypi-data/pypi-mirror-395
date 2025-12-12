from __future__ import annotations

from typing import List, Optional

from cloud_harvester.domain.enums import AzureResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.azure.clients import get_compute_client
from cloud_harvester.infrastructure.providers.azure.resource_graph import (
    collect_from_resource_graph,
)
from cloud_harvester.infrastructure.providers.azure.utils import extract_network_info


def collect_vm(
    credential=None,
    subscription_id: Optional[str] = None,
    compute_client=None,
) -> List[Resource]:
    """Collect Azure VMs and map them to the unified Resource model."""

    compute_client = compute_client or get_compute_client(
        credential=credential, subscription_id=subscription_id
    )
    vms = compute_client.virtual_machines.list_all()

    resources: List[Resource] = []
    for vm in vms:
        status = None
        try:
            rg_name = _resource_group_from_id(vm.id)
            instance_view = compute_client.virtual_machines.instance_view(
                rg_name, vm.name
            )
            statuses = instance_view.statuses or []
            status_codes = [s.code for s in statuses if s.code]
            status = next(
                (code.split("/")[-1] for code in status_codes if "PowerState" in code),
                None,
            )
        except Exception:  # pragma: no cover - best effort status
            status = None

        tags = vm.tags or {}
        network_id, subnetwork_id = extract_network_info(
            vm.as_dict() if hasattr(vm, "as_dict") else vm.__dict__
        )
        resources.append(
            Resource(
                id=vm.id,
                provider=Provider.AZURE.value,
                kind=ResourceKind.COMPUTE.value,
                resource=AzureResource.VM.value,
                name=vm.name,
                region=vm.location,
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=status,
                tags=tags,
                raw=vm.as_dict() if hasattr(vm, "as_dict") else vm.__dict__,
            )
        )
    return resources


def collect_functions(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.web/sites"],
        azure_resource=AzureResource.FUNCTIONS,
        resource_kind=ResourceKind.COMPUTE,
        credential=credential,
        subscription_id=subscription_id,
        extra_filter="| where tolower(kind) contains 'functionapp'",
    )


def collect_container_instances(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.containerinstance/containergroups"],
        azure_resource=AzureResource.CONTAINER_INSTANCE,
        resource_kind=ResourceKind.COMPUTE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_container_apps(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.app/containerapps"],
        azure_resource=AzureResource.CONTAINER_APP,
        resource_kind=ResourceKind.COMPUTE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_aks_clusters(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.containerservice/managedclusters"],
        azure_resource=AzureResource.AKS,
        resource_kind=ResourceKind.COMPUTE,
        credential=credential,
        subscription_id=subscription_id,
    )


def _resource_group_from_id(resource_id: str) -> str:
    parts = resource_id.split("/")
    for idx, part in enumerate(parts):
        if part.lower() == "resourcegroups" and idx + 1 < len(parts):
            return parts[idx + 1]
    raise ValueError(f"Unable to parse resource group from id: {resource_id}")
