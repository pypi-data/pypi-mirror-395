"""
KavachNet - AI-based VPN & Proxy Detector
"""

# Import key functions so users can access them directly from the package
from .vpn_checker import is_vpn_ip, refresh_cache, load_networks_from_cache, load_cached_ips

# Define the package version (should match pyproject.toml)
__version__ = "0.1.17"