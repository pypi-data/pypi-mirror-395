# coding=utf-8
"""
######################################################
@Description: common utils
@Author: yuanyang.li
@Date: 2025-11-28
######################################################
"""
import datetime
import hashlib
import os
import subprocess
import sys
import logging
import better_exceptions


RECURSIVE_CREATE_DIR = lambda dp: os.makedirs(dp) or dp if not os.path.exists(dp) else dp  # ---> mkdir -p

def get_current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

######################################################

def func_example(path,header,use_cols):
    """
    [Description]: Run a Flask Service
    [Args]:
        path(str): run path
        header(int): header name
        use_cols(list): target clos
    [Returns]:
        List: result list
        Examples:
                ["rst","rst_1","rst_2"]
    """
    pass
# print(func_example.__doc__)

def better_show_exception(print_type="print"):
    """
    [Description]:
        Display stack information more effectively
    [Args]:
        print_type(str): print type
    [Returns]:
        None
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
    [Description]:
        Reverse seconds to a human read string,now support to 'year' unit
    [Args]:
        seconds(int): need reverse seconds
    [Returns]:
        Str: reversed result
        Examples:
                '3h 15m 34s'
    """
    if seconds == 0:
        return "0s"

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

    sign = "-" if seconds < 0 else ""
    return sign + " ".join(parts)

def take_screenshot(f_path,monitor_index=0):
    """
    [Description]:
        Save a screenshot
    [Args]:
        f_path(str): screenshot save path
        monitor_index(int): target monitor screenshot, -1 all save all
    [Returns]:
        Bool: saved result
        Examples:
                True/False
    """
    import mss
    from mss import tools
    #  多屏截图
    if monitor_index == -1:
        with mss.mss() as sct:
            # 获取所有屏幕合成的整张图
            img = sct.grab(sct.monitors[0])  # [0] 表示虚拟桌面即将多个显示器截图合并成一张，[1]为第一台显示器截图，[2]为第二台显示器截图
            mss.tools.to_png(img.rgb, img.size, output=f_path)
            return True
    # 指定屏幕截图
    else:
        with mss.mss() as sct:
            # 1. 查看并打印所有显示器信息
            print("可用的显示器：")
            for monitor_id, monitor_info in enumerate(sct.monitors):
                print(f"显示器 {monitor_id}: {monitor_info}")
            # 2. 假设你要截取编号为1的显示器（通常是扩展屏）
            target_monitor_number = monitor_index
            # 检查目标显示器是否存在
            if target_monitor_number < len(sct.monitors):
                # 获取该显示器的信息字典
                monitor = sct.monitors[target_monitor_number]

                # 使用grab方法截取该显示器
                screenshot = sct.grab(monitor)

                # 保存截图（mss.tools.to_png很方便）
                output_filename = f_path
                tools.to_png(screenshot.rgb, screenshot.size, output=output_filename)
                print(f"显示器[{target_monitor_number}]截图已保存为: {output_filename}")
                return True
            else:
                print(f"错误：不存在编号为 {target_monitor_number} 的显示器。")
                return False

def calculate_string_md5(input_string):
    """
    [Description]:
        Calculate the MD5 of a string
    [Args]:
        f_path(str): screenshot save path
    [Returns]:
        Bool: saved result
        Examples:
                '098F6BCD4621D373CADE4E832627B4F6'
    """
    md5 = hashlib.md5()
    b = input_string.encode(encoding='utf-8')
    md5.update(b)
    str_md5 = md5.hexdigest()
    return str_md5

def run_shell(cmd):
    rst_code, rst_msg = subprocess.getstatusoutput(cmd)
    if rst_code == 0:
        return rst_msg
    else:
        logging.error("shell cmd run failed and error code is : {},detail:{}".format(rst_code, rst_msg))
        return rst_msg


def run_shell_with_map(cmd):
    """
    [Description]:
        Run shell cmd
    [Args]:
        cmd(str): run cmd
    [Returns]:
        dict: run result
        Examples:
                {"error": False, "result": "XXXX", "code": 0}
    """
    logging.debug("run cmd:{}".format(cmd))
    rst_code, rst_msg = subprocess.getstatusoutput(cmd)
    if rst_code == 0:
        rst_error = False
    else:
        subprocess.getstatusoutput("echo  {}  >> /tmp/error_cmd.log".format(cmd))
        rst_error = True
    return {"error": rst_error, "result": rst_msg, "code": rst_code}
