from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from iplooker.lookup_result import IPLookupResult
from iplooker.lookup_source import IPLookupSource

if TYPE_CHECKING:
    from ipaddress import IPv4Address, IPv6Address


class IPInfoLookup(IPLookupSource):
    """Perform IP lookups using the ipinfo.io service."""

    SOURCE_NAME: ClassVar[str] = "ipinfo.io"
    API_URL: ClassVar[str] = "https://ipinfo.io/{ip}/json"
    API_KEY_PARAM: ClassVar[str | None] = "token"
    ERROR_KEYS: ClassVar[list[str]] = ["error", "message"]

    @classmethod
    def _parse_response(
        cls, data: dict[str, Any], ip_obj: IPv4Address | IPv6Address
    ) -> IPLookupResult:
        """Parse the ipinfo.io response into a LookupResult."""
        result = IPLookupResult(
            ip=ip_obj,
            source=cls.SOURCE_NAME,
            country=data.get("country"),
            region=data.get("region"),
            city=data.get("city"),
        )

        cls._extract_organization_info(data, result)
        cls._extract_asn_info(data, result)
        cls._extract_security_info(data, result)

        # Extract IP range/CIDR if available
        if cidr := data.get("cidr"):
            result.ip_range = cidr

        return result

    @classmethod
    def _extract_organization_info(cls, data: dict[str, Any], result: IPLookupResult) -> None:
        """Extract organization and ISP information from the org field."""
        if org := data.get("org"):
            # The org field often has format "AS#### Organization Name"
            if " " in org and len(org.split(" ", 1)) > 1:
                asn_part, org_name = org.split(" ", 1)
                result.asn = asn_part
                result.asn_name = org_name
                result.isp = org_name
                result.org = org_name
            else:
                result.org = org

        # Try company field if available
        if not result.org and (company := data.get("company")):
            if isinstance(company, dict):
                result.org = company.get("name")
            elif isinstance(company, str):
                result.org = company

    @classmethod
    def _extract_asn_info(cls, data: dict[str, Any], result: IPLookupResult) -> None:
        """Extract ASN information from the asn field if not already set."""
        if result.isp:
            return  # Already have ISP info from org field

        if asn := data.get("asn"):
            if isinstance(asn, dict):
                result.isp = asn.get("name") or asn.get("domain")
                if not result.asn:
                    result.asn = asn.get("asn")
                if not result.asn_name:
                    result.asn_name = asn.get("name")
            elif isinstance(asn, str) and " " in asn:
                asn_part, isp_name = asn.split(" ", 1)
                result.isp = isp_name
                if not result.asn:
                    result.asn = asn_part
                if not result.asn_name:
                    result.asn_name = isp_name

    @classmethod
    def _extract_security_info(cls, data: dict[str, Any], result: IPLookupResult) -> None:
        """Extract security-related information from the privacy field."""
        if privacy := data.get("privacy", {}):
            result.is_vpn = privacy.get("vpn")
            result.is_proxy = privacy.get("proxy")
            result.is_tor = privacy.get("tor")
            result.is_datacenter = privacy.get("hosting")
            result.vpn_service = privacy.get("service") or None
