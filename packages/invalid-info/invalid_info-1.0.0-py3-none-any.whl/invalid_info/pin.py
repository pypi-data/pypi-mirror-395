import requests

def pin(pincode: str):
    """
    Fetch PIN code info.
    Returns full dictionary with module_dev key.
    """
    if not pincode.isdigit() or len(pincode) != 6:
        return {"error": "Invalid PIN code", "module_dev": "Invalid Ayush"}

    url = f"https://pin-code-info.gauravcyber0.workers.dev/?pincode={pincode}"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return {"error": f"API error {r.status_code}", "module_dev": "Invalid Ayush"}

        data_list = r.json()  # API returns list of dicts
        if isinstance(data_list, list) and len(data_list) > 0:
            data = data_list[0]  # Take first element as main dictionary
        else:
            data = {"error": "No data found"}

        # Add module_dev key
        data["module_dev"] = "Invalid Ayush"

        return data

    except Exception as e:
        return {"error": str(e), "module_dev": "Invalid Ayush"}
