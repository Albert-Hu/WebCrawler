# -*- coding:utf-8 -*-
import Config

def debug(message=""):
    if Config.enable_debug_message:
        print(message)
