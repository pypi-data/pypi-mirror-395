#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
"""
World Data Cache

Caches domain information (DNS, web content) in a balanced directory tree structure.
All jobs can access this cached data to avoid repeated lookups.

Directory structure:
    /sphere/app/featrix_world_data_cache/domain2info/
        <first-2-letters>/
            <second-2-letters>/
                <full-domain>/
                    web_content/
                        results.json
                    dns.json
"""
import json
import logging
import os
import socket
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import ipaddress
import requests

logger = logging.getLogger(__name__)

# Base cache directory
CACHE_BASE_DIR = Path("/sphere/app/featrix_world_data_cache")
DOMAIN_CACHE_DIR = CACHE_BASE_DIR / "domain2info"

# Cache timeout for web content (24 hours)
WEB_CONTENT_CACHE_TIMEOUT = 24 * 60 * 60  # 24 hours in seconds


def _get_domain_path(domain: str) -> Path:
    """
    Get the cache path for a domain using balanced directory tree.
    
    Structure: <first-2-letters>/<second-2-letters>/<full-domain>/
    
    Examples:
        example.com -> ex/am/example.com/
        google.com -> go/og/google.com/
        a.com -> a./a./a.com/  (padded with dots if needed)
    """
    # Remove protocol if present
    domain = domain.strip()
    if domain.startswith('http://'):
        domain = domain[7:]
    elif domain.startswith('https://'):
        domain = domain[8:]
    
    # Remove leading/trailing slashes
    domain = domain.strip('/')
    
    # Extract just the domain part (no path)
    domain = domain.split('/')[0]
    
    # Normalize: lowercase, remove www. prefix for directory structure
    domain_lower = domain.lower()
    if domain_lower.startswith('www.'):
        domain_lower = domain_lower[4:]
    
    # Get first 2 and second 2 characters
    # Pad with dots if domain is too short
    if len(domain_lower) >= 2:
        first_two = domain_lower[:2]
    else:
        first_two = domain_lower + '.' * (2 - len(domain_lower))
    
    if len(domain_lower) >= 4:
        second_two = domain_lower[2:4]
    else:
        # If domain is short, use remaining chars + padding
        remaining = domain_lower[2:] if len(domain_lower) > 2 else ''
        second_two = remaining + '.' * (2 - len(remaining))
    
    # Build path: first_two/second_two/full_domain/
    return DOMAIN_CACHE_DIR / first_two / second_two / domain_lower


def ensure_domain_cache_dir(domain: str) -> Path:
    """
    Ensure the cache directory exists for a domain.
    
    Returns:
        Path to the domain's cache directory
    """
    domain_path = _get_domain_path(domain)
    domain_path.mkdir(parents=True, exist_ok=True)
    (domain_path / "web_content").mkdir(exist_ok=True)
    return domain_path


def get_dns_cache_path(domain: str) -> Path:
    """Get the path to the DNS cache file for a domain."""
    domain_path = ensure_domain_cache_dir(domain)
    return domain_path / "dns.json"


def get_web_content_cache_path(domain: str) -> Path:
    """Get the path to the web content cache file for a domain."""
    domain_path = ensure_domain_cache_dir(domain)
    return domain_path / "web_content" / "results.json"


