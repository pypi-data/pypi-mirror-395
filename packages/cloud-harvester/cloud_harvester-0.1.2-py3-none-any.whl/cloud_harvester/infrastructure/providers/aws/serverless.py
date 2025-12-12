from __future__ import annotations

from typing import List, Optional

from botocore.exceptions import ClientError

from cloud_harvester.domain.enums import AwsResource, Provider, ResourceKind
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers.aws.auth import get_boto3_session
from cloud_harvester.infrastructure.providers.aws.utils import extract_network_info


def collect_lambda_functions(
    session=None, region: Optional[str] = None
) -> List[Resource]:
    """Collect AWS Lambda functions."""

    boto_session = get_boto3_session(session=session, region=region)
    client = boto_session.client("lambda")
    paginator = client.get_paginator("list_functions")

    resources: List[Resource] = []
    for page in paginator.paginate():
        for fn in page.get("Functions", []):
            arn = fn["FunctionArn"]
            tags = _get_lambda_tags(client, arn)
            status = fn.get("State") or fn.get("LastUpdateStatus")
            network_id, subnetwork_id = extract_network_info(fn)
            resources.append(
                Resource(
                    id=arn,
                    provider=Provider.AWS.value,
                    kind=ResourceKind.COMPUTE.value,
                    resource=AwsResource.LAMBDA.value,
                    name=fn.get("FunctionName"),
                    region=client.meta.region_name,
                    network_id=network_id,
                    subnetwork_id=subnetwork_id,
                    status=status,
                    tags=tags,
                    raw=fn,
                )
            )
    return resources


def _get_lambda_tags(client, arn: str) -> dict:
    try:
        response = client.list_tags(Resource=arn)
        return response.get("Tags", {}) or {}
    except ClientError:
        return {}
