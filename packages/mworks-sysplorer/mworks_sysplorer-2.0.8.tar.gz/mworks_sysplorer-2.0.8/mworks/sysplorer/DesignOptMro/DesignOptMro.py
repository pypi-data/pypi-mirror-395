import inspect
import time
import os
from colorama import init, Fore
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
import re
import multiprocessing
init(autoreset = True)

_num_cores = multiprocessing.cpu_count()

_name = "DesignOptMro"
_MwConnect = MwConnect()

@mw_connect_decorator(_MwConnect._process_path)
def Simulate(param:list)->list:
    params = inspect.signature(Simulate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Simulate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def CalculateResidual()->list:
    params = inspect.signature(CalculateResidual).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CalculateResidual, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def Output()->bool:
    params = inspect.signature(Output).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Output, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)
    
 
@mw_connect_decorator(_MwConnect._process_path)
def GetOptimizeStatus():
    params = inspect.signature(GetOptimizeStatus).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetOptimizeStatus, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 状态
"""
brief: 初始化响应优化
return: bool, 初始化成功与否
modelName: 模型名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def InitialApp(modelName: str, instPath:str = "")->bool:
    params = inspect.signature(InitialApp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(InitialApp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 关闭响应优化
return: bool, 关闭成功与否
modelName: 模型名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def CloseApp()->bool:
    params = inspect.signature(CloseApp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CloseApp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 会话
"""
brief: 打开会话
return: bool, 成功与否
path: 会话路径
"""
@mw_connect_decorator(_MwConnect._process_path)
def OpenSession(path: str)->bool:
    params = inspect.signature(OpenSession).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(OpenSession, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 保存会话
return: bool, 保存会话是否成功
path: 会话路径，可以指定会话名称，如"C:/Users"
"""
@mw_connect_decorator(_MwConnect._process_path)
def SaveSession(path: str)->str:
    params = inspect.signature(SaveSession).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SaveSession, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 调节参数
