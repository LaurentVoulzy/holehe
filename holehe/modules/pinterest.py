def pinterest(email, client, out):
    r = client.post(
        "https://www.pinterest.com/password/reset/",
        data={"email": email}
    )
    if "email has been sent" in r.text.lower():
        out["exists"] = True
