import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import ipaddress
import os
import sys
import json
import re

# --- PATH CONFIGURATION ---
# 1. Get the directory where this script is installed (e.g., inside site-packages)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Define the Read-Only Config Source (packaged with your code)
SOURCE_FILE = os.path.join(PACKAGE_DIR, "data", "vpn_sources.json")

# 3. Define the Writable Cache Location (User's Home Directory)
# We use the user's home folder to avoid "Permission Denied" errors in Program Files
USER_HOME = os.path.expanduser("~")
WORK_DIR = os.path.join(USER_HOME, ".kavachnet")

# Create the hidden directory if it doesn't exist
if not os.path.exists(WORK_DIR):
    try:
        os.makedirs(WORK_DIR)
    except OSError as e:
        print(f"[ERROR] Could not create cache directory at {WORK_DIR}: {e}")

CACHE_FILE = os.path.join(WORK_DIR, "vpn_ip_list.txt")

TIMEOUT = 15
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
# ---------------------------

# ... (Keep the rest of your functions: get_latest_azure, load_sources, etc. exactly the same) ...

def get_latest_azure():
    """Fetch the latest Azure ServiceTags JSON filename dynamically."""
    try:
        session = requests.Session()
        resp = session.get("https://www.microsoft.com/en-us/download/details.aspx?id=56519", timeout=10, headers=HEADERS)
        resp.raise_for_status()
        match = re.search(r'ServiceTags_Public_(\d{8})\.json', resp.text)
        if match:
            date_str = match.group(1)
            return f"https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_{date_str}.json"
    except Exception as e:
        print(f"[WARN] Could not fetch latest Azure filename: {e}")
    # Fallback to current known-good (update manually every few months if needed)
    return "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20251117.json"

def load_sources():
    """Load typed source URLs from JSON config file."""
    if not os.path.exists(SOURCE_FILE):
        raise FileNotFoundError(f"{SOURCE_FILE} not found.")
    with open(SOURCE_FILE, 'r') as f:
        data = json.load(f)
    return data  # dict with keys: VPN, TOR, PROXY, CLOUD, VPN_API

def extract_ips_from_text(text):
    lines = text.splitlines()
    cleaned = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "," in line:
            line = line.split(",")[0].strip()
        cleaned.add(line)
    return cleaned

def extract_ips_from_json(data):
    ips = set()
    if isinstance(data, dict):
        if "prefixes" in data:
            for p in data["prefixes"]:
                for key in ["ip_prefix", "ipv4Prefix", "ipv6Prefix"]:
                    if key in p:
                        ips.add(p[key])
        if "vultr" in data:
            for p in data["vultr"]:
                ips.add(p)
        if "LogicalServers" in data:
            for p in data["LogicalServers"]:
                if "EntryIP" in p:
                    ips.add(p["EntryIP"])
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                ips.add(item)
            elif isinstance(item, dict):
                for key in ["ip", "ipv4", "ipv6", "ip_prefix", "ipv4Prefix", "ipv6Prefix", "ip_address", "EntryIP"]:
                    if key in item:
                        ips.add(item[key])
    return ips

def get_session():
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def download_list(url):
    try:
        session = get_session()
        resp = session.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        text = resp.text.strip()
        if "application/json" in resp.headers.get("Content-Type", "") or text.startswith("{") or text.startswith("["):
            try:
                data = json.loads(text)
                return extract_ips_from_json(data)
            except Exception:
                return extract_ips_from_text(text)
        elif "," in text:
            return extract_ips_from_text(text)
        else:
            return extract_ips_from_text(text)
    except Exception as e:
        print(f"[WARN] Could not fetch {url}: {e}")
        return set()

def load_cached_ips(cache_path=None):
    if cache_path is None:
        cache_path = CACHE_FILE
    if not os.path.exists(cache_path):
        return {}
    cached = {}
    with open(cache_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # format: IP|TYPE
            if "|" in line:
                ip, t = line.split("|", 1)
                cached[ip] = t
            else:
                cached[line] = "UNKNOWN"
    return cached

def append_to_cache(entries, cache_path=None):
    if not entries:
        return
    if cache_path is None:
        cache_path = CACHE_FILE
    with open(cache_path, 'a', encoding='utf-8') as f:
        for ip, t in entries.items():
            # Safety filter: only allow real IPs/CIDRs and clean types
            if isinstance(ip, str) and ('/' in ip or ip.replace('.', '').replace(':', '').isdigit()):
                safe_type = t.replace('|', '').replace('\n', '').strip()
                f.write(f"{ip}|{safe_type}\n")

def refresh_cache(cache_path=None):
    typed_sources = load_sources()
    cached = load_cached_ips(cache_path)
    total_new = {}
    
    # Dynamically replace Azure URL with the latest one
    azure_url = get_latest_azure()
    print(f"[i] Using latest Azure URL: {azure_url}")
    typed_sources["CLOUD"] = [azure_url if url == "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20251124.json" else url for url in typed_sources["CLOUD"]]
    
    for t, urls in typed_sources.items():
        for url in urls:
            print(f"[i] Fetching {url}")
            fetched = download_list(url)
            new_entries = {ip: t for ip in fetched if ip not in cached}
            if new_entries:
                print(f"    + {len(new_entries)} new entries found for type {t}")
                total_new.update(new_entries)
                cached.update(new_entries)

    append_to_cache(total_new, cache_path)
    print(f"[✓] Cache updated with {len(total_new)} new entries.")
    return cached, len(total_new)  # Changed: Return tuple (data, count)

def load_networks_from_cache(cached_data):
    """
    Converts the cached dictionary {ip_str: type_str} into a list of 
    (ip_network, type_str) tuples for the detector to use.
    """
    all_networks = []
    
    # Handle the case where app.py passes the dictionary from refresh_cache
    if isinstance(cached_data, dict):
        iterator = cached_data.items()
    else:
        # Fallback if passed a list of files (legacy support, though not used by app.py)
        return []

    for ip_str, ip_type in iterator:
        try:
            # Create ip_network object for efficient matching
            # strict=False allows bits set after the prefix length (common in some lists)
            net = ipaddress.ip_network(ip_str, strict=False)
            all_networks.append((net, ip_type))
        except ValueError:
            continue
            
    return all_networks

def is_vpn_ip(ip, networks):
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return None
    
    # networks is now a list of tuples: (ip_network_object, type_string)
    for net, t in networks:
        if ip_obj in net:
            return t
    return None

def print_usage():
    print("Usage: python vpn_checker.py <IPv4 or IPv6 address>")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()

    target = sys.argv[1]

    print("[i] Refreshing VPN/IP cache (only new entries will be added)...")
    cached, _ = refresh_cache()  # Changed: Unpack tuple (ignore count here)

    print("[i] Loading networks from cache...")
    nets = load_networks_from_cache(cached)

    print(f"[i] Checking IP: {target}")
    ip_type = is_vpn_ip(target, nets)
    if ip_type:
        print(f"→ 🚨 IP detected as {ip_type} (VPN / Proxy / Tor / Cloud).")
    else:
        print("→ ✅ IP not found in VPN / Proxy / Tor / Cloud lists.")