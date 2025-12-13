from .common import *
import getopt,site
PATH=os.getcwd()
sys.path.append(PATH)
fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1=''
def get_cmd_par(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=''):
    global fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1
    if fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr:
        fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr
    python_version=platform.python_version()
    if python_version[0:3]!='3.8':
        print("\033[1;31;40m "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+"依赖python3.8，与你现在的python"+python_version+"不兼容")
        exit()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["project=","app=","modular=","plug=","user=","pwd=","host=","port=","timeout=","processcount=",
        "install","uninstall","pack","upload","cli"])
        # print("opts",opts)
        # print("args",args)
        server=False
        if 'server' in args:
            server=True
        update=False
        if 'update' in args:
            update=True
        help=False
        if 'help' in args:
            help=True
       
        project=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1  #项目名称
        appname='app'  #应用名 目前是固定值 app
        modular='intapp' #模块名
        plug=''  #插件名
        username=''
        password=''
        host='0.0.0.0'
        port=30000
        if fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1=='kcwebps':
            port=39001
        timeout='600'
        processcount='4'

        install=False
        uninstall=False
        pack=False
        upload=False
        cli=False
        
        if '--cli' in args:
            cli=True
        i=0
        for data in opts:
            if '--project' == data[0]:
                project=data[1]
            # if '--app' == data[0]:
            #     appname=data[1]
            elif '--modular' == data[0]:
                modular=data[1]
            elif '--plug' == data[0]:
                plug=data[1]
            elif '--user' == data[0]:
                username=data[1]
            elif '--pwd' == data[0]:
                password=data[1]
            elif '--host' == data[0]:
                host=data[1]
            elif '--port' == data[0]:
                port=data[1]
            elif '--timeout' == data[0]:
                timeout=data[1]
            elif '--processcount' == data[0]:
                processcount=data[1]
            
            elif '--help' == data[0]:
                help=True
            elif '--install' == data[0]:
                install=True
            elif '--uninstall' == data[0]:
                uninstall=True
            elif '--pack' == data[0]:
                pack=True
            elif '--upload' == data[0]:
                upload=True
            elif '--cli' == data[0]:
                cli=True
            i+=1
    except Exception as e:
        try:
            gcs=sys.argv[1]
        except:
            gcs=''
        if gcs=='-v':
            if fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1=='kcws':
                print(config.kcws['name']+"-"+config.kcws['version']) 
            elif fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1=='kcwebs':
                from kcwebs.config import kcwebs
                print(kcwebs['name']+"-"+kcwebs['version'])
            elif fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1=='kcwebps':
                from kcwebps.config import kcwebps
                print(kcwebps['name']+"-"+kcwebps['version']) 
        else:
            print("\033[1;31;40m有关"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+"命令的详细信息，请键入 "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" help",e)
        return False
    else:
        return {
            'server':server,
            'update':update,
            'project':project,'appname':appname,'modular':modular,'username':username,'password':password,'plug':plug,'host':host,'port':port,'timeout':timeout,'processcount':processcount,
            'help':help,'install':install,'uninstall':uninstall,'pack':pack,'upload':upload,'cli':cli,
            'index':i
        }
def temp_get_file(folder='./',lists=[]):
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if files=='__pycache__' or files=='.git':
                pass
            else:
                lists.append(folder+"/"+files)
                temp_get_file(folder+"/"+files,lists)
        else:
            pass
    return lists
