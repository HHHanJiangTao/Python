import time
import multiprocessing

from proxy import ProxyProcess
from binance_api import BINANCE_INSTANCE
from binance_api import get_sys_status
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
        ETH_USDT_STATUS = "USDT"
        # while True:
        log.info(BINANCE_INSTANCE.get_user_data("USDT"))
        log.info(BINANCE_INSTANCE.get_exchange_info("DOGEUSDT"))
        # BINANCE_INSTANCE.limit_maker("ETHUSDT", "BUY", "0.01", "1000")



if __name__ == "__main__":
    log.info("auto trade entry")
    proxy = proxy_func()
    if get_sys_status():
        auto_trade = AutoTransaction()
        auto_trade.start()
        auto_trade.join()
    proxy.kill()

