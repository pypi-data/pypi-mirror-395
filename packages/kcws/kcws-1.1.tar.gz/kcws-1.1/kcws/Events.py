# -*- coding: utf-8 -*- 
import os, time, subprocess,psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
class MyFileSystemEventHander(FileSystemEventHandler):
    __eventgtimexz=0
    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if '.py' in event.src_path and event.src_path.endswith('.py'):
            global eventgtimexz
            if time.time()-self.__eventgtimexz > 0.5:
                self.__eventgtimexz=time.time()
                # print('* 更新文件：%s' % event.src_path,event.event_type)
                if event.event_type=='modified':
                    if 'controller\__init__.py' in event.src_path or 'app\__init__.py' in event.src_path:
                        time.sleep(10)
                        pass
                    else:
                        self.restart()
class Events:
    command = ['echo', 'ok']
    process = None
    def __init__(self,argv):
        # print('event1',argv)
        # if ('--server' not in argv and 'python' not in argv[0]) or 'kcws.py' in argv:
        #     print('event2',argv)
        #     argv.insert(0, 'python')
        self.command = argv
        paths = os.path.abspath('.')
        # print(paths)
        self.start_watch(paths)
    
    def kill_process(self):
        "关闭"
        if self.process:
            if 'kcws'==self.command[0] or 'kcwebs'==self.command[0] or 'kcwebps2'==self.command[0]:
                try:
                    process = psutil.Process(self.process.pid)
                except:pass
                else:
                    for proc in process.children(recursive=True):
                        proc.kill()
                        proc.kill()
            else:
                self.process.kill()
                self.process.wait()
            self.process = None
    def start_process(self):
        "启动"
        self.process = subprocess.Popen(self.command)
    def restart_process(self):
        "重启"
        
        self.kill_process()
        time.sleep(0.1)
        self.start_process()

    def start_watch(self,path):
        "执行"
        observer = Observer()
        observer.schedule(MyFileSystemEventHander(self.restart_process), path, recursive=True)
        observer.start()
        self.start_process()
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt as e:
            self.kill_process()
            # observer.stop()
        # observer.join()
    
# Events(['server.py'])  #执行server.py文件