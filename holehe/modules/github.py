def github(email, client, out):
    r = client.post(
        "https://github.com/password_reset",
        data={"email": email}
    )
    if r.status_code == 200:
        out["exists"] = True
