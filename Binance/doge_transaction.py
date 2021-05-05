import time
from log import STREAM_INFO_INSTANCE as log
from auto_transaction import SingleTransaction
from auto_transaction import proxy_func

class DogeTransaction(SingleTransaction):
    def __init__(self):
        super().__init__("DOGE")

    def run(self):
        if not self.initialize():
            return
        # 买入
        # 涨 1% 卖出盈利， 跌0.5% 卖出止损
        while True:
            if not self._order_status and self._usdt_qty > 10: # 买入
                log.info("query trading pair")
                now_trading = self._query_trading_pair()
                log.info("ready to buy")
                if not self._buy(float("%.1f" % (self._usdt_qty / float(now_trading["seller"]))), float("%.5f" % (float(now_trading["seller"]) * 0.9999))):
                    log.info("buy error")
                    return
                self._order_start_time = time.time()
                flag = False
                while time.time() - self._order_start_time < 10:
                    query_order = self._query_order()
                    log.info(query_order)
                    if not query_order == "NEW":
                        flag = True
                        break

                if not flag:
                    self._cancel()
                    self._order_status = ""
                    log.info("buy doge failed! try to rebuy")
                    continue
                status, self._currency_qty = self._update_currency(self._currency)
                status, self._usdt_qty = self._update_currency("USDT")
                self._hold_price = float(now_trading["seller"])

            elif self._order_status == "BUY":
                now_trading = self._query_trading_pair()
                log.info("i have usdt %s doge %s" % (self._usdt_qty, self._currency_qty))
                log.info("now buyer:%s profit:%s loss:%s" % (self._hold_price, 1.01 * self._hold_price, 0.995 * self._hold_price))
                if float(now_trading["buyer"]) > 1.01 * self._hold_price:
                    if not self._sell(float("%.1f" % self._currency_qty), float("%.5f" % (float(now_trading["buyer"] * 1.0002)))):
                        log.error("sell doge error")
                        return
                elif float(now_trading["buyer"]) < 0.995 * self._hold_price:
                    if not self._sell(float("%.1f" % self._currency_qty), float("%.5f" % (float(now_trading["buyer"] * 1.0002)))):
                        log.error("sell doge error")
                        return
            elif self._order_status == "SELL":
                if not self._query_order() == "NEW":
                    self._order_status = ""

if __name__ == "__main__":
    log.info("auto trade entry")
    proxy = proxy_func()
    auto_trade = DogeTransaction()
    auto_trade.start()
    auto_trade.join()
    proxy.kill()

