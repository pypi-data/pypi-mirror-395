import requests

def song(song_name: str):
    """
    Fetch song info from API.
    Returns full dictionary with module_dev key.
    """
    if not song_name:
        return {"error": "Invalid song name", "module_dev": "Invalid Ayush"}

    query = song_name.replace(" ", "+")
    url = f"https://invalid-ayush-song-api.onrender.com/search?song={query}"

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
