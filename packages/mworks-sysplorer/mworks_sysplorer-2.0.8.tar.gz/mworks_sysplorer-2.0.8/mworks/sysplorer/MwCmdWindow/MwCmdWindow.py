import inspect
import os
from colorama import init
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator, path_resolver
from mworks.sysplorer.sysplorer_api import GetDirectory, Echo, GetModelExperiment, _IsAlgoFixedStep
init(autoreset = True)
_name = "MwCmdWindow"
_MwConnect = MwConnect()

@mw_connect_decorator(_MwConnect._process_path)
def ClearScreen():
    """
    清空命令行输出

    语法
        >>> ClearScreen()
    说明
        ClearScreen() 用于清空命令行输出
    示例
        >>> ClearScreen()
    输入参数
        None
    返回值
        操作是否成功
    另请参阅
        无
    """
    params = inspect.signature(ClearScreen).parameters
    args = tuple(v for k, v in locals().items() if k not in ('params'))
    expected_types = [v.annotation for k, v in params.items()]
    return _MwConnect.__RunCurrentFunction__(ClearScreen, args=args, kwargs={}, expected_types = expected_types, get_response = False)

cls=ClearScreen

@mw_connect_decorator(_MwConnect._process_path)
def SaveScreen(fileName:str):
    """
    清空命令行输出

    语法
        >>> SaveScreen()
    说明
        SaveScreen() 用于清空命令行输出
    示例
        >>> SaveScreen()
    输入参数
        path
    返回值
        操作是否成功
    另请参阅
        无
    """
    params = inspect.signature(SaveScreen).parameters
    args = tuple(v for k, v in locals().items() if k not in ('params'))
    expected_types = [v.annotation for k, v in params.items()]
    return _MwConnect.__RunCurrentFunction__(SaveScreen, args=args, kwargs={}, expected_types = expected_types)

@mw_connect_decorator(_MwConnect._process_path)
def TranslateModelForThermoHydraulic(modelName:str):
    """
    翻译模型

    语法
        >>> TranslateModelForThermoHydraulic(modelName)
    说明
        TranslateModelForThermoHydraulic(modelName) 用于翻译模型。
    示例
    示例1：翻译NUMAP模型
        打开模型，翻译
        >>> OpenModel('Case01_FlowInstability')
        >>> TranslateModelForThermoHydraulic("Case01_FlowInstability")
    输入参数
        modelName - 模型全名
        数据类型：str
    返回值
        翻译模型的相关信息
    另请参阅
        无
    """
    params = inspect.signature(TranslateModelForThermoHydraulic).parameters
    args = tuple(v for k, v in locals().items() if k not in ('params'))
    expected_types = [v.annotation for k, v in params.items()]
    return _MwConnect.__RunCurrentFunction__(TranslateModelForThermoHydraulic, args=args, kwargs={}, expected_types = expected_types)

@mw_connect_decorator(_MwConnect._process_path)
def SimulateModelForThermoHydraulic(modelName:str):
    """
    翻译模型

    语法
        >>> SimulateModelForThermoHydraulic(modelName)
    说明
        SimulateModelForThermoHydraulic(modelName) 用于翻译模型。
    示例
    示例1：翻译NUMAP模型
        打开模型，翻译
        >>> OpenModel('Case01_FlowInstability')
        >>> SimulateModelForThermoHydraulic("Case01_FlowInstability")
    输入参数
        modelName - 模型全名
        数据类型：str
    返回值
        翻译模型的相关信息
    另请参阅
        无
    """


