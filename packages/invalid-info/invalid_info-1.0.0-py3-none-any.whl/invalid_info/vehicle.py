import requests

def vehicle(reg_no: str):
    """
    Fetch vehicle info by registration number.
    Returns full dictionary with module_dev key.
    """
    if not reg_no:
        return {"error": "Invalid vehicle number", "module_dev": "Invalid Ayush"}

    url = f"https://vehicle-info.gauravcyber0.workers.dev/?vehicle={reg_no}"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return {"error": f"API error {r.status_code}", "module_dev": "Invalid Ayush"}

        data = r.json()

        # Add custom module_dev key
        data["module_dev"] = "Invalid Ayush"

        return data

    except Exception as e:
        return {"error": str(e), "module_dev": "Invalid Ayush"}
