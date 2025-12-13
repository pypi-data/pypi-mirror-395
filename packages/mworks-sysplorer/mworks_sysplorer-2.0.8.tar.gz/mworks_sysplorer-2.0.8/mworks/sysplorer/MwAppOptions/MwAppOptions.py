import inspect
from colorama import init
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
init(autoreset = True)
_name = "MwAppOptions"
_MwConnect = MwConnect()

@mw_connect_decorator(_MwConnect._process_path)
def SetKernelBoolOption(option:str, value:bool) -> bool:
    """
    设置内核bool选项值
    
    参数列表：
        `option` : 选项名称
        `value` : 值
    函数返回值：
        `bool` : 表示是否设置成功

    示例：
        >>> MwAppOptions.SetKernelBoolOption("MWorks.Analyzer.OutputSelectedState", False)
        True

    注意事项：
        只能设置内核bool选项
    """
    params = inspect.signature(SetKernelBoolOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetKernelBoolOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def KernelBoolOption(option:str):
    """
    获取内核bool选项值
    
    参数列表：
        `option` : 选项名称
    函数返回值：
        `bool` : 获取选项值

    示例：
        >>> MwAppOptions.KernelBoolOption("MWorks.Analyzer.OutputSelectedState")
        False

    注意事项：
        只能获取内核Bool选项，失败返回False 
    """
    params = inspect.signature(KernelBoolOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(KernelBoolOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetKernelIntOption(option:str, value:int) -> bool:
    """
    设置内核Integer选项值
    
    参数列表：
        `option` : 选项名称
        `value` : 值
    函数返回值：
        `bool` : 表示是否设置成功

    示例：
        >>> MwAppOptions.SetKernelIntOption("", 1)
        True

    注意事项：
        只能设置内核Integer选项，内核暂时未提供Integer选项
    """
    params = inspect.signature(SetKernelIntOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetKernelIntOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def KernelIntOption(option:str):
    """
    获取内核Integer选项值
    
    参数列表：
        `option` : 选项名称
    函数返回值：
        `int` : 获取选项值

    示例：
        >>> MwAppOptions.KernelIntOption("")
        1

    注意事项：
        内核暂时未提供Integer选项，失败返回0 
    """
    params = inspect.signature(KernelIntOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(KernelIntOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetKernelDoubleOption(option:str, value:float) -> bool:
    """
    设置内核浮点数选项值
    
    参数列表：
        `option` : 选项名称
        `value` : 值
    函数返回值：
        `bool` : 表示是否设置成功

    示例：
        >>> MwAppOptions.SetKernelDoubleOption("", 1.0)
        True

    注意事项：
        只能设置内核Double选项，内核暂时未提供浮点选项
    """
    params = inspect.signature(SetKernelDoubleOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetKernelDoubleOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def KernelDoubleOption(option:str):
    """
    获取内核浮点数选项值
    
    参数列表：
        `option` : 选项名称
    函数返回值：
        `double` : 获取选项值

    示例：
        >>> MwAppOptions.KernelDoubleOption("")
        1.0

    注意事项：
        内核暂时未提供浮点选项，失败返回0.0
    """
    params = inspect.signature(KernelDoubleOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(KernelDoubleOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetKernelStringOption(option:str, value:str) -> bool:
    """
    设置内核str选项值
    
    参数列表：
        `option` : 选项名称
        `value` : 值
    函数返回值：
        `bool` : 表示是否设置成功

    示例：
        >>> MwAppOptions.SetKernelStringOption(""，"")
        True

    注意事项：
        只能设置内核str选项，内核暂时未提供str选项
    """
    params = inspect.signature(SetKernelStringOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetKernelStringOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def KernelStringOption(option:str):
    """
    获取内核str选项值
    
    参数列表：
        `option` : 选项名称
    函数返回值：
        `str` : 获取选项值

    示例：
        >>> MwAppOptions.KernelStringOption("")
        ""

    注意事项：
        内核暂时未提供str选项，失败返回""
    """
    params = inspect.signature(KernelStringOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(KernelStringOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetBoolean(option:str, value:bool) -> bool:
    """
    设置bool选项值
    
    参数列表：
        `option` : 选项名称
        `value` : 值
    函数返回值：
        `bool` : 表示是否设置成功

    示例：
        >>> MwAppOptions.SetBoolean("LogFile", True)
        True

    注意事项：
        只能设置bool选项
    """
    params = inspect.signature(SetBoolean).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetBoolean, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def Boolean(option:str):
    """
    获取浮点数选项值
    
    参数列表：
        `option` : 选项名称
    函数返回值：
        `bool` : 获取选项值

    示例：
        >>> MwAppOptions.Boolean("LogFile")
        True

    注意事项：
        只能获取bool选项, 失败返回False
    """
    params = inspect.signature(Boolean).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Boolean, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetString(option:str, value:str) -> bool:
    """
    设置str选项值
    
    参数列表：
        `option` : 选项名称
        `value` : 值
    函数返回值：
        `bool` : 表示是否设置成功

    示例：
        >>> MwAppOptions.SetString("MWorks.Environment.Path.MWORKSCachePath", r"C:\ProgramData\MWORKS_Sysplorer_Cache")
        True

    注意事项：
        只能设置str选项
    """
    params = inspect.signature(SetString).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetString, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def String(option:str):
    """
    获取str选项值
    
    参数列表：
        `option` : 选项名称
    函数返回值：
        `str` : 获取选项值

    示例：
        >>> MwAppOptions.String("MWorks.Environment.Path.MWORKSCachePath")
        C:\ProgramData\MWORKS_Sysplorer_Cache

    注意事项：
        只能获取str选项, 失败返回""
    """
    params = inspect.signature(String).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(String, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetReal(option:str, value:float) -> bool:
    """
    设置浮点选项值
    
    参数列表：
        `option` : 选项名称
        `value` : 值
    函数返回值：
        `bool` : 表示是否设置成功

    示例：
        >>> MwAppOptions.SetReal("MWorks.Analyzer.InlineStepSize", 3.0)
        True

    注意事项：
        只能设置浮点选项
    """
    params = inspect.signature(SetReal).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetReal, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def Real(option:str):
    """
    获取浮点选项值
    
    参数列表：
        `option` : 选项名称
    函数返回值：
        `str` : 获取选项值

    示例：
        >>> MwAppOptions.Real("MWorks.Analyzer.InlineStepSize")
        3.0

    注意事项：
        只能获取浮点选项, 失败返回0.0
    """
    params = inspect.signature(Real).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Real, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetInt(option:str, value:int) -> bool:
    """
    设置Integer选项值
    
    参数列表：
        `option` : 选项名称
        `value` : 值
    函数返回值：
        `bool` : 表示是否设置成功

    示例：
        >>> MwAppOptions.SetInt("MWorks.General.MaxOutputEventNumber", 3)
        True

    注意事项：
        只能设置Integer选项
    """
    params = inspect.signature(SetInt).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetInt, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def Int(option:str):
    """
    获取浮点选项值
    
    参数列表：
        `option` : 选项名称
    函数返回值：
        `str` : 获取选项值

    示例：
        >>> MwAppOptions.Int("MWorks.General.MaxOutputEventNumber")
        3

    注意事项：
        只能获取浮点选项, 失败返回0
    """
    params = inspect.signature(Int).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Int, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
Author: [Wang Run]
Date: [2024/09/28]
Description:
    This module is designed to provide some interfaces for Sysplorer MwAppOption Setting. 
"""