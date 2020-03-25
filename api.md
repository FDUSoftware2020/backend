# FSDN web API

>   This file describes the APIs of FSDN(Fudan Software Developer Network), helping FSDN frontend developers to work efficiently.

![](https://img.shields.io/badge/FSDN-API-brighgreen.svg)![](https://img.shields.io/badge/API-Documentation-green.svg)

**Note:** 

1.  All keys in `json` format should use `" "` other than` ' '`. 

2.  All responses (if exists) use the format below:

    ```json
    {
    	"err_code": <int, 0 means success, otherwise fail>,
    	"message": <str, human-readable message replied from the server>,
    	"data": <data, this part is different from api to api>
    }
    ```

3.  If there is "login required" following the request url, and if you are not logged in, then the following response will be returned (with HTTP status code `403`):

    ```json
    {
    	"err_code": -1,
    	"message": "Login Required",
    	"data": {}
    }
    ```

## Table of Contents
-   [Account APIs](# Account APIs)
    -   [1. POST /account/register](# 1. POST /account/register)
    -   [2. POST /account/login](#2. POST /account/login)
    -   [3. GET /account/logout (login required)](# 3. GET /account/logout (login required))
    -   [4. POST /account/verify](# 4. POST /account/verify)
    -   [5. POST /account/modify_username (login required)](# 5. GET /account/modify_username (login required))
    -   [6. POST /account/modify_password](# 6. POST /account/modify_password)
    -   [7. GET /account/ask_user (login required)](# 7. GET /account/ask_user (login required))

-   [Issue APIs](#Issue APIs)



## Account APIs

此部分定义一些用户相关的APIs，如：注册、登录、登出、验证、修改用户名、修改密码

### 1. POST /account/register

**Description:** 注册一个新用户
* 须提供数据：用户名、密码、重复密码、邮箱、4位验证码

#### 1.1 request format

```json
{
    "username":<str>,
    "password":<str>,
    "re_password":<str>,
    "email":<str>,
    "verification":<str>
}
```

#### 1.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 2. POST /account/login

**Description:** 用户登录
* 须提供数据：用户名、密码

#### 2.1 request format

```json
{
    "username":<str>,
    "password":<str>,
}
```

#### 2.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 3. GET /account/logout (login required)

**Description:** 用户退出登录（须已有登录用户）

#### 3.1 request format

no data

#### 3.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 4. POST /account/verify

**Description:** 发送验证码
* 须提供数据：用户邮箱

#### 4.1 request format

```json
{
    "email":<str>
}
```

#### 4.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 5. POST /account/modify_username （login required)

**Description:** 修改用户名（须处于登录状态）
* 须提供数据：新用户名

#### 5.1 request format

```json
{
    "username":<str>
}
```

#### 5.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 6. POST /account/modify_password

**Description:** 修改密码
* 须提供数据：用户邮箱、密码、重复密码、4位验证码

#### 6.1 request format

```json
{
    "email":<str>,
    "password":<str>,
    "re_password":<str>,
    "verification":<str>
}
```

#### 6.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 7. GET /account/ask_user （login required)

**Description:** 查询当前登录用户信息

#### 7.1 request format
no data

#### 7.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <user or {}>
}
```
**note:** 其中user是字典类型，具体内容如下：

```
{
    "username":<str>,
    "email":<str>
}
```


## Issue APIs

