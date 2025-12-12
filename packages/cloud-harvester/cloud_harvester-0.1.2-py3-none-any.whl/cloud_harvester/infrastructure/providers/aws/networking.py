from __future__ import annotations

from typing import List, Optional

from botocore.exceptions import ClientError

from cloud_harvester.domain.enums import AwsResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.aws.auth import get_boto3_session
from cloud_harvester.infrastructure.providers.aws.utils import extract_network_info


def collect_vpc(session=None, region: Optional[str] = None) -> List[Resource]:
    """Collect AWS VPCs and normalize them to the Resource model."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("ec2")
    paginator = client.get_paginator("describe_vpcs")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for vpc in page.get("Vpcs", []):
            tags = (
                {t["Key"]: t["Value"] for t in vpc.get("Tags", [])}
                if vpc.get("Tags")
                else {}
            )
            network_id, subnetwork_id = extract_network_info(vpc)
            resources.append(
                Resource(
                    id=vpc["VpcId"],
                    provider=Provider.AWS.value,
                    kind=ResourceKind.NETWORK.value,
                    resource=AwsResource.VPC.value,
                    name=tags.get("Name", vpc.get("VpcId")),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=vpc.get("State"),
                    tags=tags,
                    raw=vpc,
                )
            )
    return resources


def collect_elbv2_load_balancers(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect Application/Network/Gateway Load Balancers."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("elbv2")
    paginator = client.get_paginator("describe_load_balancers")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for lb in page.get("LoadBalancers", []):
            tags = _elbv2_tags(client, lb.get("LoadBalancerArn"))
            lb_state = (lb.get("State") or {}).get("Code")
            network_id, subnetwork_id = extract_network_info(lb)
            resources.append(
                Resource(
                    id=lb.get("LoadBalancerArn", lb.get("DNSName")),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.NETWORK.value,
                    resource=AwsResource.ELB.value,
                    name=lb.get("LoadBalancerName"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=lb_state,
                    tags=tags,
                    raw=lb,
                )
            )
    return resources


def collect_classic_elb_load_balancers(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect Classic Load Balancers."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("elb")
    paginator = client.get_paginator("describe_load_balancers")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for lb in page.get("LoadBalancerDescriptions", []):
            name = lb.get("LoadBalancerName")
            tags = _classic_elb_tags(client, name)
            network_id, subnetwork_id = extract_network_info(lb)
            resources.append(
                Resource(
                    id=name,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.NETWORK.value,
                    resource=AwsResource.CLASSIC_ELB.value,
                    name=name,
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=None,
                    tags=tags,
                    raw=lb,
                )
            )
    return resources


def collect_api_gateway_rest_apis(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect API Gateway REST APIs."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("apigateway")
    paginator = client.get_paginator("get_rest_apis")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for api in page.get("items", []):
            arn = f"arn:aws:apigateway:{client.meta.region_name}::/restapis/{api['id']}"
            tags = _api_gateway_tags(client, arn)
            status = "disabled" if api.get("disableExecuteApiEndpoint") else "available"
            network_id, subnetwork_id = extract_network_info(api)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.NETWORK.value,
                    resource=AwsResource.API_GATEWAY_REST.value,
                    name=api.get("name"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=status,
                    tags=tags,
                    raw=api,
                )
            )
    return resources


def collect_api_gateway_http_apis(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect API Gateway HTTP/WebSocket APIs."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("apigatewayv2")
    paginator = client.get_paginator("get_apis")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for api in page.get("Items", []):
            arn = f"arn:aws:apigateway:{client.meta.region_name}::/apis/{api['ApiId']}"
            tags = _api_gateway_v2_tags(client, arn)
            network_id, subnetwork_id = extract_network_info(api)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.NETWORK.value,
                    resource=AwsResource.API_GATEWAY_HTTP.value,
                    name=api.get("Name"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=api.get("ProtocolType"),
                    tags=tags,
                    raw=api,
                )
            )
    return resources


def collect_route53_hosted_zones(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect Route 53 hosted zones."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("route53")
    paginator = client.get_paginator("list_hosted_zones")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for zone in page.get("HostedZones", []):
            zone_id = zone.get("Id", "").split("/")[-1]
            tags = _route53_tags(client, zone_id)
            visibility = (
                "private" if zone.get("Config", {}).get("PrivateZone") else "public"
            )
            network_id, subnetwork_id = extract_network_info(zone)
            resources.append(
                Resource(
                    id=zone.get("Id"),
                    provider=Provider.AWS.value,
                    kind=ResourceKind.NETWORK.value,
                    resource=AwsResource.ROUTE53.value,
                    name=zone.get("Name"),
                    region="global",
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=visibility,
                    tags=tags,
                    raw=zone,
                )
            )
    return resources


def collect_cloudfront_distributions(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect CloudFront distributions."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("cloudfront")
    paginator = client.get_paginator("list_distributions")

    resources: List[Resource] = []
    for page in paginator.paginate():
        distribution_list = page.get("DistributionList", {})
        for distribution in distribution_list.get("Items", []):
            arn = distribution.get("ARN")
            tags = _cloudfront_tags(client, arn)
            network_id, subnetwork_id = extract_network_info(distribution)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.NETWORK.value,
                    resource=AwsResource.CLOUDFRONT.value,
                    name=distribution.get("Id"),
                    region="global",
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=distribution.get("Status"),
                    tags=tags,
                    raw=distribution,
                )
            )
    return resources


def _elbv2_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.describe_tags(ResourceArns=[arn])
        tag_descriptions = response.get("TagDescriptions", [])
        if not tag_descriptions:
            return {}
        tags = tag_descriptions[0].get("Tags", [])
        return {t.get("Key"): t.get("Value") for t in tags if t.get("Key")}
    except ClientError:
        return {}


def _classic_elb_tags(client, name: Optional[str]) -> dict:
    if not name:
        return {}
    try:
        response = client.describe_tags(LoadBalancerNames=[name])
        descriptions = response.get("TagDescriptions", [])
        if not descriptions:
            return {}
        tags = descriptions[0].get("Tags", [])
        return {t.get("Key"): t.get("Value") for t in tags if t.get("Key")}
    except ClientError:
        return {}


def _api_gateway_tags(client, arn: str) -> dict:
    try:
        response = client.get_tags(resourceArn=arn)
        return response.get("tags", {}) or {}
    except ClientError:
        return {}


def _api_gateway_v2_tags(client, arn: str) -> dict:
    try:
        response = client.get_tags(ResourceArn=arn)
        return response.get("Tags", {}) or {}
    except ClientError:
        return {}


def _route53_tags(client, zone_id: str) -> dict:
    if not zone_id:
        return {}
    try:
        response = client.list_tags_for_resource(
            ResourceType="hostedzone", ResourceId=zone_id
        )
        tag_set = response.get("ResourceTagSet", {})
        return {
            t.get("Key"): t.get("Value")
            for t in tag_set.get("Tags", [])
            if t.get("Key")
        }
    except ClientError:
        return {}


def _cloudfront_tags(client, arn: Optional[str]) -> dict:
    if not arn:
        return {}
    try:
        response = client.list_tags_for_resource(Resource=arn)
        items = response.get("Tags", {}).get("Items", [])
        return {t.get("Key"): t.get("Value") for t in items if t.get("Key")}
    except ClientError:
        return {}
