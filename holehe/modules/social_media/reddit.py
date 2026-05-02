from holehe.core import *
from holehe.localuseragent import *


async def reddit(email, client, out):
    name = "reddit"
    domain = "reddit.com"
    method = "register"
    frequent_rate_limit = False

    try:
        headers = {
            'User-Agent': ua['chrome'],
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'email': email,
            'user': '',  # Not needed for check
        }
        req = await client.post(
            "https://www.reddit.com/api/check_email",
            headers=headers,
            data=data
        )
        if req.status_code == 200:
            response = req.json()
            if 'error' in response:
                if response['error'] == 'USER_DOESNT_EXIST':
                    out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                                "rateLimit": False,
                                "exists": False,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
                else:
                    out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
            else:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False,
                            "exists": True,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})