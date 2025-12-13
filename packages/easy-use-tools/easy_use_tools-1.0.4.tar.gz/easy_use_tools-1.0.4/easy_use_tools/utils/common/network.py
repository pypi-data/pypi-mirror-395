# coding=utf-8
import socket
def test_ip_port_reachable(ip, port):
    """
    description: test network port connectivity
    """
    status = True
    timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(3)
    s = socket.socket()
    try:
        s.connect((ip, port))
    except socket.error:
        status &= False
    finally:
        s.close()
        socket.setdefaulttimeout(timeout)
    return status

def ping_host_simple(host, timeout=5):
    """
    description: using ping3 tool to ping target host
    """
    try:
        from ping3 import ping
        response_time = ping(host, timeout=timeout)
        return response_time is not None
    except Exception as e:
        print(f"ping3 check error: {e}")
        return False