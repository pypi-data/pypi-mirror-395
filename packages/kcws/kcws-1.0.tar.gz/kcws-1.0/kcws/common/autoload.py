# -*- coding: utf-8 -*-
import time,hashlib,json,re,os,sys,platform,shutil,requests,importlib,traceback,pip,tarfile,zipfile,signal,psutil,filetype
from kcws import config
from . import globals
class kcwszip:
    def __clean_filename(filename):
        # 移除或替换非法字符
        filename =re.sub(r'[<>:"/\\|?*]', '', filename)
        filename=filename.replace('\t','')
        # print('filenamefilenamefilenamefilename',filename)
        return filename
    def packzip(src,dst):
        "压缩"
        filelist = []
        if os.path.isfile(src):
            filelist.append(src)
        for root, dirs, files in os.walk(src):
            for name in files:
                filelist.append(os.path.join(root, name))
        zf = zipfile.ZipFile(dst, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(src):]
            zf.write(tar,arcname)
        zf.close()
    def unzip_file(dst, src,all=True):
        "解压"
        if all:
            zf = zipfile.ZipFile(dst)
            zf.extractall(src)
            zf.close()
        else:
            zip_ref=zipfile.ZipFile(dst)
            for item in zip_ref.infolist():
                zip_ref.extract(item, src)
            zip_ref.close()
    def unzip(filename):
        "解压到文件所在目录"
        diswjj=''
        tarr=filename.split('.')
        i=0
        while i<len(tarr)-1:
            if i<=len(tarr)-3:
                diswjj+=tarr[i]+'.'
            else:
                diswjj+=tarr[i]
            i+=1
        # if not os.path.exists(diswjj):
        #     os.makedirs(diswjj,exist_ok=True)
        try:
            zip_ref=zipfile.ZipFile(filename, 'r')
            for item in zip_ref.infolist():
                try:
                    item.filename = item.filename.encode('cp437').decode('gbk')
                except:pass
                try:
                    item.filename = item.filename.replace('\t','').replace('\n','').replace('\b','')
                except:pass
                # print("item.filename",item.filename)
                try:
                    zip_ref.extract(item, diswjj)
                except Exception as e:
                    stre=str(e)
                    if 'Bad CRC-32 for fil' in stre:#文件损坏
                        print('压缩文件文件损坏',stre)
                        pass
                    elif '[Errno 2] No such file or directory: ' in stre:
                        print('不是有效文件',stre)
                        pass
                    else:
                        if os.path.exists(diswjj):
                            try:
                                shutil.rmtree(diswjj)
                            except:pass
                        try:
                            zip_ref.close()
                        except:pass
                        raise Exception(e)
            zip_ref.close()
        except Exception as e:
            stre=str(e)
            print('zip解压异常',stre)
            raise Exception(e)
            # if 'File is not a zip file' in stre or 'Bad CRC-32 for fil' in stre:
            #     if os.path.exists(diswjj):
            #         try:
            #             shutil.rmtree(diswjj)
            #         except:pass
            #     return False
            # else:
            #     if os.path.exists(diswjj):
            #         shutil.rmtree(diswjj)
            #     raise Exception(e)
        #处理中文乱码
        arr=get_file(diswjj,is_folder=False)
        for kkk in arr:
            new_name=kkk['path'].split('/')
            try:
                new_name=kkk['path'].replace(new_name[len(new_name)-1],kkk['name'].encode('cp437').decode("gbk"))
            except:
                # print(kkk['name'],'编码无需要解码')
                pass
            else:
                try:
                    os.rename(kkk['path'], new_name)
                except Exception as e:
                    stre=str(e)
                    if '当文件已存在时，无法创建该文件' in stre:
                        pass
                    else:
                        if os.path.exists(diswjj):
                            shutil.rmtree(diswjj)
                        raise Exception(e)
        return diswjj
