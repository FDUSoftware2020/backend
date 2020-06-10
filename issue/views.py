import json
from django.http import HttpResponse
from django.utils import timezone
from .models import Issue, Answer
from account.models import User, Message
from comment.models import Comment
from account.utils.message import create_message

# Create your views here.

def issue_create(request):
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
            issue = Issue(Type=Type, title=title, author=author, pub_date=pub_date, content=content)
            issue.save()
            response_content = {"err_code":0, "message":"发布成功", "data":issue.id}
    else:
        response_content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def issue_delete(request, issue_id):
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


def issue_detail(request, issue_id):
    ''' 显示某个Issue的详细内容
    '''
    try:
        issue = Issue.objects.get(id=issue_id)
        user = backend_ask_login_user(request)
        obj = conduct_issue(issue, user)
        response_content = {"err_code":0, "message":"查询成功", "data":obj}
    except Issue.DoesNotExist:
        response_content = {"err_code":-1, "message":"该问题/文章不存在", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def issue_search(request):
    ''' 搜寻Issue
    '''
    if request.method == "POST":
        data = json.loads(request.body)
        keyword = data.get("keyword")
        if keyword == "":
            issue_list = Issue.objects.all().order_by('-pub_date')[:10]
        else:
            issue_list = Issue.objects.filter(title__icontains=keyword).order_by('title')
        user = backend_ask_login_user(request)
        obj_list = []
        for issue in issue_list:
            obj = conduct_issue(issue, user, brief=True)
            obj_list.append(obj)
        response_content = {"err_code":0, "message":"查询成功", "data":obj_list}
    else:
        response_content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def issue_collect(request, issue_id):
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


def issue_collection_list(request):
    ''' 获取登录用户的收藏列表
    '''
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        obj_list = []
        for issue in user.collect_issue.all().order_by('title'):
            obj = conduct_issue(issue, user, brief=True)
            obj_list.append(obj)
        response_content = {"err_code":0, "message":"查询成功", "data":obj_list}

    return HttpResponse(json.dumps(response_content))


def issue_publication_list(request):
    ''' 获取登录用户的发布列表
    '''
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        obj_list = []
        for issue in user.create_issue.all().order_by('title'):
            obj = conduct_issue(issue, user, brief=True)
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


def answer_create(request, issue_id):
    ''' 对某个Issue新建一个回答
    '''
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        user = backend_ask_login_user(request)
        if not user:
            response_content = {"err_code":-1, "message":"当前未登录", "data":None}
        else:
            try:
                issue = Issue.objects.get(id=issue_id)
                if issue.Type != Issue.IssueType.ISSUE:
                    response_content = {"err_code":-1, "message":"无法对文章进行回答", "data":None}
                else:
                    answer = Answer(issue=issue, replier=user, pub_date=timezone.now(), content=content)
                    answer.save()
                    create_message(Message.MsgType.AnswerToIssue, answer)
                    response_content = {"err_code":0, "message":"回答已发布", "data":None}
            except Issue.DoesNotExist:
                response_content = {"err_code":-1, "message":"该问题不存在", "data":None}
    else:
        response_content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def answer_delete(request, answer_id):
    ''' 删除某个answer
    '''
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        try:
            answer = Answer.objects.get(id=answer_id)
            if answer.replier == user:
                answer.delete()
                response_content = {"err_code":0, "message":"回答已删除", "data":None}
            else:
                response_content = {"err_code":-1, "message":"您不是该回答的发布者，无法删除", "data":None}
        except Answer.DoesNotExist:
            response_content = {"err_code":-1, "message":"该回答不存在", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def answer_detail(request, answer_id):
    ''' 获取某个Answer的详细数据
    '''
    try:
        answer = Answer.objects.get(id=answer_id)
        user = backend_ask_login_user(request)
        obj = conduct_detail_answer(answer, user)
        response_content = {"err_code":0, "message":"查询成功", "data":obj}
    except Answer.DoesNotExist:
        response_content = {"err_code":-1, "message":"该回答不存在", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def answer_list(request, issue_id):
    ''' 获取某个Issue的回答列表
    '''
    try:
        issue = Issue.objects.get(id=issue_id)
        user = backend_ask_login_user(request)
        obj_list = []
        for answer in issue.answer_set.all().order_by("-pub_date"):
            obj = conduct_detail_answer(answer, user)
            obj_list.append(obj)
        response_content = {"err_code":0, "message":"查询成功", "data":obj_list}
    except Issue.DoesNotExist:
        response_content = {"err_code":-1, "message":"该问题不存在", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def answer_like(request, answer_id):
    ''' 对某个回答点赞/取消点赞
    '''
    try:
        answer = Answer.objects.get(id=answer_id)
        user = backend_ask_login_user(request)
        if not user:
            response_content = {"err_code":-1, "message":"当前未登录", "data":None}
        elif len(answer.likers.filter(id=user.id)) == 0 :
            answer.likers.add(user)
            response_content = {"err_code":0, "message":"点赞成功", "data":None}
        else:
            answer.likers.remove(user)
            response_content = {"err_code":0, "message":"已取消点赞", "data":None}
    except Answer.DoesNotExist:
        response_content = {"err_code":-1, "message":"该回答不存在", "data":None}
    
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


def conduct_issue(issue, user, brief=False):
    ''' 构造Issue实例，其中brief控制是否是简洁版
    '''
    # static data
    ID = issue.id
    Type = issue.Type
    title = issue.title
    author = issue.author.username
    pub_date = str(issue.pub_date)[0:16]
    if brief:
        content = issue.content[0:50] + "......"
    else:
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


def compute_comment_num_of_answer(answer):
    ''' 统计an answer下的评论数目
    '''
    C1_list = Comment.objects.filter(object_id=answer.id)
    comment_num = len(C1_list)
    for c1 in C1_list:
        comment_num += Comment.objects.filter(parent_comment=c1.id).count()
    return comment_num


def conduct_detail_answer(answer, user):
    ''' 构造详细版Answer实例
    '''
    ID = answer.id
    author = answer.replier.username
    pub_date = str(answer.pub_date)[0:16]
    content = answer.content
    like_num = answer.likers.count()
    if not user:
        IsLiking = False
    else:
        IsLiking = not (len(answer.likers.filter(id=user.id)) == 0)
    comment_num = compute_comment_num_of_answer(answer)

    return {"id":ID, "author":author, "pub_date":pub_date, "content":content, \
            "like_num":like_num, "IsLiking":IsLiking, "comment_num":comment_num}