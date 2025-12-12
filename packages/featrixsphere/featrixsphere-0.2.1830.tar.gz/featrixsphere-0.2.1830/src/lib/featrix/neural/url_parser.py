#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import logging
from typing import Dict, Optional
from urllib.parse import urlparse, ParseResult
import re

logger = logging.getLogger(__name__)

# TLD classifications
GENERIC_TLDS = {
    'com', 'net', 'org', 'edu', 'gov', 'mil', 'int',
    'biz', 'info', 'name', 'pro', 'coop', 'aero', 'museum'
}

# Common new gTLDs
NEW_GTLDS = {
    'io', 'ai', 'app', 'dev', 'tech', 'online', 'site', 'website',
    'store', 'shop', 'cloud', 'digital', 'media', 'network', 'xyz',
    'blog', 'news', 'tv', 'me', 'cc', 'co', 'fm', 'ws'
}

# Country codes (2-letter, some common ones)
COUNTRY_TLDS = {
    'uk', 'de', 'fr', 'ca', 'au', 'jp', 'cn', 'ru', 'in', 'br',
    'mx', 'es', 'it', 'nl', 'se', 'no', 'dk', 'fi', 'pl', 'ch',
    'at', 'be', 'ie', 'nz', 'sg', 'hk', 'kr', 'za', 'il', 'ae'
}


class URLComponents:
    """Parsed URL components with graceful defaults."""
    
    def __init__(
        self,
        protocol: str = "https",
        subdomain: str = "",
        domain_main: str = "",
        tld: str = "",
        tld_type: str = "generic",  # generic, country, new
        is_free_domain: bool = False,
        path: str = "/",
        endpoint: str = "",
        query_params: str = "",
        is_valid: bool = True,
        original: str = ""
    ):
        self.protocol = protocol
        self.subdomain = subdomain
        self.domain_main = domain_main
        self.tld = tld
        self.tld_type = tld_type
        self.is_free_domain = is_free_domain
        self.path = path
        self.endpoint = endpoint
        self.query_params = query_params
        self.is_valid = is_valid
        self.original = original
    
    def to_dict(self) -> Dict[str, any]:
        """Convert to dictionary for serialization."""
        return {
            'protocol': self.protocol,
            'subdomain': self.subdomain,
            'domain_main': self.domain_main,
            'tld': self.tld,
            'tld_type': self.tld_type,
            'is_free_domain': self.is_free_domain,
            'path': self.path,
            'endpoint': self.endpoint,
            'query_params': self.query_params,
            'is_valid': self.is_valid,
        }
    
    def __repr__(self):
        return f"URLComponents({self.to_dict()})"


def classify_tld(tld: str) -> str:
    """Classify TLD as generic, country, or new gTLD."""
    tld_clean = tld.lower().lstrip('.')
    
    if tld_clean in GENERIC_TLDS:
        return "generic"
    elif tld_clean in COUNTRY_TLDS:
        return "country"
    elif tld_clean in NEW_GTLDS:
        return "new"
    elif len(tld_clean) == 2:
        # Likely a country code we don't have in our list
        return "country"
    else:
        # Default to generic
        return "generic"


