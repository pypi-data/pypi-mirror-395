from __future__ import annotations

from typing import List, Optional

from botocore.exceptions import ClientError

from cloud_harvester.domain.enums import AwsResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.aws.auth import get_boto3_session
from cloud_harvester.infrastructure.providers.aws.utils import extract_network_info


def collect_iam_roles(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect IAM roles."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("iam")
    paginator = client.get_paginator("list_roles")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for role in page.get("Roles", []):
            tags = _iam_role_tags(client, role.get("RoleName"))
            network_id, subnetwork_id = extract_network_info(role)
            resources.append(
                Resource(
                    id=role.get("Arn"),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.IDENTITY.value,
                    resource=AwsResource.IAM.value,
                    name=role.get("RoleName"),
                    region="global",
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=role.get("Path"),
                    tags=tags,
                    raw=role,
                )
            )
    return resources


def collect_organizations_accounts(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect AWS Organizations accounts."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("organizations")
    paginator = client.get_paginator("list_accounts")

    resources: List[Resource] = []
    try:
        for page in paginator.paginate():
            for account in page.get("Accounts", []):
                tags = _organization_account_tags(client, account.get("Id"))
                network_id, subnetwork_id = extract_network_info(account)
                resources.append(
                    Resource(
                        id=account.get("Arn", account.get("Id")),
                        provider=Provider.AWS.value,
                        kind=ResourceKind.MANAGEMENT.value,
                        resource=AwsResource.ORGANIZATIONS.value,
                        name=account.get("Name"),
                        region="global",
                        network_id=network_id,
                        subnetwork_id=subnetwork_id,
                        status=account.get("Status"),
                        tags=tags,
                        raw=account,
                    )
                )
    except client.exceptions.AWSOrganizationsNotInUseException:
        return []
    return resources


def collect_kms_keys(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect KMS keys."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("kms")
    paginator = client.get_paginator("list_keys")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for key in page.get("Keys", []):
            metadata = client.describe_key(KeyId=key.get("KeyId"))["KeyMetadata"]
            tags = _kms_tags(client, key.get("KeyId"))
            network_id, subnetwork_id = extract_network_info(metadata)
            resources.append(
                Resource(
                    id=metadata.get("Arn"),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.SECURITY.value,
                    resource=AwsResource.KMS.value,
                    name=metadata.get("Description") or metadata.get("KeyId"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status="Enabled" if metadata.get("Enabled") else "Disabled",
                    tags=tags,
                    raw=metadata,
                )
            )
    return resources


def collect_secrets_manager_secrets(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect Secrets Manager secrets."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("secretsmanager")
    paginator = client.get_paginator("list_secrets")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for secret in page.get("SecretList", []):
            tags = {
                t.get("Key"): t.get("Value")
                for t in secret.get("Tags", [])
                if t.get("Key")
            }
            network_id, subnetwork_id = extract_network_info(secret)
            resources.append(
                Resource(
                    id=secret.get("ARN"),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.SECURITY.value,
                    resource=AwsResource.SECRETS_MANAGER.value,
                    name=secret.get("Name"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status="deleted" if secret.get("DeletedDate") else "active",
                    tags=tags,
                    raw=secret,
                )
            )
    return resources


def collect_acm_certificates(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect ACM certificates."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("acm")
    paginator = client.get_paginator("list_certificates")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for summary in page.get("CertificateSummaryList", []):
            arn = summary.get("CertificateArn")
            detail = client.describe_certificate(CertificateArn=arn)["Certificate"]
            tags = _acm_tags(client, arn)
            network_id, subnetwork_id = extract_network_info(detail)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.SECURITY.value,
                    resource=AwsResource.ACM.value,
                    name=summary.get("DomainName"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=detail.get("Status"),
                    tags=tags,
                    raw=detail,
                )
            )
    return resources


def collect_waf_acls(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect WAFv2 Web ACLs for regional and CloudFront scopes."""

    boto_session = get_boto3_session(session=session, region=region)
    region_name = region or boto_session.region_name or "us-east-1"
    regional_client = boto_session.client("wafv2", region_name=region_name)
    global_client = boto_session.client("wafv2", region_name="us-east-1")

    resources: List[Resource] = []
    resources.extend(_waf_scope_acls(regional_client, "REGIONAL"))
    resources.extend(_waf_scope_acls(global_client, "CLOUDFRONT"))
    return resources


def collect_shield_protections(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect AWS Shield protections."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("shield", region_name="us-east-1")

    resources: List[Resource] = []
    next_token: Optional[str] = None
    try:
        while True:
            params = {"NextToken": next_token} if next_token else {}
            response = client.list_protections(**params)
            for protection in response.get("Protections", []):
                tags = _shield_tags(client, protection.get("ProtectionArn"))
                network_id, subnetwork_id = extract_network_info(protection)
                resources.append(
                    Resource(
                        id=protection.get("ProtectionArn"),
                        provider=Provider.AWS.value,
                        kind=ResourceKind.SECURITY.value,
                        resource=AwsResource.SHIELD.value,
                        name=protection.get("Name"),
                        region="global",
                        network_id=network_id,
                        subnetwork_id=subnetwork_id,
                        status=None,
                        tags=tags,
                        raw=protection,
                    )
                )
            next_token = response.get("NextToken")
            if not next_token:
                break
    except client.exceptions.ResourceNotFoundException:
        return []
    return resources


def collect_guardduty_detectors(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect GuardDuty detectors."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("guardduty")
    sts = boto_session.client("sts")
    account_id = sts.get_caller_identity().get("Account")

    resources: List[Resource] = []
    detector_ids = client.list_detectors().get("DetectorIds", [])
    for detector_id in detector_ids:
        info = client.get_detector(DetectorId=detector_id)
        arn = f"arn:aws:guardduty:{client.meta.region_name}:{account_id}:detector/{detector_id}"
        tags = _guardduty_tags(client, arn)
        network_id, subnetwork_id = extract_network_info(info)
        resources.append(
            Resource(
                id=arn,
                provider=Provider.AWS.value,
                kind=ResourceKind.SECURITY.value,
                resource=AwsResource.GUARDDUTY.value,
                name=detector_id,
                region=client.meta.region_name,
                network_id=network_id,
                subnetwork_id=subnetwork_id,
                status=info.get("Status"),
                tags=tags,
                raw=info,
            )
        )
    return resources


def collect_security_hub_hubs(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect Security Hub configuration."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("securityhub")

    try:
        hub = client.describe_hub()
    except client.exceptions.InvalidAccessException:
        return []

    hub_arn = hub.get("HubArn")
    tags = _security_hub_tags(client, hub_arn)
    network_id, subnetwork_id = extract_network_info(hub)
    resource = Resource(
        id=hub_arn,
        provider=Provider.AWS.value,
        kind=ResourceKind.SECURITY.value,
        resource=AwsResource.SECURITY_HUB.value,
        name=hub.get("HubArn"),
        region=client.meta.region_name,
        network_id=network_id,
        subnetwork_id=subnetwork_id,
        status="enabled",
        tags=tags,
        raw=hub,
    )
    return [resource]


def _iam_role_tags(client, role_name: Optional[str]) -> dict:
    if not role_name:
        return {}
    try:
        response = client.list_role_tags(RoleName=role_name)
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("Tags", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _organization_account_tags(client, account_id: Optional[str]) -> dict:
    if not account_id:
        return {}
    try:
        response = client.list_tags_for_resource(ResourceId=account_id)
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("Tags", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _kms_tags(client, key_id: Optional[str]) -> dict:
    if not key_id:
        return {}
    try:
        response = client.list_resource_tags(KeyId=key_id)
        return {
            t.get("TagKey"): t.get("TagValue")
            for t in response.get("Tags", [])
            if t.get("TagKey")
        }
    except ClientError:
        return {}


def _acm_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_for_certificate(CertificateArn=arn)
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("Tags", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _waf_scope_acls(client, scope: str) -> List[Resource]:
    resources: List[Resource] = []
    marker: Optional[str] = None
    while True:
        params = {"Scope": scope, "Limit": 100}
        if marker:
            params["NextMarker"] = marker
        try:
            response = client.list_web_acls(**params)
        except ClientError:
            break
        for acl in response.get("WebACLs", []):
            arn = acl.get("ARN", acl.get("Id"))
            tags = _waf_tags(client, arn)
            network_id, subnetwork_id = extract_network_info(acl)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.SECURITY.value,
                    resource=AwsResource.WAF.value,
                    name=acl.get("Name"),
                    region="global"
                    if scope == "CLOUDFRONT"
                    else client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=acl.get("Description"),
                    tags=tags,
                    raw=acl,
                )
            )
        marker = response.get("NextMarker")
        if not marker:
            break
    return resources


def _waf_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_for_resource(ResourceARN=arn)
        return {
            t.get("Key"): t.get("Value")
            for t in response.get("TagInfoForResource", {}).get("TagList", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _shield_tags(client, arn: Optional[str]) -> dict:
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


def _guardduty_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_for_resource(ResourceArn=arn)
        return response.get("Tags", {}) or {}
    except ClientError:
        return {}


def _security_hub_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_for_resource(ResourceArn=arn)
        return response.get("Tags", {}) or {}
    except ClientError:
        return {}
