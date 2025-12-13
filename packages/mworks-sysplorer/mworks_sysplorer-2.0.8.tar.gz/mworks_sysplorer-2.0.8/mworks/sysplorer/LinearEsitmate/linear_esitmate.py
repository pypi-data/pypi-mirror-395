import inspect
import os
from colorama import init, Fore
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
init(autoreset = True)

_name = "LinearEsitmate"
_MwConnect = MwConnect()

@mw_connect_decorator(_MwConnect._process_path)
def GenerateLinearEsitmateModel(modelName: str, modelType = 0):
    if type(modelType) == int or type(modelType) == float:
        modelType = int(modelType)
    else:
        return False
    params = inspect.signature(GenerateLinearEsitmateModel).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('modelType')] = type(modelType)
    return _MwConnect.__RunCurrentFunction__(GenerateLinearEsitmateModel, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetSineStream(modelName: str, isLog: bool = True, sineBegin = 0.1, sineEnd = 100.0, sineNum: int = 30, sineName: str = "in_sine1", sineStatePoint = 0, sineUnits: str = "rad/s"):
    if type(sineBegin) == int or type(sineBegin) == float:
        sineBegin = float(sineBegin)
    else:
        return False
    if type(sineEnd) == int or type(sineEnd) == float:
        sineEnd = float(sineEnd)
    else:
        return False
    if type(sineStatePoint) == int or type(sineStatePoint) == float:
        sineStatePoint = str(sineStatePoint)
    else:
        return False
    params = inspect.signature(SetSineStream).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('sineBegin')] = type(sineBegin)
    expected_types[list(params.keys()).index('sineEnd')] = type(sineEnd)
    expected_types[list(params.keys()).index('sineStatePoint')] = type(sineStatePoint)
    return _MwConnect.__RunCurrentFunction__(SetSineStream, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def ChangeSineStream(modelName: str, sineNum: int = 0, sineAmplitude = 1, sinePeriodNum: int = 4, sineSettingPeriod: int = 1, sineRampPeriod: int = 0, sineSampleNum: int = 40):
    if type(sineAmplitude) == int or type(sineAmplitude) == float:
        sineAmplitude = float(sineAmplitude)
    else:
        return False
    params = inspect.signature(ChangeSineStream).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('sineAmplitude')] = type(sineAmplitude)
    return _MwConnect.__RunCurrentFunction__(ChangeSineStream, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def Estimate(modelName: str):
    params = inspect.signature(Estimate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(Estimate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def ExportLinearEsitmateResult(modelName: str, modelType, path: str, opTime = 0.0, isSaveInCsv: bool = False):
    if type(modelType) == int or type(modelType) == float:
        modelType = int(modelType)
    else:
        return False
    if type(opTime) == int or type(opTime) == float:
        opTime = float(opTime)
    else:
        return False
    params = inspect.signature(ExportLinearEsitmateResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('modelType')] = type(modelType)
    expected_types[list(params.keys()).index('opTime')] = type(opTime)
    return _MwConnect.__RunCurrentFunction__(ExportLinearEsitmateResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetOpTime(modelName: str, opTimeStr: str):
    params = inspect.signature(SetOpTime).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(SetOpTime, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def LinearizePrepare(modelName: str):
    params = inspect.signature(LinearizePrepare).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(LinearizePrepare, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def LinearizeRun(modelName: str):
    params = inspect.signature(LinearizeRun).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(LinearizeRun, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetEstimateResult(modelName: str):
    params = inspect.signature(GetEstimateResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEstimateResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetLinearResult(modelName: str, opTime = 0.0, controlType: str = "ss"):
    if type(opTime) == int or type(opTime) == float:
        opTime = float(opTime)
    else:
        return False
    params = inspect.signature(GetLinearResult).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('opTime')] = type(opTime)
    return _MwConnect.__RunCurrentFunction__(GetLinearResult, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetStateInputOutputVarName(modelName: str, opTime = 0.0, varType = 0):
    if type(opTime) == int or type(opTime) == float:
        opTime = float(opTime)
    else:
        return False
    if type(varType) == int or type(varType) == float:
        varType = int(varType)
    else:
        return False
    params = inspect.signature(GetStateInputOutputVarName).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('opTime')] = type(opTime)
    expected_types[list(params.keys()).index('varType')] = type(varType)
    return _MwConnect.__RunCurrentFunction__(GetStateInputOutputVarName, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetStateInputOutputVarValue(modelName: str, varType = 0):
    if type(varType) == int or type(varType) == float:
        varType = int(varType)
    else:
        return False
    params = inspect.signature(GetStateInputOutputVarValue).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('varType')] = type(varType)
    return _MwConnect.__RunCurrentFunction__(GetStateInputOutputVarValue, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetParamInitialValue(modelName: str, varName: str, varType = 0):
    if type(varType) == int or type(varType) == float:
        varType = int(varType)
    else:
        return False
    params = inspect.signature(GetParamInitialValue).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('varType')] = type(varType)
    return _MwConnect.__RunCurrentFunction__(GetParamInitialValue, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetParamInitialValue(modelName: str, varName: str, varType = 0, varValue = 0):
    if type(varType) == int or type(varType) == float:
        varType = int(varType)
    else:
        return False
    if type(varValue) == int or type(varValue) == float:
        varValue = float(varValue)
    else:
        return False
    params = inspect.signature(SetParamInitialValue).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('varType')] = type(varType)
    expected_types[list(params.keys()).index('varValue')] = type(varValue)
    return _MwConnect.__RunCurrentFunction__(SetParamInitialValue, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetStateInputOutputIndex(modelName: str, varName: str, varType = 0):
    if type(varType) == int or type(varType) == float:
        varType = int(varType)
    else:
        return False
    params = inspect.signature(GetStateInputOutputIndex).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('varType')] = type(varType)
    return _MwConnect.__RunCurrentFunction__(GetStateInputOutputIndex, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetModelPath(modelName: str):
    params = inspect.signature(GetModelPath).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetModelPath, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetModelParamValue(modelName: str, varName: str):
    params = inspect.signature(GetModelParamValue).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetModelParamValue, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def SetModelParamValue(modelName: str, varName: str, varValue = 0):
    if type(varValue) == int or type(varValue) == float:
        varValue = float(varValue)
    else:
        return False
    params = inspect.signature(SetModelParamValue).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('varValue')] = type(varValue)
    return _MwConnect.__RunCurrentFunction__(SetModelParamValue, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def UpdateModelParamValue(modelName: str):
    params = inspect.signature(UpdateModelParamValue).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(UpdateModelParamValue, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetModelLinearizationPosition(modelName: str):
    params = inspect.signature(GetModelLinearizationPosition).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetModelLinearizationPosition, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetLinearModelOpTimeStr(modelName: str):
    params = inspect.signature(GetLinearModelOpTimeStr).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetLinearModelOpTimeStr, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def AddLinearModelStateInputOutputVarName(modelName: str, varName: str, varType = 2):
    if type(varType) == int or type(varType) == float:
        varType = int(varType)
    else:
        return False
    params = inspect.signature(AddLinearModelStateInputOutputVarName).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('varType')] = type(varType)
    return _MwConnect.__RunCurrentFunction__(AddLinearModelStateInputOutputVarName, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def AddLinearModelStateInputOutputVarValue(modelName: str, varName: str, varType = 2, varValue = 0.0):
    if type(varType) == int or type(varType) == float:
        varType = int(varType)
    else:
        return False
    if type(varValue) == int or type(varValue) == float:
        varValue = float(varValue)
    else:
        return False
    params = inspect.signature(AddLinearModelStateInputOutputVarValue).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('varType')] = type(varType)
    expected_types[list(params.keys()).index('varValue')] = type(varValue)
    return _MwConnect.__RunCurrentFunction__(AddLinearModelStateInputOutputVarValue, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def ClearAll():
    params = inspect.signature(ClearAll).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ClearAll, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def AddOpTime(modelName:str, opTime = 0):
    if type(opTime) == int or type(opTime) == float:
        opTime = float(opTime)
    else:
        return False
    params = inspect.signature(AddOpTime).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('opTime')] = type(opTime)
    return _MwConnect.__RunCurrentFunction__(AddOpTime, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def RemoveOpTime(modelName:str, opTime = 0):
    if type(opTime) == int or type(opTime) == float:
        opTime = float(opTime)
    else:
        return False
    params = inspect.signature(RemoveOpTime).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('opTime')] = type(opTime)
    return _MwConnect.__RunCurrentFunction__(RemoveOpTime, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def RemoveAllOpTimes(modelName:str):
    params = inspect.signature(RemoveAllOpTimes).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(RemoveAllOpTimes, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetLinEstComponents(modelName:str):
    params = inspect.signature(GetLinEstComponents).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetLinEstComponents, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetLinearSsModel(modelName:str, opTime = 0):
    if type(opTime) == int or type(opTime) == float:
        opTime = float(opTime)
    else:
        return False
    params = inspect.signature(GetLinearSsModel).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('opTime')] = type(opTime)
    return _MwConnect.__RunCurrentFunction__(GetLinearSsModel, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def GetEstimateFrequencyValue(modelName:str):
    params = inspect.signature(GetEstimateFrequencyValue).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEstimateFrequencyValue, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def StartEstimate(modelName: str):
    params = inspect.signature(StartEstimate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(StartEstimate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def WaitEstimateFinished(modelName: str):
    params = inspect.signature(WaitEstimateFinished).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(WaitEstimateFinished, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

def GetLinearEsitmateCurrentSimTime():
    params = inspect.signature(GetLinearEsitmateCurrentSimTime).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetLinearEsitmateCurrentSimTime, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

def GetLinearEsitmateSimulationState():
    params = inspect.signature(GetLinearEsitmateSimulationState).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetLinearEsitmateSimulationState, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

def PauseLinearEsitmateSimulate():
    params = inspect.signature(PauseLinearEsitmateSimulate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(PauseLinearEsitmateSimulate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

def ResumeLinearEsitmateSimulate():
    params = inspect.signature(ResumeLinearEsitmateSimulate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ResumeLinearEsitmateSimulate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

def StopLinearEsitmateSimulate():
    params = inspect.signature(StopLinearEsitmateSimulate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(StopLinearEsitmateSimulate, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

def GetLinearEsitmateSimulationExitState():
    params = inspect.signature(GetLinearEsitmateSimulationExitState).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetLinearEsitmateSimulationExitState, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)

def GetEstimateFinishTime(modelName: str):
    params = inspect.signature(GetEstimateFinishTime).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(GetEstimateFinishTime, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)
    
def AddFrequency(modelName: str, isLog: bool = True, sineBegin = 0.1, sineEnd = 100.0, sineNum: int = 30):
    if type(sineBegin) == int or type(sineBegin) == float:
        sineBegin = float(sineBegin)
    else:
        return False
    if type(sineEnd) == int or type(sineEnd) == float:
        sineEnd = float(sineEnd)
    else:
        return False
    params = inspect.signature(AddFrequency).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    expected_types[list(params.keys()).index('sineBegin')] = type(sineBegin)
    expected_types[list(params.keys()).index('sineEnd')] = type(sineEnd)
    return _MwConnect.__RunCurrentFunction__(AddFrequency, args=args, kwargs={}, expected_types = expected_types, plugin_mode = _name)
    
__all__ = [name for name in globals() if not name.startswith('_')]