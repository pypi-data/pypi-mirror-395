from .Utils import MwConnect
import sys

def StartSysplorer(start_mode: str = '-gui', processPath: str = None, ip: str = None, args: list = None, port = None):
    """
    启动Sysplorer，并连接
    """
    MwConnect().__StartSysplorer__(ip = ip, port = port, processPath = processPath,
                                 start_mode = start_mode, argsparam = args)

def FindSysplorer() -> list:
    """
    查找可以连接的Sysplorer，返回端口号
    """
    processName = 'mworks'
    port_list = MwConnect().__FindSysplorer__(processName)
    if len(port_list) != 0:
        print(f"可用端口列表为{port_list.ports}")
    return port_list

def ConnectSysplorer(ip: str = None, port: int = None):
    """
    连接到已经打开的Sysplorer，通过 FindSysplorer 函数获取可以连接的端口号
    """
    if not port:
        process_ports = FindSysplorer()
        if process_ports == [] or (port == 0 and sys.platform == "win32"):
            print("将启动一个新的Sysplorer")
            StartSysplorer()
            return
        else:
            port = process_ports[0]
    print(f"Connected: {ip}:{port}")
    MwConnect().__ConnectorSysplorer__(ip, port)
    
def ConnectSysplorerForCmd(ip: str = "127.0.0.1", port: int = None):
    """
    连接到已经打开的Sysplorer，通过 FindSysplorer 函数获取可以连接的端口号
    """
    if not port:
        print(f"port = {port}")
        return False
    return MwConnect().__ConnectorSysplorer__(ip, port)

__all__ = ['StartSysplorer', 'FindSysplorer', 'ConnectSysplorer', 'ConnectSysplorerForCmd']