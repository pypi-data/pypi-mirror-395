import inspect
import os
from mworks.sysplorer.Utils import MwConnect, mw_connect_decorator
from colorama import init, Fore
import multiprocessing
init(autoreset = True)

_num_cores = multiprocessing.cpu_count()
_name = "SimulinkImporter"
_MwConnect = MwConnect()

@mw_connect_decorator(_MwConnect._process_path)
def OpenSimulinkImporter()->bool:
    """ 
    启动SimulinkImporter
     """
    params = inspect.signature(OpenSimulinkImporter).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(OpenSimulinkImporter, args, {}, expected_types, plugin_mode = _name)
    
@mw_connect_decorator(_MwConnect._process_path)
def CloseSimulinkImporter()->bool:
    """ 
    关闭SimulinkImporter
     """
    params = inspect.signature(CloseSimulinkImporter).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(CloseSimulinkImporter, args, {}, expected_types, plugin_mode = _name)

@mw_connect_decorator(_MwConnect._process_path)
def ImportSimulinkModel(SimulinkFilePath:str, ExportPath:str='', LibraryPath:str='', DataFilePath:str='', ClearBaseWorkSpace:bool=True, OpenReport:bool=True)->bool:
    """ 
    进行Simulink模型导入

    输入参数：
        SimulinkFilePath    导入的Simulink模型（.slx文件）的完整路径
        ExportPath          生成Sysblock模型位置，默认为空，为空时使用MWORKS.Sysplorer的工作路径
        LibraryPath         模型中所有Link子系统链接的模型库（.slx）所在文件夹，默认为空（不导入Link子系统）。模型库位于多个文件夹时，相互之间用分号(";")隔开
        DataFilePath        Simulink模型的数据文件（.slxdata文件）的完整路径，默认为空（不导入数据）
        ClearBaseWorkSpace  导入前是否清空基础工作区，默认为true
        OpenReport          导入后是否自动打开生成的报告文件，默认为true
     """
    params = inspect.signature(ImportSimulinkModel).parameters
    args = tuple(v for k, v in locals().items() if k not in ('self', 'params'))
    expected_types = [v.annotation for k, v in params.items() if k != 'self']
    return _MwConnect.__RunCurrentFunction__(ImportSimulinkModel, args, {}, expected_types, plugin_mode = _name)