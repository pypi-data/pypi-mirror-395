from .make_request import *
from urllib.parse import urljoin


# ============================================================
# URL + HTTP helpers
# ============================================================

def normalize(domain: str) -> str:
    return domain.rstrip("/")


def join(domain: str, path: str) -> str:
    domain = normalize(domain)
    path = path.lstrip("/")
    return f"{domain}/{path}"


def is_valid_endpoint(url: str) -> bool:
    """Return True if the URL responds with anything < 500-level error."""
    try:
        r = requests.get(url, timeout=3)
        return r.status_code < 500
    except Exception:
        return False


def fetch_json(url: str):
    """Return JSON if response==200, else None."""
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


# ============================================================
# Prefix discovery
# ============================================================

def get_prefixes(domain: str, prefix: str = None):
    """
    Returns a list of full prefix URLs:
       - If prefix is given, try only that prefix
       - Otherwise, query /prefixes
    """
    domain = normalize(domain)

    # Direct prefix override
    if prefix:
        test_url = join(domain, prefix)
        js = fetch_json(test_url)
        if js is not None:
            return [test_url]     # prefix is valid
        # else continue to auto-discovery

    # Auto-discover prefixes from /prefixes
    prefixes_url = join(domain, "prefixes")
    pref_list = fetch_json(prefixes_url)
    if not pref_list:
        return []

    # Map returned prefix strings → absolute URLs
    return [join(domain, p) for p in pref_list]


# ============================================================
# Endpoint discovery
# ============================================================

def get_endpoint_urls(domain: str, prefix: str = None):
    """
    Returns URLs like:
        /utilities/endpoints
        /math/endpoints
    for prefixes that respond correctly.
    """
    endpoints = []
    for prefix_url in get_prefixes(domain, prefix=prefix):
        ep_url = f"{prefix_url}/endpoints"
        js = fetch_json(ep_url)
        if js is not None:
            endpoints.append(ep_url)
    return endpoints


def get_endpoints(domain: str, prefix: str = None, *args, **kwargs):
    """
    Returns endpoint entries from each prefix-level /endpoints.
    Expected structure: [["/utilities/load_from_json", "GET,POST"], ...]
    """
    all_eps = []
    for ep_url in get_endpoint_urls(domain, prefix):
        result = postRequest(ep_url, **kwargs) if kwargs else postRequest(ep_url)
        if isinstance(result, list):
            all_eps.extend(result)
    return all_eps


# ============================================================
# Endpoint lookup
# ============================================================

def get_endpoint(name: str, domain: str, prefix: str = None, *args, **kwargs):
    """
    Locate endpoint containing the substring `name`.
    Returns full URL: domain + /prefix/.../name
    """
    domain = normalize(domain)
    endpoints = get_endpoints(domain, prefix, *args, **kwargs)

    matches = [e for e in endpoints if name in e[0]]
    
    if matches:
        return join(domain, matches[0][0])

    return None


def check_endpoint(domain: str, endpoint: str, prefix: str = None):
    """
    First try direct:   domain/endpoint
    Fallback:           search /prefix/endpoints
    """
    domain = normalize(domain)

    direct = join(domain, endpoint)
    if is_valid_endpoint(direct):
        return direct

    found = get_endpoint(endpoint, domain=domain, prefix=prefix)
    return found

def make_endpoint_call(*args,domain,endpoint,prefix=None,**kwargs):
    url = get_endpoint(endpoint, domain=domain, prefix=prefix)
    if url:
        response = makeRequest(url,*args,**kwargs)
        return response
