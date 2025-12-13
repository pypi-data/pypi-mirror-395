import inspect
import time
import os
from colorama import init, Fore
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
import re
import multiprocessing
init(autoreset = True)

_num_cores = multiprocessing.cpu_count()
_name = "DesignOptExpGui"
_MwConnect = MwConnect()

@mw_connect_decorator(_MwConnect._process_path)
def InitialBatchSimulate(solverPath:str, storePath: str, instNum:int = 50, options:dict = {}):
    """
    brief:初始化批量仿真
    return:bool，初始化是否成功
    storePath:仿真工作目录，计算机任意合法路径
    instNum:实例池数目，默认50
    options:仿真配置,key:"startTime":开始时间, "stopTime":结束时间, "outputStep":输出步长, "algorithm":仿真算法, "tolerance":精度, "saveEvent":存储事件时刻的变量值
    solverPath:求解器路径
    """
    params = inspect.signature(InitialBatchSimulate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(InitialBatchSimulate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def BatchSimulate(param:list, resultName:list):
    """
    brief:开始批量仿真
    return:list, list(dict(str:list())), 外层list:批量结果， dict:key:结果变量名称, value:list， 结果变量数值
    param: 仿真参数， list(dict(str:double))
    resultName:对应每次仿真的结果变量名称，list(list(str))
    """
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

@mw_connect_decorator(_MwConnect._process_path)
def InitialApp(modelName:str)->bool:
    """
    brief: 初始化模型试验
    return: bool
    modelName: 模型名称
    """
    params = inspect.signature(InitialApp).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(InitialApp, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def OpenSession(path:str)->bool:
    """
    brief: 打开会话
    return: bool
    path: 会话路径 
    """
    params = inspect.signature(OpenSession).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(OpenSession, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SaveSession(path:str)->bool:
    """
    brief: 保存会话
    return: bool
    path: 待保存会话的路径
    """
    params = inspect.signature(SaveSession).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SaveSession, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SelectParameter(parameters:list)->bool:
    """
    brief: 选择参数
    return: bool
    parameters: list,待选择的参数名称
    """
    params = inspect.signature(SelectParameter).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectParameter, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SelectVariable(variables:list)->bool:
    """
    brief: 选择变量
    return: bool
    variables: list,待选择的变量名称
    """
    params = inspect.signature(SelectVariable).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SelectVariable, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetParameter()->list:
    """
    brief: 获取全部参数
    return: list
    """
    params = inspect.signature(GetParameter).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetParameter, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)


@mw_connect_decorator(_MwConnect._process_path)
def GetVariable()->list:
    """
    brief: 获取全部变量
    return: list
    """
    params = inspect.signature(GetVariable).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetVariable, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def NewBatch(name:str)->bool:
    """
    brief: 新建批量仿真
    return: bool
    name: 待新建的批量仿真名称
    """
    params = inspect.signature(NewBatch).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewBatch, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def NewExperimentDesign(name:str)->bool:
    """
    brief: 新建实验设计
    return: bool
    name: 待新建的实验设计名称
    """
    params = inspect.signature(NewExperimentDesign).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewExperimentDesign, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def NewMentoCarlo(name:str)->bool:
    """
    brief: 新建蒙特卡洛采样
    return: bool
    name: 待新建的蒙特卡洛名称
    """
    params = inspect.signature(NewMentoCarlo).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewMentoCarlo, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def NewTimeParameter(name:str)->bool:
    """
    brief: 新建时变参数
    return: bool
    name: 待新建的时变参数名称
    """
    params = inspect.signature(NewTimeParameter).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(NewTimeParameter, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetStudyName()->list:
    """
    brief: 获取所有的研究名称
    return: list
    """
    params = inspect.signature(GetStudyName).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetStudyName, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetParameterMatrix(name:str, parameters:dict)->bool:
    """
    brief: 设置参数矩阵
    return: bool，成功与否
    name:已建的试验名称
    parameters：dict, 形式如{"name1":[参数值]}

    paramName:参数名称
    sampleType:波形类型，0：正弦波；1：三角波；2：方波
    sampleNum:int, 随机样本数量,时变参数使用
    min:参数最小值
    max:参数最大值
    value:dict,{"value":[0,1,0,1,0,1,0,1]}:

    path:文件路径
    paramname:文件参数名称绑定
    """
    params = inspect.signature(SetParameterMatrix).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetParameterMatrix, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def StartSimulation(name:str)->bool:
    """
    brief: 开始仿真
    return: bool,是否成功
    name:已建的试验名称
    parameters：dict, 形式如{"name1":[参数值]}
    variables：list, ["变量名称"]
    """
    params = inspect.signature(StartSimulation).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(StartSimulation, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def NormalSampling(number:int = 20, mean = 1, sigma = 0.57735, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 正态分布采样
    return: list, 采样结果
    number:采样个数
    mean:均值
    sigma:标准差
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(mean) == int or type(mean) == float:
        mean = float(mean)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(NormalSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def UniformSampling(number:int = 20, lower = -0.05, upper = 0.05, seed = 0.612702)->list:
    """
    brief: 均匀分布采样
    return: list, 采样结果
    number:采样个数
    seed: 随机数种子，取值范围[0, 1]
    lower:下限
    upper:上限
    """
    if type(lower) == int or type(lower) == float:
        lower = float(lower)
    else:
        return False
    if type(upper) == int or type(upper) == float:
        upper = float(upper)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
    else:
        return False
    params = inspect.signature(UniformSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('lower')] = type(lower)
    expected_types[list(params.keys()).index('upper')] = type(upper)
    expected_types[list(params.keys()).index('seed')] = type(seed)
    return _MwConnect.__RunCurrentFunction__(UniformSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def BetaSampling(number:int = 20, a = 1, b = 1,seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 贝塔分布采样
    return: list, 采样结果
    number:采样个数
    a:形状参数
    b:形状参数
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(a) == int or type(a) == float:
        a = float(a)
    else:
        return False
    if type(b) == int or type(b) == float:
        b = float(b)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(BetaSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def BinbaumSaundersSampling(number:int = 20, beta = 0.666667, gamma = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 伯恩鲍姆-桑德斯分布采样
    return: list, 采样结果
    number:采样个数
    beta:尺度参数
    gamma:形状参数
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(beta) == int or type(beta) == float:
        beta = float(beta)
    else:
        return False
    if type(gamma) == int or type(gamma) == float:
        gamma = float(gamma)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(BinbaumSaundersSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def BurrSampling(number:int = 20, alpha = 1, c = 1, k = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 伯尔XII分布采样
    return: list, 采样结果
    number:采样个数
    alpha:尺度参数
    c:形状参数
    k:形状参数
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
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
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(BurrSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def ExponentialSampling(number:int = 20, lambdaa = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 指数分布采样
    return: list, 采样结果
    number:采样个数
    lambdaa:速率参数，表示事情发生的频率或强度
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(lambdaa) == int or type(lambdaa) == float:
        lambdaa = float(lambdaa)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(ExponentialSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def ExtremeValueSampling(number:int = 20, mu = 0, sigma = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 极值分布采样
    return: list, 采样结果
    number:采样个数
    mu:位置参数
    sigma:尺度参数
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(ExtremeValueSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GammaSampling(number:int = 20, a = 1, b = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 伽马分布采样
    return: list, 采样结果
    number:采样个数
    a:形状参数， a > 0
    b:尺度参数, b > 0
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(a) == int or type(a) == float:
        a = float(a)
    else:
        return False
    if type(b) == int or type(b) == float:
        b = float(b)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GammaSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GeneralizedExtremeSampling(number:int = 20, k = 0, sigma = 1, mu = 0, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 广义极值分布采样
    return: list, 采样结果
    number:采样个数
    k:形状参数
    sigma:尺度参数, sigma > 0
    mu:位置参数
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
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
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GeneralizedExtremeSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GeneralizedParetoSampling(number:int = 20, k = 0, sigma = 1,theta = 0, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 广义帕累托分布采样
    return: list, 采样结果
    number:采样个数
    k:形状参数
    sigma:尺度参数, sigma > 0
    theta:阈值参数
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
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
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GeneralizedParetoSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def InverseGaussianSampling(number:int = 20, mu = 1, lambdaa = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 逆高斯分布采样
    return: list, 采样结果
    number:采样个数
    mu:尺度参数，mu > 0
    lambdaa:形状参数, lambdaa > 0
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(lambdaa) == int or type(lambdaa) == float:
        lambdaa = float(lambdaa)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(InverseGaussianSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def LogisticSampling(number:int = 20, mu = 0, sigma = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 逻辑分布采样
    return: list, 采样结果
    number:采样个数
    mu:均值
    sigma:尺度参数, sigma >= 0
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(LogisticSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def LoglogisticSampling(number:int = 20, mu = 0, sigma = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 对数逻辑分布采样
    return: list, 采样结果
    number:采样个数
    mu:对数值的均值, mu >= 0
    sigma:尺度参数, sigma > 0
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(LoglogisticSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def LogNormalSampling(number:int = 20, mu = 0, sigma = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 逻辑对数分布采样
    return: list, 采样结果
    number:采样个数
    mu:均值
    sigma:尺度参数, sigma > 0
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(mu) == int or type(mu) == float:
        mu = float(mu)
    else:
        return False
    if type(sigma) == int or type(sigma) == float:
        sigma = float(sigma)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(LogNormalSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def MultionmialSampling(number:int = 20, probabilitie:list = [0.5, 0.5], position:list = [0, 1], seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 多项分布采样
    return: list, 采样结果
    number:采样个数
    probabilitie:概率参数，和为1
    position:位置参数
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    params = inspect.signature(MultionmialSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(MultionmialSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def PoissonSampling(number:int = 20, lambdaa = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 泊松分布采样
    return: list, 采样结果
    number:采样个数
    lambdaa:均值,>0
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(lambdaa) == int or type(lambdaa) == float:
        lambdaa = float(lambdaa)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(PoissonSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def RayleihSampling(number:int = 20, B = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 瑞利分布采样
    return: list, 采样结果
    number:采样个数
    B:定义参数，B > 0
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(B) == int or type(B) == float:
        B = float(B)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(RayleihSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def WeibullSampling(number:int = 20, A = 1, B = 1, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 威布尔分布采样
    return: list, 采样结果
    number:采样个数
    A:尺度参数，A > 0
    B:形状参数，B > 0
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(A) == int or type(A) == float:
        A = float(A)
    else:
        return False
    if type(B) == int or type(B) == float:
        B = float(B)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(WeibullSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GeometricSampling(number:int = 20, P = 0.5, seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 几何分布采样
    return: list, 采样结果
    number:采样个数
    P:成功概率，[0, 1]
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(P) == int or type(P) == float:
        P = float(P)
    else:
        return False
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GeometricSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GaussianMixtureSampling(number:int = 20, mu:list = [5, 2], sigma:list = [10, 3], P:list = [0.7, 0.3], seed = 0.612702, min = -1e100, max = 1e100)->list:
    """
    brief: 混合高斯分布采样
    return: list, 采样结果
    number:采样个数
    mu:均值集合
    sigma:标准差集合
    P:概率集合,和为1
    seed: 随机数种子，取值范围[0, 1]
    min:下限
    max:上限
    """
    if type(seed) == int or type(seed) == float:
        seed = float(seed)
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
    params = inspect.signature(GaussianMixtureSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('seed')] = type(seed)
    expected_types[list(params.keys()).index('min')] = type(min)
    expected_types[list(params.keys()).index('max')] = type(max)
    return _MwConnect.__RunCurrentFunction__(GaussianMixtureSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def EquallySpacedSampling(initialValue = 100, stepLength = 5, lowerNum:int = 2, upperNum:int = 1)->list:
    """
    brief:等间距采样
    return:list, 采样结果
    initialValue: 初始值
    stepLength：采样步长
    lowerNum:初始值以下采样个数
    upperNum:初始值以上采样个数
    """
    if type(initialValue) == int or type(initialValue) == float:
        initialValue = float(initialValue)
    else:
        return False

    if type(stepLength) == int or type(stepLength) == float:
        stepLength = float(stepLength)
    else:
        return False
    params = inspect.signature(EquallySpacedSampling).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('initialValue')] = type(initialValue)
    expected_types[list(params.keys()).index('stepLength')] = type(stepLength)
    return _MwConnect.__RunCurrentFunction__(EquallySpacedSampling, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def FullFactorialDesign(level:list)->list:
    """
    brief:全因子设计
    return:list, 采样结果
    level: [[]],二维数组。第一个参数的水平为0，1；第二个参数的水平为10，20，30.则level = [[0,1], [10, 20, 30]]
    """
    params = inspect.signature(FullFactorialDesign).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(FullFactorialDesign, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def OrthogonalDesign(level:list)->list:
    """
    brief:正交设计
    return:list, 采样结果
    level: [[]],二维数组。第一个参数的水平为0，1；第二个参数的水平为10，20，30.则level = [[0,1], [10, 20, 30]]
    """
    params = inspect.signature(OrthogonalDesign).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(OrthogonalDesign, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def LatinHypercubeDesign(number:int, minValue:list, maxValue:list)->list:
    """
    brief:拉丁超立方设计
    return:list, 采样结果
    number:int, 样本数量
    minValue:list, 最小值数组
    maxValue:list, 最大值数组
    """
    params = inspect.signature(LatinHypercubeDesign).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(LatinHypercubeDesign, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def CenterCompositeDesign(minValue:list, maxValue:list, centerNum:list = [1, 1], typeFace:int = 0, typeAlpha:int = 0)->list:
    """
    brief:中心复合采样
    return:list, 采样结果
    minValue: list，最小值列表
    maxValue: list, 最大值列表
    centerNum: list, 中心点数量，允许输入两个数据，且为整数
    typeFace: int, 0：外接； 1：内接； 2：正面
    typeAlpha: int, 0：正交； 1：可旋转
    """
    params = inspect.signature(CenterCompositeDesign).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CenterCompositeDesign, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def DOptimalDesign(minValue:list, maxValue:list, number:int = 10, algoType:int = 0)->list:
    """
    brief:D最优设计
    return:list, 采样结果
    minValue: list，最小值列表
    maxValue: list, 最大值列表
    number: int, 样本数量
    algoType: 算法类型，0：trust-constr; 1:SLSQP; 2:COBYLA; 3:L-BFGS-B; 4:BFGS; 5:Powell
    """
    params = inspect.signature(DOptimalDesign).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(DOptimalDesign, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetSimulationOption(name:str, startTime = 0, stopTime = 1, outputStep = 0.002, algorithm:str = "Dassl", tolerance = 0.0001, saveEvent:bool = True):
    """
    brief:针对某个具体的研究进行仿真选项的设置
    return:bool, 设置是否成功
    name: str，待仿真的研究名称
    startTime: int or float，仿真开始时间。小于结束时间
    stopTime: int or float，仿真结束时间。大于开始时间
    outputStep: int or float，输出步长
    algorithm: str，算法名称，区分大小写
    tolerance: int or float，仿真精度
    saveEvent: bool，是否存储事件时刻的变量值
    """ 
    if type(startTime) == int or type(startTime) == float:
        startTime = float(startTime)
    else:
        return False
    if type(stopTime) == int or type(stopTime) == float:
        stopTime = float(stopTime)
    else:
        return False
    if type(outputStep) == int or type(outputStep) == float:
        outputStep = float(outputStep)
    else:
        return False
    if type(tolerance) == int or type(tolerance) == float:
        tolerance = float(tolerance)
    else:
        return False
    params = inspect.signature(SetSimulationOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('startTime')] = type(startTime)
    expected_types[list(params.keys()).index('stopTime')] = type(stopTime)
    expected_types[list(params.keys()).index('outputStep')] = type(outputStep)
    expected_types[list(params.keys()).index('tolerance')] = type(tolerance)
    return _MwConnect.__RunCurrentFunction__(SetSimulationOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetExperimentOption(resultPath:str, parallel:int = 10):
    """
    brief:设置模型试验工作选项
    return:bool, 设置是否成功
    resultPath: str，计算机合法路径
    parallel: int, 不大于20
    """ 
    params = inspect.signature(SetExperimentOption).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetExperimentOption, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetResultData(studyName:str, varName:str):
    """
    brief:获取仿真结果数据
    return:dict, 仿真结果数据
    studyName: str，研究名称
    varName: str, 变量名称
    """   
    params = inspect.signature(GetResultData).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetResultData, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

__all__ = [name for name in globals() if not name.startswith('_')]
#####################################jiangtao
