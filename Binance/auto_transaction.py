import time
import multiprocessing

from proxy import ProxyProcess
from binance_api import get_recent_trades
from binance_api import get_sys_status
from binance_api import get_best_trading_pair
from binance_api import get_user_data
from binance_api import SYMBOL
from log import STREAM_INFO_INSTANCE as log


def proxy_func():
    proxy = ProxyProcess()
    proxy.start()
    time.sleep(1)
    return proxy

class AutoTransaction(multiprocessing.Process):
    def __init__(self):
        super(AutoTransaction, self).__init__()

    def run(self):
        log.info(get_recent_trades(SYMBOL[0], 3))
        log.info(get_best_trading_pair(SYMBOL[0]))
        get_user_data()



if __name__ == "__main__":
    log.info("auto trade entry")
    proxy = proxy_func()
    if get_sys_status():
        auto_trade = AutoTransaction()
        auto_trade.start()
        auto_trade.join()
    proxy.kill()

