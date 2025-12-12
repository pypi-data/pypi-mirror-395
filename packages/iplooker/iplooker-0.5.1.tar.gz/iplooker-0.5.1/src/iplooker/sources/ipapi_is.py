from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address, IPv6Address


class IPAPIIsLookup(IPLookupSource):
    """Perform IP lookups using the ipapi.is service."""

    SOURCE_NAME: ClassVar[str] = "ipapi.is"
    API_URL: ClassVar[str] = "https://api.ipapi.is?ip={ip}"
    API_KEY_PARAM: ClassVar[str | None] = "key"

    @classmethod
    def _parse_response(
        cls, data: dict[str, Any], ip_obj: IPv4Address | IPv6Address
    ) -> IPLookupResult:
        """Parse the ipapi.is response into a LookupResult."""
        result = IPLookupResult(ip=ip_obj, source=cls.SOURCE_NAME)

        # Extract location data
        if location := data.get("location", {}):
            result.country = location.get("country")
            result.region = location.get("state")
            result.city = location.get("city")

        # Extract organization data
        if company := data.get("company", {}):
            result.org = company.get("name")

        # Extract ASN information
        if asn := data.get("asn", {}):
            if asn_num := asn.get("asn"):
                result.asn = f"AS{asn_num}" if not str(asn_num).startswith("AS") else str(asn_num)
            result.asn_name = asn.get("org") or asn.get("name")

            # If no org was found in company, use asn org
            if not result.org:
                result.org = asn.get("org")

            # Use ASN domain for ISP if datacenter not available
            if not result.isp:
                result.isp = asn.get("domain")

            # Extract IP range if available
            if route := asn.get("route"):
                result.ip_range = route

        # Extract ISP information (datacenter info can serve as ISP)
        if datacenter := data.get("datacenter", {}):
            result.isp = datacenter.get("datacenter")

        # Security information
        result.is_vpn = data.get("is_vpn")
        result.is_proxy = data.get("is_proxy")
        result.is_tor = data.get("is_tor")
        result.is_datacenter = data.get("is_datacenter")

        if (vpn := data.get("vpn", {})) and vpn.get("is_vpn") and vpn.get("service"):
            result.vpn_service = vpn.get("service")

        return result
