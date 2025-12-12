import requests
import psycopg2
from urllib.parse import urlparse

# External Render DB URL
DATABASE_URL = 'postgresql://api_control_panel_user:P3M6R2CJbIsdePfCep1YLXxgFc7dBPgp@dpg-d4ng4r6uk2gs739r2hs0-a.oregon-postgres.render.com/api_control_panel'
result = urlparse(DATABASE_URL)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=result.hostname,
    port=result.port,
    database=result.path[1:],
    user=result.username,
    password=result.password,
    sslmode="require"
)

cur = conn.cursor()

# Fetch all URLs
cur.execute("SELECT type, url FROM api_urls;")
rows = cur.fetchall()

# Convert to dictionary
api_urls = {row[0]: row[1] for row in rows}

# Get ONLY aadhar URL safely
aadhar_url = api_urls.get("aadhar_api", "")

cur.close()
conn.close()


def aadhar(aadhar_number: str):
    global aadhar_url

    # Aadhaar must be 12 digits
    if not aadhar_number.isdigit() or len(aadhar_number) != 12:
        return {
            "error": "Invalid Aadhaar number",
            "module_dev": "Invalid Ayush"
        }

    if aadhar_url == "":
        return {
            "error": "Aadhaar API URL not found in database",
            "module_dev": "Invalid Ayush"
        }

    # Replace {number} with actual Aadhaar number
    final_url = aadhar_url.replace("{number}", aadhar_number)

    try:
        r = requests.get(final_url, timeout=10)

        if r.status_code != 200:
            return {
                "error": f"API error {r.status_code}",
                "module_dev": "Invalid Ayush"
            }

        data = r.json()
        data["module_dev"] = "Invalid Ayush"
        return data

    except Exception as e:
        return {
            "error": str(e),
            "module_dev": "Invalid Ayush"
        }
