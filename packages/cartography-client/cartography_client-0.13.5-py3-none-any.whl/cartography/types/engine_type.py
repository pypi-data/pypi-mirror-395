# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["EngineType"]

EngineType: TypeAlias = Literal[
    "FLEET", "ZENROWS", "SCRAPINGBEE", "FLEET_ASYNC", "FLEET_WORKFLOW", "ASYNC_FLEET_STICKY"
]
