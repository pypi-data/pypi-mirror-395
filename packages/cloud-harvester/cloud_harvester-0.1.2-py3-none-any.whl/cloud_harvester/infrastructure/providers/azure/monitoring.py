from __future__ import annotations

from typing import List, Optional

from cloud_harvester.domain.enums import AzureResource, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.azure.resource_graph import (
    collect_from_resource_graph,
)


def collect_monitor_workspaces(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=[
            "microsoft.operationalinsights/workspaces",
            "microsoft.insights/components",
        ],
        azure_resource=AzureResource.MONITOR,
        resource_kind=ResourceKind.OBSERVABILITY,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_activity_log_alerts(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.insights/activitylogalerts"],
        azure_resource=AzureResource.ACTIVITY_LOG,
        resource_kind=ResourceKind.OBSERVABILITY,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_policy_assignments(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.authorization/policyassignments"],
        azure_resource=AzureResource.POLICY,
        resource_kind=ResourceKind.MANAGEMENT,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_automation_accounts(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.automation/automationaccounts"],
        azure_resource=AzureResource.AUTOMATION,
        resource_kind=ResourceKind.MANAGEMENT,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_backup_vaults(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=[
            "microsoft.recoveryservices/vaults",
            "microsoft.recoveryservices/backupvaults",
        ],
        azure_resource=AzureResource.BACKUP,
        resource_kind=ResourceKind.MANAGEMENT,
        credential=credential,
        subscription_id=subscription_id,
    )
