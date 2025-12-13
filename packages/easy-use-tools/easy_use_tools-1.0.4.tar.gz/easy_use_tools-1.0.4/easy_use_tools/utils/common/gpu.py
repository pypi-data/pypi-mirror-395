# coding=utf-8
import re
import subprocess
from numpy.core.defchararray import upper
from easy_use_tools.utils.common import base
def win_get_gpu_drivers():
    """
        description: get windows GPU drivers
    """
    import wmi
    try:
        c = wmi.WMI()
        drivers = {}

        # 获取所有显卡设备
        for adapter in c.Win32_VideoController():
            driver_version = adapter.DriverVersion
            adapter_name = adapter.Name
            drivers.update({adapter_name: driver_version})
        return drivers
    except Exception as e:
        print(f"Fail to get GPU drivers: {str(e)}")
        return None

def linux_get_gpu_drivers():
    """
        description: Get linux GPU drivers
    """

    gpu_type = base.run_shell("lsmod | grep mwv | head -n 1 | awk '{print $1}'").strip()  # mwv207d
    if gpu_type:
        gpu_driver = base.run_shell_with_map(f"dpkg -l | grep '{gpu_type}'").get("result")
        print(f"GPU Type: {gpu_type},GPU Driver: {gpu_driver}")
        _driver_ver_name = gpu_driver if gpu_driver else "N/A"
    else:
        _driver_ver_name = "N/A"
    return _driver_ver_name

def linux_get_gpu_type():
    """
        测试机器的显卡类型
    """
    result = subprocess.Popen('lspci | grep "VGA compatible controller:"', shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    tmp = str(result.stdout.readline())
    if 'JJM' in tmp:
        mat = re.match(r'.*Device (\d+) \D+.*', tmp)
        if mat is None:
            mat = re.match(r'.*JM(\d+)\D+.*', tmp)
        _gpe_type_name = 'JM' + mat.group(1)
    elif 'JM' in tmp:
        mat = re.match(r'.*JM(\d+)\D+.*', tmp)
        _gpe_type_name = 'JM' + mat.group(1)
    elif 'Jingjia Microelectronics' in tmp:
        mat = re.match(r'.*Device (\d+) \D+.*', tmp)
        _gpe_type_name = 'JM' + mat.group(1)
    elif 'AMD' in tmp:
        _gpe_type_name = 'AMD'
    else:
        _gpe_type_name = 'unknown'

    return _gpe_type_name

def linux_get_vbios():
    """
        测试机器的vbios版本
    """
    gpu_name = linux_get_gpu_type()
    print(f"[vbios]GPU: {gpu_name}")
    # AMD
    if "AMD" in upper(gpu_name):
        print("[vbios]:AMD GPU")
        get_rst = base.run_shell_with_map(
            "lspci -v -s $(lspci | grep -i 'vga\|3d\|display' | awk '{print $1}') | grep -i 'vga\|bios\|version'").get(
            "result").strip()
    # jingjia
    else:
        print("[vbios]:Jingjia GPU")
        if '72' in gpu_name:
            get_rst = base.run_shell_with_map('cat /proc/gpuinfo_0 | grep "firmware"').get("result").strip()
        elif '92' in gpu_name or '91' in gpu_name:
            get_rst = base.run_shell_with_map('cat /proc/gpuinfo_0 | grep "firmware"').get("result").strip()
        elif '11' in gpu_name:
            get_rst = base.run_shell_with_map("jm-smi -q | grep 'VBIOS Version'|awk '{print $NF}'").get("result").strip()
        else:
            get_rst = "N/A"
    _v_ios_name = get_rst
    return _v_ios_name