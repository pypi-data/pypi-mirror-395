from __future__ import annotations

import logging
from typing import Callable, Dict, Iterable, List, Optional, Sequence

from cloud_harvester.domain.enums import Provider
from cloud_harvester.domain.models import Resource
from cloud_harvester.infrastructure.providers import aws as aws_provider
from cloud_harvester.infrastructure.providers import azure as azure_provider

CollectorFn = Callable[..., List[Resource]]
logger = logging.getLogger(__name__)


def collect_resources(
    providers: Optional[Sequence[str]] = None,
    aws_session=None,
    aws_region: Optional[str] = None,
    azure_credential=None,
    azure_subscription_id: Optional[str] = None,
    collectors: Optional[Dict[str, Iterable[CollectorFn]]] = None,
) -> List[Resource]:
    """
    Application use case: gather cloud resources from multiple providers.

    Dependency injection:
        collectors: optional mapping of provider -> iterable of collector callables.
                    Defaults to built-in collectors.
        aws_session/aws_region: forwarded to AWS collectors to reuse auth/config.
    """
    selected = (
        {p.lower() for p in providers}
        if providers
        else {Provider.AWS.value, Provider.AZURE.value}
    )
    all_collectors = collectors or _default_collectors()

    resources: List[Resource] = []
    for provider in selected:
        provider_collectors = all_collectors.get(provider)
        if not provider_collectors:
            logger.warning("No collectors configured for provider '%s'", provider)
            continue

        for collector in provider_collectors:
            collector_name = getattr(collector, "__name__", str(collector))
            logger.info("Collecting resources via %s/%s", provider, collector_name)
            try:
                if provider == Provider.AWS.value:
                    collected = collector(session=aws_session, region=aws_region)
                else:
                    collected = collector(
                        credential=azure_credential,
                        subscription_id=azure_subscription_id,
                    )
                resources.extend(collected)
                logger.info(
                    "Collector %s/%s returned %d resources",
                    provider,
                    collector_name,
                    len(collected),
                )
            except Exception as exc:  # pragma: no cover - logging path
                logger.error(
                    "Collector %s/%s failed: %s",
                    provider,
                    collector_name,
                    exc,
                    exc_info=False,
                )

    return resources


def _default_collectors() -> Dict[str, Iterable[CollectorFn]]:
    return {
        Provider.AWS.value: aws_provider.AWS_COLLECTORS,
        Provider.AZURE.value: azure_provider.AZURE_COLLECTORS,
    }