class kcwstar:
    def targz(src,dst):
        """
        打包目录为tar.gz
        :param src: 需要打包的目录
        :param dst: 压缩文件名
        :return: bool
        """
        with tarfile.open(dst, "w:gz") as tar:
            tar.add(src, arcname=os.path.basename(src))
        return True
    def untar(dst, src):
        """
        解压tar.gz文件
        :param dst: 压缩文件名
        :param src: 解压后的存放路径
        :return: bool
        """
        try:
            t = tarfile.open(dst)
            t.extractall(path = src)
            return True
        except Exception as e:
            return False

def get_file(folder='./',is_folder=True,suffix="*",lists=[],append=False):
    """获取文件夹下所有文件夹和文件

    folder 要获取的文件夹路径

    is_folder  是否返回列表中包含文件夹

    suffix 获取指定后缀名的文件 默认全部
    """
    if not append:
        lists=[]
    lis=os.listdir(folder)
    for files in lis:
        if os.path.isfile(folder+"/"+files):
            if suffix=='*':
                zd={"type":"file","path":folder+"/"+files,'name':files}
                lists.append(zd)
            else:
                if files[-(len(suffix)+1):]=='.'+str(suffix):
                    zd={"type":"file","path":folder+"/"+files,'name':files}
                    lists.append(zd)
        elif os.path.isdir(folder+"/"+files):
            if is_folder:
                zd={"type":"folder","path":folder+"/"+files,'name':files}
                lists.append(zd)
            get_file(folder+"/"+files,is_folder,suffix,lists,append=True)
        
    return lists
def get_folder():
    '获取kcws框架目录'
    return os.path.split(os.path.realpath(__file__))[0][:-7] #当前框架目录
def times():
    """生成时间戳整数 精确到秒(10位数字)
    
    return int类型
    """
    return int(time.time())
def json_decode(strs):
    """json字符串转python类型"""
    try:
        return json.loads(strs)
    except Exception as e:
        if 'JSON object must be str, bytes or bytearray, not list' in str(e):
            return strs
        return []
def json_encode(strs):
    """python列表或字典转成字符串"""
    try:
        return json.dumps(strs,ensure_ascii=False)
    except Exception:
        return ""
def md5(strs):
    """md5加密
    
    参数 strs：要加密的字符串

    return String类型
    """
    m = hashlib.md5()
    b = strs.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()
def kcws_kill_path_pid(folder):
    """结束指定目录pid
    
    folder 目录
    """
    if os.path.exists(folder):
        lis=os.listdir(folder)
        for files in lis:
            if os.path.isfile(folder+"/"+files):
                f=open(folder+"/"+files,'r')
                pid=f.read()
                f.close()
                kill_pid(pid)
                os.remove(folder+"/"+files)

def kcws_save_folder_pid(folder,pid):
    """通过目录保存进程号(pid)
    
    folder 目录
    """
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    if not pid:
        pid = os.getpid()
    f=open(folder+'/'+str(pid),'w')
    f.write(str(pid))
    f.close()
def get_kcwebs_cli_pid(route):
    """通过路由地址获取进程号
    
    route 路由地址
    """
    if not os.path.isfile(get_folder()+"/pid/"+md5(route)+"_cli_pid"):
        return False
    pid=False
    with open(get_folder()+"/pid/"+md5(route)+"_cli_pid") as file:
        pid = file.read()
    return pid
def get_kcwebs_cli_info(route,types='pid'):
    """通过路由地址获取进程信息
    
    route 路由地址

    types info表示获取进程信息 否则判断进程号是否存在
    """
    pid=get_kcwebs_cli_pid(route)
    if pid:
        pid=int(pid)
        try:
            if types=='info':
                p = psutil.Process(pid)
                data={
                    'pid':pid,
                    'name':p.name(),
                    'cli':p.cmdline(),
                    'cpu':p.cpu_percent(1),
                    'memory':p.memory_info().rss
                }
                return data
            else:
                if psutil.pid_exists(pid):
                    return pid
                else:
                    try:
                        os.remove(get_folder()+"/pid/"+md5(route)+"_cli_pid")
                    except:pass
                    return False
        except:
            return False
    else:
        return False
