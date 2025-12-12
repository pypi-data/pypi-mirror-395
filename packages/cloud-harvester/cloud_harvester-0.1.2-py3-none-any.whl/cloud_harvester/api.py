from __future__ import annotations

from typing import List, Optional, Sequence

from cloud_harvester.application.collect_resources import collect_resources
from cloud_harvester.domain.models import Resource

__all__ = ["collect"]


def collect(
    providers: Optional[Sequence[str]] = None,
    aws_session=None,
    aws_region: Optional[str] = None,
    azure_credential=None,
    azure_subscription_id: Optional[str] = None,
) -> List[Resource]:
    """
    Collect resources from configured providers (application layer entry point).
    """
    return collect_resources(
        providers=providers,
        aws_session=aws_session,
        aws_region=aws_region,
        azure_credential=azure_credential,
        azure_subscription_id=azure_subscription_id,
    )
