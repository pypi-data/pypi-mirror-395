# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["RequestCreateDownloadParams"]


class RequestCreateDownloadParams(TypedDict, total=False):
    bucket_name: Required[str]

    crawl_id: Required[str]

    downloader_type: Required[str]

    urls: Required[SequenceNotStr[str]]
