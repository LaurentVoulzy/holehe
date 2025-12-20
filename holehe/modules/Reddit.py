import requests

def reddit(email, client, out):
    r = client.post(
        "https://www.reddit.com/account/recovery",
        data={"email": email},
        headers={"User-Agent": "Mozilla/5.0"}
    )
    if "sent an email" in r.text.lower():
        out["exists"] = True