"""
brief: 获取全部调节参数
return: dict，{name: {value: , unit: , min: , max: , description: }}
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetTunerParam()->dict:
    params = inspect.signature(GetTunerParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetTunerParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 选择调节参数
return: bool
array: tuple, 存放选择的调节参数的名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SelectTunerParam(array: tuple)->bool:
    params = inspect.signature(SelectTunerParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectTunerParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取已选择的调节参数名称
return: dict,key:参数名称，value:dict。例子：{"length": {"min":0, "max":2, "value":1, "description":"矩形长度"}}
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetSelectedTunerParam()->dict:
    params = inspect.signature(GetSelectedTunerParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetSelectedTunerParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置调节参数
return: bool
paramName: 待配置的调节参数名称
minVal: 最小值
maxVal: 最大值
initialVal: 初始值
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigTunerParam(paramName: str, minVal = -1e100, maxVal = 1e100, initialVal = 0.0)->bool:
    if type(minVal) == int or type(minVal) == float:
        minVal = float(minVal)
    else:
        return False
    if type(maxVal) == int or type(maxVal) == float:
        maxVal = float(maxVal)
    else:
        return False
    if type(initialVal) == int or type(initialVal) == float:
        initialVal = float(initialVal)
    else:
        return False
    params = inspect.signature(ConfigTunerParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('minVal')] = type(minVal)
    expected_types[list(params.keys()).index('maxVal')] = type(maxVal)
    expected_types[list(params.keys()).index('initialVal')] = type(initialVal)
    return _MwConnect.__RunCurrentFunction__(ConfigTunerParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)   

"""
brief: 删除调节参数
return: bool
paramName: 待删除的调节参数名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def DeleteTunerParam(paramName:str)->bool:
    params = inspect.signature(DeleteTunerParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(DeleteTunerParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 清空调节参数
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def ClearTunerParam()->bool:
    params = inspect.signature(ClearTunerParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ClearTunerParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 需求
"""
brief: 获取支持的需求类型
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetRequirement()->list:
    params = inspect.signature(GetRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 选择需求
return: bool
array: tuple, 包括选择的需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SelectRequirement(array: tuple)->bool:
    params = inspect.signature(SelectRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 新建变量属性需求
return: bool
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewVariablePropertyRequirement(reqName: str)->bool:
    params = inspect.signature(NewVariablePropertyRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewVariablePropertyRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 新建阶跃响应需求
return: bool
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewStepResponseRequirement(reqName: str)->bool:
    params = inspect.signature(NewStepResponseRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewStepResponseRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 新建变量边界需求
return: bool
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewVariableLinearBoundRequirement(reqName: str)->bool:
    params = inspect.signature(NewVariableLinearBoundRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewVariableLinearBoundRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 新建变量追踪需求
return: bool
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewVariableTrackingRequirement(reqName: str)->bool:
    params = inspect.signature(NewVariableTrackingRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewVariableTrackingRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取需求的配置数据
return: dict
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetRequirementData(reqName: str)->dict:
    params = inspect.signature(GetRequirementData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetRequirementData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取已经创建的需求名称
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetCreatedRequirement()->list:
    params = inspect.signature(GetCreatedRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetCreatedRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置变量属性需求
return: bool
reqName: 需求名称
varProperty: 变量属性, 支持设置11种属性设置
varType: 约束类型, 用于约束变量的属性
value: 约束类型的边界数值
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigVariablePropertyRequirement(reqName: str, varProperty: str = "Final Value", varType: str = "Minimization", value = 0.0)->bool:
    if type(value) == int or type(value) == float:
        value = float(value)
    else:
        return False
    params = inspect.signature(ConfigVariablePropertyRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('value')] = type(value)
    return _MwConnect.__RunCurrentFunction__(ConfigVariablePropertyRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置阶跃响应需求
return: bool
reqName: 需求名称
initialValue: 初始值
finalValue: 终值
stepResponseTime: 阶跃响应时间
riseTime: 上升时间
rise: 上升百分比
settlingTime: 稳定时间
settling: 稳定百分比
overshoot: 超调百分比
undershoot: 下冲百分比
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigStepResponseRequirement(reqName: str, initialValue = 0, finalValue = 1, stepResponseTime = 0, riseTime = 5, rise = 80, 
        settlingTime = 7, settling = 1, overshoot = 10, undershoot = 1)->bool:
    if type(initialValue) == int or type(initialValue) == float:
        initialValue = float(initialValue)
    else:
        return False
    if type(finalValue) == int or type(finalValue) == float:
        finalValue = float(finalValue)
    else:
        return False
    if type(stepResponseTime) == int or type(stepResponseTime) == float:
        stepResponseTime = float(stepResponseTime)
    else:
        return False
    if type(riseTime) == int or type(riseTime) == float:
        riseTime = float(riseTime)
    else:
        return False
    if type(rise) == int or type(rise) == float:
        rise = float(rise)
    else:
        return False
    if type(settlingTime) == int or type(settlingTime) == float:
        settlingTime = float(settlingTime)
    else:
        return False
    if type(settling) == int or type(settling) == float:
        settling = float(settling)
    else:
        return False
    if type(overshoot) == int or type(overshoot) == float:
        overshoot = float(overshoot)
    else:
        return False
    if type(undershoot) == int or type(undershoot) == float:
        undershoot = float(undershoot)
    else:
        return False
    params = inspect.signature(ConfigStepResponseRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('initialValue')] = type(initialValue)
    expected_types[list(params.keys()).index('finalValue')] = type(finalValue)
    expected_types[list(params.keys()).index('stepResponseTime')] = type(stepResponseTime)
    expected_types[list(params.keys()).index('riseTime')] = type(riseTime)
    expected_types[list(params.keys()).index('rise')] = type(rise)
    expected_types[list(params.keys()).index('settlingTime')] = type(settlingTime)
    expected_types[list(params.keys()).index('settling')] = type(settling)
    expected_types[list(params.keys()).index('overshoot')] = type(overshoot)
    expected_types[list(params.keys()).index('undershoot')] = type(undershoot)
    return _MwConnect.__RunCurrentFunction__(ConfigStepResponseRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置变量线性边界需求
return: bool
reqName: 需求名称
boundType: 边界类型, >= 或者 <=
array: 边界数值，包括时间和幅值，依次输入（开始时间, 开始幅值, 结束时间， 结束幅值）
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigVariableLinearBoundRequirement(reqName: str, boundType:str = "<=", array: tuple = (0,1,1,1))->bool:
    params = inspect.signature(ConfigVariableLinearBoundRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ConfigVariableLinearBoundRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置变量追踪需求
return: bool
reqName: 需求名称
time: 时间序列
value: 数值序列
method: 追踪方法，等同于残差计算方法
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigVariableTrackingRequirement(reqName: str, time: tuple = (0,0.1,0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), 
value:tuple = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), method:str = "Mean Absolute Percentage Error")->bool:
    params = inspect.signature(ConfigVariableTrackingRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ConfigVariableTrackingRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 为需求配置变量集
return: bool
reqName: 需求名称
array: 变量集元组
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetRequirementVariableSet(reqName:str, array: tuple)->bool:
    params = inspect.signature(SetRequirementVariableSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetRequirementVariableSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取需求内的变量集
return: list
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetVariableSetInRequirement(reqName: str)->list:
    params = inspect.signature(GetVariableSetInRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetVariableSetInRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 删除需求
return: bool
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def DeleteRequirement(reqName:str)->bool:
    params = inspect.signature(DeleteRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(DeleteRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 清空需求
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def ClearRequirement()->bool:
    params = inspect.signature(ClearRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ClearRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 变量集
"""
brief: 删除变量集
return: bool
setName:待删除的变量集名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def DeleteVariableSet(setName: str)->bool:
    params = inspect.signature(DeleteVariableSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(DeleteVariableSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 清空变量集
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def ClearVariableSet()->bool:
    params = inspect.signature(ClearVariableSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ClearVariableSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取变量
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetVariable()->list:
    params = inspect.signature(GetVariable).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetVariable, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 新建变量集
return: bool
setName:待新建的变量集名称
array：变量集合
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewVariableSet(setName: str, array:tuple)->bool:
    params = inspect.signature(NewVariableSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewVariableSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取变量集内的变量
return: list
setName:变量集名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetVariableInSet(setName: str)->list:
    params = inspect.signature(GetVariableInSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetVariableInSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取变量集
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetVariableSet()->list:
    params = inspect.signature(GetVariableSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetVariableSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 固定参数
"""
brief: 选择固定参数
return: bool
array：固定参数集合
"""
@mw_connect_decorator(_MwConnect._process_path)
def SelectFixParam(array: tuple)->bool:
    params = inspect.signature(SelectFixParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectFixParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取固定参数
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetFixParam()->list:
    params = inspect.signature(GetFixParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetFixParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)  

"""
brief: 获取已经选择的固定参数
return: dict,{固定参数名称:固定参数数值}
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetSelectedFixParam()->dict:
    params = inspect.signature(GetSelectedFixParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetSelectedFixParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置固定参数
return: bool
paramName:固定参数名称
initialVal:固定参数初始值
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigFixParam(paramName: str, initialVal = 0.0)->bool:
    if type(initialVal) == int or type(initialVal) == float:
        initialVal = float(initialVal)
    else:
        return False
    params = inspect.signature(ConfigFixParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('initialVal')] = type(initialVal)
    return _MwConnect.__RunCurrentFunction__(ConfigFixParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 删除固定参数
return: bool
paramName:固定参数名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def DeleteFixParam(paramName:str)->bool:
    params = inspect.signature(DeleteFixParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(DeleteFixParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 清空固定参数
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def ClearFixParam()->bool:
    params = inspect.signature(ClearFixParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ClearFixParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 算法
"""
brief: 获取优化算法名称
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetAlgorithm()->list:
    params = inspect.signature(GetAlgorithm).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetAlgorithm, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 选择优化算法
return: bool
name: 优化算法名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SelectAlgorithm(name: str)->bool:
    params = inspect.signature(SelectAlgorithm).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectAlgorithm, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取当前的优化算法名称
return: str
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetCurrentAlgorithm()->str:
    params = inspect.signature(GetCurrentAlgorithm).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetCurrentAlgorithm, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置PSO算法
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigPSOAlgorithm(relativeTolerance = 0.001, convergenceTime:int = 3, maxIterStep:int = 100, populationSize:int = 20, 
                       parameterAdaptive: bool = False, w = 0.6, c1 = 1.5, c2 = 2)->bool:
    if type(relativeTolerance) == int or type(relativeTolerance) == float:
        relativeTolerance = float(relativeTolerance)
    else:
        return False
    if type(w) == int or type(w) == float:
        w = float(w)
    else:
        return False
    if type(c1) == int or type(c1) == float:
        c1 = float(c1)
    else:
        return False
    if type(c2) == int or type(c2) == float:
        c2 = float(c2)
    else:
        return False
    params = inspect.signature(ConfigPSOAlgorithm).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('relativeTolerance')] = type(relativeTolerance)
    expected_types[list(params.keys()).index('w')] = type(w)
    expected_types[list(params.keys()).index('c1')] = type(c1)
    expected_types[list(params.keys()).index('c2')] = type(c2)
    return _MwConnect.__RunCurrentFunction__(ConfigPSOAlgorithm, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置GA算法
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigGAAlgorithm(relativeTolerance = 0.001, convergenceTime:int = 5, maxIterStep:int = 100, crossoverRate = 0.8, mutationRate = 0.25, populationSize:int = 30)->bool:
    if type(relativeTolerance) == int or type(relativeTolerance) == float:
        relativeTolerance = float(relativeTolerance)
    else:
        return False
    if type(crossoverRate) == int or type(crossoverRate) == float: 
        crossoverRate = float(crossoverRate)
    else:
        return False
    if type(mutationRate) == int or type(mutationRate) == float:
        mutationRate = float(mutationRate)
    else:
        return False
    params = inspect.signature(ConfigGAAlgorithm).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('relativeTolerance')] = type(relativeTolerance)
    expected_types[list(params.keys()).index('crossoverRate')] = type(crossoverRate)
    expected_types[list(params.keys()).index('mutationRate')] = type(mutationRate)
    return _MwConnect.__RunCurrentFunction__(ConfigGAAlgorithm, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 选项
"""
brief: 设置仿真选项
return: bool
startTime: 仿真开始时间
endTime: 仿真结束时间
stepNumber: 仿真步数
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetSimulationOption(startTime = 0, endTime = 1, stepNumber:int = 500)->bool:
    if type(startTime) == int or type(startTime) == float:
        startTime = float(startTime)
    else:
        return False
    if type(endTime) == int or type(endTime) == float:
        endTime = float(endTime)
    else:
        return False
    params = inspect.signature(SetSimulationOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('startTime')] = type(startTime)
    expected_types[list(params.keys()).index('endTime')] = type(endTime)
    return _MwConnect.__RunCurrentFunction__(SetSimulationOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 设置优化选项
return: bool
continueOptimize: 仿真失败后继续优化
parallelNum: 并行数目
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetOptimizeOption(continueOptimize: bool = True, parallelNum:int = int(_num_cores / 2))->bool:
    params = inspect.signature(SetOptimizeOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetOptimizeOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 优化
"""
brief: 开始优化
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def Optimize()->bool:
    params = inspect.signature(Optimize).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Optimize, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def EvaluateCurrentParameter()->bool:
    params = inspect.signature(EvaluateCurrentParameter).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(EvaluateCurrentParameter, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 开始评估当前参数，阻塞接口
return: bool
"""
def StartEvaluate()->bool:
    res = EvaluateCurrentParameter()
    if res is False:
        return False
    res = __WaitOptFinish()
    return res

def __WaitOptFinish():
    while True:
        res = GetOptimizeStatus()
        print("status:", res)
        if res == -1:
            time.sleep(3)
            continue
        elif res == 0:
            return True
        else:
            return False

"""
brief: 开始优化，阻塞接口
return: bool
"""
def StartOptimize()->bool:
    res = Optimize()
    print("optimize:", res)
    if res is False:
        return False
    res = __WaitOptFinish()
    return res

# 结果
"""
brief: 获取评估当前参数的优化结果数据
return: dict， {变量名称：[变量数值]}
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetEvaluateResultData(reqName: str)->dict:
    params = inspect.signature(GetEvaluateResultData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEvaluateResultData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取需求内， 变量的时间序列结果数据
return: dict,{变量名称：[变量数值]}
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetOptimizeReqTimeData(reqName: str)->dict:
    params = inspect.signature(GetOptimizeReqTimeData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetOptimizeReqTimeData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取全部数据，包括每一步的需求时序数据、需求迭代数据、参数迭代数据
return: dict， 参数迭代数据dict["params"], {迭代次数：{参数名称：参数数值}}。 变量属性需求迭代数据：dict["reqs],{需求名称：{迭代次数：{变量名称：变量数值}}}。其他需求数据{需求名称：{迭代次数：{变量名称：[[时序数据][迭代数据]]}}}
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetOptimizeData()->dict:
    params = inspect.signature(GetOptimizeData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetOptimizeData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取需求内， 变量的迭代序列结果数据
return: dict， {迭代次数：{变量名称：变量数值}}
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetOptimizeReqIterData(reqName: str)->dict:
    params = inspect.signature(GetOptimizeReqIterData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetOptimizeReqIterData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取所有的优化结果名称
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetOptimizeResult()->list:
    params = inspect.signature(GetOptimizeResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetOptimizeResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取参数的迭代数据
return: dict, {迭代次数：参数数值}
paramName: 参数名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetOptimizeParamIterData(paramName:str)->dict:
    params = inspect.signature(GetOptimizeParamIterData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetOptimizeParamIterData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取参数的最终优化数据
return: dict, {参数名称：参数数值}
resultName: 优化结果名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetOptimizeParamData(resultName:str)->dict:
    params = inspect.signature(GetOptimizeParamData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetOptimizeParamData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 删除优化结果
return: bool
resultName: 优化结果名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def DeleteOptimizeResult(resultName: str)->bool:
    params = inspect.signature(DeleteOptimizeResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(DeleteOptimizeResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 清空优化结果
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)  
def ClearOptimizeResult()->bool:
    params = inspect.signature(ClearOptimizeResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ClearOptimizeResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 以Json文件路径的方式进行响应优化
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)  
def StartResponseOptimizer(jsonPath:str)->bool:
    params = inspect.signature(StartResponseOptimizer).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(StartResponseOptimizer, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)
#-----------------------------------------------------------------------------------------------

def __CheckString(name):
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
        return True
    else:
        return False
__all__ = [name for name in globals() if not name.startswith('_')]