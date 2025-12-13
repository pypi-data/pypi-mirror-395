# -*- coding: utf-8 -*-
# 应用配置
import sys
app={}
app['app_debug']=True  #是否开启调试模式
app['tpl_folder']='./tpl'  #设置模板文件目录名 注意：不能配置目录路径
app['before_request']=''  #设置请求前执行的函数
app['after_request']=''    #设置请求后执行的函数  
app['staticpath']='static'
app['http_server']='wsgiref' #使用的开发服务器 支持 wsgiref
app['cli']=False
app['save_cli_pid']=False #是否开启cli运行时保存pid
app['temp_folder']='app/runtime/temp' #是否开启cli运行时保存pid


#路由配置
route={}
route['default']=True #是否开启默认路由  默认路由开启后面不影响以下配置的路由，模块名/版本名/控制器文件名/方法名 作为路由地址   如：http://www.kcws.com/modular/plug/index/index/
route['modular']='' #指定访问配置固定模块 （如果配置了该值，将无法通过改变url访问不同模块）
route['plug']='' #指定访问固定插件 （如果配置了该值，将无法通过改变url访问不同插件）
route['defmodular']='index' #默认模块 当url不包括模块名时
route['defplug']='index' #默认插件 当url不包括插件名时
route['files']='index' #默认路由文件（控制器） 当url不包括控制器名时
route['funct']='index'  #默认路由函数 (操作方法) 当url不包括操作方法名时
route['methods']=['POST','GET'] #默认请求方式
route['children']=[]

kcws={}
kcws['name']='kcws'                             #项目的名称
kcws['version']='1.0'							#项目版本
kcws['description']='超轻量级http框架'       #项目的简单描述
kcws['long_description']='kcws是一个由kcwebs抽象出来的超轻量级http框架'     #项目详细描述
kcws['license']='MIT License'                    #开源协议   mit开源
kcws['url']='https://docs.kwebapp.cn/index/index/1'
kcws['author']='百里-坤坤'  					 #名字
kcws['author_email']='kcwebs@kwebapp.cn' 	     #邮件地址
kcws['maintainer']='坤坤' 						 #维护人员的名字
kcws['maintainer_email']='fk1402936534@qq.com'    #维护人员的邮件地址
kcws['username']=''
kcws['password']=''

domain={}
domain['kcwebsfile']="https://file.kwebapp.cn"
domain['kcwebsstatic']="https://static.kwebapp.cn"
domain['kcwebsimg']="https://img.kwebapp.cn"
domain['kcwebsapi']="https://kcwebsapi.kwebapp.cn"

#其他配置
other={}

fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=kcws['name'] #不要修改改参数，否则无法上传模块和插件

