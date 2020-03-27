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

**1.Account相关功能** (2020-03-27)  
具体有：注册、登录、登出、验证码、修改用户名、修改密码。

**2.允许跨域** (2020-03-27)  
后端可支持跨域请求。只开启一些基本设置，如ORIGIN、HEADERS、METHODS。


## Install
* 安装python：版本在3.6及以上
* 安装django：版本在2.2及以上，建议3.0
* 安装django-cors-headers：pip install django-cors-headers

## Usage

**1.修改EMAIL_HOST_PASSWORD**  
django作为第三方发送邮件，需要提供EMAIL_HOST_PASSWORD。请咨询starshine获取正确的EMAIL_HOST_PASSWORD值，并在setting.py文件中修改EMAIL_HOST_PASSWORD为正确值。EMAIL_HOST_PASSWORD属安全信息，请大家在push时**勿包含**此信息！

**2.运行指令**
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver <IP>:<PORT>
```

## Contributing

贡献者

## License

协议