from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address, IPv6Address


class IPRegistryLookup(IPLookupSource):
    """Perform IP lookups using the IPRegistry API."""

    SOURCE_NAME: ClassVar[str] = "ipregistry.co"
    API_URL: ClassVar[str] = "https://api.ipregistry.co/{ip}"
    REQUIRES_USER_KEY: ClassVar[bool] = True
    API_KEY_PARAM: ClassVar[str | None] = "key"

    @classmethod
    def _parse_response(
        cls, data: dict[str, Any], ip_obj: IPv4Address | IPv6Address
    ) -> IPLookupResult:
        """Parse the IPRegistry API response into a LookupResult."""
        # Handle the case where the response has a 'results' array
        if "results" in data and isinstance(data["results"], list) and data["results"]:
            data = data["results"][0]

        result = IPLookupResult(ip=ip_obj, source=cls.SOURCE_NAME)

        cls._extract_location_info(data, result)
        cls._extract_connection_info(data, result)
        cls._extract_security_info(data, result)

        return result

    @classmethod
    def _extract_location_info(cls, data: dict[str, Any], result: IPLookupResult) -> None:
        """Extract location information from the location field."""
        if location := data.get("location", {}):
            if country := location.get("country", {}):
                result.country = country.get("name")

            if region := location.get("region", {}):
                result.region = region.get("name")

            result.city = location.get("city")

    @classmethod
    def _extract_connection_info(cls, data: dict[str, Any], result: IPLookupResult) -> None:
        """Extract organization, ISP, and ASN information from connection field."""
        if connection := data.get("connection", {}):
            result.isp = connection.get("domain")
            result.org = connection.get("organization")

            # Extract ASN information if available
            if asn_num := connection.get("asn"):
                result.asn = f"AS{asn_num}" if not str(asn_num).startswith("AS") else str(asn_num)
            if asn_name := connection.get("organization"):
                result.asn_name = asn_name
            if route := connection.get("route"):
                result.ip_range = route

        elif company := data.get("company", {}):
            result.org = company.get("name")

    @classmethod
    def _extract_security_info(cls, data: dict[str, Any], result: IPLookupResult) -> None:
        """Extract security-related information from the security field."""
        if security := data.get("security", {}):
            result.is_vpn = security.get("is_vpn")
            result.is_proxy = security.get("is_proxy")
            result.is_tor = security.get("is_tor")
            result.is_datacenter = security.get("is_cloud_provider")
            result.is_anonymous = security.get("is_anonymous")
