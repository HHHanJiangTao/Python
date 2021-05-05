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
        self._hold_price = 0
        self._mark_price = 0
        self._decline_count = 0
        self._usdt_qty = 0
        self._currency_qty = 0
        self._side = ""
        self._order_id = ""
        self._order_status = ""
        self._order_start_time = 0
        log.info("%s class entry!", self.__class__.__name__)
        log.info(BINANCE_INSTANCE.get_exchange_info(self._trading_pair))

    def initialize(self):
        if not BINANCE_INSTANCE.get_sys_status():
            log.error("remote binance system is maintenance!")
            return False
        log.info("binance system is normal")

        status, self._usdt_qty = self._update_currency("USDT")
        if not status:
            return
        log.info("the account has %f usdt free!" % self._usdt_qty)

        status, self._currency_qty = self._update_currency(self._currency)
        if not status:
            return
        log.info("the account has %f %s free!" % (self._currency_qty, self._currency))

        return True

    def _update_currency(self, currency):
        currency_data = BINANCE_INSTANCE.get_user_data(currency)
        if not currency_data:
            log.error("can not fetch account %s" % currency)
            return False, 0
        return True, float(currency_data["free"])

    def _sell(self, qty, price):
        log.info("SELL %s qty:%s price:%s" % self._trading_pair, qty, price)
        res = BINANCE_INSTANCE.limit_maker(self._trading_pair, "SELL", qty, price)
        if not "orderId" in res:
            return False
        self._order_id = res["orderId"]
        self._order_status = "SELL"
        return True

    def _buy(self, qty, price):
        log.info("BUY %s qty:%s price:%s" % (self._trading_pair, qty, price))
        res = BINANCE_INSTANCE.limit_maker(self._trading_pair, "BUY", qty, price)
        if not "orderId" in res:
            return False
        self._order_id = res["orderId"]
        self._order_status = "BUY"
        return True

    def _cancel(self):
        if not self._order_status:
            log.warning("there is no order found!")
            return False
        return BINANCE_INSTANCE.cancel_order(self._trading_pair, self._order_id)

    def _query_order(self):
        if not self._order_status:
            log.warning("there is no order found!")
            return False
        query = BINANCE_INSTANCE.query_order(self._trading_pair, self._order_id)
        return query.get("status", "NEW")

    def _query_trading_pair(self):
        return BINANCE_INSTANCE.get_best_trading_pair(self._trading_pair)


if __name__ == "__main__":
    log.info("auto trade entry")
    proxy = proxy_func()
    auto_trade = SingleTransaction("DOGE")
    auto_trade.start()
    auto_trade.join()
    proxy.kill()

