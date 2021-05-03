from typing import Tuple
from typing import List
from typing import Dict
import requests
from log import STREAM_INFO_INSTANCE as log

BINANCE_BASE_URL="https://api.binance.com"

# Proxy config
PROXIES = {
    'http': 'socks5h://127.0.0.1:19001',
    'https': 'socks5h://127.0.0.1:19001'
}

SYMBOL=["DOGEUSDT", "TLMUSDT"]

def get_sys_status() -> bool:
    """get binance system status
    
    @return bool: True: normal, False: system maintenance"""
    url = "%s/sapi/v1/system/status" % BINANCE_BASE_URL
    res = eval(requests.get(url, proxies=PROXIES).text)
    if not isinstance(res, dict):
        log.error("error responce:%s" % res)
        return False
    return True if not res.get("status", 1) else False

def get_recent_trades(symbol: str = None, limit: int = 1) -> List:
    """get_recent_trades

    @param symbol: trading pair
    @param limit: Trading volume 1 < limit < 1000

    @return list(if empty is not correct)
    """
    url = "%s/api/v3/trades" % BINANCE_BASE_URL

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

def get_best_trading_pair(symbol: str = None) -> Dict:
    """get_best_trading_pair

    @param symbol: trading pair

    @return Dict {"seller": , "buyer":}
    """
    url = "%s/api/v3/ticker/bookTicker" % BINANCE_BASE_URL
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

