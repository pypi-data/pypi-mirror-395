import inspect
import time
import os
from colorama import init, Fore
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
import re
import multiprocessing
init(autoreset = True)

_num_cores = multiprocessing.cpu_count()
_name = "DesignOptPsa"
_MwConnect = MwConnect()
    
@mw_connect_decorator(_MwConnect._process_path)
def GetEvaluateStatus()->int:
    params = inspect.signature(GetEvaluateStatus).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEvaluateStatus, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# APP状态
"""
brief: 初始化敏感度分析
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
brief: 关闭敏感度分析
return: bool, 是否关闭
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
return: bool, 打开会话是否成功
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
return: str, 会话路径
path: 会话路径，也可以指定会话名称，如"C:/Users/xxxx.xml"
"""
@mw_connect_decorator(_MwConnect._process_path)
def SaveSession(path: str)->str:
    params = inspect.signature(SaveSession).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SaveSession, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 参数
"""
brief: 获取全部调节参数
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetTunerParam()->list:
    params = inspect.signature(GetTunerParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetTunerParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 参数集
"""
brief: 新建参数集并选择参数
return: bool
name: 参数集名称
param: tuple, 将选择的参数放入该元组内
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewParameterSetAttachParam(name: str, param: tuple)->bool:
    params = inspect.signature(NewParameterSetAttachParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewParameterSetAttachParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置参数集
return: bool
setName: 参数集名称
param: dict, key:参数名称, value:参数初值 
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigParameterSet(setName: str, param: dict)->bool:
    params = inspect.signature(ConfigParameterSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ConfigParameterSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 设置为当前参数集
return: bool
setName: 参数集名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetCurrentParameterSet(setName: str)->bool:
    params = inspect.signature(SetCurrentParameterSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetCurrentParameterSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取当前参数集
return: str, 当前参数集名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetCurrentParameterSet()->str:
    params = inspect.signature(GetCurrentParameterSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetCurrentParameterSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 删除参数集
return: bool
setName: 待删除的参数集名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def DeleteParameterSet(setName:str)->bool:
    params = inspect.signature(DeleteParameterSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(DeleteParameterSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 清空参数集
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def ClearParameterSet()->bool:
    params = inspect.signature(ClearParameterSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ClearParameterSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 新建参数集
return: bool
setName: 待创建的参数集名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewParameterSet(setName:str)->bool:
    params = inspect.signature(NewParameterSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewParameterSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取全部参数集
return: list, 全部参数集名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetParameterSet()->list:
    params = inspect.signature(GetParameterSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetParameterSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 采样
"""
brief: 设置采样选项
return: bool
number: 采样个数
method: 采样算法
overWrite: True:使用生成的参数值覆盖原有参数集, False:在原有参数集上追加生成的参数集
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetSampleOption(number: int = 10, method: str = "Random", overWrite: bool = True)->bool:
    params = inspect.signature(SetSampleOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetSampleOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 设置参数的采样分布
return: bool
paramName: 参数名称
distribute: 采样分布名称
array: 对应的采样分布参数, 如均匀分布的lower和upper数值
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetParamSampleDistribution(paramName:str, distribute: str, array: tuple)->bool:
    params = inspect.signature(SetParamSampleDistribution).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetParamSampleDistribution, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取全部支持的采样分布方式
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetDistributionType()->list:
    params = inspect.signature(GetDistributionType).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetDistributionType, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 开始采样
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def StartSampling()->bool:
    params = inspect.signature(StartSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(StartSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取采样结果数据
return: dict, key: 参数名称, value: 采样数据列表
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetSamplingResultData()->dict:
    params = inspect.signature(GetSamplingResultData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetSamplingResultData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

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
    for item in array:
        if isinstance(item, str) is False:
            return False
    params = inspect.signature(SelectRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 删除需求
return: bool
reqName: 待删除的需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def DeleteRequirement(reqName: str)->bool:
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

"""
brief: 新建变量匹配需求
return: bool
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewVariableMatchingRequirement(reqName: str)->bool:
    params = inspect.signature(NewVariableMatchingRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewVariableMatchingRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

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
def NewLinearBoundRequirement(reqName: str)->bool:
    params = inspect.signature(NewLinearBoundRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewLinearBoundRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

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
brief: 配置变量匹配需求
return: bool
reqName: 需求名称
path: 实验文件路径
variable: ditc, key:仿真变量名称, value: 测量变量名称
fix: 固定参数, key: 固定参数名称, value: 固定参数数值
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigVariableMatchingRequirement(reqName: str, path: str, variable:dict, fix:dict = {})->bool:
    params = inspect.signature(ConfigVariableMatchingRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ConfigVariableMatchingRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

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
def ConfigVariableTrackingRequirement(reqName: str, time: tuple = (0,0.1,0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)
, value:tuple = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), method:str = "Mean Absolute Percentage Error")->bool:
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
return: list，变量集名称
reqName: 需求名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetVariableSetInRequirement(reqName: str)->list:
    params = inspect.signature(GetVariableSetInRequirement).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetVariableSetInRequirement, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)


# 变量集、变量
"""
brief: 新建变量集
return: bool
setName: 变量集名称
array: 变量元组
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewVariableSet(setName:str, array:tuple)->bool:
    params = inspect.signature(NewVariableSet).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewVariableSet, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取模型内的变量
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetVariable()->list:
    params = inspect.signature(GetVariable).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetVariable, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 仿真和需求评估选项
"""
brief: 设置仿真选项
return: bool
startTime: 仿真开始时间
endTime: 仿真结束时间
stepNumber: 仿真步数
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetSimulateOption(startTime = 0, endTime = 1, stepNumber:int = 500)->bool:
    if type(startTime) == int or type(startTime) == float:
        startTime = float(startTime)
    else:
        return False
    if type(endTime) == int or type(endTime) == float:
        endTime = float(endTime)
    else:
        return False
    params = inspect.signature(SetSimulateOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('startTime')] = type(startTime)
    expected_types[list(params.keys()).index('endTime')] = type(endTime)
    return _MwConnect.__RunCurrentFunction__(SetSimulateOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 设置需求评估选项
return: bool
continueEvaluate: 仿真失败后继续计算
saveEvaluate: 保存设置, True: 新建计算结果, False: 覆盖现有计算结果
parallelNum: 并行数目
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetEvaluateOption(continueEvaluate: bool = True, saveEvaluate: bool = True, parallelNum:int = int(_num_cores / 2))->bool:
    # print("计算机核数为" + str(_num_cores))
    params = inspect.signature(SetEvaluateOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetEvaluateOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 计算
@mw_connect_decorator(_MwConnect._process_path)
def Evaluate()->bool:
    params = inspect.signature(Evaluate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Evaluate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

def __WaitOptFinish():
    while True:
        res = GetEvaluateStatus()
        if res == -1:
            time.sleep(3)
            continue
        elif res == 0:
            return True
        else:
            return False
        
"""
brief: 设开始计算需求评估
return: bool
"""
def StartEvaluate()->bool:
    Evaluate()
    res = __WaitOptFinish()
    return res

"""
brief: 开始量化分析
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def StartQuantifiedAnalysis()->bool:
    params = inspect.signature(StartQuantifiedAnalysis).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(StartQuantifiedAnalysis, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 需求评估结果、量化分析
"""
brief: 选择评估结果
return: bool
resultName: 需求评估结果名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SelectEvaluateResult(resultName:str)->bool:
    params = inspect.signature(SelectEvaluateResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectEvaluateResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 设置相关分析方法
return: bool
correlation:bool, 相关
standardizedRegression:bool, 标准化回归
partialCorrelation:bool, 偏相关
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetQuantifiedMethod(correlation:bool = False, standardizedRegression:bool = False, partialCorrelation:bool = False)->bool:
    params = inspect.signature(SetQuantifiedMethod).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetQuantifiedMethod, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 设置相关分析类型
return: bool
linear:bool, 线性 
ranked:bool, 排序 
kendall:bool, 肯德尔
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetQuantifiedType(linear:bool = False, ranked:bool = False, kendall:bool = False)->bool:
    params = inspect.signature(SetQuantifiedType).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetQuantifiedType, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取评估结果名称
return: list, 需求偏差名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetEvaluateResult()->list:
    params = inspect.signature(GetEvaluateResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEvaluateResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取评估结果数据
return: dict, 字典包由“需求名称：需求偏差列表”组成， key:str, value:list
resultName: 评估结果的名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetEvaluateResultData(resultName: str)->dict:
    params = inspect.signature(GetEvaluateResultData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEvaluateResultData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取量化分析结果名称
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetQuantifiedResult()->list:
    params = inspect.signature(GetQuantifiedResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetQuantifiedResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取量化分析结果数据
return: list,[[量化分析方法-类型， 需求名称，{参数名称：量化分析数值}]] 
resultName: 量化分析结果的名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetQuantifiedResultData(resultName: str)->list:
    params = inspect.signature(GetQuantifiedResultData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetQuantifiedResultData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取量化分析的方法和类型
return: dict, 参考{'Method': ['Correlation', 'Partial Correlation', 'Standardized Regression'], 'Type': ['Kendall', 'Linear', 'Ranked']}
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetQuantifiedMethodAndType()->dict:
    params = inspect.signature(GetQuantifiedMethodAndType).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetQuantifiedMethodAndType, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 正态分布采样
return: list, 采样结果
number:采样个数
mean:均值
sigma:标准差
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def NormalSampling(number:int = 10, mean = 1, sigma = 0.57735, min = -1e100, max = 1e100)->list:
    if type(mean) == int or type(mean) == float:
        mean = float(mean)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(NormalSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('mean')] = type(mean)
    expected_types[list(params.keys()).index('sigma')] = type(sigma)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(NormalSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 均匀分布采样
return: list, 采样结果
number:采样个数
lower:下限
upper:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def UniformSampling(number:int = 10, lower = -0.05, upper = 0.05)->list:
    if type(lower) == int or type(lower) == float:
        lower = float(lower)
    else:
        return False
    if type(upper) == int or type(upper) == float:
        upper = float(upper)
    else:
        return False
    params = inspect.signature(UniformSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('lower')] = type(lower)
    expected_types[list(params.keys()).index('upper')] = type(upper)
    return _MwConnect.__RunCurrentFunction__(UniformSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 贝塔分布采样
return: list, 采样结果
number:采样个数
a:形状参数
b:形状参数
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def BetaSampling(number:int = 10, a = 1, b = 1, min = -1e100, max = 1e100)->list:
    if type(a) == int or type(a) == float:
        a = float(a)
    else:
        return False
    if type(b) == int or type(b) == float:
        b = float(b)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(BetaSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('a')] = type(a)
    expected_types[list(params.keys()).index('b')] = type(b)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(BetaSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 为参数设置采样数据
return: bool
paramName:参数名称
samplingData:list,采样数据列表
tips:若调用的SetSampleOption()设置了采样数目，则samplingData的数量应与设置的采样数目保持一致；若没有调用SetSampleOption()，则应保持为每个参数设置的采样数据的个数相等
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetParamSamplingData(paramName:str, samplingData:list):
    params = inspect.signature(SetParamSamplingData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetParamSamplingData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 伯恩鲍姆-桑德斯分布采样
return: list, 采样结果
number:采样个数
beta:尺度参数
gamma:形状参数
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def BinbaumSaundersSampling(number:int = 10, beta = 0.666667, gamma = 1, min = -1e100, max = 1e100)->list:
    if type(beta) == int or type(beta) == float:
        beta = float(beta)
    else:
        return False
    if type(gamma) == int or type(gamma) == float:
        gamma = float(gamma)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(BinbaumSaundersSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('beta')] = type(beta)
    expected_types[list(params.keys()).index('gamma')] = type(gamma)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(BinbaumSaundersSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 伯尔XII分布采样
return: list, 采样结果
number:采样个数
alpha:尺度参数
c:形状参数
k:形状参数
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def BurrSampling(number:int = 10, alpha = 1, c = 1, k = 1, min = -1e100, max = 1e100)->list:
    if type(alpha) == int or type(alpha) == float:
        alpha = float(alpha)
    else:
        return False
    if type(c) == int or type(c) == float:
        c = float(c)
    else:
        return False
    if type(k) == int or type(k) == float:
        k = float(k)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(BurrSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('alpha')] = type(alpha)
    expected_types[list(params.keys()).index('c')] = type(c)
    expected_types[list(params.keys()).index('k')] = type(k)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(BurrSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 指数分布采样
return: list, 采样结果
number:采样个数
lambdaa:速率参数，表示事情发生的频率或强度
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def ExponentialSampling(number:int = 10, lambdaa = 1, min = -1e100, max = 1e100)->list:
    if type(lambdaa) == int or type(lambdaa) == float:
        lambdaa = float(lambdaa)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(ExponentialSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('lambdaa')] = type(lambdaa)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(ExponentialSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 极值分布采样
return: list, 采样结果
number:采样个数
mu:位置参数
sigma:尺度参数
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def ExtremeValueSampling(number:int = 10, mu = 0, sigma = 1, min = -1e100, max = 1e100)->list:
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(ExtremeValueSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('mu')] = type(mu)
    expected_types[list(params.keys()).index('sigma')] = type(sigma)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(ExtremeValueSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 伽马分布采样
return: list, 采样结果
number:采样个数
a:形状参数， a > 0
b:尺度参数, b > 0
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def GammaSampling(number:int = 10, a = 1, b = 1, min = -1e100, max = 1e100)->list:
    if type(a) == int or type(a) == float:
        a = float(a)
    else:
        return False
    if type(b) == int or type(b) == float:
        b = float(b)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(GammaSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('a')] = type(a)
    expected_types[list(params.keys()).index('b')] = type(b)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GammaSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 广义极值分布采样
return: list, 采样结果
number:采样个数
k:形状参数
sigma:尺度参数, sigma > 0
mu:位置参数
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def GeneralizedExtremeSampling(number:int = 10, k = 0, sigma = 1, mu = 0, min = -1e100, max = 1e100)->list:
    if type(k) == int or type(k) == float:
        k = float(k)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(GeneralizedExtremeSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('k')] = type(k)
    expected_types[list(params.keys()).index('sigma')] = type(sigma)
    expected_types[list(params.keys()).index('mu')] = type(mu)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GeneralizedExtremeSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 广义帕累托分布采样
return: list, 采样结果
number:采样个数
k:形状参数
sigma:尺度参数, sigma > 0
theta:阈值参数
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def GeneralizedParetoSampling(number:int = 10, k = 0, sigma = 1,theta = 0, min = -1e100, max = 1e100)->list:
    if type(k) == int or type(k) == float:
        k = float(k)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(theta) == int or type(theta) == float:
        theta = float(theta)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(GeneralizedParetoSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('k')] = type(k)
    expected_types[list(params.keys()).index('sigma')] = type(sigma)
    expected_types[list(params.keys()).index('theta')] = type(theta)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GeneralizedParetoSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 逆高斯分布采样
return: list, 采样结果
number:采样个数
mu:尺度参数，mu > 0
lambdaa:形状参数, lambdaa > 0
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def InverseGaussianSampling(number:int = 10, mu = 1, lambdaa = 1, min = -1e100, max = 1e100)->list:
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(lambdaa) == int or type(lambdaa) == float:
        lambdaa = float(lambdaa)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(InverseGaussianSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('mu')] = type(mu)
    expected_types[list(params.keys()).index('lambdaa')] = type(lambdaa)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(InverseGaussianSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 逻辑分布采样
return: list, 采样结果
number:采样个数
mu:均值
sigma:尺度参数, sigma >= 0
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def LogisticSampling(number:int = 10, mu = 0, sigma = 1, min = -1e100, max = 1e100)->list:
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(LogisticSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('mu')] = type(mu)
    expected_types[list(params.keys()).index('sigma')] = type(sigma)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(LogisticSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 对数逻辑分布采样
return: list, 采样结果
number:采样个数
mu:对数值的均值, mu >= 0
sigma:尺度参数, sigma > 0
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def LoglogisticSampling(number:int = 10, mu = 0, sigma = 1, min = -1e100, max = 1e100)->list:
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(LoglogisticSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('mu')] = type(mu)
    expected_types[list(params.keys()).index('sigma')] = type(sigma)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(LoglogisticSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 逻辑对数分布采样
return: list, 采样结果
number:采样个数
mu:均值
sigma:尺度参数, sigma > 0
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def LogNormalSampling(number:int = 10, mu = 0, sigma = 1, min = -1e100, max = 1e100)->list:
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(LogNormalSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('mu')] = type(mu)
    expected_types[list(params.keys()).index('sigma')] = type(sigma)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(LogNormalSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 多项分布采样
return: list, 采样结果
number:采样个数
probabilitie:概率参数，和为1
position:位置参数
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def MultionmialSampling(number:int = 10, probabilitie:list = [0.5, 0.5], position:list = [0, 1], min = -1e100, max = 1e100)->list:
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(MultionmialSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(MultionmialSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 泊松分布采样
return: list, 采样结果
number:采样个数
lambdaa:均值,>0
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def PoissonSampling(number:int = 10, lambdaa = 1, min = -1e100, max = 1e100)->list:
    if type(lambdaa) == int or type(lambdaa) == float:
        lambdaa = float(lambdaa)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(PoissonSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('lambdaa')] = type(lambdaa)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(PoissonSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 瑞利分布采样
return: list, 采样结果
number:采样个数
B:定义参数，B > 0
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def RayleihSampling(number:int = 10, B = 1, min = -1e100, max = 1e100)->list:
    if type(B) == int or type(B) == float:
        B = float(B)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(RayleihSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('B')] = type(B)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(RayleihSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 威布尔分布采样
return: list, 采样结果
number:采样个数
A:尺度参数，A > 0
B:形状参数，B > 0
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def WeibullSampling(number:int = 10, A = 1, B = 1, min = -1e100, max = 1e100)->list:
    if type(A) == int or type(A) == float:
        A = float(A)
    else:
        return False
    if type(B) == int or type(B) == float:
        B = float(B)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(WeibullSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('A')] = type(A)
    expected_types[list(params.keys()).index('B')] = type(B)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(WeibullSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 几何分布采样
return: list, 采样结果
number:采样个数
P:成功概率，[0, 1]
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def GeometricSampling(number:int = 10, P = 0.5, min = -1e100, max = 1e100)->list:
    if type(P) == int or type(P) == float:
        P = float(P)
    else:
        return False
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(GeometricSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('P')] = type(P)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GeometricSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 混合高斯分布采样
return: list, 采样结果
number:采样个数
mu:均值集合
sigma:标准差集合
P:概率集合,和为1
min:下限
max:上限
"""
@mw_connect_decorator(_MwConnect._process_path)
def GaussianMixtureSampling(number:int = 10, mu:list = [5, 2], sigma:list = [10, 3], P:list = [0.7, 0.3], min = -1e100, max = 1e100)->list:
    if type(min) == int or type(min) == float:
        min = float(min)
    else:
        return False
    if type(max) == int or type(max) == float:
        max = float(max)
    else:
        return False
    params = inspect.signature(GaussianMixtureSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GaussianMixtureSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

__all__ = [name for name in globals() if not name.startswith('_')]
#####################################jiangtao
