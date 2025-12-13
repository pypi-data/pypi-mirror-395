import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import ipaddress
import os
import sys
import json
import re
import csv

# --- PATH CONFIGURATION ---
# 1. Get the directory where this script is installed (for read-only config)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DATA_DIR = os.path.join(PACKAGE_DIR, "data")

# 2. Define the Writable Data Directory (User's Home Directory)
# We use the user's home folder to avoid "Permission Denied" errors in site-packages
USER_HOME = os.path.expanduser("~")
USER_DATA_DIR = os.path.join(USER_HOME, ".kavachnet")

# Ensure user data directory exists
os.makedirs(USER_DATA_DIR, exist_ok=True)

# --- FILE PATHS ---
# Read-only source config (shipped with package)
SOURCE_FILE = os.path.join(PACKAGE_DATA_DIR, "vpn_sources.json")

# Writable data files (downloaded at runtime)
CACHE_FILE = os.path.join(USER_DATA_DIR, "vpn_ip_list.txt")
ASN_FILE_V4 = os.path.join(USER_DATA_DIR, "asn_ipv4.csv")
ASN_FILE_V6 = os.path.join(USER_DATA_DIR, "asn_ipv6.csv")

TIMEOUT = 15  # seconds for HTTP requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# --- ASN / HOSTING LOGIC ---

def get_session():
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

def download_asn_db():
    """Downloads the optimized ASN CSV databases (IPv4 and IPv6) from sapics/ip-location-db."""
    urls = {
        "v4": ("https://raw.githubusercontent.com/sapics/ip-location-db/main/asn/asn-ipv4.csv", ASN_FILE_V4),
        "v6": ("https://raw.githubusercontent.com/sapics/ip-location-db/refs/heads/main/asn/asn-ipv6.csv", ASN_FILE_V6)
    }
    
    success = True
    for ver, (url, filepath) in urls.items():
        print(f"[i] Fetching ASN {ver.upper()} Database from {url}...")
        try:
            session = get_session()
            r = session.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(r.content)
            print(f"[✓] ASN {ver.upper()} Database updated.")
        except Exception as e:
            print(f"[WARN] Could not fetch ASN {ver.upper()} DB: {e}")
            success = False
            
    return success

def load_asn_db():
    """
    Loads ASN CSVs into memory.
    Returns a dict: {'v4': [(start, end, org), ...], 'v6': [(start, end, org), ...]}
    """
    asn_data = {'v4': [], 'v6': []}
    
    files = {
        'v4': ASN_FILE_V4,
        'v6': ASN_FILE_V6
    }
    
    for ver, filepath in files.items():
        if not os.path.exists(filepath):
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    # Format: start_ip, end_ip, asn, org_name
                    if len(row) < 4: continue
                    try:
                        if ver == 'v4':
                            start_int = int(ipaddress.IPv4Address(row[0]))
                            end_int = int(ipaddress.IPv4Address(row[1]))
                        else:
                            start_int = int(ipaddress.IPv6Address(row[0]))
                            end_int = int(ipaddress.IPv6Address(row[1]))
                            
                        org_name = row[3]
                        asn_data[ver].append((start_int, end_int, org_name))
                    except ValueError:
                        continue
        except Exception as e:
            print(f"[!] Error loading ASN {ver} DB: {e}")
    
    return asn_data

def check_asn_hosting(ip_str, asn_db):
    """
    Checks if an IP belongs to a hosting provider using the ASN DB.
    """
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        ip_int = int(ip_obj)
    except ValueError:
        return None 

    # Select correct DB based on IP version
    if ip_obj.version == 4:
        db_list = asn_db.get('v4', [])
    else:
        db_list = asn_db.get('v6', [])

    # Linear Search 
    for start, end, org in db_list:
        if start <= ip_int <= end:
            return org
    return None

# --- DOWNLOADER / PARSER LOGIC ---

def load_sources():
    if not os.path.exists(SOURCE_FILE):
        return {}
    with open(SOURCE_FILE, 'r') as f:
        data = json.load(f)
    return data

def extract_ips_from_text(text):
    lines = text.splitlines()
    cleaned = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "," in line and "{" not in line:
            line = line.split(",")[0].strip()
        if len(line) < 3: continue 
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
                for key in ["ip", "ipv4", "ipv6", "ip_prefix", "ipv4Prefix", "ipv6Prefix", "ip_address", "EntryIP", "station"]:
                    if key in item:
                        ips.add(item[key])
    return ips

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
        else:
            return extract_ips_from_text(text)
    except Exception as e:
        print(f"[WARN] Could not fetch {url}: {e}")
        return set()

