# FSDN backend README

>   This repository contains the backend of FSDN(Fudan Software Developer Network).

![](https://img.shields.io/badge/FSDN-backend-brightgreen.svg)![](https://img.shields.io/badge/Framework-Django-green.svg)

## Table of Contents

-   [Background](#background)
-   [Install](#install)
-   [Usage](#Usage)
-   [Contributing](#contributing)
-   [License](#license)

## Background

简单介绍背景

## Release

详见看板

## Install

* 安装python：版本在3.6及以上
* 安装django：版本在2.2及以上（建议3.0），pip3 install django==3.0
* 安装django-cors-headers：该插件用于支持跨域请求，pip3 install django-cors-headers

## Usage

**1.修改EMAIL_HOST_PASSWORD**  

django作为第三方发送邮件，需要提供EMAIL_HOST_PASSWORD。请咨询starshine获取正确的EMAIL_HOST_PASSWORD值，并在setting.py文件中修改EMAIL_HOST_PASSWORD为正确值。EMAIL_HOST_PASSWORD属安全信息，请大家在push时**勿包含**此信息！

**2.添加目录uploads**
核对在外层的backend目录中是否有uploads文件夹，若无，应当添加，用于存放图片。

**3.运行指令**

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver <IP>:<PORT>
```

**note：** 
1) 本地测试时，IP和PORT可省略,默认是127.0.0.1:8000。部署到服务器上时，目前服务器开放的端口是8000，设置为"0:8000"（不包含引号）即可。 
2) 关于csrf设置。在测试时，可能出现Forbidden (CSRF cookie not set.)错误。此时，简单粗暴的方法是在setting.py文件的MIDDLEWARE中注释掉'django.middleware.csrf.CsrfViewMiddleware'，关闭csrf检测。

## Contributing

贡献者

## License

协议