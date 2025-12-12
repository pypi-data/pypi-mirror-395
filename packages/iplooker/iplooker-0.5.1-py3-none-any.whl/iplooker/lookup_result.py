from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipaddress import IPv4Address, IPv6Address


@dataclass
class IPLookupResult:
    """Dataclass to hold the result of an IP lookup from a single source."""

    ip: IPv4Address | IPv6Address
    source: str
    country: str | None = None
    region: str | None = None
    city: str | None = None
    isp: str | None = None
    org: str | None = None

    # Network information
    asn: str | None = None  # ASN number (e.g., "AS15169")
    asn_name: str | None = None  # ASN organization name
    ip_range: str | None = None  # IP range/block in CIDR notation

    # Security information
    is_vpn: bool | None = None
    vpn_service: str | None = None
    is_proxy: bool | None = None
    is_tor: bool | None = None
    is_datacenter: bool | None = None
    is_anonymous: bool | None = None
