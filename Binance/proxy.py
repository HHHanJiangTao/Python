import subprocess
import multiprocessing
from log import STREAM_INFO_INSTANCE as log


class ProxyProcess(multiprocessing.Process):
    def __init__(self, config_file="/home/hanjiangtao/.proxy/config.json"):
        """ProxyProcess"""
        super(ProxyProcess, self).__init__()
        self.config_file = config_file
        log.info("ProxyProcess init!")

    def run(self):
        """Proxy Run"""
        log.debug("ProxyProcess Start!")
        subprocess.run(["pkill", "-f", "trojan"])
        subprocess.run(["trojan", self.config_file])