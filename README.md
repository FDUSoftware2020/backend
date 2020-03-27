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

记录更新日志

## Install

安装教程

## Usage

使用教程  

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