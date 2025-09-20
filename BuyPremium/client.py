import httpx
import logging
from  config import DATA, FRAGMENT_HASH, FRAGMENT_ADDRES,FRAGMENT_PUBLICKEY,FRAGMENT_WALLETS

def get_cookies(DATA):
    return {
        'stel_ssid': DATA.get('stel_ssid', ''),
        'stel_dt': DATA.get('stel_dt', ''),
        'stel_ton_token': DATA.get('stel_ton_token', ''),
        'stel_token': DATA.get('stel_token', ''),
    }

class FragmentClient:
    URL = F"https://fragment.com/api?hash={FRAGMENT_HASH}"

    async def fetch_recipient(self, query, mountity):
        data = {"query": query,  "months": mountity, "method": "searchPremiumGiftRecipient"}
        print(data)
        async with httpx.AsyncClient() as client:
            response = await client.post(self.URL, cookies=get_cookies(DATA), data=data)
            print(response.json())
            return response.json().get("found", {}).get("recipient")

    async def fetch_req_id(self, recipient, mountity):
        data = {"recipient": recipient, "months": mountity, "method": "initGiftPremiumRequest"}
        async with httpx.AsyncClient() as client:
            response = await client.post(self.URL, cookies=get_cookies(DATA), data=data)
            print(response.json())
            return response.json().get("req_id")

    async def fetch_buy_link(self, recipient, req_id, mountity):
        data = {
            "address": f"{FRAGMENT_ADDRES}", "chain": "-239",
            "walletStateInit": f"{FRAGMENT_WALLETS}",
            "publicKey": f"{FRAGMENT_PUBLICKEY}",
            "features": ["SendTransaction", {"name": "SendTransaction", "maxMessages": 255}], "maxProtocolVersion": 2,
            "platform": "iphone", "appName": "Tonkeeper", "appVersion": "5.0.14",
            "transaction": "1",
            "id": req_id,
            "show_sender": "0",
            "method": "getGiftPremiumLink"
        }
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://fragment.com",
            "referer": f"https://fragment.com/premium/gift?recipient={recipient}&months={mountity}",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "x-requested-with": "XMLHttpRequest"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.URL, headers=headers, cookies=get_cookies(DATA), data=data)
            json_data = response.json()
            print(json_data)
            if json_data.get("ok") and "transaction" in json_data:
                transaction = json_data["transaction"]
                return transaction["messages"][0]["address"], transaction["messages"][0]["amount"], transaction["messages"][0]["payload"]
        return None, None, None
