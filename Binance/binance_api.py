from typing import Tuple
from typing import List
from typing import Dict
import os
import time
import hmac
import json
import hashlib
import requests
from log import STREAM_INFO_INSTANCE as log

# Proxy config
PROXIES = {
    'http': 'socks5h://127.0.0.1:19001',
    'https': 'socks5h://127.0.0.1:19001'
}

SYMBOL=["DOGEUSDT", "TLMUSDT"]


class BinanceApi:
    def __init__(self):
        self.binance_base_url = "https://api.binance.com"
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.secret_key = os.getenv("BINANCE_SECRET_KEY")
        self.timestamp_offset = 0

    def get_sys_status(self) -> bool:
        """get binance system status
        
        @return bool: True: normal, False: system maintenance"""
        "https://api.binance.com/sapi/v1/system/status"
        url = "%s/sapi/v1/system/status" % self.binance_base_url
        res = eval(requests.get(url, proxies=PROXIES).text)
        if not isinstance(res, dict):
            log.error("error responce:%s" % res)
            return False
        return True if not res.get("status", 1) else False

    def _update_headers_with_signature(self, params:dict):
        query_string = '&'.join(["{}={}".format(d, params[d]) for d in params])
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        params['signature'] = signature.hexdigest()
        return params

    def limit_maker(self, symbol, side, quantity, price):
        url = "%s/api/v3/order" % self.binance_base_url
        params = {
            "timestamp": str(int(time.time() * 1000)),
            "symbol": symbol,
            "side": side,
            "type": "LIMIT_MAKER",
            "quantity": quantity,
            "price": price,
            "newOrderRespType": "ACK"
        }
        params = self._update_headers_with_signature(params)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        res = requests.post(url, headers=headers, params=params, proxies=PROXIES).text
        log.info(res)
        return eval(res)

    def cancel_order(self, symbol, order_id):
        url = "%s/api/v3/order" % self.binance_base_url
        params = {
            "timestamp": str(int(time.time() * 1000)),
            "symbol": symbol,
            "orderId": order_id
        }
        params = self._update_headers_with_signature(params)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        res = requests.delete(url, headers=headers, params=params, proxies=PROXIES).text
        res = eval(res)
        if res["status"] == "CANCELED":
            return True
        log.error("cancled failed!!")
        return False

    def get_user_data(self, currency):
        """get_user_data
        """
        url = "%s/api/v3/account" % self.binance_base_url
        params = {
            "timestamp": str(int(time.time() * 1000))
        }
        params = self._update_headers_with_signature(params)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        res = requests.get(url, headers=headers, params=params, proxies=PROXIES).text
        res = res.replace("false", "False").replace("true", "True")
        res = eval(res)
        if not "balances" in res:
            log.info(res)
            return None
        for item in res["balances"]:
            if item["asset"] == currency:
                return item
        return None

    def query_order(self, symbol, order_id):
        url = "%s/api/v3/order" % self.binance_base_url
        params = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": str(int(time.time() * 1000))
        }
        params = self._update_headers_with_signature(params)
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        res = requests.get(url, headers=headers, params=params, proxies=PROXIES).text
        res = res.replace("false", "False").replace("true", "True")
        return eval(res)

    def get_exchange_info(self, symbol):
        url = "%s/api/v3/exchangeInfo" % self.binance_base_url
        res = requests.get(url, proxies=PROXIES).text
        res = res.replace("false", "False").replace("true", "True")
        res = eval(res)
        for item in res["symbols"]:
            if item["symbol"] == symbol:
                return item
        return None

    def get_recent_trades(self, symbol: str = None, limit: int = 1) -> List:
        """get_recent_trades

        @param symbol: trading pair
        @param limit: Trading volume 1 < limit < 1000

        @return list(if empty is not correct)
        """
        url = "%s/api/v3/trades" % self.binance_base_url

        if not symbol or limit > 1000 or limit < 1:
            err_info = \
                "symbol or limit is illegal." \
                "symbol must not None, 1 < limit < 1000!"
            log.error(err_info)
            return []

        params = {
            "symbol": symbol,
            "limit": limit
        }
        res = requests.get(url, params=params, proxies=PROXIES).text
        res = res.replace("false", "False").replace("true", "True")
        res = eval(res)
        return res

    def get_best_trading_pair(self, symbol: str = None) -> Dict:
        """get_best_trading_pair

        @param symbol: trading pair

        @return Dict {"seller": , "buyer":}
        """
        url = "%s/api/v3/ticker/bookTicker" % self.binance_base_url
        params = {
            "symbol": symbol
        }
        res = requests.get(url, params=params, proxies=PROXIES).text
        res = eval(res)
        return {
            "symbol": symbol,
            "buyer": res.get("bidPrice", 0),
            "seller": res.get("askPrice", 0)
        }


BINANCE_INSTANCE = BinanceApi()