def load_cached_ips():
    """
    Loads IPs from the cache file. 
    If file doesn't exist, returns empty dict (does NOT create file here).
    """
    if not os.path.exists(CACHE_FILE):
        return {}

    cached = {}
    with open(CACHE_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "|" in line:
                ip, t = line.split("|", 1)
                cached[ip] = t
            else:
                cached[line] = "UNKNOWN"
    return cached

def append_to_cache(entries):
    """
    Appends new entries to the cache file. Creates file if missing.
    """
    if not entries:
        return
    
    # 'a' mode will create the file if it does not exist
    with open(CACHE_FILE, 'a', encoding='utf-8') as f:
        for ip, t in entries.items():
            if isinstance(ip, str) and ('/' in ip or ip.replace('.', '').replace(':', '').isalnum()):
                safe_type = t.replace('|', '').replace('\n', '').strip()
                f.write(f"{ip}|{safe_type}\n")

def refresh_cache():
    """
    Downloads both blocklists and the ASN DB.
    """
    # 1. Download ASN DB First (v4 and v6)
    download_asn_db()
    
    # 2. Download Blocklists
    typed_sources = load_sources()
    cached = load_cached_ips()
    total_new = {}
    
    print(f"[i] Starting Blocklist Update...")
    for t, urls in typed_sources.items():
        if t == "ASN": continue 
        for url in urls:
            print(f"    - Fetching {t}: {url[:50]}...")
            fetched = download_list(url)
            new_entries = {ip: t for ip in fetched if ip not in cached}
            if new_entries:
                print(f"      + {len(new_entries)} new entries.")
                total_new.update(new_entries)
                cached.update(new_entries)

    append_to_cache(total_new)
    print(f"[✓] Blocklists updated with {len(total_new)} new entries.")
    return cached, len(total_new)

def load_networks_from_cache(cached_data):
    all_networks = []
    if isinstance(cached_data, dict):
        iterator = cached_data.items()
    else:
        return []

    for ip_str, ip_type in iterator:
        try:
            net = ipaddress.ip_network(ip_str, strict=False)
            all_networks.append((net, ip_type))
        except ValueError:
            continue
    return all_networks

# --- MAIN DECISION LOGIC ---

def is_vpn_ip(ip, networks, asn_db=None):
    """
    Detects if an IP is a VPN/Proxy.
    Returns a tuple: (is_threat, info_string, asn_org)
    """
    asn_org = None
    clean_ip = ip.strip()

    try:
        ip_obj = ipaddress.ip_address(clean_ip)
    except ValueError:
        # Attempt to handle IP:Port format
        parsed = False
        # IPv4 with port (e.g., 1.2.3.4:80)
        if '.' in clean_ip and ':' in clean_ip:
            try:
                clean_ip = clean_ip.split(':')[0]
                ip_obj = ipaddress.ip_address(clean_ip)
                parsed = True
            except ValueError:
                pass
        
        # IPv6 with brackets (e.g., [::1]:80)
        if not parsed and clean_ip.startswith('[') and ']:' in clean_ip:
            try:
                clean_ip = clean_ip.split(']:')[0].strip('[')
                ip_obj = ipaddress.ip_address(clean_ip)
                parsed = True
            except ValueError:
                pass

        if not parsed:
            return (None, "Invalid IP Format", None)

    # 0. Always fetch ASN if DB is available
    if asn_db:
        asn_org = check_asn_hosting(clean_ip, asn_db)

    # 1. Check Blocklists (Specific Lists)
    for net, t in networks:
        if ip_obj in net:
            return (True, f"Matched Blocklist: {t}", asn_org)

    # 2. Check ASN / Hosting (Broad Ownership Check)
    if asn_org:
        # Keywords that indicate non-residential, likely VPN/Proxy infrastructure
        hosting_keywords = [
            'AMAZON', 'GOOGLE', 'MICROSOFT', 'DIGITALOCEAN', 'HETZNER', 
            'OVH', 'M247', 'LEASEWEB', 'DATACAMP', 'LINODE', 'VULTR', 
            'CHOOPA', 'ORACLE', 'ALIBABA', 'TENCENT', 'FASTLY', 'CLOUDFLARE',
            'AKAMAI', 'CDN77', 'HOSTINGER', 'CONTABO', 'NORDVPN', 'EXPRESSVPN'
        ]
        org_upper = asn_org.upper()
        
        for keyword in hosting_keywords:
            if keyword in org_upper:
                return (True, f"Matched Hosting Keyword: {asn_org}", asn_org)
        
        return (False, f"Organization: {asn_org}", asn_org)

    return (False, "Unknown Organization (Not in any list)", None)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vpn_checker.py <IP_Address> [refresh]")
        print("Add 'refresh' to update databases manually.")
        sys.exit(1)

    # Simple CLI argument parsing
    target = None
    should_refresh = False
    
    # Check if cache file exists; if not, force refresh
    if not os.path.exists(CACHE_FILE):
        print(f"[!] Cache file not found at {CACHE_FILE}.")
        print("[!] Auto-triggering data refresh to populate lists...")
        should_refresh = True
    
    # Check args for manual refresh override
    for arg in sys.argv[1:]:
        if arg.lower() == "refresh":
            should_refresh = True
        else:
            target = arg

    if should_refresh:
        refresh_cache()
        # Reload after refresh
        cached_data = load_cached_ips()
        nets = load_networks_from_cache(cached_data)
        asn_data = load_asn_db()
    else:
        # Quietly load data
        cached_data = load_cached_ips()
        nets = load_networks_from_cache(cached_data)
        asn_data = load_asn_db()

    if target:
        # Perform Check
        is_threat, info, asn_org = is_vpn_ip(target, nets, asn_db=asn_data)
        
        # --- FINAL OUTPUT FORMAT ---
        print("-" * 50)
        print(f"Target IP: {target}")
        print("-" * 50)
        
        if is_threat:
            print(f"🚨 STATUS: THREAT DETECTED")
            print(f"ℹ️  INFO:   {info}")
        elif is_threat is None:
            print(f"⚠️ STATUS: INVALID INPUT")
            print(f"ℹ️  INFO:   {info}")
        else:
            print(f"✅ STATUS: CLEAN")
            print(f"ℹ️  INFO:   {info}")
        
        if asn_org:
            print(f"🏢 ASN:    {asn_org}")
            
        print("-" * 50)
    else:
        if not should_refresh:
            print("[!] Please provide an IP address to check.")