@mw_connect_decorator(_MwConnect._process_path)
@path_resolver(['path'], False, GetDirectory, Echo)
def SimulateModelForThermoHydraulic(modelName:str, startTime = None, stopTime = None,
    interval = None, tolerance = None, algo = None , integralStep = None,
    storeDouble:bool = True, storeEvent:bool = True, simMode = 0, isPieceWiseStep:bool = False, path:str = "",
    pieceWiseStep:tuple = ((0, 0.002),),**kwargs):
    """
    热力学模型仿真
    
    语法
        >>> SimulateModelForThermoHydraulic(modelName)
        >>> SimulateModelForThermoHydraulic(modelName, startTime, stopTime,
        >>>     interval, tolerance, algo, integralStep,
        >>>     storeDouble, storeEvent, simMode, isPieceWiseStep, path,
        >>>     pieceWiseStep)
    说明
        SimulateModelForThermoHydraulic(modelName) 用于以默认设置仿真模型。modelName 为仿真模型名称必须指定。
        SimulateModelForThermoHydraulic(modelName, startTime, stopTime, interval, tolerance, algo, integralStep,
            storeDouble, storeEvent, simMode, isPieceWiseStep, path, pieceWiseStep)
        用于仿真模型，参数modelName必须指定，其余参数可按默认值。
    示例
    示例1：Dassl算法仿真模型并保存结果
        加载标准模型库`Modelica 3.2.1`，仿真模型`Modelica.Blocks.Examples.PID_Controller`，选用Dassl算法，将实例文件生成在D:\\Data文件夹下，不使用分段固定积分步长，其余仿真设置采用缺省设置，即：仿真开始时间为0，结束时间为1，输出步数为500，精度为0.0001，积分步长为0.002，结果保存为Float精度，不保存事件点。
        >>> LoadLibrary('Modelica', '3.2.1')
        >>> SimulateModelForThermoHydraulic(modelName="Modelica.Blocks.Examples.PID_Controller", algo="Dassl", path=r"D:\\Data", isPieceWiseStep=False)
        可以在Sysplorer中打开相关曲线图：
    示例2：Euler算法仿真模型并保存结果
        加载标准模型库`Modelica 3.2.1`，仿真模型`Modelica.Blocks.Examples.PID_Controller`，选用Euler算法，将实例文件生成在D:\\Data文件夹下，使用分段固定积分步长[0, 0.001]，其余仿真设置采用缺省设置，即：仿真开始时间为0，结束时间为1，输出步数为500，精度为0.0001，积分步长为0.002，结果保存为Float精度，不保存事件点。
        >>> LoadLibrary('Modelica', '3.2.1')
        >>> SimulateModelForThermoHydraulic(modelName="Modelica.Blocks.Examples.PID_Controller", algo="Euler", path="D:\\Data", isPieceWiseStep=True, pieceWiseStep=((0, 0.001), ))
        可以在Sysplorer中打开相关曲线图：
    输入参数
        modelName - 模型名
        数据类型：str

        startTime - 仿真开始时间
        数据类型：float

        stopTime - 仿真终止时间
        数据类型：float

        interval - 输出区间长度
        数据类型：float

        algo - 积分算法
        数据类型：str
        可选变量如下：
        - Integration.Dassl: 积分算法:Dassl,命令中可缩写为"Dassl"
        - Integration.Radau5: 积分算法:Radau5,命令中可缩写为"Radau5"
        - Integration.Dop853: 积分算法:Dop853,命令中可缩写为"Dop853"
        - Integration.Dopri5: 积分算法:Dopri5,命令中可缩写为"Dopri5"
        - Integration.Mebdf: 积分算法:Mebdf,命令中可缩写为"Mebdf"
        - Integration.Mebdfi: 积分算法:Mebdfi,命令中可缩写为"Mebdfi"
        - Integration.Lsode: 积分算法:Lsode,命令中可缩写为"Lsode"
        - Integration.Lsodar: 积分算法:Lsodar,命令中可缩写为"Lsodar"
        - Integration.Cvode: 积分算法:Cvode,命令中可缩写为"Cvode"
        - Integration.Ida: 积分算法:Ida,命令中可缩写为"Ida"
        - Integration.Sdirk34: 积分算法:Sdirk34,命令中可缩写为"Sdirk34"
        - Integration.Esdirk23: 积分算法:Esdirk23,命令中可缩写为"Esdirk23"
        - Integration.Esdirk34: 积分算法:Esdirk34,命令中可缩写为"Esdirk34"
        - Integration.Esdirk45: 积分算法:Esdirk45,命令中可缩写为"Esdirk45"
        - Integration.Euler: 积分算法:Euler,命令中可缩写为"Euler"
        - Integration.Rkfix2: 积分算法:Rkfix2,命令中可缩写为"Rkfix2"
        - Integration.Rkfix3: 积分算法:Rkfix3,命令中可缩写为"Rkfix3"
        - Integration.Rkfix4: 积分算法:Rkfix4,命令中可缩写为"Rkfix4"
        - Integration.Rkfix6: 积分算法:Rkfix6,命令中可缩写为"Rkfix6"
        - Integration.Rkfix8: 积分算法:Rkfix8,命令中可缩写为"Rkfix8"
        - Integration.lmplicitEuler: 积分算法:lmplicitEuler,命令中可缩写为"lmplicitEuler"
        - Integration.lmplicitTrapezoid: 积分算法:lmplicitTrapezoid,命令中可缩写为"lmplicitTrapezoid"
        - Integration.Custom: 积分算法:Custom,命令中可缩写为"Custom" 

        integralStep - 初始积分步长
        数据类型：float

        storeDouble - 结果是否存为双精度
        数据类型：bool

        storeEvent - 是否存储事件时刻的变量值
        数据类型：bool

        simMode - 设置仿真模式，0为使用当前仿真模式，1为独立仿真，2为实时仿真
        数据类型：int

        isPieceWiseStep - 是否使用分段固定积分步长
        数据类型：bool

        path - 仿真结果文件存放的文件夹路径
        数据类型：str

        pieceWiseStep - 设置某段时间节点采用的积分步长。pieceWiseStep = ((0, xxx), (m, xxx), (n, xxx), ...), pieceWiseStep以二维数组表示，第一个数为时间节点，"xxx"为从当前时间节点开始的步长。
        数据类型：tuple
    返回值
        `bool` : 表示是否仿真成功
    另请参阅
        无
    """
    oldEcho = _MwConnect.get_echo_on()
    _MwConnect.set_echo_on(False)
    ModelExperiment = GetModelExperiment(modelName)
    if(startTime == None):
        startTime = ModelExperiment.get('startTime')
    if(stopTime == None):
        stopTime = ModelExperiment.get('stopTime')
    if(interval == None):
        interval = ModelExperiment.get('interval')
        if(interval == 0):
            numberOfIntervals = ModelExperiment.get('numberOfIntervals')
            if(numberOfIntervals != 0):
                interval = (stopTime - startTime)/numberOfIntervals
    if(interval > 10):
        print(f"Parameter \"interval\" is greater than 10, please confirm whether it meets your expectations.")
    if(algo == None):
        algo = ModelExperiment.get('algorithm')
    if(tolerance == None):
        tolerance = ModelExperiment.get('tolerance')
    if(integralStep == None):
        if(ModelExperiment.get('fixedOrInitStepSize') > 0):
            integralStep = ModelExperiment.get('fixedOrInitStepSize')
        else:
            if(_IsAlgoFixedStep(algo) == True):
                integralStep = interval
            else:
                integralStep = 0
    _MwConnect.set_echo_on(oldEcho)
    if type(startTime) == int or type(startTime) == float:
        startTime = float(startTime)
    else:
        return False
    if type(stopTime) == int or type(stopTime) == float:
        stopTime = float(stopTime)
    else:
        return False
    if type(interval) == int or type(interval) == float:
        interval = float(interval)
    else:
        return False
    if type(tolerance) == int or type(tolerance) == float:
        tolerance = float(tolerance)
    else:
        return False
    if type(integralStep) == int or type(integralStep) == float:
        integralStep = float(integralStep)
    else:
        return False
    if type(simMode) == int or type(simMode) == float:
        simMode = int(simMode)
    else:
        return False
    params = inspect.signature(SimulateModelForThermoHydraulic).parameters
    if kwargs != {}:
        valid_kwargs = set(params.keys())
        valid_kwargs.update(["resultFile"])
        # 判断参数是否传递正确
        for key in kwargs:
            if key in valid_kwargs:
                continue
            raise TypeError(f"SimulateModelForThermoHydraulic() got an unexpected keyword argument '{key}'")
        # 兼容旧版调用
        path = kwargs["resultFile"]

    args = tuple(v for k, v in locals().items() if k not in ('kwargs', 'params','ModelExperiment','numberOfIntervals','oldEcho'))
    expected_types = [v.annotation for k, v in params.items() if k != 'kwargs']
    expected_types[list(params.keys()).index('startTime')] = type(startTime)
    expected_types[list(params.keys()).index('stopTime')] = type(stopTime)
    expected_types[list(params.keys()).index('interval')] = type(interval)
    expected_types[list(params.keys()).index('algo')] = type(algo)
    expected_types[list(params.keys()).index('tolerance')] = type(tolerance)
    expected_types[list(params.keys()).index('integralStep')] = type(integralStep)
    expected_types[list(params.keys()).index('simMode')] = type(simMode)
    return _MwConnect.__RunCurrentFunction__(SimulateModelForThermoHydraulic, args=args, kwargs={}, expected_types = expected_types)

"""
Author: [Wang Run]
Date: [2025/02/08]
Description:
    This module is only intended for Sysplorer cmd window，which cannot call by external entities.
"""