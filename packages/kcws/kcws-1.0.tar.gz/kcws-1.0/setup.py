
# 打包上传 python setup.py sdist upload
# 打包并安装 python setup.py sdist install
# twine upload --repository-url https://test.pypi.org/legacy/ dist/* #上传到测试
# pip install --index-url https://pypi.org/simple/ kcwebs   #安装测试服务上的kcwebs pip3 install kcwebs==4.12.4 -i https://pypi.org/simple/
# 安装 python setup.py install 
#############################################
import os,sys
from setuptools import setup, find_packages,Extension
from kcws import config
class setupconfig:
    kcws={}
    kcws['name']=config.kcws['name']                             #项目的名称
    kcws['version']=config.kcws['version']								#项目版本
    kcws['description']=config.kcws['description']       #项目的简单描述
    kcws['long_description']=config.kcws['long_description']     #项目详细描述
    kcws['license']=config.kcws['license']                    #开源协议   mit开源
    kcws['url']=config.kcws['url']
    kcws['author']=config.kcws['author']  					 #名字
    kcws['author_email']=config.kcws['author_email'] 	     #邮件地址
    kcws['maintainer']=config.kcws['maintainer'] 						 #维护人员的名字
    kcws['maintainer_email']=config.kcws['maintainer_email']    #维护人员的邮件地址
confkcws={}
confkcws['name']=setupconfig.kcws['name']                            #项目的名称 
confkcws['version']=setupconfig.kcws['version']							#项目版本
confkcws['description']=setupconfig.kcws['description']       #项目的简单描述
confkcws['long_description']=setupconfig.kcws['long_description']     #项目详细描述
confkcws['license']=setupconfig.kcws['license']                   #开源协议   mit开源
confkcws['url']=setupconfig.kcws['url']
confkcws['author']=setupconfig.kcws['author']  					 #名字
confkcws['author_email']=setupconfig.kcws['author_email'] 	     #邮件地址
confkcws['maintainer']=setupconfig.kcws['maintainer'] 						 #维护人员的名字
confkcws['maintainer_email']=setupconfig.kcws['maintainer_email']    #维护人员的邮件地址
def get_file(folder='./',lists=[]):
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if files=='__pycache__' or files=='.git':
                pass
            else:
                lists.append(folder+"/"+files)
                get_file(folder+"/"+files,lists)
        else:
            pass
    return lists
def start():
    b=get_file("kcws",['kcws'])
    setup(
        name = confkcws["name"],
        version = confkcws["version"],
        keywords = "kcws"+confkcws['version'],
        description = confkcws["description"],
        long_description = confkcws["long_description"],
        license = confkcws["license"],
        author = confkcws["author"],
        author_email = confkcws["author_email"],
        maintainer = confkcws["maintainer"],
        maintainer_email = confkcws["maintainer_email"],
        url=confkcws['url'],
        packages =  b,
        # data_files=[('Scripts', ['kcws/bin/kcws.exe'])],
        install_requires = ['gunicorn==20.0.4','watchdog==4.0.0','filetype==1.2.0','psutil==5.8.0','requests==2.32.4',], #第三方包
        package_data = {
            '': ['*.html', '*.js','*.css','*.jpg','*.png','*.gif'],
        },
        entry_points = {
            'console_scripts':[
                'kcws = kcws.kcws:cill_start'
            ]
        }
    )
start()