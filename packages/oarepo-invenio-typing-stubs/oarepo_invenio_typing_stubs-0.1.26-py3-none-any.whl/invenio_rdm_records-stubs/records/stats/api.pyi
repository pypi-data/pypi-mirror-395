from __future__ import annotations

from typing import TypedDict

class _VersionStats(TypedDict):
    views: int
    unique_views: int
    downloads: int
    unique_downloads: int
    data_volume: int

class _RecordStats(TypedDict):
    this_version: _VersionStats
    all_versions: _VersionStats

class Statistics:
    @classmethod
    def _get_query(cls, query_name: str): ...
    @classmethod
    def get_record_stats(cls, recid: str, parent_recid: str) -> _RecordStats: ...
