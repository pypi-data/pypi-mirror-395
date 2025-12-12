import os
from typing import Optional

import boto3


def get_boto3_session(session=None, region: Optional[str] = None):
    """
    Return a boto3 Session using default credential chain with optional overrides.

    Credentials are resolved in this order:
    1) Provided session
    2) CLOUD_HARVESTER_AWS_PROFILE or AWS_PROFILE (profile-based)
    3) Environment/EC2/ECS/SSO defaults handled by boto3
    """
    if session:
        return session

    profile = os.getenv("CLOUD_HARVESTER_AWS_PROFILE") or os.getenv("AWS_PROFILE")
    region_override = region or os.getenv("CLOUD_HARVESTER_AWS_REGION")
    return boto3.Session(profile_name=profile, region_name=region_override)