def kill_pid(pid):
    """通过进程结束进程
    
    pid 进程号
    """
    if pid:
        if 'Linux' in get_sysinfo()['platform']:
            os.system("kill -9 "+str(pid))
        else:
            try:
                os.kill(int(pid), signal.SIGTERM)
            except:pass
def kill_route_cli(route):
    """通过路由结束进程
    
    route 路由地址
    """
    pid=get_kcwebs_cli_pid(route)
    if pid:
        kill_pid(pid)
        try:
            os.remove(get_folder()+"/pid/"+md5(route)+"_cli_pid")
        except:pass
def save_route_cli_pid(route):
    """通过路由保存进程号(pid)
    
    route 路由地址
    """
    pid = os.getpid()
    f=open(get_folder()+"/pid/"+md5(route)+"_cli_pid",'w')
    f.write(str(pid))
    f.close()
def kill_all_pid():
    """结束kcws框架的所有子进程"""
    folder=get_folder()+"/pid"
    kcws_kill_path_pid(folder)
if not os.path.exists(get_folder()+"/pid/"):
    os.makedirs(get_folder()+"/pid/", exist_ok=True)
get_sysinfodesffafew=None
def get_sysinfo():
    """获取系统信息

    return dict类型
    """
    global get_sysinfodesffafew
    if get_sysinfodesffafew:
        sysinfo=get_sysinfodesffafew
    else:
        sysinfo={} 
        sysinfo['platform']=platform.platform()        #获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'  
        sysinfo['version']=platform.version()         #获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
        sysinfo['architecture']=platform.architecture()    #获取操作系统的位数，('32bit', 'ELF')
        sysinfo['machine']=platform.machine()         #计算机类型，'i686'
        sysinfo['node']=platform.node()            #计算机的网络名称，'XF654'
        sysinfo['processor']=platform.processor()       #计算机处理器信息，''i686'
        sysinfo['uname']=platform.uname()           #包含上面所有的信息汇总，('Linux', 'XF654', '3.13.0-46-generic', '#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015', 'i686', 'i686')
        sysinfo['start_time']=times()
        get_sysinfodesffafew=sysinfo
            # 还可以获得计算机中python的一些信息：
            # import platform
            # platform.python_build()
            # platform.python_compiler()
            # platform.python_branch()
            # platform.python_implementation()
            # platform.python_revision()
            # platform.python_version()
            # platform.python_version_tuple()
    return sysinfo
