# -*- coding:utf-8 -*-
import Config
import os
import time
import platform
from selenium import webdriver as Webdriver

def webdriver_create():
    driver = Webdriver.PhantomJS(executable_path=Config.phantomjs_path, service_args=["--load-images=false"])
    driver.implicitly_wait(10)
    return driver

def wait_element_loaded(webdriver, xpath, time_to_retry=0):
    while time_to_retry >= 0:
        try:
            webdriver.find_element_by_xpath(xpath)
            return True
        except:
            if time_to_retry > 0:
                webdriver.refresh()
                time.sleep(1)
        time_to_retry -= 1
    return False

def click_element(webdriver, xpath, index=0):
    try:
        webdriver.find_elements_by_xpath(xpath)[index].click()
    except:
        return False
    return True

def build_path(keyword):
    timestamp = time.time()
    timestamp_str = str(timestamp).split('.')[0]
    if platform.system() == 'Windows':
        return Config.crawler_data_path + '\\' + keyword + '\\' + timestamp_str
    else:
        return Config.crawler_data_path + '/' + keyword + '/' + timestamp_str

def append_path(root_path, append):
    if platform.system() == 'Windows':
        return root_path + '\\' + append
    else:
        return root_path + '/' + append

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
