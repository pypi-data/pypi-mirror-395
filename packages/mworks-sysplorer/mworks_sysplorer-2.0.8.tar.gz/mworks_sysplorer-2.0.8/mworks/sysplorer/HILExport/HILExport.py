import inspect
import os
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
from colorama import init, Fore
import multiprocessing
init(autoreset = True)

_num_cores = multiprocessing.cpu_count()
_name = "HILExport"
_MwConnect = MwConnect()

@mw_connect_decorator(_MwConnect._process_path)
def CheckAndSetExportConfig(ModelAbsPath:str, GenerateType:str, StopTime:str='1', StepSize:str='0.001', Algorithm:str='Euler', FMIVersion:str="V2",FMUType: str="CS" ):
    params = inspect.signature(CheckAndSetExportConfig).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CheckAndSetExportConfig, args, {}, expected_types, plugin_mode = _name)
    
@mw_connect_decorator(_MwConnect._process_path)
def CheckAndSetSystem(Platform:str='Linux', Bit:str='x64' ):
    params = inspect.signature(CheckAndSetSystem).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CheckAndSetSystem, args, {}, expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def CheckAndSetParameters(SelectedParams:str=''):
    params = inspect.signature(CheckAndSetParameters).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CheckAndSetParameters, args, {}, expected_types, plugin_mode = _name)
   
@mw_connect_decorator(_MwConnect._process_path)
def CheckAndSetSaveConfig(SavePath:str, CompilerPath:str='',FmuRename:str='',VSTPath:str='',MainPath:str='', ExtraList:str='', NeedBit:bool=False):
    params = inspect.signature(CheckAndSetSaveConfig).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CheckAndSetSaveConfig, args, {}, expected_types, plugin_mode = _name)


@mw_connect_decorator(_MwConnect._process_path)
def RunGenerate():
    params = inspect.signature(RunGenerate).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(RunGenerate, args, {}, expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def RunFMU(ModelAbsPath:str, SavePath:str, Platform:str='Linux', Bit:str='x64', 
    StopTime:str='1',  StepSize:str='0.001', Algorithm:str='Euler', Params:str = '', CompilerPath:str='',
    FmuRename:str='', FMIVersion:str="V2",FMUType: str="CS"):
    params = inspect.signature(RunFMU).parameters        
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(RunFMU, args, {}, expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def RunSCL(ModelAbsPath:str, SavePath:str, Platform:str='Linux', Bit:str='x64',
    StopTime:str='1', StepSize:str='0.001', Algorithm:str='Euler', Params:str = '', MainPath:str='', 
    ExtraList:str='', NeedBit:bool=False):
    params = inspect.signature(RunSCL).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(RunSCL, args, {}, expected_types, plugin_mode = _name)
    
@mw_connect_decorator(_MwConnect._process_path)
def RunRTP(ModelAbsPath:str, SavePath:str, Bit:str='x86',StopTime:str='1', StepSize:str='0.001', Algorithm:str='Euler', 
    VSTPath:str=''):
    params = inspect.signature(RunRTP).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(RunRTP, args, {}, expected_types, plugin_mode = _name)
    

   
    
