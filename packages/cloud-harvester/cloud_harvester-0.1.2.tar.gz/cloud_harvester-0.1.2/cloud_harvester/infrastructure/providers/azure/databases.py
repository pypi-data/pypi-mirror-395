from __future__ import annotations

from typing import List, Optional

from cloud_harvester.domain.enums import AzureResource, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.azure.resource_graph import (
    collect_from_resource_graph,
)


def collect_sql_databases(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.sql/servers/databases"],
        azure_resource=AzureResource.SQL_DATABASE,
        resource_kind=ResourceKind.DATABASE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_postgresql_servers(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=[
            "microsoft.dbforpostgresql/servers",
            "microsoft.dbforpostgresql/flexibleservers",
        ],
        azure_resource=AzureResource.POSTGRESQL,
        resource_kind=ResourceKind.DATABASE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_mysql_servers(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=[
            "microsoft.dbformysql/servers",
            "microsoft.dbformysql/flexibleservers",
        ],
        azure_resource=AzureResource.MYSQL,
        resource_kind=ResourceKind.DATABASE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_mariadb_servers(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.dbformariadb/servers"],
        azure_resource=AzureResource.MARIADB,
        resource_kind=ResourceKind.DATABASE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_cosmos_db_accounts(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.documentdb/databaseaccounts"],
        azure_resource=AzureResource.COSMOS_DB,
        resource_kind=ResourceKind.DATABASE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_redis_caches(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.cache/redis"],
        azure_resource=AzureResource.REDIS,
        resource_kind=ResourceKind.DATABASE,
        credential=credential,
        subscription_id=subscription_id,
    )


def collect_synapse_workspaces(
    credential=None, subscription_id: Optional[str] = None
) -> List[Resource]:
    return collect_from_resource_graph(
        resource_types=["microsoft.synapse/workspaces"],
        azure_resource=AzureResource.SYNAPSE,
        resource_kind=ResourceKind.DATABASE,
        credential=credential,
        subscription_id=subscription_id,
    )
