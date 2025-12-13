import inspect
import time
import os
from colorama import init, Fore
import multiprocessing
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
init(autoreset = True)

_num_cores = multiprocessing.cpu_count()
_name = "DesignOpt"
_MwConnect = MwConnect()

@mw_connect_decorator(_MwConnect._process_path)
def GetSimStatus()->int:
    params = inspect.signature(GetSimStatus).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetSimStatus, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 状态
"""
brief: 关闭参数估计
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def CloseApp()->bool:
    params = inspect.signature(CloseApp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CloseApp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 初始化参数估计
return: bool
modelName: 模型名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def InitialApp(modelName: str, instPath:str = "")->bool:
    params = inspect.signature(InitialApp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(InitialApp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 会话
"""
brief: 打开会话
return: bool
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
return: 会话路径或会话名称
path:会话路径或会话名称
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
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetTunerParam()->list:
    params = inspect.signature(GetTunerParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetTunerParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 选择调节参数
return: bool
array: tuple,待选择的调节参数名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SelectTunerParam(array: tuple)->bool:
    for item in array:
        if isinstance(item, str) is False:
            return False
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
def ConfigTunerParam(paramName: str, minVal = -1e100, maxVal = 1e100, initialVal = 0)->bool:
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
def DeleteTunerParam(paramName: str)->bool:
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

# 试验
"""
brief: 新建试验
return: bool
expName: 待新建的试验名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewExp(expName: str)->bool:
    if type(expName) != str:
        return False
    params = inspect.signature(NewExp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewExp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 新建试验并且配置试验
return: bool
expName: 待新建的试验名称
path: 测量文件路径
"""
@mw_connect_decorator(_MwConnect._process_path)
def NewExpAttachPath(expName: str, path: str)->bool:
    if type(expName) != str:
        return False
    params = inspect.signature(NewExpAttachPath).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewExpAttachPath, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取已经创建的试验名称
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetExp()->list:
    params = inspect.signature(GetExp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetExp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取当前的估计试验名称
return: str
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetCurrentEstimateExp()->str:
    params = inspect.signature(GetCurrentEstimateExp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetCurrentEstimateExp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取当前的验证试验
return: str
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetCurrentValidateExp()->str:
    params = inspect.signature(GetCurrentValidateExp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetCurrentValidateExp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 设置为估计试验
return: bool
expName: 待设置的试验名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetEstimateExp(expName: str)->bool:
    params = inspect.signature(SetEstimateExp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetEstimateExp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 设置为验证试验
return: bool
expName: 待设置的试验名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetValidateExp(expName: str)->bool:
    params = inspect.signature(SetValidateExp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetValidateExp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置试验
return: bool
expName: 待设置的试验名称
path: 测量文件路径
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigExp(expName: str, path: str)->bool:
    params = inspect.signature(ConfigExp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ConfigExp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 删除试验
return: bool
expName: 待删除的试验名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def DeleteExp(expName: str)->bool:
    params = inspect.signature(DeleteExp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(DeleteExp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 清空试验
return: bool
"""
@mw_connect_decorator(_MwConnect._process_path)
def ClearExp()->bool:
    params = inspect.signature(ClearExp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ClearExp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 固定参数
"""
brief: 选择固定参数
return: bool
expName: 试验名称
array: tuple,待选择的固定参数
"""
@mw_connect_decorator(_MwConnect._process_path)
def SelectFixParam(expName: str, array: tuple)->bool:
    for item in array:
        if isinstance(item, str) is False:
            return False
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
return: list
expName: 试验名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetSelectedFixParam(expName: str)->list:
    params = inspect.signature(GetSelectedFixParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetSelectedFixParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 配置固定参数
return: bool
expName: 试验名称
paramName: 固定参数名称
initialVal: 固定参数初始值
"""
@mw_connect_decorator(_MwConnect._process_path)
def ConfigFixParam(expName:str, paramName: str, initialVal = 0)->bool:
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
expName: 试验名称
paramName: 固定参数名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def DeleteFixParam(expName:str, paramName: str)->bool:
    params = inspect.signature(DeleteFixParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(DeleteFixParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 清空固定参数
return: bool
expName: 试验名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def ClearFixParam(expName:str)->bool:
    params = inspect.signature(ClearFixParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ClearFixParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 变量
"""
brief: 获取全部变量
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetVariable()->list:
    params = inspect.signature(GetVariable).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetVariable, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取测量变量
return: list
expName: 试验名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetMeasureVariable(expName: str)->list:
    params = inspect.signature(GetMeasureVariable).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetMeasureVariable, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 绑定仿真变量和测量变量
return: bool
expName: 试验名称
simulateVariable: 仿真变量名称
measureVariable: 测量变量名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetSimulateVariable(expName:str, simulateVariable: str, measureVariable: str)->bool:
    params = inspect.signature(SetSimulateVariable).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetSimulateVariable, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 优化算法
"""
brief: 获取支持的算法
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetAlgorithm()->list:
    params = inspect.signature(GetAlgorithm).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetAlgorithm, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 选择算法
return: bool
name: 算法名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SelectAlgorithm(name:str)->bool:
    params = inspect.signature(SelectAlgorithm).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectAlgorithm, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取当前选择的算法
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
def ConfigPSOAlgorithm(relativeTolerance = 0.001, convergenceTime:int = 3, maxIterStep:int = 100, populationSize:int = 20, parameterAdaptive: bool = True, w = 0.6, c1 = 1.5, c2 = 2)->bool:
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

"""
brief: 设置仿真选项
return: bool
SimStartTime: 仿真开始时间
SimEndTime: 仿真结束时间
estimateStartTime: 估计开始时间
estimateEndTime: 估计结束时间
stepNumber: 仿真步数
"""
# 仿真选项
@mw_connect_decorator(_MwConnect._process_path)
def SetSimulateOption(SimStartTime = 0.0, SimEndTime = 1, estimateStartTime = 0, estimateEndTime = 1, stepNumber:int = 500)->bool:
    if type(SimStartTime) == int or type(SimStartTime) == float:
        SimStartTime = float(SimStartTime)
    else:
        return False
    if type(SimEndTime) == int or type(SimEndTime) == float:
        SimEndTime = float(SimEndTime)
    else:
        return False
    if type(estimateStartTime) == int or type(estimateStartTime) == float:
        estimateStartTime = float(estimateStartTime)
    else:
        return False
    if type(estimateEndTime) == int or type(estimateEndTime) == float:
        estimateEndTime = float(estimateEndTime)
    else:
        return False
    params = inspect.signature(SetSimulateOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('SimStartTime')] = type(SimStartTime)
    expected_types[list(params.keys()).index('SimEndTime')] = type(SimEndTime)
    expected_types[list(params.keys()).index('estimateStartTime')] = type(estimateStartTime)
    expected_types[list(params.keys()).index('estimateEndTime')] = type(estimateEndTime)
    res = _MwConnect.__RunCurrentFunction__(SetSimulateOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)
    return res

"""
brief: 设置参数验证选项
return: bool
SimStartTime: 仿真开始时间
SimEndTime: 仿真结束时间
validateStartTime: 验证开始时间
validateEndTime: 验证结束时间
stepNumber: 仿真步数
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetValidateSimulateOption(simStartTime = 0.0, simEndTime = 1.0, validateStartTime = 0.0, validateEndTime = 1.0, stepNumber:int = 500)->bool:
    if type(simStartTime) == int or type(simStartTime) == float:
        simStartTime = float(simStartTime)
    else:
        return False
    if type(simEndTime) == int or type(simEndTime) == float:
        simEndTime = float(simEndTime)
    else:
        return False
    if type(validateStartTime) == int or type(validateStartTime) == float:
        validateStartTime = float(validateStartTime)
    else:
        return False
    if type(validateEndTime) == int or type(validateEndTime) == float:
        validateEndTime = float(validateEndTime)
    else:
        return False
    params = inspect.signature(SetValidateSimulateOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('simStartTime')] = type(simStartTime)
    expected_types[list(params.keys()).index('simEndTime')] = type(simEndTime)
    expected_types[list(params.keys()).index('validateStartTime')] = type(validateStartTime)
    expected_types[list(params.keys()).index('validateEndTime')] = type(validateEndTime)
    return _MwConnect.__RunCurrentFunction__(SetValidateSimulateOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取已设置的仿真选项数据
return: dict, key: "SimulationStartTime", "SimulationEndTime", "EstimateStartTime", "EstimateEndTime"
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetSimulateOption()->dict:
    params = inspect.signature(GetSimulateOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetSimulateOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取残差的计算方式
return: list
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetResidualFunc()->list:
    params = inspect.signature(GetResidualFunc).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetResidualFunc, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 设置仿真选项
return: bool
residualFunc: 残差计算方式
parallelNum: 并行数目
continueEstimate: 仿真失败后是否继续仿真
"""
@mw_connect_decorator(_MwConnect._process_path)
def SetEstimateOption(residualFunc: str = "Mean Absolute Percentage Error", parallelNum: int = int(_num_cores / 2), continueEstimate: bool = True)->bool:
    params = inspect.signature(SetEstimateOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetEstimateOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取已设置的估计选项数据
return: dict, key:"ResidualFunc":残差计算方式, "ParallelNumber":并行数目, "ContinueEstimate":失败后是否继续仿真
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetEstimateOption()->dict:
    params = inspect.signature(GetEstimateOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEstimateOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 仿真
@mw_connect_decorator(_MwConnect._process_path)
def EvaluateCurrentParam()->bool:
    params = inspect.signature(EvaluateCurrentParam).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(EvaluateCurrentParam, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 评估当前参数
return: bool
"""
def StartEvaluate()->bool:
    res = EvaluateCurrentParam()
    if res is False:
        return res
    return __WaitSimFinish()

@mw_connect_decorator(_MwConnect._process_path)
def Estimate()->bool:
    params = inspect.signature(Estimate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Estimate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 为Python自定义算法开发start
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
# 为Python自定义算法开发end

@mw_connect_decorator(_MwConnect._process_path)
def Validate()->bool:
    params = inspect.signature(Validate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Validate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

def __WaitSimFinish():
    while True:
        res = GetSimStatus()
        if res == -1:
            time.sleep(3)
            continue
        elif res == 0:
            return True
        else:
            return False

"""
brief: 开始参数估计
return: bool
"""
def StartEstimate()->bool:
    res = Estimate()
    if res is False:
        return False
    return __WaitSimFinish() 

"""
brief: 开始参数验证
return: bool
"""
def StartValidate()->bool:
    res = Validate()
    if res is False:
        return False
    return __WaitSimFinish()

# 结果、报告
"""
brief: 获取参数估计的报告
return: list, list内为dict, key: "iteration": 迭代次数, "residual": 残差, "参数名称": 获取参数值
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetEstimateReport()->list:
    params = inspect.signature(GetEstimateReport).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEstimateReport, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取评估当前参数的结果数据
return: dict, key: "Residual": 残差值, "变量名称": 获取变量数据.如获取残差dict["residual"], 获取评估结果dict["carBody.a"], 获取时间序列dict["time"]
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetEvaluateResultData()->dict:
    params = inspect.signature(GetEvaluateResultData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEvaluateResultData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取参数估计结果名称
return: list, 包含所有的参数估计的结果名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetEstimateResult()->str:
    params = inspect.signature(GetEstimateResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEstimateResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取参数估计最新一次估计的仿真结果和残差值
return: dist, key: 仿真变量名称、时间"time"、残差"Residual", value: 对应的值
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetEstimateResultData()->dict:
    params = inspect.signature(GetEstimateResultData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEstimateResultData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取参数估计的参数结果值
return: dist, key: 调节参数的名称, value: 对应的值
resultName: 参数估计结果名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetEstimateParamData(resultName: str)->dict:
    if type(resultName) != str:
        return False
    params = inspect.signature(GetEstimateParamData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEstimateParamData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 选择参数估计结果，用于参数验证
return: bool
resultName: 参数估计结果名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def SelectEstimateResult(resultName: str)->bool:
    params = inspect.signature(SelectEstimateResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectEstimateResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取参数验证的结果数据
return: dist, key: 调节参数的名称或者残差"residual", value: 对应的值
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetValidateResultData()->dict:
    params = inspect.signature(GetValidateResultData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetValidateResultData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

# 数据预处理接口开发start
"""
brief: 导入数据预处理数据
path:文件路径
name:此次导入数据的自定义名称
return: bool, 导入成功与否
"""
@mw_connect_decorator(_MwConnect._process_path)
def ImportData(path:str, dataName:str)->bool:
    params = inspect.signature(ImportData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ImportData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 偏移数据
dataName：数据名称
lineName：线段名称，或者输入all:代表对所有的线段进行处理
offsetValue：str,偏移量，可以输入数字、Initial Value、Mean Value
resultName：对本次数据预处理的生成结果进行命名
return: bool, 成功与否
"""
@mw_connect_decorator(_MwConnect._process_path)
def ChangeOffsetData(dataName:str, lineName:str, resultName:str, offsetValue:str)->bool:
    params = inspect.signature(ChangeOffsetData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ChangeOffsetData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 缩放数据
dataName：数据名称
lineName：线段名称，或者输入all:代表对所有的线段进行处理
scaleValue:str,缩放因子，可以输入数字、Max Value、Initial Value
resultName：对本次数据预处理的生成结果进行命名
return: bool, 成功与否
"""
@mw_connect_decorator(_MwConnect._process_path)
def ScaleData(dataName:str, lineName:str, resultName:str, scaleValue:str)->bool:
    params = inspect.signature(ScaleData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ScaleData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 提取数据
dataName：数据名称
lineName：线段名称，或者输入all:代表对所有的线段进行处理
startTime:开始时间，输入数字
endTime:结束时间，输入数字
resultName：对本次数据预处理的生成结果进行命名
return: bool, 成功与否
"""
@mw_connect_decorator(_MwConnect._process_path)
def ExtractData(dataName:str, lineName:str, resultName:str, startTime = 0, endTime = 1)->bool:
    if type(startTime) == int or type(startTime) == float:
        startTime = float(startTime)
    else:
        return False
    if type(endTime) == int or type(endTime) == float:
        endTime = float(endTime)
    else:
        return False
    params = inspect.signature(ExtractData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('startTime')] = type(startTime)
    expected_types[list(params.keys()).index('endTime')] = type(endTime)
    return _MwConnect.__RunCurrentFunction__(ExtractData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 重采样数据
dataName：数据名称
lineName：线段名称，或者输入all:代表对所有的线段进行处理
resamplePeriod:重采样周期，输入数字
resultName：对本次数据预处理的生成结果进行命名
return: bool, 成功与否
"""
@mw_connect_decorator(_MwConnect._process_path)
def ResampleData(dataName:str, lineName:str, resultName:str, resamplePeriod = 0.002)->bool:
    if type(resamplePeriod) == int or type(resamplePeriod) == float:
        resamplePeriod = float(resamplePeriod)
    else:
        return False
    params = inspect.signature(ResampleData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('resamplePeriod')] = type(resamplePeriod)
    return _MwConnect.__RunCurrentFunction__(ResampleData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 替换数据
dataName：数据名称
lineName：线段名称，或者输入all:代表对所有的线段进行处理
scaleValue:缩放因子，可以输入数字、Max Value、Initial Value
resultName：对本次数据预处理的生成结果进行命名
return: bool, 成功与否
"""
# @mw_connect_decorator
# def ReplaceData(dataName:str, lineName:str, scaleValue:str, resultName:str)->bool:
#     params = inspect.signature(ReplaceData).parameters
#     args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
#     expected_types = [v.annotation for k, v in params.items() if k != 'self']
#     return _MwConnect.__RunCurrentFunction__(ReplaceData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 低通滤波数据处理
dataName：数据名称
lineName：线段名称，或者输入all:代表对所有的线段进行处理
cutoffFrequency:截止频率，输入数字
filterOrder:滤波器阶数
resultName：对本次数据预处理的生成结果进行命名
return: bool, 成功与否
"""
@mw_connect_decorator(_MwConnect._process_path)
def LowFilterData(dataName:str, lineName:str, resultName:str, cutoffFrequency = 0.2, filterOrder:int = 4)->bool:
    if type(cutoffFrequency) == int or type(cutoffFrequency) == float:
        cutoffFrequency = float(cutoffFrequency)
    else:
        return False
    params = inspect.signature(LowFilterData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('cutoffFrequency')] = type(cutoffFrequency)
    return _MwConnect.__RunCurrentFunction__(LowFilterData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 高通滤波数据处理
dataName：数据名称
lineName：线段名称，或者输入all:代表对所有的线段进行处理
cutoffFrequency:截止频率，输入数字
filterOrder:int, 滤波器阶数
resultName：对本次数据预处理的生成结果进行命名
return: bool, 成功与否
"""
@mw_connect_decorator(_MwConnect._process_path)
def HighFilterData(dataName:str, lineName:str, resultName:str, cutoffFrequency = 0.2, filterOrder:int = 4)->bool:
    if type(cutoffFrequency) == int or type(cutoffFrequency) == float:
        cutoffFrequency = float(cutoffFrequency)
    else:
        return False
    params = inspect.signature(HighFilterData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('cutoffFrequency')] = type(cutoffFrequency)
    return _MwConnect.__RunCurrentFunction__(HighFilterData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 带通滤波数据处理
dataName：数据名称
lineName：线段名称，或者输入all:代表对所有的线段进行处理
startCutoffFrequency:截止开始频率，输入数字
endCutoffFrequency：截止结束频率，输入数字
filterOrder:滤波器阶数
resultName：对本次数据预处理的生成结果进行命名
return: bool, 成功与否
"""
@mw_connect_decorator(_MwConnect._process_path)
def BandFilterData(dataName:str, lineName:str, resultName:str, startCutoffFrequency = 0.2, endCutoffFrequency = 0.9, filterOrder:int = 4)->bool:
    if type(startCutoffFrequency) == int or type(startCutoffFrequency) == float:
        startCutoffFrequency = float(startCutoffFrequency)
    else:
        return False
    if type(endCutoffFrequency) == int or type(endCutoffFrequency) == float:
        endCutoffFrequency = float(endCutoffFrequency)
    else:
        return False
    params = inspect.signature(BandFilterData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('startCutoffFrequency')] = type(startCutoffFrequency)
    expected_types[list(params.keys()).index('endCutoffFrequency')] = type(endCutoffFrequency)
    return _MwConnect.__RunCurrentFunction__(BandFilterData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取所有的数据预处理结果
return: list, 所有的结果名称
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetDataProcessResult()->list:
    params = inspect.signature(GetDataProcessResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetDataProcessResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 获取所有的数据预处理结果的数据
resultName：待获取的结果名称
return: dict, 数据
"""
@mw_connect_decorator(_MwConnect._process_path)
def GetDataProcessResultData(resultName:str)->dict:
    params = inspect.signature(GetDataProcessResultData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetDataProcessResultData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

"""
brief: 导出处理数据为csv文件
path：导出路径,计算机合法路径
resultName：待导出的结果名称
return: bool, 成功与否
"""
@mw_connect_decorator(_MwConnect._process_path)
def ExportData(path:str, resultName:str)->bool:
    params = inspect.signature(ExportData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ExportData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)
# 数据预处理接口开发end