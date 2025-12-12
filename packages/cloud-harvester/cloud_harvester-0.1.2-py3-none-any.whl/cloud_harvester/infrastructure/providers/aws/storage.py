from __future__ import annotations

from typing import List, Optional

from botocore.exceptions import ClientError

from cloud_harvester.domain.enums import AwsResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.aws.auth import get_boto3_session
from cloud_harvester.infrastructure.providers.aws.utils import extract_network_info


def collect_s3_buckets(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect S3 buckets."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("s3")
    response = client.list_buckets()

    resources: List[Resource] = []
    for bucket in response.get("Buckets", []):
        name = bucket.get("Name")
        bucket_region = _bucket_region(client, name)
        tags = _bucket_tags(client, name)
        network_id, subnetwork_id = extract_network_info(bucket)
        resources.append(
            Resource(
                id=name,
                provider=Provider.AWS.value,
                kind=ResourceKind.STORAGE.value,
                resource=AwsResource.S3.value,
                name=name,
                region=bucket_region,
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=bucket.get("CreationDate").isoformat()
                if bucket.get("CreationDate")
                else None,
                tags=tags,
                raw=bucket,
            )
        )
    return resources


def collect_ebs_volumes(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect EBS volumes."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("ec2")
    paginator = client.get_paginator("describe_volumes")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for volume in page.get("Volumes", []):
            tags = {
                t.get("Key"): t.get("Value")
                for t in volume.get("Tags", [])
                if t.get("Key")
            }
            network_id, subnetwork_id = extract_network_info(volume)
            resources.append(
                Resource(
                    id=volume.get("VolumeId"),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.STORAGE.value,
                    resource=AwsResource.EBS.value,
                    name=volume.get("VolumeId"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=volume.get("State"),
                    tags=tags,
                    raw=volume,
                )
            )
    return resources


def collect_efs_file_systems(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect EFS file systems."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("efs")
    paginator = client.get_paginator("describe_file_systems")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for fs in page.get("FileSystems", []):
            tags = _efs_tags(client, fs.get("FileSystemId"))
            network_id, subnetwork_id = extract_network_info(fs)
            resources.append(
                Resource(
                    id=fs.get("FileSystemArn", fs.get("FileSystemId")),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.STORAGE.value,
                    resource=AwsResource.EFS.value,
                    name=fs.get("Name"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=fs.get("LifeCycleState"),
                    tags=tags,
                    raw=fs,
                )
            )
    return resources


def _bucket_region(client, name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    try:
        response = client.get_bucket_location(Bucket=name)
        region = response.get("LocationConstraint")
        return region or "us-east-1"
    except ClientError:
        return None


def _bucket_tags(client, name: Optional[str]) -> dict:
    if not name:
        return {}
    try:
        response = client.get_bucket_tagging(Bucket=name)
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("TagSet", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _efs_tags(client, fs_id: Optional[str]) -> dict:
    if not fs_id:
        return {}
    try:
        response = client.describe_tags(FileSystemId=fs_id)
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("Tags", [])
            if t.get("Key")
        }
    except ClientError:
        return {}
