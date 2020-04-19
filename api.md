# FSDN web API

>   This file describes the APIs of FSDN(Fudan Software Developer Network), helping FSDN frontend developers to work efficiently.

![](https://img.shields.io/badge/FSDN-API-brighgreen.svg)![](https://img.shields.io/badge/API-Documentation-green.svg)

**Note:** 

1.  All keys in `json`format should use `" "` other than` ' '`. 

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
-    [Account APIs](#Account APIs)
        -   [1. POST /account/register](#1-post-accountregister)
        -   [2. POST /account/login](#2-post-accountlogin)
        -   [3. GET /account/logout (login required)](#3-get-accountlogout-login-required)
-   [Passage APIs](#Passage APIs)
-   [User Actions APIs](#User Actions APIs)



## Account APIs

This part includes functions related to user account, like register, login and logout.

### 1. POST /account/register

**Description:** register a new user

#### 1.1 request format

```json
{
    "username":<str>,
    "password":<str>,
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

**Description:** user log in;

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

**Description:**  user logout, need to login first.

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



## Passage APIs



## User Actions APIs

