import subprocess
import multiprocessing
from log import STREAM_INFO_INSTANCE as log


class ProxyProcess(multiprocessing.Process):
    def __init__(self, config_file="/home/han/.proxy/config.json"):
        """ProxyProcess"""
        super(ProxyProcess, self).__init__()
        self.config_file = config_file
        log.info("ProxyProcess init!")

    def run(self):
        """Proxy Run"""
        log.info("ProxyProcess Start!")
        subprocess.run(["pkill", "-f", "trojan"])
        subprocess.run(["rm", "-rf", "trojan.log"])
        subprocess.run(["trojan", "-l", "trojan.log", "-c", self.config_file])