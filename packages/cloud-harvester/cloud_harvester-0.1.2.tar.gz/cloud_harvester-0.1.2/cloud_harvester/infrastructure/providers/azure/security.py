from __future__ import annotations

import logging
from typing import List, Optional

from azure.mgmt.security import SecurityCenter

from cloud_harvester.domain.enums import AzureResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.azure.clients import (
    get_credential,
    get_graph_client,
    get_subscription_id,
)
from cloud_harvester.infrastructure.providers.azure.resource_graph import (
    collect_from_resource_graph,
)
from cloud_harvester.infrastructure.providers.azure.utils import extract_network_info


logger = logging.getLogger(__name__)


def collect_active_directory_domains(
    credential=None,
    subscription_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> List[Resource]:
    cred = get_credential(credential)
    if not hasattr(cred, "signed_session"):
        logger.warning(
            "Skipping Azure AD collection: credential lacks signed_session (Graph client requires legacy auth)"
        )
        return []

    try:
        graph_client = get_graph_client(credential=cred, tenant_id=tenant_id)
    except ValueError as exc:
        logger.warning("Skipping Azure AD collection: %s", exc)
        return []
    except AttributeError as exc:
        logger.warning("Skipping Azure AD collection: %s", exc)
        return []

    try:
        domains = graph_client.domains.list()
    except AttributeError as exc:
        logger.warning(
            "Azure AD client not compatible with provided credential: %s", exc
        )
        return []

    resources: List[Resource] = []
    for domain in domains:
        data = domain.as_dict() if hasattr(domain, "as_dict") else domain.__dict__
        status = "verified" if getattr(domain, "is_verified", False) else "unverified"
        network_id, subnetwork_id = extract_network_info(data)
        resources.append(
            Resource(
                id=data.get("_id") or data.get("id") or domain.name,
                provider=Provider.AZURE.value,
                kind=ResourceKind.IDENTITY.value,
                resource=AzureResource.ACTIVE_DIRECTORY.value,
                name=domain.name,
                region=None,
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=status,
                tags={"isDefault": str(getattr(domain, "is_default", False))},
                raw=data,
            )
        )
    return resources


def collect_management_groups(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.management/managementgroups"],
        azure_resource=AzureResource.MANAGEMENT_GROUP,
        resource_kind=ResourceKind.MANAGEMENT,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_key_vaults(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.keyvault/vaults"],
        azure_resource=AzureResource.KEY_VAULT,
        resource_kind=ResourceKind.SECURITY,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_key_vault_keys(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.keyvault/vaults/keys"],
        azure_resource=AzureResource.KEY_VAULT_KEY,
        resource_kind=ResourceKind.SECURITY,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_key_vault_secrets(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.keyvault/vaults/secrets"],
        azure_resource=AzureResource.KEY_VAULT_SECRET,
        resource_kind=ResourceKind.SECURITY,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_key_vault_certificates(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=[
            "microsoft.keyvault/vaults/certificates",
            "microsoft.web/certificates",
        ],
        azure_resource=AzureResource.KEY_VAULT_CERTIFICATE,
        resource_kind=ResourceKind.SECURITY,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_waf_policies(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=[
            "microsoft.network/applicationgatewaywebapplicationfirewallpolicies",
            "microsoft.network/frontdoorwebapplicationfirewallpolicies",
        ],
        azure_resource=AzureResource.WAF,
        resource_kind=ResourceKind.SECURITY,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_ddos_plans(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.network/ddosprotectionplans"],
        azure_resource=AzureResource.DDOS,
        resource_kind=ResourceKind.SECURITY,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_defender_settings(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    client = _get_security_client(
        credential=credential, subscription_id=subscription_id
    )
    scope = f"/subscriptions/{get_subscription_id(subscription_id)}"
    pricings = client.pricings.list(scope_id=scope)

    resources: List[Resource] = []
    for pricing in getattr(pricings, "value", []) or []:
        data = pricing.as_dict() if hasattr(pricing, "as_dict") else pricing.__dict__
        network_id, subnetwork_id = extract_network_info(data)
        resources.append(
            Resource(
                id=data.get("id") or pricing.name,
                provider=Provider.AZURE.value,
                kind=ResourceKind.SECURITY.value,
                resource=AzureResource.DEFENDER.value,
                name=pricing.name,
                region=None,
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=data.get("pricing_tier"),
                tags={},
                raw=data,
            )
        )
    return resources


def collect_secure_scores(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    client = _get_security_client(
        credential=credential, subscription_id=subscription_id
    )
    scores = client.secure_scores.list()

    resources: List[Resource] = []
    for score in scores:
        data = score.as_dict() if hasattr(score, "as_dict") else score.__dict__
        status = str(data.get("score"))
        network_id, subnetwork_id = extract_network_info(data)
        resources.append(
            Resource(
                id=data.get("id") or score.name,
                provider=Provider.AZURE.value,
                kind=ResourceKind.SECURITY.value,
                resource=AzureResource.SECURE_SCORE.value,
                name=data.get("display_name") or score.name,
                region=None,
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=status,
                tags={},
                raw=data,
            )
        )
    return resources


def _get_security_client(
    credential=None, subscription_id: Optional[str] = None
) -> SecurityCenter:
    cred = get_credential(credential)
    sub_id = get_subscription_id(subscription_id)
    return SecurityCenter(cred, sub_id)
