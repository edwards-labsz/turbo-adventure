import sys
import re
import requests

# REPLACE THIS WITH YOUR ACTUAL CLOUDFLARE TEST PAGE URL
TEST_URL = "https://www.boomlings.com/database/accounts/accountManagement.php"
PROXY_LIST_URL = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"

def fetch_proxies():
    try:
        response = requests.get(PROXY_LIST_URL, timeout=30)
        return [p.strip() for p in response.text.split('\n') if p.strip()]
    except Exception as e:
        print(f"Failed to fetch ProxyScrape list: {e}")
        sys.exit(1)

def check_proxy(proxy_url):
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        # Strict timeout requirement: if it takes too long, it's marked dead
        response = requests.get(TEST_URL, proxies=proxies, timeout=5)
        html_content = response.text

        # Scan the response page text for Cloudflare error codes
        if "error code: 1005" in html_content or "Error 1005" in html_content:
            print(f"❌ Dead: {proxy_url} triggered Cloudflare Error 1005 (ASN Banned).")
            return False
        if "error code: 1006" in html_content or "Error 1006" in html_content:
            print(f"❌ Dead: {proxy_url} triggered Cloudflare Error 1006 (IP Banned).")
            return False
            
        # Inspect HTTP Status flags for direct Cloudflare 403 blocks
        if response.status_code == 403 and ("cloudflare" in html_content.lower() or "ray id" in html_content.lower()):
            print(f"❌ Dead: {proxy_url} was blocked by a Cloudflare WAF rule.")
            return False

        print(f"✅ Success: {proxy_url} passed Cloudflare check.")
        return True

    except requests.exceptions.Timeout:
        print(f"❌ Dead: {proxy_url} timed out (Took too long).")
        return False
    except requests.exceptions.RequestException:
        print(f"❌ Dead: {proxy_url} network/connection dropped.")
        return False

def main():
    print("Gathering candidate IPs from ProxyScrape...")
    proxy_candidates = fetch_proxies()
    
    # Evaluate up to the top 25 proxies to find a functional choice
    for proxy in proxy_candidates[:9999]:
        if check_proxy(proxy):
            # Parse components cleanly out of the string structure
            clean_proxy = proxy.replace("http://", "")
            ip, port = clean_proxy.split(":")
            
            # Append the successful target details to the GitHub environment logs
            with open("working_proxy.env", "w") as f:
                f.write(f"PROXY_IP={ip}\nPROXY_PORT={port}\n")
            sys.exit(0)
            
    print("Error: Explored top candidates and no active proxies cleared Cloudflare restrictions.")
    sys.exit(1)

if __name__ == "__main__":
    main()
