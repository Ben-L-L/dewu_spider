import frida, sys
import time, requests


class DeWu():
    def __init__(self):
        self.app = 'com.shizhuang.duapp'
    def get_script(self):
        with open('./dewu_sign.js', 'r', encoding='utf-8')as f:
            jscode = f.read()
        process = frida.get_usb_device(1000).attach(self.app)
        script = process.create_script(jscode)
        script.load()
        return script

dw = DeWu()
