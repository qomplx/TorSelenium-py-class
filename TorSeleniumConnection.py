import json
import os
import requests
import time
from datetime import datetime
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

class TorSeleniumConnection:
    def __init__(self, url):
        self.url = f'http://{url}'
        self.binary = FirefoxBinary(os.getenv('TORPATH'))
        self.profile = FirefoxProfile(os.getenv('TORPROFILE'))
        self.profile.set_preference('network.proxy.type', 1)
        self.profile.set_preference('network.proxy.socks', '127.0.0.1')
        self.profile.set_preference('network.proxy.socks_port', 9150)
        self.profile.set_preference('network.proxy.socks_version', 5 )
        self.profile.set_preference('network.proxy.socks_remote_dns', True )

        self.tries = 1
        self.timeout = 30

        self.options = Options()
        self.options.headless = True

        self.caps=DesiredCapabilities.FIREFOX
        self.caps["wires"]=True

        self.browser = self.start_browser()
        # self.browser.set_page_load_timeout(self.timeout)s

    def start_browser(self):
        return webdriver.Firefox(
            firefox_profile=self.profile,
            firefox_binary=self.binary,
            capabilities=self.caps,
            options=self.options
        )

    def get_site(self, count=0):

        while self.tries > count:
            try:
                print(f"{count + 1} | Site {self.url}")
                self.browser.set_page_load_timeout(self.timeout)
                self.browser.get(self.url)

                print(f"=== {self.url} has responded ===")

                # Do not Delete this as it is required to wait for JavaScript to load
                time.sleep(5)
                source = self.browser.page_source
                self.browser.close()

                return True, source
            except Exception as e:
                count +=1
                print(f"=== EXCEPTION: {e} ===")
                self.browser.close()

                if count >= self.tries or "error" in e:
                    print("=== Moving on ===")

                    return False, None
                elif "neterror" in e:
                    return False, None
                else:
                    self.browser = self.start_browser()
                    break

            count += 1
        return False, None
