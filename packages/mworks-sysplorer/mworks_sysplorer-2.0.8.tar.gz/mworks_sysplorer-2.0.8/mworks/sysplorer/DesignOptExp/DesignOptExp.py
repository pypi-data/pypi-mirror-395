import inspect
import time
import os
from colorama import init, Fore
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
import re
import multiprocessing
init(autoreset = True)

_num_cores = multiprocessing.cpu_count()
_name = "DesignOptExp"
_MwConnect = MwConnect()

"""
brief:初始化批量仿真
return:bool，初始化是否成功
storePath:仿真工作目录，计算机任意合法路径
instNum:实例池数目，默认50
options:仿真配置,key:"startTime":开始时间, "stopTime":结束时间, "outputStep":输出步长, "algorithm":仿真算法, "tolerance":精度, "saveEvent":存储事件时刻的变量值
solverPath:求解器路径
"""
@mw_connect_decorator(_MwConnect._process_path)
def InitialBatchSimulate(solverPath:str, storePath: str, instNum:int = 50, options:dict = {}):
    params = inspect.signature(InitialBatchSimulate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(InitialBatchSimulate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief:开始批量仿真
return:list, list(dict(str:list())), 外层list:批量结果， dict:key:结果变量名称, value:list， 结果变量数值
param: 仿真参数， list(dict(str:double))
resultName:对应每次仿真的结果变量名称，list(list(str))
"""
@mw_connect_decorator(_MwConnect._process_path)
def BatchSimulate(param:list, resultName:list):
    for inner_param in param:
        if type(inner_param) != dict:
            return False
    for name in resultName:
        if type(name) != list:
            return False
    params = inspect.signature(BatchSimulate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(BatchSimulate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

__all__ = [name for name in globals() if not name.startswith('_')]
#####################################jiangtao