def parse_domain_parts(hostname: str) -> tuple[str, str, str]:
    """
    Parse hostname into subdomain, domain_main, and TLD.
    
    Returns: (subdomain, domain_main, tld)
    
    Examples:
        www.example.com -> ("www", "example", "com")
        api.service.example.co.uk -> ("api.service", "example", "co.uk")
        example.com -> ("", "example", "com")
        localhost -> ("", "localhost", "")
    """
    if not hostname:
        return "", "", ""
    
    # Handle IP addresses
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname):
        return "", hostname, ""
    
    parts = hostname.split('.')
    
    if len(parts) == 1:
        # Just a hostname, no domain
        return "", parts[0], ""
    elif len(parts) == 2:
        # Simple case: domain.tld
        return "", parts[0], parts[1]
    else:
        # Check for compound TLDs like .co.uk, .com.au, etc.
        # Common pattern: if last two parts look like country TLD
        last_two = f"{parts[-2]}.{parts[-1]}"
        if parts[-2] in {'co', 'com', 'net', 'org', 'gov', 'ac', 'edu'} and parts[-1] in COUNTRY_TLDS:
            # Compound TLD
            if len(parts) == 3:
                # subdomain.domain.co.uk -> no subdomain
                return "", parts[0], last_two
            else:
                # www.subdomain.domain.co.uk
                subdomain = '.'.join(parts[:-3])
                domain_main = parts[-3]
                tld = last_two
                return subdomain, domain_main, tld
        else:
            # Standard case: subdomain(s).domain.tld
            subdomain = '.'.join(parts[:-2])
            domain_main = parts[-2]
            tld = parts[-1]
            return subdomain, domain_main, tld


def extract_endpoint(path: str) -> str:
    """
    Extract the endpoint (last non-empty path segment).
    
    Examples:
        /api/v1/users -> "users"
        /products/item/ -> "item"
        / -> ""
    """
    if not path or path == '/':
        return ""
    
    segments = [s for s in path.strip('/').split('/') if s]
    return segments[-1] if segments else ""


def normalize_url(url_str: str) -> str:
    """
    Normalize URL string by adding protocol if missing.
    Handles various malformed inputs gracefully.
    """
    if not url_str or not isinstance(url_str, str):
        return ""
    
    url_str = url_str.strip()
    
    # If it looks like it already has a protocol, use as-is
    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', url_str):
        return url_str
    
    # If it starts with //, prepend https:
    if url_str.startswith('//'):
        return 'https:' + url_str
    
    # Otherwise, prepend https://
    return 'https://' + url_str


def parse_url(url_str: str, check_free_domain_fn=None) -> URLComponents:
    """
    Parse a URL string into components with graceful error handling.
    
    Args:
        url_str: URL string to parse (may be malformed)
        check_free_domain_fn: Optional function to check if domain is free (from Hubspot list)
    
    Returns:
        URLComponents with parsed data or sensible defaults
    """
    if not url_str or not isinstance(url_str, str):
        logger.debug(f"Invalid URL input: {url_str}")
        return URLComponents(is_valid=False, original=str(url_str))
    
    original = url_str
    
    try:
        # Normalize URL
        normalized = normalize_url(url_str)
        
        # Parse using urllib
        parsed: ParseResult = urlparse(normalized)
        
        # Extract protocol
        protocol = parsed.scheme or "https"
        
        # Parse hostname into components
        hostname = parsed.netloc or ""
        subdomain, domain_main, tld = parse_domain_parts(hostname)
        
        # Classify TLD
        tld_type = classify_tld(tld) if tld else "generic"
        
        # Check if free domain
        is_free_domain = False
        if check_free_domain_fn and domain_main and tld:
            full_domain = f"{domain_main}.{tld}" if tld else domain_main
            try:
                is_free_domain = check_free_domain_fn(full_domain)
            except Exception as e:
                logger.debug(f"Error checking free domain for {full_domain}: {e}")
        
        # Extract path
        path = parsed.path if parsed.path else "/"
        
        # Extract endpoint
        endpoint = extract_endpoint(path)
        
        # Extract query parameters
        query_params = parsed.query if parsed.query else ""
        
        return URLComponents(
            protocol=protocol,
            subdomain=subdomain,
            domain_main=domain_main,
            tld=tld,
            tld_type=tld_type,
            is_free_domain=is_free_domain,
            path=path,
            endpoint=endpoint,
            query_params=query_params,
            is_valid=True,
            original=original
        )
    
    except Exception as e:
        logger.warning(f"Failed to parse URL '{url_str}': {e}")
        return URLComponents(is_valid=False, original=original)


def parse_url_batch(urls, check_free_domain_fn=None):
    """Parse a batch of URLs, returning list of URLComponents."""
    return [parse_url(url, check_free_domain_fn) for url in urls]

