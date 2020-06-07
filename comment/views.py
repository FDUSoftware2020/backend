from django.shortcuts import render
import json
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from account.models import User, Message
from issue.models import Issue, Answer
from .models import Comment
from account.utils.message import create_message

# Create your views here.


def comment_create(request):
    """
    new comment.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        from_user = backend_ask_login_user(request)
        pub_date = timezone.now()
        if not from_user:
            response_content = {"err_code": -1, "message": "当前未登录", "data": None}
        else:
            type = int(data.get("target_type"))
            object_id = int(data.get("target_id"))
            to_user = None
            content_object = None
            parent_comment_id = int(data.get("parent_comment_id"))
            if parent_comment_id == -1:
                parent_comment = None
            else:
                parent_comment = Comment.objects.get(id=parent_comment_id)
            if type == 1:  # article
                content_object = Issue.objects.get(id=object_id)
                to_user = content_object.author
            elif type == 2:  # answer
                content_object = Answer.objects.get(id=object_id)
                to_user = content_object.replier
            elif type == 3:
                content_object = Comment.objects.get(id=object_id)
                to_user = content_object.from_id
            content = data.get("content")
            comment = Comment(from_id=from_user, to_id=to_user, pub_date=pub_date, content=content,
                                   content_object=content_object, parent_comment=parent_comment)
            comment.save()
            create_message_for_comment(type, comment)
            response_content = {"err_code": 0, "message": "发布成功", "data": None}
    else:
        response_content = {"err_code": -1, "message": "请求方式错误", "data": None}
    return HttpResponse(json.dumps(response_content))


def comment_delete(request, comment_id):
    """
    delete one comment by id
    :param request:
    :param comment_id:
    :return:
    """
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code": -1, "message": "当前未登录", "data": None}
    else:
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.from_id == user:
                comment.delete()
                response_content = {"err_code": 0, "message": "删除成功", "data": None}
            else:
                response_content = {"err_code": -1, "message": "您不是发布者，无法删除", "data": None}
        except Comment.DoesNotExist:
            response_content = {"err_code": -1, "message": "该评论不存在", "data": None}

    return HttpResponse(json.dumps(response_content))


def comment_detail(request, comment_id):
    """
    Display the detail of a comment.
    :param request:
    :param comment_id:
    :return:
    """
    try:
        comment = Comment.objects.get(id=comment_id)
        user = backend_ask_login_user(request)
        obj = conduct_detail_comment(comment, user)
        response_content = {"err_code": 0, "message": "查询成功", "data": obj}
    except Comment.DoesNotExist:
        response_content = {"err_code": -1, "message": "该评论不存在", "data": None}
    return HttpResponse(json.dumps(response_content))


def comment_list(request):
    """
    fetch all comments of a target(article, answer, even comment)
    :param request:
    :param target_id:
    :return:
    """
    if request.method == "POST":
        data = json.loads(request.body)
        target_type = int(data.get("target_type"))
        target_id = int(data.get("target_id"))
        issue_ct = ContentType.objects.get_for_model(Issue)
        answer_ct = ContentType.objects.get_for_model(Answer)
        if target_type == 1:
            try:
                user = backend_ask_login_user(request)
                obj_list = []
                for comment in Comment.objects.filter(content_type=issue_ct, object_id=target_id).order_by("-pub_date"):
                    obj = conduct_detail_comment(comment, user)
                    obj_list.append(obj)
                response_content = {"err_code": 0, "message": "查询成功", "data": obj_list}
            except Issue.DoesNotExist:
                response_content = {"err_code": -1, "message": "该文章不存在", "data": None}
        elif target_type == 2:
            try:
                user = backend_ask_login_user(request)
                obj_list = []
                for comment in Comment.objects.filter(content_type=answer_ct, object_id=target_id).order_by("-pub_date"):
                    obj = conduct_detail_comment(comment, user)
                    obj_list.append(obj)
                response_content = {"err_code": 0, "message": "查询成功", "data": obj_list}
            except Answer.DoesNotExist:
                response_content = {"err_code": -1, "message": "该回答不存在", "data": None}
        elif target_type == 3:
            try:
                user = backend_ask_login_user(request)
                obj_list = []
                for comment in Comment.objects.filter(parent_comment=target_id).order_by("-pub_date"):
                    obj = conduct_detail_comment(comment, user)
                    obj_list.append(obj)
                response_content = {"err_code": 0, "message": "查询成功", "data": obj_list}
            except Comment.DoesNotExist:
                response_content = {"err_code": -1, "message": "该评论不存在", "data": None}
        else:
            response_content = {"err_code": -1, "message": "查询错误", "data": None}
    else:
        response_content = {"err_code": -1, "message": "请求方式错误", "data": None}
    return HttpResponse(json.dumps(response_content))


def comment_like(request, comment_id):
    """
    like or dislike a comment
    :param request:
    :param comment_id:
    :return:
    """
    try:
        comment = Comment.objects.get(id=comment_id)
        user = backend_ask_login_user(request)
        if not user:
            response_content = {"err_code": -1, "message": "当前未登录", "data": None}
        elif len(comment.likers.filter(id=user.id)) == 0:
            comment.likers.add(user)
            response_content = {"err_code": 0, "message": "点赞成功", "data": None}
        else:
            comment.likers.remove(user)
            response_content = {"err_code": 0, "message": "已取消点赞", "data": None}
    except Comment.DoesNotExist:
        response_content = {"err_code": -1, "message": "该评论不存在", "data": None}
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


def conduct_detail_comment(comment, user):
    """
    Conduct detail comment instance.
    :param comment:
    :param user:
    :return:
    """
    id = comment.id
    from_user_name = comment.from_id.username
    to_user_name = comment.to_id.username
    pub_date = str(comment.pub_date)
    content = comment.content
    like_num = comment.likers.count()
    if not user:
        IsLiking = False
    else:
        IsLiking = not (len(comment.likers.filter(id=user.id)) == 0)
    return {
        "id": id,
        "from": from_user_name,
        "to": to_user_name,
        "pub_date": pub_date,
        "content": content,
        "like_num": like_num,
        "IsLiking": IsLiking,
    }


def create_message_for_comment(Type, comment):
    ''' 为评论新建通知消息
    Arguments:
        Type: 1, 对文章添加评论；2，对回答添加评论；3，对评论添加评论
    '''
    issue_ct = ContentType.objects.get_for_model(Issue)
    answer_ct = ContentType.objects.get_for_model(Answer)

    if comment.content_type == issue_ct:
        create_message(Message.MsgType.CommentToArticle, comment)
    elif comment.content_type == answer_ct:
        create_message(Message.MsgType.CommentToAnswer, comment)
    elif comment.parent_comment:
        if comment.parent_comment.content_type == issue_ct:
            create_message(Message.MsgType.CommentToArticle, comment)
        elif comment.parent_comment.content_type == answer_ct:
            create_message(Message.MsgType.CommentToAnswer, comment)