class create:
    project=''
    appname=None
    modular=None
    path=get_folder() #当前框架目录
    def __init__(self,appname="app",modular="api",project=''):
        self.appname=str(appname)
        self.modular=str(modular)
        if project:
            if os.path.exists(project):
                print('项目已存在，请进入'+str(project)+'目录命令执行命令')
                exit()
            if not os.path.exists(self.appname):
                self.project=str(project)+'/'
                os.makedirs(self.project, exist_ok=True)
    def uninstallplug(self,plug):
        """卸载插件

        plug 插件名
        """
        f=open(self.project+self.appname+"/"+self.modular+"/controller/__init__.py","r",encoding='utf-8')
        text=f.read()
        f.close()
        text=re.sub("\nfrom . import "+plug,"",text)
        text=re.sub("from . import "+plug,"",text)
        f=open(self.project+self.appname+"/"+self.modular+"/controller/__init__.py","w",encoding='utf-8')
        f.write(text)
        f.close()
        shutil.rmtree(self.project+self.appname+"/"+self.modular+"/controller/"+plug)
        return True,"成功"
    def packplug(self,plug):
        """打包插件
        
        plug 插件名
        """
        """打包模块"""
        if os.path.exists(self.project+self.appname+"/"+self.modular+"/controller/"+plug):
            kcwszip.packzip(self.project+self.appname+"/"+self.modular+"/controller/"+plug,self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return True,"成功"
        else:
            return False,"失败,插件目录不存在"
    def uploadplug(self,plug,username='',password='',cli=False,relyonlist=[]):
        "上传一个插件"
        if not os.path.isfile(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip"):
            self.packplug(plug=plug)
        i=0
        relyonlist=json_encode(relyonlist)
        while True:
            timestamp=times()
            sign=md5(str(username)+str(timestamp)+md5(md5(password)))
            ress=requests.get(config.domain['kcwebsapi']+"/user/userinfo/?username="+username+"&timestamp="+str(timestamp)+"&sign="+sign)
            arr=json_decode(ress.text)
            if not arr:
                os.remove(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                if config.app['app_debug']:
                    print(ress.text)
                return False,"用户身份验证失败，服务器暂时无法处理"
            if (arr['code']==-1 or arr['code']==2) and cli:
                if i >= 3:
                    os.remove(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                    return False,"用户名或密码错误"
                elif i:
                    print("用户名或密码错误，请重新输入")
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                else:
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                i+=1
            elif arr['code']==0:
                break
            else:
                os.remove(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                return False,arr['msg']
        ress=requests.request(url=config.domain['kcwebsapi']+"/user/uploadplug/?username="+username+"&timestamp="+str(timestamp)+"&sign="+sign,method='POST',
        data={'name':str(plug),'describes':'','modular':self.modular,'relyonlist':relyonlist,'relyon':config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr},
        files={'file':open(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip", 'rb')})
        arr=json_decode(ress.text)
        if not arr:
            os.remove(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            if config.app['app_debug']:
                print(ress.text)
            return False,"上传失败，服务器暂时无法处理上传"
        elif arr['code']==-1 or arr['code']==2:
            os.remove(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return False,"用户名或密码错误"
        elif arr['code']==0:
            os.remove(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return True,arr['msg']
        elif arr['code']==0:
            os.remove(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return False,arr['msg']
        else:
            os.remove(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return False,arr['msg']
    def installplug(self,plug,edition='',token='',cli=False,mandatory=False,username=''):
        """创建一个插件，如果您的模块目录下没有插件包，则创建默认插件文件
        
        plug 插件名
        """
        plug=str(plug)
        if os.path.exists(self.project+self.appname+"/"+self.modular+"/controller/"+plug) and not mandatory:
            return False,"该插件已存在"
        else:
            i=0
            j=0
            tplug=plug
            modular=self.modular
            while True:
                ress=requests.get(config.domain['kcwebsapi']+"/pub/plug",params={"modular":modular,"name":str(tplug),'relyon':config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr,"edition":str(edition),"token":token,'username':username})
                arr=json_decode(ress.text)
                # print(modular,tplug,edition,arr)
                if arr:
                    if arr['code']==-1 and cli:
                        if i >= 3:
                            return False,plug+"插件授权码错误"
                        elif i:
                            token = input("授权码错误，请重新输入授权码，从而获得该插件\n")
                        else:
                            token = input("请输入授权码，从而获得该插件\n")
                        i+=1
                    elif arr['code']==-1:
                        return False,plug+"插件授权码错误"
                    elif arr['code']==-5:
                        return False,plug+","+arr['data']
                    elif arr['code']==0 and not arr['data']:
                        modular="api"
                        tplug="index" #默认插件
                        # print(modular,tplug)
                    elif arr['code']==0 and arr['data']:
                        i=0
                        j+=1
                        arr=arr['data']
                        r=requests.get(arr['dowurl'],verify=False)
                        f = open(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip", "wb")
                        for chunk in r.iter_content(chunk_size=512):
                            if chunk:
                                f.write(chunk)
                        f.close()
                        if zipfile.is_zipfile(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip") and os.path.isfile(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip"):
                            break
                        if j >= 10:
                            return False,str(plug)+"插件下载失败"
                        time.sleep(0.1)
                    else:
                        return False,str(plug)+"插件搜索失败"
                else:
                    return False,self.modular+"模块下找不到"+str(plug)+"插件"
            if os.path.isfile(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip"):#安装打包好的插件
                kcwszip.unzip_file(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip",self.project+self.appname+"/"+self.modular+"/controller/"+plug+"/")
                os.remove(self.project+self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                if os.path.isfile(self.project+self.appname+"/"+self.modular+"/controller/"+plug+"/install.txt"): #安装依赖包
                    install_requires=[]
                    try:
                        f=open(self.project+self.appname+"/"+self.modular+"/controller/"+plug+"/install.txt")
                        while True:
                            line = f.readline()
                            if not line:
                                break
                            elif len(line) > 2:
                                install_requires.append(line)
                        f.close()
                    except:
                        shutil.rmtree(self.project+self.appname+"."+self.modular+"/controller/"+plug)
                        return False,"依赖包错误"
                    if len(install_requires):
                        try:
                            install_requires.insert(0,"install")
                            if 0 != pip.main(install_requires):
                                shutil.rmtree(self.project+self.appname+"/"+self.modular+"/controller/"+plug)
                                return False,"依赖包安装错误"
                        except AttributeError as e:
                            shutil.rmtree(self.project+self.appname+"/"+self.modular+"/controller/"+plug)
                            if config.app['app_debug']:
                                print("建议更新您的pip版本。参考命令：python3 -m pip install --upgrade pip==21.2.4 -i https://mirrors.aliyun.com/pypi/simple/")
                            return False,str(e)
                if os.path.isfile(self.project+self.appname+"."+self.modular+"/controller/"+plug+"/install.py"):
                    try:
                        m=importlib.import_module(self.project+self.appname+"."+self.modular+"/controller/"+plug+".install")
                    except:
                        shutil.rmtree(self.project+self.appname+"."+self.modular+"/controller/"+plug)
                        print(traceback.format_exc())
                        return False,"插件依赖包文件不存在或依赖包文件格式错误"
                    else:
                        try:
                            a=m.install()
                        except:
                            shutil.rmtree(self.project+self.appname+"."+self.modular+"/controller/"+plug)
                            return False,"插件依赖包install函数被破坏"
                        # if not a[0]:
                        #     shutil.rmtree(self.project+self.appname+"."+self.modular+"/controller/"+plug)
                        #     return False,str(a[1])

                f=open(self.project+self.appname+"/"+self.modular+"/controller/__init__.py","r",encoding='utf-8')
                text=f.read()
                f.close()
                text=re.sub("\nfrom . import "+plug,"",text)
                text=re.sub("from . import "+plug,"",text)
                f=open(self.project+self.appname+"/"+self.modular+"/controller/__init__.py","w",encoding='utf-8')
                text+="\nfrom . import "+plug
                f.write(text)
                f.close()

                f=open(self.project+self.appname+"/"+self.modular+"/controller/"+plug+"/common/autoload.py","r",encoding='utf-8')
                text=f.read()
                f.close()
                text=re.sub("app.api",self.appname+"."+self.modular,text)
                f=open(self.project+self.appname+"/"+self.modular+"/controller/"+plug+"/common/autoload.py","w",encoding='utf-8')
                f.write(text)
                f.close()

                
                return True,"插件安装成功，"+plug+"=="+str(arr['edition'])
            else:
                return False,str(plug)+"插件获取失败"
    def uninstallmodular(self):
        "卸载模块"
        f=open(self.project+self.appname+"/__init__.py","r")
        text=f.read()
        f.close()
        text=re.sub("\nfrom . import "+self.modular,"",text)
        text=re.sub("from . import "+self.modular,"",text)
        f=open(self.project+self.appname+"/__init__.py","w")
        f.write(text)
        f.close()
        shutil.rmtree(self.project+self.appname+"/"+self.modular)
        return True,"成功"
    def packmodular(self):
        """打包模块"""
        if self.modular=='index':
            return False,"index为内置模块，因此不能打包"
        if os.path.exists(self.project+self.appname+"/"+self.modular):
            kcwszip.packzip(self.project+self.appname+"/"+self.modular,self.project+self.appname+"/"+self.modular+".zip")
            return True,"成功"
        else:
            return False,"失败，模块目录不存在"
    def uploadmodular(self,username='',password='',cli=False,relyonlist=[]):
        "上传模块"
        if self.modular=='index':
            return False,"index为内置模块，因此不能上传"
        if not os.path.isfile(self.project+self.appname+"/"+self.modular+".zip"):
            self.packmodular()
        i=0
        relyonlist=json_encode(relyonlist)
        while True:
            timestamp=times()
            sign=md5(str(username)+str(timestamp)+md5(md5(password)))
            ress=requests.request(url=config.domain['kcwebsapi']+"/user/uploadmodular/?username="+username+"&timestamp="+str(timestamp)+"&sign="+sign,method='POST',
            data={'name':str(self.modular),'describes':'','relyonlist':relyonlist,'relyon':config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr},
            files={'file':open(self.project+self.appname+"/"+self.modular+".zip", 'rb')})
            arr=json_decode(ress.text)
            if not arr:
                os.remove(self.project+self.appname+"/"+self.modular+".zip")
                if config.app['app_debug']:
                    print(ress.text)
                return False,"用户身份验证失败，服务器暂时无法处理"
            if (arr['code']==-1 or arr['code']==2) and cli:
                if i >= 3:
                    os.remove(self.project+self.appname+"/"+self.modular+".zip")
                    return False,"用户名或密码错误"
                elif i:
                    print("用户名或密码错误，请重新输入")
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                else:
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                i+=1
            elif arr['code']==0:
                break
            elif arr['code']==-1:
                os.remove(self.project+self.appname+"/"+self.modular+".zip")
                return False,"用户名或密码错误"
            else:
                os.remove(self.project+self.appname+"/"+self.modular+".zip")
                return False,arr['msg']
        
        ress=requests.request(url=config.domain['kcwebsapi']+"/user/uploadmodular/?username="+username+"&timestamp="+str(timestamp)+"&sign="+sign,method='POST',
        data={'name':str(self.modular),'describes':'','relyonlist':relyonlist,'relyon':config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr},
        files={'file':open(self.project+self.appname+"/"+self.modular+".zip", 'rb')})
        arr=json_decode(ress.text)
        if not arr:
            os.remove(self.project+self.appname+"/"+self.modular+".zip")
            if config.app['app_debug']:
                print(ress.text)
            return False,"上传失败，服务器暂时无法处理上传"
        elif arr['code']==-1 or arr['code']==2:
            os.remove(self.project+self.appname+"/"+self.modular+".zip")
            return False,"用户名或密码错误"
        elif arr['code']==0:
            os.remove(self.project+self.appname+"/"+self.modular+".zip")
            return True,arr['msg']
        else:
            os.remove(self.project+self.appname+"/"+self.modular+".zip")
            return False,arr['msg']
    def installmodular(self,token='',cli=False):
        "创建模块，如果应用不存，则创建默认应用，如果在您的应用目录下没有模块包，则创建默认模块文件"
        if not os.path.exists(self.project+self.appname):
            if config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=='kcwebps2':
                r=requests.get(config.domain['kcwebsfile']+"/kcwebs/kcwebps2.zip")
                f = open("./"+self.project+"kcwebps2.zip", "wb")
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
                f.close()
                kcwszip.unzip_file("./"+self.project+"kcwebps2.zip","./"+self.project+self.appname)
                os.remove("./"+self.project+"kcwebps2.zip")
            elif config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=='kcwebs':
                r=requests.get(config.domain['kcwebsfile']+"/kcwebs/kcwebs.zip")
                f = open("./"+self.project+"kcwebs.zip", "wb")
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
                f.close()
                kcwszip.unzip_file("./"+self.project+"kcwebs.zip","./"+self.project+self.appname)
                os.remove("./"+self.project+"kcwebs.zip")
            elif config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=='kcws':
                r=requests.get(config.domain['kcwebsfile']+"/kcwebs/kcws.zip")
                f = open("./"+self.project+"kcws.zip", "wb")
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
                f.close()
                kcwszip.unzip_file("./"+self.project+"kcws.zip","./"+self.project+self.appname)
                os.remove("./"+self.project+"kcws.zip")
            else:
                raise Exception('包名错误')
            if not os.path.isfile("./"+self.project+"server.py"):
                # if "Windows" in platform.platform():
                #     pythonname="python"
                # else:
                #     pythonname="python3.8"
                servertext=('#项目运行文件，请务修改\n'+
                        'import kcws,sys,'+self.appname+'\n'+
                        'app=kcws.web(__name__,'+self.appname+')\n'+
                        'if __name__ == "__main__":\n'+
                        '    try:\n'+
                        '        route=sys.argv[1]\n'+
                        '        if "eventlog"==route:\n'+
                        '            raise Exception("")\n'+
                        '    except:\n'+
                        '        #host监听ip port端口 name python解释器名字 (windows一般是python  linux一般是python3) \n'+
                        '        app.run(host="0.0.0.0",port="39001",name="python3.8")\n'+
                        '    else:\n'+
                        '        app.cli(route)\n'
                        )
                f=open("./"+self.project+"server.py","w+",encoding='utf-8')
                f.write(servertext)
                f.close()
            return True,"应用创建成功"
        else:
            if not os.path.isfile(self.project+self.appname+"/__init__.py") or not os.path.exists(self.project+self.appname+"/common"):
                return False,self.appname+"不是kcws应用"
        if self.modular=='index':
            return False,"index为内置模块，因此不能创建"
        if os.path.exists(self.project+self.appname+"/"+self.modular):
            return False,self.project+self.appname+"/"+self.modular+"已存在"
        else:
            i=0
            modular=self.modular
            while True:
                ress=requests.request(url=config.domain['kcwebsapi']+"/pub/modular",method="POST",params={"name":modular,"token":token,'relyon':config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr})
                arr=json_decode(ress.text)
                
                if arr:
                    
                    if arr['code']==-1 and cli:
                        if i >= 3:
                            return False,self.modular+"模块授权码错误"
                        elif i:
                            token = input("授权码错误，请重新输入授权码，从而获得该模块\n")
                        else:
                            token = input("请输入授权码，从而获得该模块\n")
                        i+=1
                    elif arr['code']==-1:
                        return False,self.modular+"模块授权码错误"
                    elif not arr['data']:
                        modular="api"
                    elif arr['code']==0 and arr['data']:
                        arr=arr['data']
                        #循环下载模块
                        i=0
                        while i < 5:
                            r=requests.get(arr['dowurl'])
                            f = open(self.project+self.appname+"/"+self.modular+".zip", "wb")
                            for chunk in r.iter_content(chunk_size=1024*100):
                                if chunk:
                                    f.write(chunk)
                            f.close()
                            time.sleep(0.3)
                            if os.path.isfile(self.project+self.appname+"/"+self.modular+".zip"):
                                break
                            i+=1
                        if os.path.isfile(self.project+self.appname+"/"+self.modular+".zip"):#安装打包好的模块
                            kcwszip.unzip_file(self.project+self.appname+"/"+self.modular+".zip",self.project+self.appname+"/"+self.modular+"/")
                            os.remove(self.project+self.appname+"/"+self.modular+".zip")

                            if os.path.isfile(self.project+self.appname+"/"+self.modular+"/install.txt"): #安装依赖包
                                install_requires=[]
                                try:
                                    f=open(self.project+self.appname+"/"+self.modular+"/install.txt")
                                    while True:
                                        line = f.readline()
                                        if not line:
                                            break
                                        elif len(line) > 3:
                                            install_requires.append(line)
                                    f.close()
                                except:
                                    shutil.rmtree(self.project+self.appname+"/"+self.modular)
                                    return False,"模块依赖包错误"
                                if len(install_requires):
                                    try:
                                        install_requires.insert(0,"install")
                                        if 0 != pip.main(install_requires):
                                            shutil.rmtree(self.project+self.appname+"/"+self.modular)
                                            return False,"模块依赖包安装错误"
                                    except AttributeError as e:
                                        shutil.rmtree(self.project+self.appname+"/"+self.modular)
                                        if config.app['app_debug']:
                                            print("建议更新您的pip版本。参考命令：Python -m pip install --user --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/")
                                        return False,str(e)
                            if os.path.isfile(self.project+self.appname+"/"+self.modular+"/install.py"):#如果存在依赖文件
                                try:
                                    m=importlib.import_module(self.project+self.appname+'.'+self.modular+'.install')
                                except:
                                    shutil.rmtree(self.project+self.appname+"/"+self.modular)
                                    print(traceback.format_exc())
                                    return False,"模块依赖包文件不存在或依赖包文件格式错误"
                                else:
                                    try:
                                        a=m.install()
                                    except:
                                        shutil.rmtree(self.project+self.appname+"/"+self.modular)
                                        return False,"模块依赖包install方法被破坏"
                                    # if not a[0]:
                                    #     shutil.rmtree(self.project+self.appname+"/"+self.modular)
                                    #     return False,str(a[1])
                            content="\nfrom . import "+self.modular
                            f=open(self.project+self.appname+"/__init__.py","a",encoding='utf-8')
                            f.write(content)
                            f.close()

                            content=''
                            f=open(self.project+self.appname+"/"+self.modular+"/common/autoload.py","r",encoding='utf-8')
                            while True:
                                line = f.readline()
                                if not line:
                                    break
                                # elif 'from' not in line and 'import' not in line:
                                #     content+=line
                                elif 'from app.common import *' not in line:
                                    content+=line
                            f.close()
                            f=open(self.project+self.appname+"/"+self.modular+"/common/autoload.py","w",encoding='utf-8')
                            f.write("from "+self.appname+".common import *\n"+content)
                            f.close()
                            if os.path.exists(self.project+self.appname+"/"+self.modular+"/controller/index"):
                                content=''
                                f=open(self.project+self.appname+"/"+self.modular+"/controller/index/common/autoload.py","r",encoding='utf-8')
                                while True:
                                    line = f.readline()
                                    if not line:
                                        break
                                    # elif 'from' not in line and 'import' not in line:
                                    #     content+=line
                                    else:
                                        content+=line
                                f.close()
                                f=open(self.project+self.appname+"/"+self.modular+"/controller/index/common/autoload.py","w",encoding='utf-8')
                                f.write("from "+self.appname+"."+self.modular+".common import *\n"+content)
                                f.close()
                        else:
                            return False,self.modular+"模块下载失败"
                        if not os.path.isfile("./server.py"):
                            if "Windows" in platform.platform():
                                pythonname="python"
                            else:
                                pythonname="python3"
                            # sys.argv[0]=re.sub('.py','',sys.argv[0])
                            servertext=('# -*- coding: utf-8 -*-\n#gunicorn -b 0.0.0.0:39010 '+self.appname+':app\n'+
                                    'from kcws import web\n'+
                                    'import '+self.appname+' as application\n'+
                                    'app=web(__name__,application)\n'+
                                    'if __name__ == "__main__":\n'+
                                    '    #host监听ip port端口 name python解释器名字 (windows一般是python  linux一般是python3)\n'+
                                    '    app.run(host="0.0.0.0",port="39001",name="'+pythonname+'")')
                            f=open("./"+self.project+"server.py","w+",encoding='utf-8')
                            f.write(servertext)
                            f.close()
                        return True,"安装成功"
                    else:
                        
                        return False,"模块下载失败"
                else:
                    return False,"找不到"+self.modular+"模块"