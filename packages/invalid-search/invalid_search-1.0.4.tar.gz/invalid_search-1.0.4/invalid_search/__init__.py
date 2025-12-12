import httpx
import types
import sys
import json

def _search_number(number: str) -> dict:
    url = "https://allinfofinder.vercel.app/api/search"
    params = {"number": number}

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Windows NT 10.0)",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://allinfofinder.vercel.app/api",
    }

    try:
        client = httpx.Client(timeout=20)
        r = client.get(url, params=params, headers=headers)


        raw_text = r.content.decode("utf-8", errors="ignore")
        data = json.loads(raw_text)


        if "fetched" in data and "developer" in data["fetched"]:
            data["fetched"]["developer"] = "@AyushIsInvalidd"

        return data

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

class _CallableModule(types.ModuleType):
    def __call__(self, number):
        return _search_number(number)

sys.modules[__name__].__class__ = _CallableModule
