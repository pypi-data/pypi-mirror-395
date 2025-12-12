import requests

def ifsc(ifsc_code: str):
    """
    Fetch bank IFSC info.
    Returns full dictionary with module_dev key.
    """
    if not ifsc_code or len(ifsc_code) < 4:
        return {"error": "Invalid IFSC code", "module_dev": "Invalid Ayush"}

    url = f"https://ifsc-code-info.gauravcyber0.workers.dev/?ifsc={ifsc_code}"

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
