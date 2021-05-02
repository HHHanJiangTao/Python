import time
import requests
import subprocess
import multiprocessing

# Proxy config
PROXIES = {
    'http': 'socks5h://127.0.0.1:19001',
    'https': 'socks5h://127.0.0.1:19001'
}


class ProxyProcess(multiprocessing.Process):
    def __init__(self, config_file="/home/hanjiangtao/.proxy/config.json"):
        """ProxyProcess"""
        super(ProxyProcess, self).__init__()
        self.config_file = config_file
        print("ProxyProcess init")

    def run(self):
        """Proxy Run"""
        print("Proxy Run")
        subprocess.run(["trojan", self.config_file])

if __name__ == "__main__":
    proxy = ProxyProcess()
    proxy.start()
    time.sleep(1)
    url = 'https://api.binance.com/wapi/v3/systemStatus.html'  
    html = requests.get(url, proxies=PROXIES).text  
    print(html)
    proxy.kill()
