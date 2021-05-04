
from log import STREAM_INFO_INSTANCE as log
from auto_transaction import SingleTransaction
from auto_transaction import proxy_func

class DogeTransaction(SingleTransaction):
    def __init__(self):
        super().__init__("DOGE")

    def run(self):
        if not self.initialize():
            return




if __name__ == "__main__":
    log.info("auto trade entry")
    proxy = proxy_func()
    auto_trade = DogeTransaction()
    auto_trade.start()
    auto_trade.join()
    proxy.kill()

