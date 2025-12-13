import inspect
import os
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
from colorama import init
init(autoreset = True)
#按照Test仿写自己需要的函数即可
# 此处为C++接口名
_name = "TextViewPlugin"
_MwConnect = MwConnect()

@mw_connect_decorator(_MwConnect._process_path)
def ShowView():
    params = inspect.signature(ShowView).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ShowView, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def TestVoid():
    params = inspect.signature(TestVoid).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(TestVoid, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def TestInt(Par1 = 1):
    if type(Par1) == int or type(Par1) == float:
        Par1 = int(Par1)
    else:
        return False
    params = inspect.signature(TestInt).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index("Par1") - 1] = type(Par1)
    return _MwConnect.__RunCurrentFunction__(TestInt, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def TestBool(Par1:bool = True):
    params = inspect.signature(TestBool).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(TestBool, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def TestStr(Par1:str = "6"):
    params = inspect.signature(TestStr).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(TestStr, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 私有变量函数，命名首字符加'_'
# __all__ 保证在使用from  import * 时，只导出公有函数即不带'_'的变量和函数，避免相同名称冲突
__all__ = [name for name in globals() if not name.startswith('_')]