from .config import load_endpoints, save_endpoints


def add_endpoint(alias: str, url: str, method: str = "GET"):
    """Add a new endpoint using current config"""
    data = load_endpoints()

    endpoint_data = {
        "url": url,
        "method": method.upper(),
    }

    data["endpoints"][alias] = endpoint_data
    save_endpoints(data)
