# -*- coding: utf-8 -*-
import threading,urllib,cgi
from . common import *
from . import config
from datetime import datetime
class web:
    __name=None
    __appname=None
    __config=config 
    __httpd=None
    def __new__(self,name,appname=None):
        self.__name=name
        self.__appname=appname
        if self.__name == '__main__' or self.__name=='kcws.kcws' or self.__name=='kcwebs.kcwebs' or self.__name=='kcwebps.kcwebps':
            # print("web__new__",self.__name)
            return super().__new__(self)
        else:
            def apps(env, start_response):
                p=(config.app['staticpath']+env['RAW_URI'].replace(' ',''))
                status='200 ok'
                if os.path.isfile(p):
                    resheader=[("Cache-Control","public, max-age=2592000"),]
                    ETag=md5(p)
                    try:
                        HTTP_IF_NONE_MATCH=env['HTTP_IF_NONE_MATCH']
                    except KeyError:
                        HTTP_IF_NONE_MATCH=None
                    if HTTP_IF_NONE_MATCH:
                        status="304 Not Modified"
                        body=''
                    else:
                        kind = filetype.guess(p)
                        if kind is None:
                            f=open(p,"rb")
                            body=f.read()
                            f.close()
                        else:
                            f=open(p,"rb")
                            body=f.read()
                            f.close()
                            resheader=[
                                ("Content-Type",kind.mime),
                                ("Cache-Control","public, max-age=43200"),
                                ("Accept-Ranges","bytes"),
                            ]
                            resheader.append(('Content-Type',kind.mime))
                            resheader.append(("Accept-Ranges","bytes"))
                    dateArray = datetime.fromtimestamp(int(time.time())-86400)
                    otherStyleTime = dateArray.strftime('%a, %d %b %Y %H:%M:%S GMT')
                    resheader.append(("Last-Modified",otherStyleTime))
                    resheader.append(("ETag",ETag))
                else:
                    files=None
                    try:
                        CONTENT_TYPE=env['CONTENT_TYPE']
                    except:
                        pass
                    else:
                        if 'multipart/form-data; boundary' in CONTENT_TYPE:#上传文件
                            files = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
                        else:
                            files=None
                    env['files']=files
                    try:
                        env['BODY_DATA']=str(env['wsgi.input'].next(), encoding = "utf-8")
                    except:
                        env['BODY_DATA']=""
                    try:
                        env['HTTP_X_REAL_IP']=env['HTTP_X_REAL_IP']
                    except:
                        env['HTTP_X_REAL_IP']=""
                    try:
                        env['url_scheme']=env['HTTP_X_REAL_IP']
                    except:
                        env['url_scheme']=env['wsgi.url_scheme'],
                    status,resheader,body=self.__routes(self,env)
                    if type(body) is bytes:
                        pass
                    else:
                        body=bytes(body, encoding='utf-8')
                # print(env)
                start_response(status,resheader)
                return [body]
            return apps
    # __host=''
    # __port=''
    # __filename=''
    def run(self,host="127.0.0.1",port="39001",name=None):
        """运行开发环境

        host: 监听地址
        
        port: 端口

        name: python命令行解释机名字 (该参数即将废弃)
        """
        # self.__host=host
        # self.__port=port
        
        cmd=sys.argv
        config.app['cli']=False
        if 'eventlog' in cmd or len(cmd)==1 or (len(cmd)>=2 and cmd[len(cmd)-1]=='server'):
            # config.app['cli']=False
            if 'kcwebps' in cmd[0]: #基于新版本4.13.32之后 kcwebps server运行
                cmd[0]='kcwebps'
                filename=cmd[0]
            elif 'kcwebs' in cmd[0]: #基于新版本4.13.32之后 kcwebs server运行
                cmd[0]='kcwebs'
                filename=cmd[0]
            elif 'kcws' in cmd[0]:
                cmd[0]='kcws'
                filename=cmd[0]
            else: #基于老版本4.13.32之前 python server.py运行
                filename=cmd[0][:-3]
            # self.__filename=filename
            if self.__config.app['app_debug']:
                if 'eventlog' in cmd:
                    self.__impl(host=host,port=port,filename=filename)
                else:
                    if name:
                        cmd.insert(0,name)
                    cmd.append('eventlog')
                    from . Events import Events
                    Events(cmd)
            else:
                self.__impl(host=host,port=port,filename=filename)
        elif len(sys.argv)==3 and sys.argv[2]=='--cli':
            try:
                RAW_URI=sys.argv[1]
            except:pass
            else:
                self.cli(RAW_URI)
    def cli(self,RAW_URI):
        config.app['cli']=True
        if RAW_URI:
            PATH_INFO=RAW_URI.split("?")[0] #/aa/bb/cc
            if PATH_INFO[0]=='/':
                PATH_INFO=PATH_INFO[1:]
        else:
            PATH_INFO=RAW_URI
        clipidpath=get_folder()+"/pid/"+md5(RAW_URI)+"_cli_pid"
        pid=''
        if(config.app['save_cli_pid']):
            kill_route_cli(RAW_URI)
            save_route_cli_pid(RAW_URI)
        QUERY_STRING=RAW_URI.replace(str(PATH_INFO),'').replace('?','') #a=1&b=1
        reqheader={ 
            'REQUEST_METHOD':'GET',
            'RAW_URI':RAW_URI,
            'PATH_INFO':PATH_INFO,
            'QUERY_STRING':QUERY_STRING,
            'SERVER_PROTOCOL':'',
            'HTTP_HOST':'',
            'HTTP_COOKIE':'',
            'REMOTE_ADDR':'',
            'HTTP_X_REAL_IP':'',
            'HTTP_USER_AGENT':'',
            'BODY_DATA':''
        }
        status,resheader,body=self.__routes(reqheader)
        print(body)
        if(config.app['save_cli_pid']) and pid:

            try:
                os.remove(clipidpath)
            except:pass
    def __impl(self,host,port,filename):
        "运行测试服务器"
        try:
            # if config.app['http_server']=='wsgiref':
            #     self.__http_wsgi( 
            #         host=host,
            #         port=port,
            #         filename=filename
            #     )
            # elif config.app['http_server']=='kcwebs':
            #     self.__http_sever(
            #         host=host,
            #         port=port,
            #         filename=filename
            #     )
            # elif config.app['http_server']=='kcwebs_server':
            #     self.__http_server(
            #         host=host,
            #         port=port,
            #         filename=filename
            #     )
            # else:
            #     self.__http_wsgi(
            #         host=host,
            #         port=port,
            #         filename=filename
            #     )
            self.__http_wsgi(
                host=host,
                port=port,
                filename=filename
            )
        except KeyboardInterrupt:
            pass
    
    def __getconfigroute(self,PATH_INFO,header):
        "使用配置路由"
        route=self.__config.route
        routedefault=route['default']
        methods=route['methods']
        paths=''
        for path in PATH_INFO:
            paths+="/"+path
        try:
            for item in route['children']:
                if ':' in item['path']:
                    path=item['path'].split(':')
                    if(len(path)==len(PATH_INFO)):
                        is_pp=False
                        try:
                            item['methods']
                        except:pass
                        else:
                            methods=item['methods']
                        for k in methods: #匹配请求方式
                            if header['REQUEST_METHOD'] in k:
                                is_pp=True
                                break
                        if path[0]==paths[:len(path[0])] and is_pp:
                            del PATH_INFO[0]
                            cs=PATH_INFO
                            PATH_INFO=item['component'].split('/')
                            for v in cs:
                                PATH_INFO.append(v)
                            routedefault=True
                            break
                elif item['path']==paths or item['path']+'/'==paths:
                    PATH_INFO=item['component'].split('/')
                    routedefault=True
                    break
        except:pass
        return routedefault,PATH_INFO
    def __get_modular(self,header):
        "获取模块"
        modular=''
        route=self.__config.route
        if route['modular']:
            if isinstance(route['modular'],str):
                modular=route['modular']
            else:
                HTTP_HOST=header['HTTP_HOST'].split(".")[0]
                for mk in route['modular']:
                    if HTTP_HOST in mk:
                        modular=mk[HTTP_HOST]            
        return modular
    def __get_plug(self,header):
        "获取插件"
        plug=''
        route=self.__config.route
        globals.VAR.defplug=''
        if route['plug']:
            if isinstance(route['plug'],str):
                plug=route['plug']
            else:
                HTTP_HOST=header['HTTP_HOST'].split(".")[0]
                for mk in route['plug']:
                    if HTTP_HOST in mk:
                        plug=mk[HTTP_HOST]
        
        return plug
    def defaultroute(self,header,PATH_INFO):
        "路由匹配"
        globals.VAR.defmodular=''
        globals.VAR.defplug=''
        route=self.__config.route
        modular=web.__get_modular(self,header)
        if route['plug']:
            getplug=web.__get_plug(self,header)
        else:
            getplug=''
        routedefault=route['default']
        methods=route['methods']
        plug=''
        if routedefault:
            files=route['files']
            funct=route['funct']
        else:
            files=''
            funct=''
        param=[]
        urls=''
        i=0
        if modular:
            # if route['plug']:  #匹配模块并且匹配了插件
            #     plug=route['plug']
            if getplug:
                plug=getplug
                routedefault,PATH_INFO=web.__getconfigroute(
                    self,
                    PATH_INFO,
                    header
                )
                if routedefault: #使用路由
                    for path in PATH_INFO:
                        if path:
                            if i==0:
                                files=path
                                urls=urls+"/"+str(path)
                            elif i==1:
                                funct=path
                                urls=urls+"/"+str(path)
                            else:
                                param.append(urllib.parse.unquote(path))
                        i+=1
            else:                  #配置模块没有配置插件
                routedefault,PATH_INFO=web.__getconfigroute(
                    self,
                    PATH_INFO,
                    header
                )
                if routedefault: #使用默认路由
                    for path in PATH_INFO:
                        if path:
                            if i==0:
                                plug=path
                                globals.VAR.defplug=plug
                            elif i==1:
                                files=path
                                urls=urls+"/"+str(path)
                            elif i==2:
                                funct=path
                                urls=urls+"/"+str(path)
                            else:
                                param.append(urllib.parse.unquote(path))
                        i+=1
        # elif route['plug']:  #配置模块但没有匹配插件
        #     plug=route['plug']
        elif getplug:
            # print('getplug',getplug)
            plug=getplug
            routedefault,PATH_INFO=web.__getconfigroute(
                self,
                PATH_INFO,
                header
            )
            if routedefault: #使用默认路由
                for path in PATH_INFO:
                    if path:
                        if i==0:
                            modular=path
                            globals.VAR.defmodular=modular
                        elif i==1:
                            files=path
                            urls=urls+"/"+str(path)
                        elif i==2:
                            funct=path
                            urls=urls+"/"+str(path)
                        else:
                            param.append(urllib.parse.unquote(path))
                    i+=1
        else: #完全默认
            # print('完全默认')
            routedefault,PATH_INFO=web.__getconfigroute(self,PATH_INFO,header)
            if routedefault: #使用默认路由
                for path in PATH_INFO:
                    if path:
                        if i==0:
                            modular=path
                            globals.VAR.defmodular=modular
                        elif i==1:
                            plug=path
                            globals.VAR.defplug=plug
                        elif i==2:
                            files=path
                            urls=urls+"/"+str(path)
                        elif i==3:
                            funct=path
                            urls=urls+"/"+str(path)
                        else:
                            param.append(urllib.parse.unquote(path))
                    i+=1
        #默认路由end ############################################################
        if not modular:
            modular=route['defmodular']
            globals.VAR.defmodular=modular
        if not plug:
            plug=route['defplug']
            globals.VAR.defplug=plug
        return methods,modular,plug,files,funct,tuple(param)
    def __tran(self,data,status,resheader):
        "转换控制器返回的内容"
        if isinstance(data,tuple):
            i=0
            for item in data:
                if i==0:
                    body=item
                elif i==1:
                    status=item
                elif i==2:
                    if isinstance(item,dict):
                        for key in item:
                            resheader[key]=item[key]
                    else:
                        raise Exception('错误！这个不是一个字典')
                else:
                    break
                i+=1
        else:
            body=data
        return body,status,resheader
    def __set_globals(self,header):
        globals.HEADER.GET=header
        # globals.HEADER.url_scheme=header['url_scheme']
        globals.HEADER.Method=header['REQUEST_METHOD']
        globals.HEADER.URL=header['RAW_URI']
        globals.HEADER.PATH_INFO=header['PATH_INFO']
        globals.HEADER.QUERY_STRING=header['QUERY_STRING']
        globals.HEADER.SERVER_PROTOCOL=header['SERVER_PROTOCOL']
        globals.HEADER.HTTP_HOST=header['HTTP_HOST']
        globals.HEADER.BODY_DATA=header['BODY_DATA']
        globals.HEADER.REMOTE_ADDR=header['REMOTE_ADDR']
        globals.HEADER.HTTP_X_REAL_IP=header['HTTP_X_REAL_IP']
        try:
            globals.HEADER.files=header['files']
        except:
            globals.HEADER.files=None
        try:
            globals.HEADER.HTTP_COOKIE=header['HTTP_COOKIE']
        except:
            globals.HEADER.HTTP_COOKIE=None
        try:
            globals.HEADER.HTTP_USER_AGENT=header['HTTP_USER_AGENT']
        except:
            globals.HEADER.HTTP_USER_AGENT=None
    def __del_globals():
        globals.VAR = threading.local()
        globals.HEADER = threading.local()
        globals.G = threading.local()
    def __routes(self,header):
        body="这是一个http测试服务器"
        status="200 ok"
        resheader={"Content-Type":"application/json; charset=utf-8"}
        web.__set_globals(self,header)
        PATH_INFO=header['PATH_INFO'].split('/')
        if PATH_INFO[0]==' ' or PATH_INFO[0]=='':
            del PATH_INFO[0]
        methods,modular,plug,files,funct,param=web.defaultroute(self,header,PATH_INFO)
        globals.VAR.component=(methods,modular,plug,files,funct,param)
        if header['REQUEST_METHOD'] in methods:
            try:
                obj=getattr(web.__appname,modular)
            except (AttributeError,UnboundLocalError):
                status="500 Internal Server Error"
                body=web.__tpl(
                    title = status,
                    e=status,
                    data="路由不存在："+str(modular)+"/"
                )
            else:
                try:
                    obj=getattr(obj,"controller")
                except (AttributeError,UnboundLocalError):
                    status="404 Not Found"
                    body=web.__tpl(
                        title = status,
                        e=status,
                        data="路由不存在："+str(modular)+"/controller/"
                    )
                else:
                    try:
                        obj=getattr(obj,plug)
                    except (AttributeError,UnboundLocalError) as e:
                        con="无法找到目录："+str(modular)+"/controller/"+str(plug)+"/"
                        try:
                            data=getattr(obj,"error")(e,con)
                            body,status,resheader=web.__tran(
                                self,
                                data,
                                status,
                                resheader
                            )
                        except (AttributeError,UnboundLocalError):
                            status="404 Not Found"
                            body=web.__tpl(
                                title = status,
                                e=status,data=con
                            )
                        except Exception as e:
                            status="500 Internal Server Error"
                            errms=status
                            if self.__config.app['app_debug']:
                                print(traceback.format_exc())
                                errms=traceback.format_exc().split("\n")
                            body=web.__tpl(
                                title = status,
                                data=errms,e=e
                            )
                    else:
                        try:
                            obj=getattr(obj,files)
                        except (AttributeError,UnboundLocalError) as e:
                            con="无法找到文件："+str(modular)+"/controller/"+str(plug)+"/"+str(files)+".py"
                            try:
                                data=getattr(obj,"error")(e,con)
                                body,status,resheader=web.__tran(
                                    self
                                    ,data
                                    ,status
                                    ,resheader
                                )
                            except (AttributeError,UnboundLocalError):
                                status="404 Not Found"
                                body=web.__tpl(
                                    title = status
                                    ,data=con
                                    ,e=status)
                            except Exception as e:
                                status="500 Internal Server Error"
                                errms=status
                                if self.__config.app['app_debug']:
                                    print(traceback.format_exc())
                                    errms=traceback.format_exc().split("\n")
                                body=web.__tpl(
                                    title = status,
                                    data=errms,
                                    e=e
                                )
                        else:
                            try:
                                data=None
                                if self.__config.app['before_request']:  #请求前执行的函数
                                    try:
                                        data=getattr(obj,self.__config.app['before_request'])()
                                        if data:
                                            body,status,resheader=web.__tran(
                                                self,data,
                                                status,
                                                resheader
                                            )
                                    except (AttributeError):
                                        print(traceback.format_exc())
                                        pass
                                    except Exception as e:
                                        try:
                                            data=getattr(obj,"error")(e,traceback.format_exc().split("\n"))
                                            body,status,resheader=web.__tran(
                                                self,data,
                                                status,
                                                resheader
                                            )
                                        except (AttributeError):
                                            data=True
                                            status="500 Internal Server Error"
                                            errms=status
                                            if self.__config.app['app_debug']:
                                                # print(traceback.format_exc())
                                                errms=traceback.format_exc().split("\n")
                                            body=web.__tpl(
                                                title = status,
                                                data=errms,e=e
                                            )
                                        except Exception as e:
                                            data=True
                                            status="500 Internal Server Error"
                                            errms=status
                                            if self.__config.app['app_debug']:
                                                print(traceback.format_exc())
                                                errms=traceback.format_exc().split("\n")
                                            body=web.__tpl(
                                                title = status,
                                                data=errms,e=e
                                            )
                                if not data:
                                    try:
                                        objclass=getattr(obj,files) #新增
                                    except:
                                        data=getattr(obj,funct)(*param) #兼容性之前的控制器
                                    else:
                                        data=getattr(objclass,funct)(*param)
                                    body,status,resheader=web.__tran(
                                        self,data,
                                        status,
                                        resheader
                                    )
                            except Exception as e:
                                try:
                                    data=getattr(obj,"error")(e,traceback.format_exc().split("\n"))
                                    body,status,resheader=web.__tran(
                                        self,data,
                                        status,
                                        resheader
                                    )
                                except (AttributeError):
                                    status="500 Internal Server Error"
                                    errms=status
                                    if self.__config.app['app_debug']:
                                        print(traceback.format_exc())
                                        errms=traceback.format_exc().split("\n")
                                    body=web.__tpl(
                                        title = status,
                                        data=errms,
                                        e=e
                                    )
                                except Exception as e:
                                    status="500 Internal Server Error"
                                    errms=status
                                    if self.__config.app['app_debug']:
                                        print(traceback.format_exc())
                                        errms=traceback.format_exc().split("\n")
                                    body=web.__tpl(
                                        title = status,
                                        data=errms,
                                        e=e
                                    )
        else:
            status="405 Method Not Allowed"
            body=web.__tpl(
                title = status,
                data='405 Method Not Allowed',
                e=''
            )
        try:
            resheader['set-cookie']=globals.set_cookie
            del globals.set_cookie
        except:pass
        
        if self.__config.app['after_request']:  #请求后执行的函数
            try:
                data=getattr(obj,self.__config.app['after_request'])(body,status,resheader)
                if data:
                    body,status,resheader=web.__tran(self,data,status,resheader)
            except (AttributeError,UnboundLocalError):pass
            except Exception as e:
                try:
                    data=getattr(obj,"error")(e,traceback.format_exc().split("\n"))
                    body,status,resheader=web.__tran(
                        self,data,
                        status,
                        resheader
                    )
                except AttributeError as e:
                    status="500 Internal Server Error"
                    errms=status
                    if self.__config.app['app_debug']:
                        print(traceback.format_exc())
                        errms=traceback.format_exc().split("\n")
                    body=web.__tpl(
                        title = status
                        ,data=errms,
                        e=e
                    )
                except Exception as e:
                    status="500 Internal Server Error"
                    errms=status
                    if self.__config.app['app_debug']:
                        print(traceback.format_exc())
                        errms=traceback.format_exc().split("\n")
                    body=web.__tpl(
                        title = status,
                        data=errms,
                        e=""
                    )
        resheaders=[]
        for key in resheader:
            resheaders.append((key,resheader[key]))
        web.__del_globals()

        
        if self.__config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=='kcwebs' or self.__config.fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=='kcwebps':#请求后执行的函数
            try:
                getattr(obj,"rfdsgeagesegdsfdsfdrrsebskcwebsafterrequest")() #关闭数据库相关连接
            except:pass


        if isinstance(resheaders,list):
            if not body:
                body=''
            if type(body) is bytes:
                pass
            else:
                body=str(body)
            return str(status),resheaders,body
        else:
            raise Exception()
    def __tpl(**context):
        arr=json_encode({
            'title':context['title'],
            'msg':str(context['e']),
            'error':context['data']
        })
        return arr
    # def __tpl(**context):
    #     title,status,error=context
    #     arr=json_encode({
    #         'title':title,
    #         'status':status,
    #         'error':error
    #     })
    #     headers={"Content-Type":"application/json; charset=utf-8","Access-Control-Allow-Origin":"*"}
    #     return arr,'500 error',headers
    def __application(self,env, start_response):
        # print(env)
        try:
            request_body_size = int(env.get('CONTENT_LENGTH', '0'))
        except (ValueError):
            request_body_size = 0
        if 'multipart/form-data; boundary' in env['CONTENT_TYPE']:#上传文件
            files = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
            # open(form["file"].filename, 'wb').write(form["file"].value) 
            # print(files["file"].name)
            # print(files["name"].filename)
            # print(files["name"].value)
            env['BODY_DATA']=None
        else:
            files=None
            BODY_DATA=env['wsgi.input'].read(request_body_size)
            env['BODY_DATA']=BODY_DATA.decode()
        env['RAW_URI']=env['PATH_INFO']
        if env.get('QUERY_STRING'):
            env['RAW_URI']=str(env['PATH_INFO'])+"?"+str(env.get('QUERY_STRING'))
        try:
            env['REMOTE_ADDR']
        except:
            env['REMOTE_ADDR']=''
        try:
            env['wsgi.url_scheme']
        except:
            env['wsgi.url_scheme']=''
        try:
            env['HTTP_X_REAL_IP']
        except:
            env['HTTP_X_REAL_IP']=''
        try:
            env['HTTP_COOKIE']
        except:
            env['HTTP_COOKIE']=''
        try:
            env['HTTP_USER_AGENT']
        except:
            env['HTTP_USER_AGENT']=''
        reqheader={ 
            'REQUEST_METHOD':env['REQUEST_METHOD'],
            'url_scheme':env['wsgi.url_scheme'],
            'RAW_URI':env['RAW_URI'],
            'PATH_INFO':env['PATH_INFO'],
            'QUERY_STRING':env['QUERY_STRING'],
            'SERVER_PROTOCOL':env['SERVER_PROTOCOL'],
            'HTTP_HOST':env['HTTP_HOST'],
            'HTTP_COOKIE':env['HTTP_COOKIE'],
            'REMOTE_ADDR':env['REMOTE_ADDR'],
            'HTTP_USER_AGENT':env['HTTP_USER_AGENT'],
            'BODY_DATA':env['BODY_DATA'],
            'HTTP_X_REAL_IP':env['HTTP_X_REAL_IP'],
            'files':files
        }
        p=(config.app['staticpath']+reqheader['RAW_URI'].replace(' ',''))
        status='200 ok'
        if os.path.isfile(p):
            resheader=[("Cache-Control","public, max-age=2592000"),("Accept-Ranges","bytes")]
            ETag=md5(p)
            try:
                HTTP_IF_NONE_MATCH=globals.HEADER.GET['HTTP_IF_NONE_MATCH']
            except:
                HTTP_IF_NONE_MATCH=None
            if HTTP_IF_NONE_MATCH:
                status="304 Not Modified"
            else:
                kind = filetype.guess(p)
                if kind is None:
                    f=open(p,"rb")
                    body=f.read()
                    f.close()
                    if '.css' in p[-5:]:
                        resheader.append(("Content-Type","text/css"))
                    elif '.js' in p[-5:]:
                        resheader.append(("Content-Type","application/javascript"))
                else:
                    f=open(p,"rb")
                    body=f.read()
                    f.close()
                    resheader.append(("Content-Type",kind.mime))
            dateArray = datetime.fromtimestamp(int(time.time())-86400)
            otherStyleTime = dateArray.strftime('%a, %d %b %Y %H:%M:%S GMT')
            resheader.append(("Last-Modified",otherStyleTime))
            resheader.append(("ETag",ETag))
        else:
            status,resheader,body=web.__routes(self,reqheader)
            resheader.append(('Server', "kcws"+config.kcws['version']))
            if type(body) is bytes:
                pass
            else:
                body=bytes(body, encoding='utf-8')
        start_response(status,resheader)
        return [body]
    
    def __http_wsgi(self,host,port,filename):
        "http——wsgi测试服务"
        from wsgiref.simple_server import make_server
        print("* \033[1;31;40m! 警告：\033[0m这是一个wsgiref开发服务器。不要在生产环境中部署使用它")
        # print('* 生产环境中建议使用gunicorn,gunicorn运行命令如：gunicorn -b '+host+':'+str(port)+' '+str(filename)+':app')
        if host=='0.0.0.0':
            print("\033[32m* （CTRL+单击打开）http://127.0.0.1:"+str(port)+"（按CTRL+C退出）")
        else:
            print("\033[32m* 运行在http://"+host+":"+str(port)+"（按CTRL+C退出）")
        if self.__config.app['app_debug']:
            print('\033[37m* 调试器：开启')
        else:
            print('\033[37m* 调试器：已关闭')
        self.__httpd = make_server(host, int(port), self.__application)
        self.__httpd.serve_forever()
    # def __server_client(self,new_socket):
    #     # 处理http的的请求
    #     data=new_socket.recv(1047576).decode()
    #     if data:
    #         datas=data.split("\r\n")
    #         data1=datas[0]
    #         #reqsest
    #         REQUEST_METHOD=data1.split("/")[0].replace(' ','') ##GET
    #         RAW_URI=re.findall(REQUEST_METHOD+"(.+?) HTTP", data1) #/aa/bb/cc?a=1&b=1
    #         if RAW_URI:
    #             RAW_URI=RAW_URI[0]
    #         else:
    #             RAW_URI=''
    #         PATH_INFO=RAW_URI.split("?")[0] #/aa/bb/cc
    #         QUERY_STRING=RAW_URI.replace(str(PATH_INFO),'').replace('?','') #a=1&b=1
    #         SERVER_PROTOCOL=data1.split(" ")[-1] #HTTP/1.1
    #         HTTP_HOST=re.findall("Host: (.+?)\r\n", data)#212.129.149.238:39010
    #         if HTTP_HOST:
    #             HTTP_HOST=HTTP_HOST[0]
    #         else:
    #             HTTP_HOST=''
    #         HTTP_COOKIE=re.findall("Cookie: (.+?)\r\n", data)#cookie
    #         if HTTP_COOKIE:
    #             HTTP_COOKIE=HTTP_COOKIE[0]
    #         else:
    #             HTTP_COOKIE=''
    #         REMOTE_ADDR=''
    #         HTTP_USER_AGENT=re.findall("User-Agent: (.+?)\r\n", data) #Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0
    #         if HTTP_USER_AGENT:
    #             HTTP_USER_AGENT=HTTP_USER_AGENT[0]
    #         else:
    #             HTTP_USER_AGENT=''
    #         BODY_DATA=datas[len(datas)-1]
    #         # print(data)
    #         #reqsest
    #         reqheader={ 
    #             'REQUEST_METHOD':REQUEST_METHOD,
    #             'RAW_URI':RAW_URI,
    #             'PATH_INFO':PATH_INFO,
    #             'QUERY_STRING':QUERY_STRING,
    #             'SERVER_PROTOCOL':SERVER_PROTOCOL,
    #             'HTTP_HOST':HTTP_HOST,
    #             'HTTP_COOKIE':HTTP_COOKIE,
    #             'REMOTE_ADDR':REMOTE_ADDR,
    #             'HTTP_X_REAL_IP':'',
    #             'HTTP_USER_AGENT':HTTP_USER_AGENT,
    #             'BODY_DATA':BODY_DATA
    #         }
    #         p=(config.app['staticpath']+RAW_URI.replace(' ',''))
    #         # print("目录",p)
    #         status='200 ok'
    #         if os.path.isfile(p):
    #             # print('静态文件',p)
    #             kind = filetype.guess(p)
    #             if kind is None:
                    
    #                 f=open(p,"rb")
    #                 body=f.read()
    #                 f.close()
    #                 resheader=[("Cache-Control","public, max-age=43200"),("Expires","Thu, 07 Nov 2019 02:59:02 GMT")]
                    
    #                 header="HTTP/1.1 %s \n" % status
    #                 header+="Content-Length:%d\n" % len(body)
    #             else:
    #                 f=open(p,"rb")
    #                 body=f.read()
    #                 f.close()
    #                 resheader=[("Content-Type",kind.mime),("Cache-Control","public, max-age=43200"),("Accept-Ranges","bytes"),("Expires","Thu, 07 Nov 2019 02:59:02 GMT")]
    #                 header="HTTP/1.1 %s \n" % status
    #                 header+="Content-Length:%d\n" % len(body)
    #         else:
    #             status,resheader,body=self.__routes(reqheader)
    #             if type(body) is bytes:
    #                 pass
    #             else:
    #                 body=body.encode()
    #             header="HTTP/1.1 %s \n" % status
    #             header+="Content-Length:%d\n" % len(body)
            
    #         print(HTTP_HOST+' -- ['+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'] "'+REQUEST_METHOD+" "+RAW_URI +" "+SERVER_PROTOCOL + '" '+status+"-")
    #         t=time.time()
    #         header+="Server:kcwebs"+str(config.kcwebs['version'])+"\n"
    #         header+="Date:%s\n" % datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    #         for t in resheader:
    #             header+="%s:%s\n" % (t[0],t[1])
    #         header+="\n"
    #         try:
    #             new_socket.send(header.encode())
    #             new_socket.send(body)
    #         except Exception as e:
    #             pass
    #     new_socket.close() 
    # def __http_server(self,host,port,filename):
    #     "http测试服务"
    #     tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #     try:
    #         tcp_socket.bind((host,int(port)))
    #     except OSError:
    #         print("通常每个套接字地址(协议/网络地址/端口)只允许使用一次（按CTRL+C退出）")
    #     else:
    #         tcp_socket.listen(1024)
    #         print('! \033[1;31;40m警告：\033[0m这是一个kcwebs_server开发服务器。不要在生产环境中部署使用它')
    #         print('* 生产环境中建议使用gunicorn,gunicorn运行命令如：gunicorn -b '+host+':'+str(port)+' '+str(filename)+':app')
    #         if self.__config.app['app_debug']:
    #             print('* 调试器：开启')
    #         else:
    #             print('* 调试器：已关闭')
    #         print("* 运行在http://"+host+":"+str(port)+"/ （按CTRL+C退出）")
    #         while True:
    #             new_tcp_socket,client_info=tcp_socket.accept()
    #             t=threading.Thread(target=self.__server_client,args=(new_tcp_socket,))
    #             t.daemon=True
    #             t.start()
    #         tcp_socket.close()
    
    # def __http_sever(self,host,port,filename):
    #     #http测试服务器
    #     print('\033[1;31;40m! 警告：\033[0m这是一个kcwebs开发服务器。不要在生产环境中部署使用它')
    #     print('* 生产环境中建议使用gunicorn,gunicorn运行命令如：gunicorn -b '+host+':'+str(port)+' '+str(filename)+':app')
    #     if self.__config.app['app_debug']:
    #         print('* 调试器：开启')
    #     else:
    #         print('* 调试器：已关闭')
    #     print("* 运行在http://"+host+":"+str(port)+"/ （按CTRL+C退出）")
    #     tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #     tcp_socket.bind((host,int(port)))
    #     tcp_socket.listen(1024)
    #     pack_length=1024
    #     tcp_socket.setblocking(False)
    #     tcp_socket_list=list()
    #     while True:
    #         try:
    #             new_tcp_socket,client_info=tcp_socket.accept()
    #         except:
    #             pass
    #         else:
    #             new_tcp_socket.setblocking(False)
    #             tcp_socket_list.append(new_tcp_socket)
    #         for cli_soc in tcp_socket_list:
    #             try:
    #                 data=cli_soc.recv(pack_length).decode()
    #             except Exception as e:
    #                 pass
    #             else:
    #                 if data:
    #                     datas=data.split("\r\n")
    #                     data1=datas[0]
    #                     #reqsest
    #                     REQUEST_METHOD=data1.split("/")[0].replace(' ','') ##GET
    #                     RAW_URI=re.findall(REQUEST_METHOD+"(.+?) HTTP", data1) #/aa/bb/cc?a=1&b=1
    #                     if RAW_URI:
    #                         RAW_URI=RAW_URI[0]
    #                     else:
    #                         RAW_URI=''
    #                     PATH_INFO=RAW_URI.split("?")[0] #/aa/bb/cc
    #                     QUERY_STRING=RAW_URI.replace(str(PATH_INFO),'').replace('?','') #a=1&b=1
    #                     SERVER_PROTOCOL=data1.split(" ")[-1] #HTTP/1.1
    #                     HTTP_HOST=re.findall("Host: (.+?)\r\n", data)#212.129.149.238:39010
    #                     if HTTP_HOST:
    #                         HTTP_HOST=HTTP_HOST[0]
    #                     else:
    #                         HTTP_HOST=''
    #                     HTTP_COOKIE=re.findall("Cookie: (.+?)\r\n", data)#cookie
    #                     if HTTP_COOKIE:
    #                         HTTP_COOKIE=HTTP_COOKIE[0]
    #                     else:
    #                         HTTP_COOKIE=''
    #                     REMOTE_ADDR=''
    #                     HTTP_USER_AGENT=re.findall("User-Agent: (.+?)\r\n", data) #Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0
    #                     if HTTP_USER_AGENT:
    #                         HTTP_USER_AGENT=HTTP_USER_AGENT[0]
    #                     else:
    #                         HTTP_USER_AGENT=''
    #                     BODY_DATA=datas[len(datas)-1]
    #                     # print(data)
    #                     #reqsest
    #                     reqheader={ 
    #                         'REQUEST_METHOD':REQUEST_METHOD,
    #                         'RAW_URI':RAW_URI,
    #                         'PATH_INFO':PATH_INFO,
    #                         'QUERY_STRING':QUERY_STRING,
    #                         'SERVER_PROTOCOL':SERVER_PROTOCOL,
    #                         'HTTP_HOST':HTTP_HOST,
    #                         'HTTP_COOKIE':HTTP_COOKIE,
    #                         'REMOTE_ADDR':REMOTE_ADDR,
    #                         'HTTP_X_REAL_IP':'',
    #                         'HTTP_USER_AGENT':HTTP_USER_AGENT,
    #                         'BODY_DATA':BODY_DATA
    #                     }
    #                     p=(config.app['staticpath']+RAW_URI.replace(' ',''))
    #                     # print("目录",p)
    #                     status='200 ok'
    #                     if os.path.isfile(p):
    #                         # print('静态文件',p)
    #                         kind = filetype.guess(p)
    #                         if kind is None:
                                
    #                             f=open(p,"rb")
    #                             body=f.read()
    #                             f.close()
    #                             resheader=[("Cache-Control","public, max-age=43200"),("Expires","Thu, 07 Nov 2019 02:59:02 GMT")]
                                
    #                             header="HTTP/1.1 %s \n" % status
    #                             header+="Content-Length:%d\n" % len(body)
    #                         else:
    #                             f=open(p,"rb")
    #                             body=f.read()
    #                             f.close()
    #                             resheader=[("Content-Type",kind.mime),("Cache-Control","public, max-age=43200"),("Accept-Ranges","bytes"),("Expires","Thu, 07 Nov 2019 02:59:02 GMT")]
    #                             header="HTTP/1.1 %s \n" % status
    #                             header+="Content-Length:%d\n" % len(body)
    #                     else:
    #                         status,resheader,body=self.__routes(reqheader)
    #                         if type(body) is bytes:
    #                             pass
    #                         else:
    #                             body=body.encode()
    #                         header="HTTP/1.1 %s \n" % status
    #                         header+="Content-Length:%d\n" % len(body)
                        
    #                     print(HTTP_HOST+' -- ['+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'] "'+REQUEST_METHOD+" "+RAW_URI +" "+SERVER_PROTOCOL + '" '+status+"-")
    #                     t=time.time()
    #                     header+="Server:kcwebs"+str(config.kcwebs['version'])+"\n"
    #                     header+="Date:%s\n" % datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    #                     for t in resheader:
    #                         header+="%s:%s\n" % (t[0],t[1])
    #                     header+="\n"
    #                     try:
    #                         cli_soc.send(header.encode())
    #                         cli_soc.send(body)
    #                     except Exception as e:
    #                         cli_soc.close()
    #                 else:
    #                     cli_soc.close()
    #                     tcp_socket_list.remove(cli_soc)
    #     tcp_socket.close()
