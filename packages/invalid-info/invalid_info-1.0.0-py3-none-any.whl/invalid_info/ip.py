import requests

def ip(ip_address: str):
    """
    Fetch IP info.
    Returns full dictionary with module_dev key.
    """
    if not ip_address:
        return {"error": "Invalid IP address", "module_dev": "Invalid Ayush"}

    url = f"https://ipinfo.io/{ip_address}/geo"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return {"error": f"API error {r.status_code}", "module_dev": "Invalid Ayush"}

        data = r.json()  # API returns dictionary

        # Add module_dev key
        data["module_dev"] = "Invalid Ayush"

        return data

    except Exception as e:
        return {"error": str(e), "module_dev": "Invalid Ayush"}
