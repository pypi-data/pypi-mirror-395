from __future__ import annotations

from typing import List, Optional

from cloud_harvester.domain.enums import AwsResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.aws.auth import get_boto3_session
from cloud_harvester.infrastructure.providers.aws.utils import extract_network_info


def collect_ec2(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect AWS EC2 instances and map them to the unified Resource model."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("ec2")
    paginator = client.get_paginator("describe_instances")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                tags = (
                    {t["Key"]: t["Value"] for t in instance.get("Tags", [])}
                    if instance.get("Tags")
                    else {}
                )
                network_id, subnetwork_id = extract_network_info(instance)
                resources.append(
                    Resource(
                        id=instance["InstanceId"],
                        provider=Provider.AWS.value,
                        kind=ResourceKind.COMPUTE.value,
                        resource=AwsResource.EC2.value,
                        name=_name_from_tags(tags),
                        region=client.meta.region_name,
                        network_id=network_id,
                        subnetwork_id=subnetwork_id,
                        status=instance.get("State", {}).get("Name"),
                        tags=tags,
                        raw=instance,
                    )
                )
    return resources


def _name_from_tags(tags: dict) -> Optional[str]:
    return tags.get("Name")