def cllfunction():
    global fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1
    cmd_par=get_cmd_par()
    if not cmd_par:
        exit()
    if cmd_par['help']:
        try:
            cs=sys.argv[2:][0]
        except:
            cs=None
        print("\033[1;31;40m有关某个命令的详细信息，请键入 "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" help 命令名")
        print("\033[36m执行 "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" help server             可查看server相关命令")
        print("\033[36m执行 "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" help modular            可查看赋值相关命令")
        print("\033[36m执行 "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" help install            可查看安装相关命令")
        print("\033[36m执行 "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" help pack               可查看打包相关命令")
        print("\033[36m执行 "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" help upload             可查看上传相关命令")
        print("\033[36m执行 "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" help uninstall          可查看卸载相关命令\n")
        if 'server' == cs:
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --host 0.0.0.0 --port 39001 server     启动web服务")
            print("\033[32mhost、port并不是必须的，如果要使用默认值，您可以使用下面简短的命令来启动服务")
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" server\n")
        if 'modular' == cs:
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular api --plug plug --install    进行安装")
            print("\033[1;31;40m初始化一个web应用示例,通常情况下modular、plug、install同时使用")
            print("\033[32mmodular、plug并不是必须的，如果要使用默认值，您可以使用下面简短的命令来安装")
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" install\n")
        if 'install' == cs:
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --install                                                           安装一个默认的应用")
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular base --install                                  在app应用中安装一个base模块")
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular base --plug plug1 --install                     在app应用base模块中安装一个plug1插件")
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular intapp --plug plug1 --user 181*** --install     在app应用intapp模块中安装一个指定用户的plug1插件")
            # print("\033[32m如果您需要新建一个项目 可以使用以下命令")
            # print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --project projectname --modular intapp --plug plug1 --user 181*** --install     在projectname项目下的app应用下intapp模块中安装一个指定用户的plug1插件\n")
        if 'pack' == cs:
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular api --pack                打包一个模块")
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular api --plug plug1 --pack   可以打包一个插件\n")
        if 'upload' == cs:
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular intapp --user 181*** --pwd pwd123 --upload                上传一个intapp模块")
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular intapp --plug plug1 --user 181*** --pwd pwd123 --upload   向intapp模块中上传一个plug1插件")
            print("\033[1;31;40m注意：181*** 和 pwd123 是您的用户或密码")
        if 'uninstall' == cs:
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular api --uninstall                  卸载app/api模块")
            print("\033[32m"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --modular api --plug plug1 --uninstall     卸载app/api/plug1插件\n")
    else:
        if cmd_par['cli']:#通过命令行执行控制器的方法
            try:
                obj=importlib.import_module(cmd_par['appname']+'.common')
                if obj.config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr!=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1:
                    print("该项目只能使用"+obj.config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr+"开头的命令!")
                    exit()
            except Exception as e:
                print('项目不合法',traceback.format_exc())
                exit()
            config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1
            from kcws import web
            try:
                import app as application
            except Exception as e:
                if "No module named 'app'" in str(e):
                    print("请在"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+"项目下运行")
                else:
                    print(traceback.format_exc())
                exit()
            else:
                app=web(__name__,application)
                try:
                    RAW_URI=sys.argv[1]
                except:pass
                else:
                    if RAW_URI=='--cli':
                        RAW_URI=''
                    app.cli(RAW_URI)
        elif cmd_par['update']:#更新kcws包:
            # print(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1)
            # exit()
            serall=['kcws','kcwebs','kcwebps']
            if fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1 not in serall:
                print('不支持该命令')
                exit()
            for bs in serall:
                if 'kcws'==bs:
                    response=requests.get("https://gitee.com/open_source_official_website/kcws/raw/master/kcws.zip")
                elif 'kcwebs'==bs:
                    response=requests.get("https://gitee.com/open_source_official_website/kcwebs/raw/develop/kcwebs.zip")
                elif 'kcwebps'==bs:
                    response=requests.get("https://gitee.com/open_source_official_website/kcwebps/raw/develop/kcwebps.zip")
                f=open(bs+'.zip',"wb")
                f.write(response.content)
                f.close()
                kcwszip.unzip_file(bs+'.zip','')
                os.remove(bs+'.zip')
                if os.name == 'nt': #windows
                    os.system("pip uninstall "+bs+" -y")
                    os.system("python setup.py sdist install")
                    try:
                        shutil.rmtree('__pycache__')
                    except:pass
                    shutil.rmtree('build')
                    shutil.rmtree('dist')
                    shutil.rmtree(bs)
                    shutil.rmtree(bs+'.egg-info')
                    os.remove('setup.py')
                elif os.name == 'posix': #linux
                    os.system("pip3.8 uninstall "+bs+" -y")
                    os.system("python3.8 setup.py sdist install")
                    try:
                        shutil.rmtree('__pycache__')
                    except:pass
                    shutil.rmtree('build')
                    shutil.rmtree('dist')
                    shutil.rmtree(bs)
                    shutil.rmtree(bs+'.egg-info')
                    os.remove('setup.py')
                    # os.system("pip3 uninstall "+bs+" -y")
                    # sys.argv=['setup.py', 'sdist', 'install']
                    # import setup
                    # importlib.reload(setup)
                    # setup.start()

                    # try:
                    #     shutil.rmtree('__pycache__')
                    # except:pass
                    # shutil.rmtree('build')
                    # shutil.rmtree('dist')
                    # shutil.rmtree(bs)
                    # shutil.rmtree(bs+'.egg-info')
                    # os.remove('setup.py')
                else:
                    print("该操作系统不支持更新"+bs)
                if bs==fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1:
                    break
        elif cmd_par['server']:#启动web服务
            
            try:
                obj=importlib.import_module(cmd_par['appname']+'.common')
                if obj.config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr!=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1:
                    print("该项目只能使用"+obj.config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr+"开头的命令.")
                    exit()
            except Exception as e:
                print('项目不合法',traceback.format_exc())
                exit()
            config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1
            types=sys.argv[len(sys.argv)-1]
            if get_sysinfo()['uname'][0]=='Linux':
                pythonpath=site.getsitepackages()[0].replace('\\','/')
                t=pythonpath.split('/')
                tt='/'+t[-3]+'/'+t[-2]+'/'+t[-1]
                pythonpath=pythonpath.replace(tt,'')
                if not os.path.exists('/usr/bin/'+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1) and os.path.isfile(pythonpath+'/bin/'+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1):
                    os.system("ln -s "+pythonpath+"/bin/"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" /usr/bin/"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1)
                # if types=='-stop' or types=='-start':
                #     pass
                # else:
                #     print("启动参数错误，支持 -start和-stop")
                #     exit()
                # try:
                #     f=open("pid",'r')
                #     pid=f.read()
                #     f.close()
                #     if pid:
                #         os.system("kill "+pid)
                # except:pass
                if __name__ == 'kcws.kcws':
                    kill_route_cli('pid/'+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+'_server_pid')
                    if types=='-stop':
                        pass
                    else:
                        save_route_cli_pid('pid/'+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+'_server_pid')
                        from gunicorn.app.wsgiapp import run
                        sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$','',sys.argv[0])
                        sys.argv=[sys.argv[0], '-w', str(cmd_par['processcount']), '-b', cmd_par['host']+':'+str(cmd_par['port']),'-t',cmd_par['timeout'], 'server:'+cmd_par['appname']]
                        sys.exit(run())
                        exit()
            else:
                from kcws import web
                try:
                    import app as application
                except Exception as e:
                    if "No module named 'app'" in str(e):
                        print("请在"+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+"项目下运行")
                    else:
                        print(traceback.format_exc())
                    exit()
                else:
                    app=web(__name__,application)
                    if __name__ == 'kcws.kcws':
                        tar=len(sys.argv)
                        kill_route_cli('pid/'+str(sys.argv[tar-1])+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+'_server_pid')
                        if types=='-stop':
                            pass
                        else:
                            save_route_cli_pid('pid/'+str(sys.argv[tar-1])+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+'_server_pid')
                            app.run(host=cmd_par['host'],port=int(cmd_par['port']))
        else:
            if cmd_par['install']:#插入 应用、模块、插件
                if cmd_par['appname'] and cmd_par['modular']:
                    if os.path.exists(cmd_par['appname']):
                        try:
                            obj=importlib.import_module(cmd_par['appname']+'.common')
                            if obj.config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr!=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1:
                                print("该项目只能使用"+obj.config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr+"开头的命令。")
                                exit()
                        except Exception as e:
                            print('项目不合法',traceback.format_exc())
                            exit()
                    config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1
                    server=create(cmd_par['appname'],cmd_par['modular'],project=cmd_par['project'])
                    t=server.installmodular(cli=True)
                    if cmd_par['plug']:
                        t=server.installplug(cmd_par['plug'],cli=True,username=cmd_par['username'])
                        print(t)
                    else:
                        if '应用创建成功' in t[1]:
                            print("创建应用成功，接下来进入入项目目录 在终端中执行："+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" server 运行项目")
                        else:
                            print(t)
                    return t
                else:
                    print("\033[1;31;40m安装时 必须指定应该app和modular，参考命令： "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --app app --modular api")
                    exit()
            if cmd_par['pack']:#打包 模块、插件
                config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1
                if cmd_par['appname'] and cmd_par['modular']:
                    server=create(cmd_par['appname'],cmd_par['modular'],project=cmd_par['project'])
                    if cmd_par['plug']:
                        res=server.packplug(plug=cmd_par['plug'])
                    else:
                        res=server.packmodular()
                    print(res)
                    if not res[0]:
                        exit()
                else:
                    print("\033[1;31;40m打包时 必须指定应该app和modular，参考命令： "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --app app --modular api")
                    exit()
            if cmd_par['upload']:#上传 模块、插件
                if cmd_par['appname'] and cmd_par['modular']:
                    try:
                        obj=importlib.import_module(cmd_par['appname']+'.common')
                        if obj.config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr!=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1:
                            print("该项目只能使用"+obj.config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr+"开头的命令")
                            exit()
                    except Exception as e:
                        print('项目不合法',traceback.format_exc())
                        exit()
                    config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1
                    server=create(cmd_par['appname'],cmd_par['modular'],project=cmd_par['project'])
                    if cmd_par['plug']:
                        res=server.packplug(plug=cmd_par['plug'])
                        if res[0]:
                            res=server.uploadplug(cmd_par['plug'],cmd_par['username'],cmd_par['password'],cli=True)
                        else:
                            print(res)
                            exit()
                    else:
                        res=server.packmodular()
                        if res[0]:
                            res=server.uploadmodular(cmd_par['username'],cmd_par['password'],cli=True)
                        else:
                            print(res)
                            exit()
                    print(res)
                    if not res[0]:
                        exit()
                else:
                    print("\033[1;31;40m上传时 必须指定应该app和modular，参考命令： "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --app app --modular api")
                    exit()
            if cmd_par['uninstall']:#卸载 模块、插件
                config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1
                if cmd_par['appname'] and cmd_par['modular']:
                    server=create(cmd_par['appname'],cmd_par['modular'],project=cmd_par['project'])
                    if cmd_par['plug']:
                        res=server.uninstallplug(plug=cmd_par['plug'])
                    else:
                        res=server.uninstallmodular()
                    print(res)
                    if not res[0]:
                        exit()
                else:
                    print("\033[1;31;40m卸载时 必须指定应该app和modular，参考命令： "+fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1+" --app app --modular api")
                    exit()
def cill_start(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr='kcws'):
    "脚本入口"
    global fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1
    fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr1=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr
    return cllfunction()