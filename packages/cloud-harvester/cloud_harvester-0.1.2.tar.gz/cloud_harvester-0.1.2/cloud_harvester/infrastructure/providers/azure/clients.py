import os
from typing import Any, List, Optional

from azure.identity import DefaultAzureCredential
from azure.graphrbac import GraphRbacManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest


def _env(name: str) -> Optional[str]:
    return os.getenv(name) or os.getenv(name.upper())


def get_subscription_id(subscription_id: Optional[str] = None) -> str:
    sub_id = (
        subscription_id
        or _env("CLOUD_HARVESTER_AZURE_SUBSCRIPTION_ID")
        or _env("AZURE_SUBSCRIPTION_ID")
    )
    if not sub_id:
        raise ValueError(
            "Azure subscription id is required. Set AZURE_SUBSCRIPTION_ID or pass subscription_id."
        )
    return sub_id


def get_credential(credential=None):
    if credential:
        return credential
    return DefaultAzureCredential(exclude_interactive_browser_credential=False)


def get_tenant_id(tenant_id: Optional[str] = None, credential=None) -> str:
    tenant = (
        tenant_id or _env("CLOUD_HARVESTER_AZURE_TENANT_ID") or _env("AZURE_TENANT_ID")
    )
    if not tenant and credential is not None:
        for attr in ("tenant_id", "_tenant_id"):
            tenant = getattr(credential, attr, None)
            if tenant:
                break
    if not tenant:
        raise ValueError(
            "Azure tenant id is required. Set AZURE_TENANT_ID or CLOUD_HARVESTER_AZURE_TENANT_ID."
        )
    return tenant


def build_clients(credential=None, subscription_id: Optional[str] = None):
    cred = get_credential(credential)
    sub_id = get_subscription_id(subscription_id)
    compute_client = ComputeManagementClient(cred, sub_id)
    network_client = NetworkManagementClient(cred, sub_id)
    return compute_client, network_client


def get_compute_client(
    credential=None, subscription_id: Optional[str] = None
) -> ComputeManagementClient:
    cred = get_credential(credential)
    sub_id = get_subscription_id(subscription_id)
    return ComputeManagementClient(cred, sub_id)


def get_network_client(
    credential=None, subscription_id: Optional[str] = None
) -> NetworkManagementClient:
    cred = get_credential(credential)
    sub_id = get_subscription_id(subscription_id)
    return NetworkManagementClient(cred, sub_id)


def get_storage_client(
    credential=None, subscription_id: Optional[str] = None
) -> StorageManagementClient:
    cred = get_credential(credential)
    sub_id = get_subscription_id(subscription_id)
    return StorageManagementClient(cred, sub_id)


def build_resource_graph_client(credential=None) -> ResourceGraphClient:
    cred = get_credential(credential)
    return ResourceGraphClient(cred)


def query_resource_graph(
    query: str, credential=None, subscription_id: Optional[str] = None
) -> List[dict]:
    client = build_resource_graph_client(credential=credential)
    sub_id = get_subscription_id(subscription_id)
    request = QueryRequest(subscriptions=[sub_id], query=query)
    response = client.resources(request)
    data = response.data
    if not data:
        return []

    columns = [column.name for column in getattr(data, "columns", [])]
    rows: List[List[Any]] = getattr(data, "rows", [])
    results: List[dict] = []
    for row in rows:
        record = {name: value for name, value in zip(columns, row)}
        results.append(record)
    return results


def get_graph_client(
    credential=None, tenant_id: Optional[str] = None
) -> GraphRbacManagementClient:
    cred = get_credential(credential)
    tenant = get_tenant_id(tenant_id, credential=cred)
    return GraphRbacManagementClient(cred, tenant)
