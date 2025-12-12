import httpx
import sys

def _search_number(number: str) -> dict:
    url = "https://allinfofinder.vercel.app/api/search"
    params = {"number": number}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/142.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://allinfofinder.vercel.app/api",
    }

    try:
        with httpx.Client(http2=True, timeout=20) as client:
            r = client.get(url, params=params, headers=headers)

            data = r.json()

            if "fetched" in data and "developer" in data["fetched"]:
                data["fetched"]["developer"] = "@AyushIsInvalidd"

            return data

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

sys.modules[__name__].__call__ = _search_number