def lookup_domain_ips(domain: str) -> Tuple[List[str], bool]:
    """
    Look up IP addresses for a domain (both www.<domain> and <domain>).
    
    Returns:
        (sorted_ip_list, has_ipv6) tuple
    """
    if not domain:
        return [], False
    
    all_ips = []
    has_ipv6 = False
    
    # Try both www.<domain> and <domain>
    domains_to_try = []
    if not domain.startswith('www.'):
        domains_to_try.append(f"www.{domain}")
    domains_to_try.append(domain)
    
    for d in domains_to_try:
        try:
            # Get all IP addresses (both IPv4 and IPv6)
            ip_list = socket.getaddrinfo(d, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
            for family, socktype, proto, canonname, sockaddr in ip_list:
                if family == socket.AF_INET:
                    # IPv4
                    ip_str = sockaddr[0]
                    if ip_str not in all_ips:
                        all_ips.append(ip_str)
                elif family == socket.AF_INET6:
                    # IPv6
                    ip_str = sockaddr[0]
                    if ip_str not in all_ips:
                        all_ips.append(ip_str)
                        has_ipv6 = True
        except (socket.gaierror, socket.herror, OSError) as e:
            logger.debug(f"DNS lookup failed for {d}: {e}")
            continue
        except Exception as e:
            logger.debug(f"Unexpected error during DNS lookup for {d}: {e}")
            continue
    
    # Sort IPs deterministically (convert to IP objects for proper sorting)
    try:
        sorted_ips = sorted(all_ips, key=lambda ip: ipaddress.ip_address(ip))
    except Exception as e:
        logger.debug(f"Error sorting IPs: {e}")
        sorted_ips = sorted(all_ips)  # Fallback to string sort
    
    return sorted_ips, has_ipv6


def get_or_lookup_dns(domain: str, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Get DNS information from cache or perform lookup.
    
    Args:
        domain: Domain name to look up
        force_refresh: If True, force a fresh DNS lookup even if cache exists
        
    Returns:
        Dictionary with 'ip_addresses' (list), 'has_ipv6' (bool), 'lookup_time' (timestamp)
    """
    dns_cache_path = get_dns_cache_path(domain)
    
    # Try to load from cache
    if not force_refresh and dns_cache_path.exists():
        try:
            with open(dns_cache_path, 'r') as f:
                cached_data = json.load(f)
                logger.debug(f"✅ Loaded DNS cache for {domain}: {len(cached_data.get('ip_addresses', []))} IPs")
                return cached_data
        except Exception as e:
            logger.warning(f"Failed to load DNS cache for {domain}: {e}, performing fresh lookup")
    
    # Perform DNS lookup
    logger.info(f"🔍 Performing DNS lookup for {domain}")
    ip_addresses, has_ipv6 = lookup_domain_ips(domain)
    
    # Create cache data
    dns_data = {
        'ip_addresses': ip_addresses,
        'has_ipv6': has_ipv6,
        'lookup_time': time.time(),
        'domain': domain
    }
    
    # Save to cache
    try:
        with open(dns_cache_path, 'w') as f:
            json.dump(dns_data, f, indent=2)
        logger.debug(f"💾 Cached DNS data for {domain}: {len(ip_addresses)} IPs")
    except Exception as e:
        logger.warning(f"Failed to save DNS cache for {domain}: {e}")
    
    return dns_data


def fetch_web_content(domain: str) -> Optional[Dict[str, Any]]:
    """
    Fetch web content from cache.featrix.com/scrape-raw/<domain>.
    
    Returns:
        Dictionary with web content data, or None if fetch failed
    """
    url = f"https://cache.featrix.com/scrape-raw/{domain}"
    
    try:
        logger.info(f"🌐 Fetching web content for {domain} from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to fetch web content for {domain}: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON response for {domain}: {e}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error fetching web content for {domain}: {e}")
        return None


def get_or_fetch_web_content(domain: str, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Get web content from cache or fetch from cache.featrix.com.
    
    Args:
        domain: Domain name to fetch content for
        force_refresh: If True, force a fresh fetch even if cache exists
        
    Returns:
        Dictionary with web content data or placeholder if fetch failed
    """
    web_content_path = get_web_content_cache_path(domain)
    
    # Try to load from cache
    if not force_refresh and web_content_path.exists():
        try:
            with open(web_content_path, 'r') as f:
                cached_data = json.load(f)
                
                # Check if cache is expired
                last_attempt = cached_data.get('last_attempt_time', 0)
                if time.time() - last_attempt < WEB_CONTENT_CACHE_TIMEOUT:
                    logger.debug(f"✅ Loaded web content cache for {domain} (age: {time.time() - last_attempt:.0f}s)")
                    return cached_data
                else:
                    logger.debug(f"🔄 Web content cache expired for {domain}, fetching fresh data")
        except Exception as e:
            logger.warning(f"Failed to load web content cache for {domain}: {e}, fetching fresh data")
    
    # Fetch from API
    web_content = fetch_web_content(domain)
    
    # Create cache data
    if web_content:
        cache_data = {
            'results': web_content,
            'last_attempt_time': time.time(),
            'success': True,
            'domain': domain
        }
    else:
        # Create placeholder for failed fetch
        cache_data = {
            'results': None,
            'last_attempt_time': time.time(),
            'success': False,
            'domain': domain,
            'error': 'No data returned from cache.featrix.com'
        }
        logger.debug(f"📝 Created placeholder cache entry for {domain} (no data returned)")
    
    # Save to cache
    try:
        with open(web_content_path, 'w') as f:
            json.dump(cache_data, f, indent=2)
        logger.debug(f"💾 Cached web content for {domain}")
    except Exception as e:
        logger.warning(f"Failed to save web content cache for {domain}: {e}")
    
    return cache_data


def get_domain_info(domain: str, include_web_content: bool = True, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Get comprehensive domain information (DNS + optionally web content).
    
    Args:
        domain: Domain name
        include_web_content: If True, also fetch web content
        force_refresh: If True, force fresh lookups/fetches
        
    Returns:
        Dictionary with DNS and web content information
    """
    # Get DNS info
    dns_info = get_or_lookup_dns(domain, force_refresh=force_refresh)
    
    result = {
        'domain': domain,
        'dns': dns_info
    }
    
    # Optionally get web content
    if include_web_content:
        web_content = get_or_fetch_web_content(domain, force_refresh=force_refresh)
        result['web_content'] = web_content
    
    return result


# Initialize cache directory on import
try:
    DOMAIN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    logger.debug(f"✅ World data cache directory initialized: {DOMAIN_CACHE_DIR}")
except Exception as e:
    logger.warning(f"Failed to initialize world data cache directory: {e}")

