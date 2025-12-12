from __future__ import annotations

from typing import List, Optional

from cloud_harvester.domain.enums import AzureResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.azure.clients import get_network_client
from cloud_harvester.infrastructure.providers.azure.resource_graph import (
    collect_from_resource_graph,
)
from cloud_harvester.infrastructure.providers.azure.utils import extract_network_info


def collect_vnet(
    credential=None,
    subscription_id: Optional[str] = None,
    network_client=None,
) -> List[Resource]:
    """Collect Azure Virtual Networks and map them to the unified Resource model."""

    network_client = network_client or get_network_client(
        credential=credential, subscription_id=subscription_id
    )
    vnets = network_client.virtual_networks.list_all()

    resources: List[Resource] = []
    for vnet in vnets:
        tags = vnet.tags or {}
        network_id, subnetwork_id = extract_network_info(
            vnet.as_dict() if hasattr(vnet, "as_dict") else vnet.__dict__
        )
        resources.append(
            Resource(
                id=vnet.id,
                provider=Provider.AZURE.value,
                kind=ResourceKind.NETWORK.value,
                resource=AzureResource.VNET.value,
                name=vnet.name,
                region=vnet.location,
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=getattr(vnet, "provisioning_state", None),
                tags=tags,
                raw=vnet.as_dict() if hasattr(vnet, "as_dict") else vnet.__dict__,
            )
        )
    return resources


def collect_load_balancers(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.network/loadbalancers"],
        azure_resource=AzureResource.LOAD_BALANCER,
        resource_kind=ResourceKind.NETWORK,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_application_gateways(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.network/applicationgateways"],
        azure_resource=AzureResource.APPLICATION_GATEWAY,
        resource_kind=ResourceKind.NETWORK,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_traffic_manager_profiles(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.network/trafficmanagerprofiles"],
        azure_resource=AzureResource.TRAFFIC_MANAGER,
        resource_kind=ResourceKind.NETWORK,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_api_management_services(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.apimanagement/service"],
        azure_resource=AzureResource.API_MANAGEMENT,
        resource_kind=ResourceKind.NETWORK,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_dns_zones(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.network/dnszones"],
        azure_resource=AzureResource.DNS,
        resource_kind=ResourceKind.NETWORK,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_front_door_instances(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.network/frontdoors"],
        azure_resource=AzureResource.FRONT_DOOR,
        resource_kind=ResourceKind.NETWORK,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_cdn_profiles(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.cdn/profiles"],
        azure_resource=AzureResource.CDN,
        resource_kind=ResourceKind.NETWORK,
        credential=credential,
        subscription_id=subscription_id,
    )
