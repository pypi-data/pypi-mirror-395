# coding=utf-8
import datetime
import hashlib
import os
import sys
import logging
import better_exceptions
import pyautogui

RECURSIVE_CREATE_DIR = lambda dp: os.makedirs(dp) or dp if not os.path.exists(dp) else dp  # ---> mkdir -p

def get_current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

def better_show_exception(print_type="print"):
    """
        详细打印异常的堆栈信息

    """
    e_type, value, e_traceback = sys.exc_info()
    msg = ''
    rst = better_exceptions.format_exception(e_type, value, e_traceback)
    for i in rst:
        msg += i
        msg += '\n'
    if print_type == "print":
        print(msg)
    else:
        logging.error(msg)


def human_duration(seconds: int) -> str:
    """
    将秒数自动转换成易读字符串
    支持的最大单位是 year，可根据需要扩展
    """
    if seconds == 0:
        return "0s"

    # 定义时间单位与秒数的映射（从大到小）
    units = [
        ("year", 365 * 24 * 3600),
        ("day", 24 * 3600),
        ("h", 3600),
        ("m", 60),
        ("s", 1)
    ]

    parts = []
    remainder = abs(seconds)
    for name, count in units:
        if remainder >= count:
            num = remainder // count
            parts.append(f"{num}{name}")
            remainder -= num * count

    # 拼接并保留符号
    sign = "-" if seconds < 0 else ""
    return sign + " ".join(parts)

def take_screenshot(f_path):
    """
    截图并保存为文件
    """
    screenshot = pyautogui.screenshot()
    rst = screenshot.save(f_path)
    return rst

def calculate_string_md5(input_string):
    """
    description: 计算字符串的md5值
    :param input_string:md5
    :return:  eg: 098F6BCD4621D373CADE4E832627B4F6

    """
    md5 = hashlib.md5()
    b = input_string.encode(encoding='utf-8')
    md5.update(b)
    str_md5 = md5.hexdigest()
    return str_md5