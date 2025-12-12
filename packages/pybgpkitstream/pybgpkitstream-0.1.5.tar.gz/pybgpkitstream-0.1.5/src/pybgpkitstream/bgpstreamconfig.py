import datetime
from pydantic import BaseModel, Field, DirectoryPath, field_validator
from typing import Literal
from ipaddress import IPv4Address, IPv6Address


class FilterOptions(BaseModel):
    """A unified model for the available filter options."""

    origin_asn: int | None = Field(
        default=None, description="Filter by the origin AS number."
    )
    prefix: str | None = Field(
        default=None, description="Filter by an exact prefix match."
    )
    prefix_super: str | None = Field(
        default=None,
        description="Filter by the exact prefix and its more general super-prefixes.",
    )
    prefix_sub: str | None = Field(
        default=None,
        description="Filter by the exact prefix and its more specific sub-prefixes.",
    )
    prefix_super_sub: str | None = Field(
        default=None,
        description="Filter by the exact prefix and both its super- and sub-prefixes.",
    )
    peer_ip: str | IPv4Address | IPv6Address | None = Field(
        default=None, description="Filter by the IP address of a single BGP peer."
    )
    peer_ips: list[str | IPv4Address | IPv6Address] | None = Field(
        default=None, description="Filter by a list of BGP peer IP addresses."
    )
    peer_asn: str | None = Field(
        default=None, description="Filter by the AS number of the BGP peer."
    )
    update_type: Literal["withdraw", "announce"] | None = Field(
        default=None, description="Filter by the BGP update message type."
    )
    as_path: str | None = Field(
        default=None, description="Filter by a regular expression matching the AS path."
    )
    ip_version: Literal["ipv4", "ipv6"] | None = Field(
        default=None, description="Filter by ip version."
    )


class BGPStreamConfig(BaseModel):
    """
    Unified BGPStream config.

    Filters are primarily written for BGPKit but utils to convert to pybgpstream are provided in tests/pybgpstream_utils.
    """

    start_time: datetime.datetime = Field(description="Start of the stream")
    end_time: datetime.datetime = Field(description="End of the stream")
    collectors: list[str] = Field(description="List of collectors to get data from")
    data_types: list[Literal["ribs", "updates"]] = Field(
        description="List of archives files to consider (`ribs` or `updates`)"
    )
    cache_dir: DirectoryPath | None = Field(
        default=None,
        description="Specifies the directory for caching downloaded files.",
    )
    filters: FilterOptions | None = Field(default=None, description="Optional filters")
    max_concurrent_downloads: int | None = Field(
        default=None, description="Maximum concurrent downloads when caching"
    )
    chunk_time: datetime.timedelta | None = Field(
        default=datetime.timedelta(hours=2),
        description="Interval for the fetch/parse cycle (avoid long prefetch time)",
    )

    @field_validator("start_time", "end_time")
    @classmethod
    def normalize_to_utc(cls, dt: datetime.datetime) -> datetime.datetime:
        # if naive datetime (not timezone-aware) assume it's UTC
        if dt.tzinfo is None:
            return dt.replace(tzinfo=datetime.timezone.utc)
        # if timezone-aware, convert to utc
        else:
            return dt.astimezone(datetime.timezone.utc)
