from __future__ import annotations

from typing import Iterable, List, Optional

from botocore.exceptions import ClientError

from cloud_harvester.domain.enums import AwsResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.aws.auth import get_boto3_session
from cloud_harvester.infrastructure.providers.aws.utils import extract_network_info


def collect_ecs_clusters(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect AWS ECS clusters."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("ecs")
    paginator = client.get_paginator("list_clusters")

    cluster_arns: List[str] = []
    for page in paginator.paginate():
        cluster_arns.extend(page.get("clusterArns", []))

    resources: List[Resource] = []
    if not cluster_arns:
        return resources

    for batch in _chunked(cluster_arns, 100):
        response = client.describe_clusters(clusters=batch)
        for cluster in response.get("clusters", []):
            tags = _ecs_tags(client, cluster.get("clusterArn"))
            network_id, subnetwork_id = extract_network_info(cluster)
            resources.append(
                Resource(
                    id=cluster.get("clusterArn", cluster.get("clusterName")),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.COMPUTE.value,
                    resource=AwsResource.ECS.value,
                    name=cluster.get("clusterName"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=cluster.get("status"),
                    tags=tags,
                    raw=cluster,
                )
            )

    return resources


def collect_eks_clusters(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect AWS EKS clusters."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("eks")
    paginator = client.get_paginator("list_clusters")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for name in page.get("clusters", []):
            cluster = client.describe_cluster(name=name)["cluster"]
            arn = cluster.get("arn", name)
            arn_parts = arn.split(":") if arn else []
            cluster_region = (
                arn_parts[3] if len(arn_parts) > 3 else client.meta.region_name
            )
            network_id, subnetwork_id = extract_network_info(cluster)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.COMPUTE.value,
                    resource=AwsResource.EKS.value,
                    name=cluster.get("name"),
                    region=cluster_region,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=cluster.get("status"),
                    tags=cluster.get("tags", {}) or {},
                    raw=cluster,
                )
            )

    return resources


def _ecs_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_for_resource(resourceArn=arn)
        return {
            t.get("key"): t.get("value")
            for t in response.get("tags", [])
            if t.get("key")
        }
    except ClientError:
        return {}


def _chunked(values: Iterable[str], size: int) -> Iterable[List[str]]:
    values_list = list(values)
    for idx in range(0, len(values_list), size):
        yield values_list[idx : idx + size]
