# coding=utf-8
import platform
import socket
import sys

from easy_use_tools.utils.common import gpu

def is_win_sys():
    """
        description:
    """
    if sys.platform.startswith('win'):
        return True
    elif sys.platform.startswith('linux'):
        return False





class SystemInfo:
    def __init__(self):
        self.is_win=is_win_sys()

    def _get_system_info(self):
        """
            description: Get system info
        """
        import cpuinfo
        cpu = cpuinfo.get_cpu_info()
        info = {
            "sys_type": platform.system(),
            "sys_version": platform.version(),
            "sys_arch_hardware": platform.machine(),
            "sys_arch_interpreter": platform.architecture()[0],
            "host_name": platform.node(),
            "cpu_simple": platform.processor(),
            "cpu_detail": cpu.get('brand_raw'),
            "cpu_arch": cpu.get('arch'),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
        }
        return info

    def _get_other_info(self):
        """
            description: Get other info
        """
        info = {
            "vbios": "N/A" if self.is_win else gpu.linux_get_vbios(),
        }
        return info

    def _get_gpu_drivers(self):
        """
            description: Get all GPU driver info, includes GPU name/version
        """
        if self.is_win:
            return gpu.win_get_gpu_drivers()
        else:
            return gpu.linux_get_gpu_drivers()

    def get_info(self):
        """
            description: Get system info
        """
        re_data = {
            "sys_info": self._get_system_info(),
            "gpu_info": self._get_gpu_drivers(),
            "other_info": self._get_other_info()
        }
        return re_data

print(SystemInfo().get_info())

