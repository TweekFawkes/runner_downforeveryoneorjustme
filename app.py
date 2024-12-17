import sys
import argparse
from urllib.parse import urlparse
import socket
import requests
from requests.exceptions import RequestException

def extract_domain_and_port(input_str):
    # Parse URL if given a full URL
    parsed = urlparse(input_str if '://' in input_str else f'http://{input_str}')
    domain = parsed.netloc or parsed.path
    
    # Split domain and port if port exists
    if ':' in domain:
        domain, port = domain.split(':')
        port = int(port)
    else:
        port = None
        
    return domain.strip('/'), port

def check_connection(domain, port, protocol='http'):
    try:
        url = f'{protocol}://{domain}{":" + str(port) if port else ""}'
        response = requests.get(url, timeout=5)
        return True, response.status_code
    except RequestException:
        return False, None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain_name', required=True, help='Domain name to check')
    args = parser.parse_args()

    domain, port = extract_domain_and_port(args.domain_name)
    print(f"\n[*] Checking domain: {domain}")

    if port:
        # Check specific port for both HTTP and HTTPS
        print(f"[*] Checking port {port}")
        http_success, http_code = check_connection(domain, port, 'http')
        https_success, https_code = check_connection(domain, port, 'https')
        
        print(f"[*] HTTP (port {port}): {'UP' if http_success else 'DOWN'}")
        print(f"[*] HTTPS (port {port}): {'UP' if https_success else 'DOWN'}")
    else:
        # Check default ports (80 and 443)
        http_success, http_code = check_connection(domain, 80, 'http')
        https_success, https_code = check_connection(domain, 443, 'https')
        
        print(f"[*] HTTP (port 80): {'UP' if http_success else 'DOWN'}")
        print(f"[*] HTTPS (port 443): {'UP' if https_success else 'DOWN'}")

if __name__ == "__main__":
    main()
