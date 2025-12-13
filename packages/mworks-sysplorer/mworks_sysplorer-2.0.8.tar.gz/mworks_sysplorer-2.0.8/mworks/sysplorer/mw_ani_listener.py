import threading
import time

# 单例装饰器
def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper
    
@singleton
class MwAniListener:
    def __init__(self) -> None:
        self.handle = None
        self.userdata = None
        self.vars = None
        self.timer_interval = 0.5
        self.timer = threading.Thread(target = self.GetWatchVarsValues)
        self.stop_event = threading.Event()
        self.flag = 0
        
    def OpenCallback(self):
        if self.flag == 1:
            print('The current state is opened')
            return
        self.timer.start()
        self.flag = 1
        
    def CloseCallback(self):
        if self.flag == 0:
            print('The current state is closed')
            return
        self.stop_event.set()
        self.timer.join()
        self.timer = threading.Thread(target = self.GetWatchVarsValues)
        self.stop_event.clear()
        self.flag = 0
    
    def SetHandle(self, handle, userdata: any = None):
        self.handle = handle
        self.userdata = userdata
        
    def SetWatchVariables(self, vars: list):
        self.vars = vars
        self.vars.insert(0, 'time')

    def GetWatchVarsValues(self):
        while not self.stop_event.is_set():
            time.sleep(self.timer_interval)
            if self.handle == None:
                continue;
            from .sysplorer_api import _GetWatchVarsValues
            last_vars = _GetWatchVarsValues()
            if type(last_vars) != list:
                print("获取结果失败")
                continue;
            if len(last_vars) == 0:
                # 没有数据则跳过
                continue;
            if len(last_vars[0]) == 0:
                # 没有数据则跳过
                continue;
            if (self.handle != None):
                self.handle(self.vars, last_vars, self.userdata)