import time
import multiprocessing

from proxy import ProxyProcess
from binance_api import BINANCE_INSTANCE
from binance_api import SYMBOL
from log import STREAM_INFO_INSTANCE as log


def proxy_func():
    proxy = ProxyProcess()
    proxy.start()
    time.sleep(1)
    return proxy

class SingleTransaction(multiprocessing.Process):
    def __init__(self, currency):
        super().__init__()
        self._currency = currency
        self._trading_pair = "%sUSDT" % self._currency
        self._usdt_qty = 0
        self._currency_qty = 0
        self._side = ""
        log.info("%s class entry!", self.__class__.__name__)

    def initialize(self):
        if not BINANCE_INSTANCE.get_sys_status():
            log.error("remote binance system is maintenance!")
            return False
        log.info("binance system is normal")

        usdt = BINANCE_INSTANCE.get_user_data("USDT")
        if not usdt:
            log.error("can not fetch account USDT")
            return False
        self._usdt_qty = float(usdt["free"])
        log.info("the account has %f usdt free!" % self._usdt_qty)

        currency = BINANCE_INSTANCE.get_user_data(self._currency)
        if not currency:
            log.error("can not fetch account %s" % currency)
            return False
        self._currency_qty = float(currency["free"])
        log.info("the account has %f %s free!" % (self._currency_qty, self._currency))

        return True


if __name__ == "__main__":
    log.info("auto trade entry")
    proxy = proxy_func()
    auto_trade = SingleTransaction("DOGE")
    auto_trade.start()
    auto_trade.join()
    proxy.kill()

