import requests
import random
import string
from instaloader import Instaloader, Profile

L = Instaloader()

def fetch_uid(username):
    profile = Profile.from_username(L.context, username)
    return profile.userid

def year_from_uid(uid):
    ranges = [
        (1279000, 2010),
        (17750000, 2011),
        (279760000, 2012),
        (900990000, 2013),
        (1629010000, 2014),
        (2500000000, 2015),
        (3713668786, 2016),
        (5699785217, 2017),
        (8597939245, 2018),
        (21254029834, 2019),
        (33254029834, 2020),
        (43254029834, 2021),
        (51254029834, 2022),
        (57254029834, 2023),
        (62254029834, 2024),
        (66254029834, 2025),
    ]
    for limit, yr in ranges:
        if uid <= limit:
            return yr
    return None

def instagram(username):
    """Returns full Instagram API response as Python dict with module_dev key"""

    try:
        user_id = fetch_uid(username)
    except Exception as e:
        return {"error": f"UID fetch failed: {e}", "module_dev": "Invalid Ayush"}

    year = year_from_uid(user_id)

    lsd = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    variables = {"id": user_id, "render_surface": "PROFILE"}
    data = {
        "lsd": lsd,
        "variables": str(variables),
        "doc_id": "25618261841150840"
    }

    headers = {
        "X-FB-LSD": lsd,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        resp = requests.post("https://www.instagram.com/api/graphql", headers=headers, data=data)
        resp.raise_for_status()
        resp_json = resp.json()
    except Exception as e:
        return {"error": f"Instagram request failed: {e}", "module_dev": "Invalid Ayush"}

    user_data = resp_json.get("data", {}).get("user")
    if not user_data:
        return {"error": "User not found", "module_dev": "Invalid Ayush"}

    # Add estimated year if available
    if year:
        user_data["estimated_creation_year"] = year

    # Add module_dev key
    user_data["module_dev"] = "Invalid Ayush"

    # Return full dictionary (all fields)
    return user_data
