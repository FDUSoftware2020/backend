import json
from django.http import HttpResponse
from django.utils import timezone
from account.models import User
from .models import Issue, Answer

# Create your views here.

def create(request):
    ''' 创建一个新Issue
    '''
    if request.method == "POST":
        data = json.loads(request.body)
        Type = int(data.get("type"))
        title = data.get("title")
        author = backend_ask_login_user(request)
        pub_date = timezone.now()
        content = data.get("content")
        if not author:
            response_content = {"err_code":-1, "message":"当前未登录", "data":None}
        else:
            Issue.objects.create(Type=Type, title=title, author=author, pub_date=pub_date, content=content)
            response_content = {"err_code":0, "message":"发布成功", "data":None}
    else:
        response_content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def delete(request, issue_id):
    ''' 删除某个Issue
    '''
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        try:
            issue = Issue.objects.get(id=issue_id)
            if issue.author == user:
                issue.delete()
                response_content = {"err_code":0, "message":"删除成功", "data":None}
            else:
                response_content = {"err_code":-1, "message":"您不是发布者，无法删除", "data":None}
        except Issue.DoesNotExist:
            response_content = {"err_code":-1, "message":"该问题/文章不存在", "data":None}

    return HttpResponse(json.dumps(response_content))


def detail(request, issue_id):
    ''' 显示某个Issue的详细内容
    '''
    try:
        issue = Issue.objects.get(id=issue_id)
        user = backend_ask_login_user(request)
        obj = conduct_detail_issue(issue, user)
        response_content = {"err_code":0, "message":"查询成功", "data":obj}
    except Issue.DoesNotExist:
        response_content = {"err_code":-1, "message":"该问题/文章不存在", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def search(request):
    ''' 搜寻Issue
    '''
    if request.method == "POST":
        data = json.loads(request.body)
        keyword = data.get("keyword")
        issue_list = Issue.objects.filter(title__icontains=keyword).order_by('title')
        obj_list = []
        for issue in issue_list:
            obj = conduct_brief_issue(issue)
            obj_list.append(obj)
        response_content = {"err_code":0, "message":"查询成功", "data":obj_list}
    else:
        response_content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def collect(request, issue_id):
    '''收藏或取消收藏某个Issue
    '''
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        try:
            issue = Issue.objects.get(id=issue_id)
            if len(issue.collectors.filter(id=user.id)) != 0:
                issue.collectors.remove(user)
                response_content = {"err_code":0, "message":"已取消收藏", "data":None}
            else:
                issue.collectors.add(user)
                response_content = {"err_code":0, "message":"收藏成功", "data":None}
        except Issue.DoesNotExist:
            response_content = {"err_code":-1, "message":"该问题/文章不存在", "data":None}

    return HttpResponse(json.dumps(response_content))


def collection_list(request):
    ''' 获取登录用户的收藏列表
    '''
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        obj_list = []
        for issue in user.issue_set.all().order_by('title'):
            obj = conduct_brief_issue(issue)
            obj_list.append(obj)
        response_content = {"err_code":0, "message":"查询成功", "data":obj_list}

    return HttpResponse(json.dumps(response_content))


def issue_like(request, issue_id):
    ''' 对某个Issue点赞/取消点赞
    '''
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        try:
            issue = Issue.objects.get(id=issue_id)
            if len(issue.likers.filter(id=user.id)) != 0:
                issue.likers.remove(user)
                response_content = {"err_code":0, "message":"已取消点赞", "data":None}
            else:
                issue.likers.add(user)
                response_content = {"err_code":0, "message":"点赞成功", "data":None}
        except Issue.DoesNotExist:
            response_content = {"err_code":-1, "message":"该问题/文章不存在", "data":None}

    return HttpResponse(json.dumps(response_content))



# some assist functions

def backend_ask_login_user(request):
    ''' 查询当前登录用户，仅用于后端处理

    Return:
        已登录时，返回登录对象即an object of class User;
        未登录时，返回None
    '''

    cookie_value = request.COOKIES.get("cookie_value")
    if not cookie_value:
        return None
    else:
        if not User.objects.filter(cookie_value=cookie_value).exists():
            return None
        else:
            return User.objects.filter(cookie_value=cookie_value)[0]


def conduct_detail_issue(issue, user):
    ''' 构造详细版Issue实例
    '''
    # static data
    ID = issue.id
    Type = issue.Type
    title = issue.title
    author = issue.author.username
    pub_date = str(issue.pub_date)[0:16]
    content = issue.content
    collect_num = issue.collectors.count()
    like_num = issue.likers.count()
    # dynamic data
    if not user:
        IsCollecting = False
        IsLiking = False
    else:
        IsCollecting = not (len(issue.collectors.filter(id=user.id)) == 0)
        IsLiking = not (len(issue.likers.filter(id=user.id)) == 0)
    
    return {"id":ID, "type":Type, "title":title, "author":author, "pub_date":pub_date, "content":content, \
            "collect_num":collect_num, "like_num":like_num, "IsCollecting":IsCollecting, "IsLiking":IsLiking}


def conduct_brief_issue(issue):
    ''' 构造简洁版Issue实例
    '''
    return {"id":issue.id, "type":issue.Type, "title":issue.title, "author":issue.author.username, "pub_date":str(issue.pub_date)[0:16], \
            "collect_num":issue.collectors.count(), "like_num":issue.likers.count()}