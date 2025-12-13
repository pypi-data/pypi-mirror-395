import inspect
import time
import os
from colorama import init, Fore
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
import re
import multiprocessing

init(autoreset = True)
_num_cores = multiprocessing.cpu_count()
_name = "ROMPlugin"
_MwConnect = MwConnect()

#按照Test仿写自己需要的函数即可
def ShowRomWindow():
    params = inspect.signature(ShowRomWindow).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ShowRomWindow, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)
    
def CloseRomWindow():
    params = inspect.signature(CloseRomWindow).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CloseRomWindow, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)
     
    
def TestStr(Par1:str = "6"):
    params = inspect.signature(TestStr).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(TestStr, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)


       