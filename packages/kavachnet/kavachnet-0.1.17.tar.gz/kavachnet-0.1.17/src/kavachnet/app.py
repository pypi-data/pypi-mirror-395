import streamlit as st
import json
import os
import sys
from pathlib import Path

# --- PATH & IMPORT CONFIGURATION ---
# Get the directory of this app.py file
CURRENT_DIR = Path(__file__).parent

# Add the current directory to sys.path so we can import vpn_checker locally
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

# Try importing the logic
try:
    # Attempt absolute import (if installed as package)
    from kavachnet.vpn_checker import refresh_cache, load_networks_from_cache, is_vpn_ip, load_cached_ips, CACHE_FILE, load_asn_db
except ImportError:
    try:
        # Attempt local import (if running from source)
        from vpn_checker import refresh_cache, load_networks_from_cache, is_vpn_ip, load_cached_ips, CACHE_FILE, load_asn_db
    except ImportError as e:
        st.error(f"Critical Error: Could not import vpn_checker. Details: {e}")
        st.stop()

# path to the read-only sources file for the sidebar
SOURCES_JSON = CURRENT_DIR / "data" / "vpn_sources.json"

# ────────────────────────────────────────────────────────────────
# Streamlit Page Config
st.set_page_config(
    page_title="KAVACHNET",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ────────────────────────────────────────────────────────────────
# Custom Styling
st.markdown("""
<style>
    .big-font {font-size:50px !important; font-weight: bold; text-align: center; color: #FF9933;}
    .stButton>button {width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white;}
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
# Header
st.markdown('<p class="big-font">KavachNet </p>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>🛡️KavachNet: VPN & Proxy Detection System by Rishabh KRW</h3>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
# Sidebar – Sources
with st.sidebar:
    st.header("🌍 Data Sources")
    
    # Update Button in Sidebar
    if st.button("🔄 Update Database Now"):
        with st.spinner("Fetching latest IP lists..."):
            try:
                _, new_count = refresh_cache()
                st.success(f"Database updated! {new_count} new entries.")
            except Exception as e:
                st.error(f"Update failed: {e}")
    
    st.info("💡 **Note:** If this is your first time running the new version, please click **'Update Database Now'** to download the required databases.")

    if SOURCES_JSON.exists():
        try:
            with open(SOURCES_JSON, 'r') as f:
                data = json.load(f)
            
            for category, urls in data.items():
                with st.expander(f"{category} ({len(urls)} sources)"):
                    for url in urls:
                        # Truncate long URLs for display
                        display_url = url.replace("https://", "").replace("http://", "")
                        if len(display_url) > 30:
                            display_url = display_url[:27] + "..."
                        st.markdown(f"• [{display_url}]({url})")
        except Exception as e:
            st.error(f"Error reading sources: {e}")
    else:
        st.warning(f"Source file not found at: {SOURCES_JSON}")
    
    st.divider()
    st.caption(f"Cache Location:\n{CACHE_FILE}")
    st.markdown("---")
    st.markdown("Developed by **Rishabh KRW**")

# ────────────────────────────────────────────────────────────────
# Main App
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 IP Inspection")
    ip_input = st.text_input("Enter IP Address", placeholder="e.g., 1.1.1.1", help="Supports IPv4 and IPv6")

    if st.button("🚀 Initiating Scan"):
        if not ip_input.strip():
            st.warning("⚠️ Please enter a valid IP address.")
        else:
            status_container = st.empty()
            
            try:
                with st.spinner("⚙️ Analyzing Network Signatures..."):
                    # Strip port if present (e.g., "1.1.1.1:80" -> "1.1.1.1")
                    clean_ip = ip_input.strip().split(':')[0]
                    
                    # 1. Load Local Cache (Fast)
                    cached_data = load_cached_ips()
                    
                    # 2. Load Networks
                    networks = load_networks_from_cache(cached_data)

                    # 3. Load ASN DB
                    asn_data = load_asn_db()
                    
                    # 4. Check IP
                    is_threat, info, asn_org = is_vpn_ip(clean_ip, networks, asn_db=asn_data)

                # 5. Display Results
                if is_threat:
                    st.error(f"### 🚨 THREAT DETECTED")
                    st.markdown(f"""
                    The IP `{clean_ip}` has been positively identified as:
                    # **{info}**
                    """)
                    if asn_org:
                        st.warning(f"🏢 **ISP:** {asn_org}")
                elif is_threat is None:
                    st.warning(f"⚠️ Invalid IP Address: {info}")
                else:
                    st.success(f"### ✅ CLEAN IP")
                    st.markdown(f"The IP `{clean_ip}` does not match any known VPN, Proxy, or Cloud signatures.")
                    if asn_org:
                        st.info(f"🏢 **ISP:** {asn_org}")
                    else:
                        st.info(f"ℹ️ {info}")
                
            except Exception as e:
                st.error(f"An execution error occurred: {e}")
                import traceback
                st.code(traceback.format_exc())

with col2:
    st.info("ℹ️ **System Intelligence**")
    st.markdown("""
    **KavachNet** aggregates real-time threat intelligence from open-source feeds.
    
    **Detection Capabilities:**
    * 🕵️ **Commercial VPNs** (Nord, Express, etc.)
    * 🧅 **Tor Exit Nodes**
    * 🔓 **Public Proxies** (SOCKS4/5, HTTP)
    * ☁️ **Cloud Ranges** (AWS, Azure, Google Cloud)
    * 🏢 **ISP / ASN Analysis** (Hosting vs Residential)
    """)
