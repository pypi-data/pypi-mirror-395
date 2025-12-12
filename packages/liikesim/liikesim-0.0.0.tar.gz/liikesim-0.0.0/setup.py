from setuptools import setup,find_packages
setup(name='liikesim',
version='0.0.0',
description=f'simple test for liikesim',
long_description=open('README.md','r',encoding='utf-8').read(),
long_description_content_type='text/markdown',
packages=find_packages(),
license='Apache-2.0',
keywords=['liikesim'],
install_requires=[]
)
#name:用户使用pip命令安装时你的库的名字,文件夹是的名字是用户在代码调用你的库的名字
#version：package的版本号
#autoor:作者名称(非必须)
#author_email:作者email地址(非必须)
#descriptoion:一段简介明了的介绍，几十字就可以了。
#long_description:这里推荐你将项目的readme.md文件直接作为long_description,并且你可以先在#github内写好后下载到本地,接着使用open语句读取
#url：项目的链接,若你有能力可以为该项目自己搭建一个简介网站,若没有能力老老实实在github上上传项目之后把链接放到这里即可(非必须)
#packages:使用find_packages()函数即可。
#license:我这里选择的是Apache-2.0
#keywords：关键字
#install_requires:你的项目中用到的别人的库,全部以List[str]的形式写在这里,这里推荐使用库名>=版本号的格式