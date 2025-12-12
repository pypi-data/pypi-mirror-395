from __future__ import annotations

from typing import List, Optional

from botocore.exceptions import ClientError

from cloud_harvester.domain.enums import AwsResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.aws.auth import get_boto3_session
from cloud_harvester.infrastructure.providers.aws.utils import extract_network_info


def collect_cloudwatch_alarms(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect CloudWatch metric and composite alarms."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("cloudwatch")
    paginator = client.get_paginator("describe_alarms")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for alarm in page.get("MetricAlarms", []):
            tags = _cloudwatch_tags(client, alarm.get("AlarmArn"))
            network_id, subnetwork_id = extract_network_info(alarm)
            resources.append(
                Resource(
                    id=alarm.get("AlarmArn"),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.OBSERVABILITY.value,
                    resource=AwsResource.CLOUDWATCH.value,
                    name=alarm.get("AlarmName"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=alarm.get("StateValue"),
                    tags=tags,
                    raw=alarm,
                )
            )
        for alarm in page.get("CompositeAlarms", []):
            tags = _cloudwatch_tags(client, alarm.get("AlarmArn"))
            network_id, subnetwork_id = extract_network_info(alarm)
            resources.append(
                Resource(
                    id=alarm.get("AlarmArn"),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.OBSERVABILITY.value,
                    resource=AwsResource.CLOUDWATCH.value,
                    name=alarm.get("AlarmName"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=alarm.get("StateValue"),
                    tags=tags,
                    raw=alarm,
                )
            )
    return resources


def collect_cloudtrail_trails(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect CloudTrail trails."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("cloudtrail")
    response = client.describe_trails(includeShadowTrails=True)

    resources: List[Resource] = []
    for trail in response.get("trailList", []):
        trail_name = trail.get("Name")
        trail_arn = trail.get("TrailARN")
        try:
            status = client.get_trail_status(Name=trail_arn or trail_name)
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")
            if error_code == "TrailNotFoundException":
                continue
            raise
        tags = _cloudtrail_tags(client, trail_arn)
        network_id, subnetwork_id = extract_network_info(trail)
        resources.append(
            Resource(
                id=trail_arn,
                provider=Provider.AWS.value,
                kind=ResourceKind.OBSERVABILITY.value,
                resource=AwsResource.CLOUDTRAIL.value,
                name=trail_name,
                region=trail.get("HomeRegion"),
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=status.get("IsLogging"),
                tags=tags,
                raw=trail,
            )
        )
    return resources


def collect_config_recorders(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect AWS Config recorders."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("config")
    recorders = client.describe_configuration_recorders().get(
        "ConfigurationRecorders", []
    )
    statuses = client.describe_configuration_recorder_status().get(
        "ConfigurationRecordersStatus", []
    )
    status_map = {entry.get("name"): entry for entry in statuses}

    resources: List[Resource] = []
    for recorder in recorders:
        name = recorder.get("name")
        status_entry = status_map.get(name, {})
        status = "recording" if status_entry.get("recording") else "stopped"
        network_id, subnetwork_id = extract_network_info(recorder)
        resources.append(
            Resource(
                id=name,
                provider=Provider.AWS.value,
                kind=ResourceKind.OBSERVABILITY.value,
                resource=AwsResource.CONFIG.value,
                name=name,
                region=client.meta.region_name,
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=status,
                tags={},
                raw=recorder,
            )
        )
    return resources


def collect_ssm_managed_instances(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect Systems Manager managed instances."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("ssm")
    paginator = client.get_paginator("describe_instance_information")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for instance in page.get("InstanceInformationList", []):
            instance_id = instance.get("InstanceId")
            tags = _ssm_tags(client, instance_id)
            network_id, subnetwork_id = extract_network_info(instance)
            resources.append(
                Resource(
                    id=instance_id,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.MANAGEMENT.value,
                    resource=AwsResource.SYSTEMS_MANAGER.value,
                    name=instance.get("ComputerName") or instance_id,
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=instance.get("PingStatus"),
                    tags=tags,
                    raw=instance,
                )
            )
    return resources


def collect_backup_vaults(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect AWS Backup vaults."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("backup")
    paginator = client.get_paginator("list_backup_vaults")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for vault in page.get("BackupVaultList", []):
            name = vault.get("BackupVaultName")
            vault_arn = vault.get("BackupVaultArn")
            tags = _backup_tags(client, vault_arn)
            network_id, subnetwork_id = extract_network_info(vault)
            resources.append(
                Resource(
                    id=vault_arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.MANAGEMENT.value,
                    resource=AwsResource.BACKUP.value,
                    name=name,
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=vault.get("LockedState"),
                    tags=tags,
                    raw=vault,
                )
            )
    return resources


def _cloudwatch_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_for_resource(ResourceARN=arn)
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("Tags", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _cloudtrail_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags(ResourceIdList=[arn])
        tag_list = response.get("ResourceTagList", [])
        if not tag_list:
            return {}
        tags = tag_list[0].get("TagsList", [])
        return {t.get("Key"): t.get("Value") for t in tags if t.get("Key")}
    except ClientError:
        return {}


def _ssm_tags(client, instance_id: Optional[str]) -> dict:
    if not instance_id:
        return {}
    try:
        response = client.list_tags_for_resource(
            ResourceType="ManagedInstance", ResourceId=instance_id
        )
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("TagList", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _backup_tags(client, vault_arn: Optional[str]) -> dict:
    if not vault_arn:
        return {}
    try:
        response = client.list_tags(ResourceArn=vault_arn)
        return response.get("Tags", {}) or {}
    except ClientError:
        return {}
