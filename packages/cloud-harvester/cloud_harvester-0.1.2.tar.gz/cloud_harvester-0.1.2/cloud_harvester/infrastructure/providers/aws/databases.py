from __future__ import annotations

from typing import List, Optional

from botocore.exceptions import ClientError

from cloud_harvester.domain.enums import AwsResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.aws.auth import get_boto3_session
from cloud_harvester.infrastructure.providers.aws.utils import extract_network_info


def collect_rds(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect AWS RDS database instances."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("rds")
    paginator = client.get_paginator("describe_db_instances")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for db in page.get("DBInstances", []):
            tags = _list_rds_tags(client, db.get("DBInstanceArn"))
            network_id, subnetwork_id = extract_network_info(db)
            resources.append(
                Resource(
                    id=db.get("DBInstanceIdentifier"),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.DATABASE.value,
                    resource=AwsResource.RDS.value,
                    name=db.get("DBInstanceIdentifier"),
                    region=db.get("AvailabilityZone") or client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=db.get("DBInstanceStatus"),
                    tags=tags,
                    raw=db,
                )
            )
    return resources


def collect_dynamodb_tables(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect DynamoDB tables."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("dynamodb")
    paginator = client.get_paginator("list_tables")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for table_name in page.get("TableNames", []):
            table = client.describe_table(TableName=table_name)["Table"]
            arn = table.get("TableArn") or table_name
            tags = _dynamodb_tags(client, arn)
            network_id, subnetwork_id = extract_network_info(table)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.DATABASE.value,
                    resource=AwsResource.DYNAMODB.value,
                    name=table.get("TableName"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=str(table.get("TableStatus")),
                    tags=tags,
                    raw=table,
                )
            )
    return resources


def collect_elasticache_clusters(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect ElastiCache clusters."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("elasticache")
    paginator = client.get_paginator("describe_cache_clusters")

    resources: List[Resource] = []
    for page in paginator.paginate(ShowCacheNodeInfo=True):
        for cluster in page.get("CacheClusters", []):
            arn = cluster.get("ARN", cluster.get("CacheClusterId"))
            tags = _elasticache_tags(client, arn)
            network_id, subnetwork_id = extract_network_info(cluster)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.DATABASE.value,
                    resource=AwsResource.ELASTICACHE.value,
                    name=cluster.get("CacheClusterId"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=cluster.get("CacheClusterStatus"),
                    tags=tags,
                    raw=cluster,
                )
            )
    return resources


def collect_redshift_clusters(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect Redshift clusters."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("redshift")
    paginator = client.get_paginator("describe_clusters")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for cluster in page.get("Clusters", []):
            arn = cluster.get("ClusterNamespaceArn") or cluster.get("ClusterIdentifier")
            tags = _redshift_tags(client, arn)
            network_id, subnetwork_id = extract_network_info(cluster)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.DATABASE.value,
                    resource=AwsResource.REDSHIFT.value,
                    name=cluster.get("ClusterIdentifier"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=cluster.get("ClusterStatus"),
                    tags=tags,
                    raw=cluster,
                )
            )
    return resources


def _dynamodb_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_of_resource(ResourceArn=arn)
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("Tags", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _elasticache_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_for_resource(ResourceName=arn)
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("TagList", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _redshift_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.describe_tags(ResourceName=arn)
        tagged = response.get("TaggedResources", [])
        tags = {}
        for entry in tagged:
            tag = entry.get("Tag") or {}
            key = tag.get("Key")
            if key:
                tags[key] = tag.get("Value")
        return tags
    except ClientError:
        return {}


def _list_rds_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_for_resource(ResourceName=arn)
        tag_list = response.get("TagList", [])
        return {t.get("Key"): t.get("Value") for t in tag_list if t.get("Key")}
    except ClientError:
        return {}
