from typing import Tuple
import requests
from log import STREAM_INFO_INSTANCE as log

BINANCE_BASE_URL="https://api.binance.com"

# Proxy config
PROXIES = {
    'http': 'socks5h://127.0.0.1:19001',
    'https': 'socks5h://127.0.0.1:19001'
}

SYMBOL=["DOGEUSDT"]

def get_recent_trades(symbol: str = None, limit: int = 1) -> Tuple:
    """get_recent_trades

    @param symbol: trading pair
    @param limit: Trading volume 1 < limit < 1000

    @return (status, info, trading list)
    """
    url = "%s/api/v3/trades" % BINANCE_BASE_URL

    if not symbol or limit > 1000 or limit < 1:
        err_info = \
            "symbol or limit is illegal." \
            "symbol must not None, 1 < limit < 1000!"
        return False, err_info, []

    params = {
        "symbol": symbol,
        "limit": limit
    }
    res = requests.get(url, params=params, proxies=PROXIES).text
    res = res.replace("false", "False").replace("true", "True")
    res = eval(res)
    return True, "get recent trades success!", res
    

