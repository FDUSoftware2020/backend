# FSDN web API (草案)

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

-   [Account APIs](#Account-APIs)
    -   [1. POST /account/register/](#1-post-accountregister)
    -   [2. POST /account/login/](#2-post-accountlogin)
    -   [3. GET /account/logout/](#3-get-accountlogout)
	-   [4. POST /account/verify/](#4-post-accountverify)
	-   [5. POST /account/modify_password/](#5-post-accountmodify_password)
	-   [6. POST /account/modify_username/](#6-post-accountmodify_username)
	-   [7. POST /account/modify_signature/](#7-post-accountmodify_signature)
    -   [8. GET /account/ask_login_user/](#7-get-accountask_login_user)
	-   [9. POST /account/ask_user/](#9-post-accountask_user)
	-   [10. GET /account/message/list/](#10-get-accountmessagelist)
	-   [11. GET /account/message/&lt;int:msg_id&gt;/read/](#11-get-accountmessage&lt;int:msg_id&gt;read)
	-   [12. GET /account/message/&lt;int:msg_id&gt;/delete/](#12-get-accountmessage&lt;int:msg_id&gt;delete)
-   [Issue APIs](#Issue-APIs)
    -   [1. POST /issue/create/](#1-post-issuecreate)
    -   [2. GET /issue/&lt;int:issue_id&gt;/delete/](#2-get-issue&lt;int:issue_id&gt;delete)
	-   [3. GET /issue/&lt;int:issue_id&gt;/detail/](#3-get-issue&lt;int:issue_id&gt;detaile)
	-   [4. POST /issue/search/](#4-post-issuesearch)
	-   [5. GET /issue/&lt;int:issue_id&gt;/collect/](#5-get-issue&lt;int:issue_id&gt;collect)
	-   [6. GET /issue/collection_list/](#6-get-issuecollection_list)
	-   [7. GET /issue/publication_list/](#7-get-issuepublication_list)
	-   [8. GET /issue/&lt;int:issue_id&gt;/like/](#8-get-issue&lt;int:issue_id&gt;like)
	-   [9. POST /issue/&lt;int:issue_id&gt;/answer/create/](#9-post-issue&lt;int:issue_id&gt;answercreate)
	-   [10. GET /issue/answer/&lt;int:answer_id&gt;/delete/](#10-get-issueanswer&lt;int:answer_id&gt;delete)
	-   [11. GET /issue/answer/&lt;int:answer_id&gt;/detail/](#11-get-issueanswer&lt;int:answer_id&gt;detail)
	-   [12. GET /issue/&lt;int:issue_id&gt;/answer_list/](#12-get-issue&lt;int:issue_id&gt;answer_list)
    -   [13. GET /issue/answer/&lt;int:answer_id&gt;/like/](#13-get-issueanswer&lt;int:answer_id&gt;like)
-   [Comment APIs](#Comment-APIs)
    -   [1. POST /comment/create/](#1-post-commentcreate)
	-   [2. GET /comment/&lt;int:comment_id&gt;/delete/](#2-get-comment&lt;int:comment_id&gt;delete)
	-   [3. GET /comment/&lt;int:comment_id&gt;/detail/](#3-get-comment&lt;int:comment_id&gt;detail)
	-   [4. POST /comment/list/](#4-post-commentlist)
	-   [5. GET /comment/&lt;int:comment_id&gt;/like/](#5-get-comment&lt;int:comment_id&gt;like)
-   [Image APIs](#Image-APIs)
    -   [1. POST /image/upload/](#1-post-imageupload)

## Preface

* starshine在编写api.md草案时惊觉Issue和Article在数据结构、操作逻辑上有着较高的相似度，为避免重复造轮子，尝试将Article并入Issue中，增加字段Type用于区分。在此文档中Issue对象泛指问题（issue）和文章（article），进而形成如下APIs。

* 在下述APIs中，若err_code为-1，则data一律为空，即no data。

* 凡是以登录为前提的操作，后端实现中会包含检测是否登录的逻辑。以创建问题为例，在调用相应API发送问题的内容时，若未登录，则不会创建问题，此时返回err_code=-1，message是类似于“当前未登录”的提示语句。

* pub_date的格式是“Y-M-D h:m"，一个例子是："2019-05-24 14:36"

* 不足之处：Issue暂时未考虑标签



## Account APIs

定义用户相关的APIs，具体有：注册、登录、登出、验证、修改密码、修改用户名、查询用户信息

### 1. POST /account/register/

**Description:** 注册一个新用户

#### 1.1 request format

```json
{
    "username": <str, 用户名>,
    "password": <str, 密码>,
    "email": <str, 邮箱>,
    "verification": <str, 4位验证码>
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

### 2. POST /account/login/

**Description:** 用户登录

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

### 3. GET /account/logout/

**Description:** 用户退出登录，须处于登录状态

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

### 4. POST /account/verify/

**Description:** 发送验证码

#### 4.1 request format

```json
{
    "email": <str>
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

### 5. POST /account/modify_password/

**Description:** 修改密码

#### 5.1 request format

```json
{
    "email": <str>,
    "password": <str>,
    "verification": <str>
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

### 6. POST /account/modify_username/

**Description:** 修改用户名，须处于登录状态

#### 6.1 request format

```json
{
    "username": <str>
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

### 7. POST /account/modify_signature/

**Description:** 修改个性签名，须处于登录状态

#### 7.1 request format

```json
{
    "signature": <str>
}
```

#### 7.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 8. GET /account/ask_login_user/

**Description:** 查询当前登录用户用户名，须处于登录状态

#### 8.1 request format

no data

#### 8.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <str, 即username>
}
```
**Note:** 若当前无登录用户，则err_code=-1，此时data为空，即no data.

### 9. POST /account/ask_user/

**Description:** 查询任意用户信息

#### 9.1 request format

```json
{
    "username": <str>
}
```

#### 9.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <user>
}
```

**Note:** 其中user是字典类型，如下：

```
{
    "username": <str, 用户名>,
    "email": <str, 邮箱>,
	"signature": <str, 个性签名>,
	"contribution": <int, 贡献值>
}
```

### 10. GET/account/message/list/

**Description:** 获取通知消息列表，须处于登录状态

#### 10.1 request format

no data

#### 10.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": a list of 'message'
}
```

**note:** message是消息的结构体，字典类型，具体字段如下。有五种消息：问题新增回答、文章新增评论、回答新增评论

* 问题新增回答：type = 1, issue_id是被回答的问题；answer_id是该新增回答；parent_comment_id = comment_id = -1
* 文章新增评论：type = 2, issue_id是被评论的文章；answer_id = -1；若新增一级评论，则parent_comment_id = -1，否则parent_comment_id是新增评论所属一级评论；comment_id是该新增评论
* 回答新增评论：type = 3, issue_id是对应问题；answer_id是对应回答；若新增一级评论，则parent_comment_id = -1，否则parent_comment_id是新增评论所属一级评论；comment_id是该新增评论

```
{
	"msg_id": <int, 消息的id>,
    "type": <int, 消息类型>,
	"issue_id": <int>,
	"answer_id": <int>,
	"parent_comment_id": <int>,
	"comment_id": <int>,
	"from": <str, 回复者的用户名>,
	"pub_date": <str, 回复时间>,
	"content": <text, 后端自组织内容，描述行为>,
    "IsReading": <bool, 是否已读>
}
```

**Note:** 返回的消息列表按时间排序，最新者在前。


### 11. GET /account/message/&lt;int:msg_id&gt;/read/

**description:** 将某条通知消息标记为已读，须处于登录状态

#### 11.1 request format

no data

#### 11.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 12. GET /account/message/&lt;int:msg_id&gt;/delete/

**description:** 删除某条通知消息，须处于登录状态

#### 12.1 request format

no data

#### 12.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

**Note:** 后端自带删除功能，已读消息7天后自动删除，未读消息30天后自动删除。


## Issue APIs

定义Issue相关的APIs，具体有：
* 创建Issue、删除Issue、获取Issue详细信息、搜索Issue、Issue的收藏/取消收藏、查询收藏列表、Issue的点赞/取消点赞
* 创建Answer、删除Answer、获取回答列表、Answer的点赞/取消点赞

### 1. POST /issue/create/

**Description:** 创建一个新Issue，须处于登录状态

#### 1.1 request format

```json
{
	"type": <int, 0指问题, 1指文章>
	"title": <str, 标题>, 
    "content": <str, 详细内容>
}
```

#### 1.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <int, id of the new issue when it is successful>
}
```

### 2. GET /issue/&lt;int:issue_id&gt;/delete/

**Description:** 删除某个Issue，须处于登录状态且该Issue是由该用户发起的

#### 2.1 request format

no data

#### 2.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 3. GET /issue/&lt;int:issue_id&gt;/detail/

**Description:** 获取某个Issue的详细信息

#### 3.1 request format

no data

#### 3.2 response format

```json
{
    "err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <issue>
}
```

**Note:** 其中issue是字典类型，包含内容如下所示。

```
{
	"id": <int>,
	"type": <int, 1指问题, 2指文章>,
	"title": <str, 标题>,
	"author": <str, 作者用户名>,
	"pub_date": <str, 发布时间>,
	"content": <str, 详细内容>
	"collect_num": <int, 收藏人数>,
    "like_num": <int, 点赞数>,
	"IsCollecting": <bool, True表示当前用户已收藏, False表示未收藏, 未登录时默认False>,
	"IsLiking":  <bool, True表示当前用户已点赞, False表示未点赞, 未登录时默认False>
}
```

### 4. POST /issue/search/

**Description:** 根据输入的关键词，搜索相关Issues

#### 4.1 request format

```json
{
	"keyword": <str, 输入的搜索词>
}
```

#### 4.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <brief_issue_list>
}
```

**Note:** 搜索的结果可能含有大量的Issue对象，直接返回Issue的全部内容须耗费较多带宽。因此，返回brief_issue_list即brief_issue的列表,其中brief_issue是字典类型，结构与上文的issue一致，区别在于issue的content字段含有全部内容，而brief_issue的content字段仅含有原文的一小段首文字。注意：后端默认排序方式是title的字符顺序，故提供其他字段以便前端改变排序方式。


### 5. GET /issue/&lt;int:issue_id&gt;/collect/

**Description:** 收藏/取消收藏某个issue，须处于登录状态。

#### 5.1 request format

no data

#### 5.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 6. GET /issue/collection_list/

**Description:** 获取当前登录用户收藏的Issue列表，须处于登录状态。

#### 6.1 request format

no data

#### 6.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <brief_issue_list>
}
```

### 7. GET /issue/publication_list/

**Description:** 获取当前登录用户发布的Issue列表，须处于登录状态。

#### 7.1 request format

no data

#### 7.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <brief_issue_list>
}
```

### 8. GET /issue/&lt;int:issue_id&gt;/like/

**Description:** 点赞/取消点赞某个issue，须处于登录状态。

#### 8.1 request format

no data

#### 8.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 9. POST /issue/&lt;int:issue_id&gt;/answer/create/

**Description:** 新建对某个Issue的回答，其中issue_id指明是哪个issue，须处于登录状态

#### 9.1 request format

```json
{
	"content": <str, 回答的内容>
}
```

#### 9.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 10. GET /issue/answer/&lt;int:answer_id&gt;/delete/

**Description:** 删除某个回答，其中answer_id指明是哪个answer，须处于登录状态

#### 10.1 request format

no data

#### 10.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 11. GET /issue/answer/&lt;int:answer_id&gt;/detail

**Description:** 获取某个answer的详细信息

#### 11.1 request format

no data

#### 11.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <answer>
}
```

**Note:** 其中answer是字典类型，如下所示。

```
{
    "id": <int>,
	"author": <str, 回答者的用户名>,
	"pub_date": <str, 回答时间>,
	"content": <str, 回答的内容>,
	"like_num": <int, 点赞数>,
	"IsLiking": <bool, True表示当前用户已点赞, False表示未点赞, 未登录时默认False>,
	"comment_num": <int, 评论数目>
}
```

### 12. GET /issue/&lt;int:issue_id&gt;/answer_list/

**Description:** 获取某个Issue的回答列表

#### 12.1 request format

no data

#### 12.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <answer_list>
}
```

**Note:** answer_list即answer的列表，默认按照pub_date排序，最新者在前。

### 13. GET /issue/answer/&lt;int:answer_id&gt;/like/

**Description:** 对某个answer点赞/取消点赞，其中answer_id指明是哪个answer，须处于登录状态

#### 13.1 request format

no data

#### 13.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```


## Comment APIs

定义Comment相关APIs, 具体有：创建评论、删除评论、获取评论详情、获取评论列表、对评论点赞/取消点赞

### 1. POST /comment/create/

**Description:** 创建一条新评论，须处于登录状态

#### 1.1 request format

```json
{
	"target_type": <int, 1指article, 2指answer, 3指comment>,
	"target_id": <int, 目标的ID>,
    "parent_comment_id": <int, 所属父评论（一级评论）的id,如本身为一级评论则传入-1>,
	"content": <str, 评论的详细内容>
}
```

**Note:** 由于可以对Article、Answer、Comment三者进行评论，因此需要使用target_type加以区分。

#### 1.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 2. GET /comment/&lt;int:comment_id&gt;/delete/

**Description:** 删除一条评论，须处于登录状态，且该评论由该用户发布

#### 2.1 request format

no data

#### 2.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

### 3. GET /comment/&lt;int:comment_id&gt;/detail/

**Description:** 获取一条评论的详细信息

#### 3.1 request format

no data

#### 3.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <comment>
}
```

**Note:** 其中comment是字典类型，包含内容如下：

```
{
	"id": <int>,
	"from": <str, 发送方>,
	"to": <str, 接收方>,
	"pub_date": <str, 发布时间>,
	"content": <str, 内容>,
	"like_num": <str, 点赞数>,
	"IsLiking": <bool, True表示当前用户已点赞, False表示未点赞, 未登录时默认False>
}
```

### 4. POST /comment/list/

**Description:** 获取评论列表，返回对应target下所有评论（含套娃形式的评论）

#### 4.1 request format

```json
{
	"target_type": <int, 1指article, 2指answer, 3指comment>,
	"target_id": <int, 目标的ID>
}
```

**Note:** 由于可以对Article、Answer、Comment三者进行评论，因此需要使用target_type加以区分。

注意：此处如果是对Article或者Answer获取评论，则会返回所有的一级评论。

如果是对Comment获取评论，返回的是以该comment作为父评论的所有评论。

因此，对于一篇回答或者文章，需要先获取一级评论，然后对每条一级评论获取各自的所有二级评论。

>   形如：
>
>   -   Article A
>       -   一级评论11 reply to Article A
>           -   二级评论21 reply to 一级评论11
>           -   二级评论22 reply to 二级评论21
>
>   对于评论11来说，target_type是1，target_id是Article A 的id, parent_comment_id = -1
>
>   而对于评论21来说，target_type是3，target_id是一级评论11的id, parent_comment_id = 11的id
>
>   而对于评论22来说，target_type是3，target_id是二级评论21的id, parent_comment_id = 11的id

#### 4.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <comment_list>
}
```

**Note:** comment_list即comment对象的列表。至于列表内是否“良好排序”，待定。


### 5. GET /comment/&lt;int:comment_id&gt;/like/

**Description:** 对某条评论点赞/取消点赞，须处于登录状态

#### 5.1 request format

no data

#### 5.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <no data>
}
```

## Image APIs

### 1. POST /image/upload/

**Description:** 单批次统一上传一组图片，后端进行存储，并返回这些图片的url。

### 1.1 request format

```
{
    img_index_1: img_file_1,
	img_index_2: img_file_2,
	...
}
```

**note:** 图片组须直接以formdata格式传输，外部不嵌套任何封装。

### 1.2 response format

```json
{
	"err_code": <int, 0 means success, -1 means fail>,
	"message": <str, tell user success or failure details>,
	"data": <dictionary, give url list>
}
```

**note:** data字段是字典类型，结构如下。注：img_index_i是关键字变量；img_file_i是数据文件；img_url_i是对应的url(string类型)。响应报文中的img_index_i同请求报文中的img_index_i相对应。

```
{
	img_index_1: img_url_1,
	img_index_2: img_url_2,
	...
}
```