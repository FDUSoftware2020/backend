import json, random, datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils import timezone
from .models import User, VerificationCode, Message
from .utils.verification import make_verification_code, check_verification_code, save_verification_code
from .utils.message import conduct_message

# Create your views here.

def register(request):
    ''' 实现用户注册功能，须以POST方式

    Arguments:
        request: It should contains {"username":<str>, "email":<str>, "password":<str>, "verification":<str>} in the body.
    
    Return:
        An HttpRepsonse, which contains {"err_code":<int>, "message":<str>, "data":None}
    '''

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        code = data.get("verification")
        # try registering
        if username == "" or email == "" or password == "" or code == "":
            content = {"err_code":-1, "message":"用户名、邮箱、密码或验证码为空", "data":None}
        elif User.objects.filter(username=username).exists():
            content = {"err_code":-1, "message":"该用户名已存在", "data":None}
        elif User.objects.filter(email=email).exists():
            content = {"err_code":-1, "message":"该邮箱已被注册", "data":None}
        elif not check_verification_code(email, code):
            content = {"err_code":-1, "message":"验证码错误或已过期", "date":None}
        else:
            User.objects.create(username=username, email=email, password=password)
            content = {"err_code":0, "message":"注册成功", "data":None}
    else:
        content = {"err_code":-1, "message":"请求方式错误", "data":None}

    return HttpResponse(json.dumps(content))
  

def login(request):
    ''' 实现登录功能，须以POST方式. If successful, cookie would be set.

    Arguments:
        request: It should contains {"username":<str>, "password":<str>} in the body.
    
    Return:
        An HttpRepsonse, which contains {"err_code":<int>, "message":<str>, "data":None}
    '''

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = backend_ask_user(username, password)
        if backend_ask_login_user(request):
            content = {"err_code":-1, "message":"当前已登录，请先退出登录", "data":None}
            return HttpResponse(json.dumps(content))
        elif not user:
            content = {"err_code":-1, "message":"用户名或密码错误", "data":None}
            return HttpResponse(json.dumps(content))
        else:
            cookie_value = make_cookie()
            # save cookie_value in user
            user.cookie_value = cookie_value
            user.save()
            # conduct response
            content = {"err_code":0, "message":"登录成功", "data":None}
            response = HttpResponse(json.dumps(content))
            response.set_cookie("cookie_value", cookie_value, max_age=6*60*60)  
            return response  
    else:
        content = {"err_code":-1, "message":"请求方式错误", "data":None}
        return HttpResponse(json.dumps(content))


def logout(request):
    ''' 退出登录. If successful, cookie would be deleted.

    Arguments:
        request: no data in the body
    
    Return:
        An HttpRepsonse, which contains {"err_code":<int>, "message":<str>, "data":None}
    '''
    
    if not backend_ask_login_user(request):
        content = {"err_code":-1, "message":"当前未登录", "data":None}
        return HttpResponse(json.dumps(content))
    else:
        content = {"err_code":0, "message":"成功退出登录", "data":None}
        response = HttpResponse(json.dumps(content))
        response.delete_cookie("cookie_value")
        return response


def verify(request):
    ''' 进行验证, 须以POST方式

    Arguments:
        request: It should contains {"email":<str>} in the body.
    
    Return:
        An HttpRepsonse, which contains {"err_code":<int>, "message":<str>, "data":None}
    '''

    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        if email == "":
            content = {"err_code":-1, "message":"邮箱为空", "data":None}
        else:
            code = make_verification_code()
            # save verification code
            save_verification_code(email, code)
            # send verification email
            subject = "FSDN论坛"
            message = "欢迎使用FSDN论坛！您本次操作的验证码是{}。此验证码10分钟内有效。".format(code)
            send_mail(subject, message, "fdc_forum@163.com", [email], fail_silently=False)
            # conduct the content
            content = {"err_code":0, "message":"成功发送验证码", "data":None}
    else:
        content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(content))


def modify_password(request):
    ''' 修改密码, 须以POST方式

    Arguments:
        request: It should contains {"email":<str>, "password":<str>, "verification":<str>} in the body.
    
    Return:
        An HttpRepsonse, which contains {"err_code":<int>, "message":<str>, "data":None}
    '''

    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        code = data.get("verification")
        if email == "" or password == "" or code == "":
            content = {"err_code":-1, "message":"邮箱、密码或验证码为空", "data":None}
        elif not check_verification_code(email, code):
            content = {"err_code":-1, "message":"验证码错误或过期", "data":None}
        else:
            if not User.objects.filter(email=email).exists():
                content = {"err_code":-1, "message":"该邮箱无对应用户", "data":None}
            else:
                user = User.objects.filter(email=email)[0]
                user.password = password
                user.save()
                content = {"err_code":0, "message":"密码修改成功", "data":None}
    else:
        content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(content))


def modify_username(request):
    ''' 修改用户名, 须以POST方式

    Arguments:
        request: It should contains {"username":<str>} in the body.
    
    Return:
        An HttpRepsonse, which contains {"err_code":<int>, "message":<str>, "data":None}
    '''

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        user = backend_ask_login_user(request)
        if not user:
            content = {"err_code":-1, "message":"当前未登录", "data":None}
        elif username == "":
            content = {"err_code":-1, "message":"用户名为空", "data":None}
        elif User.objects.filter(username=username).exists():
            content = {"err_code":-1, "message":"该用户名已存在", "data":None}
        else:
            user.username = username
            user.save()
            content = {"err_code":0, "message":"用户名修改成功", "data":None}
    else:
        content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(content))


def modify_signature(request):
    ''' 个性签名, 须以POST方式

    Arguments:
        request: It should contains {"signature":<str>} in the body.
    
    Return:
        An HttpRepsonse, which contains {"err_code":<int>, "message":<str>, "data":None}
    '''

    if request.method == "POST":
        content = json.loads(request.body)
        signature = content.get("signature")
        user = backend_ask_login_user(request)
        if not user:
            content = {"err_code":-1, "message":"当前未登录", "data":None}
        else:
            user.signature = signature
            user.save()
            content = {"err_code":0, "message":"个性签名修改成功", "data":None}
    else:
        content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(content))


def ask_user(request):
    ''' 查询用户信息，仅返回非安全相关信息

    Arguments:
        request: It should contains {"username":<str>} in the body.
    
    Return:
        An HttpRepsonse, which contains {"err_code":<int>, "message":<str>, "data":user}
    '''
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        if not User.objects.filter(username=username).exists():
            content = {"err_code":-1, "message":"该用户名不存在", "data":None}
        else:
            obj = User.objects.filter(username=username)[0]
            user = {"username":obj.username, "email":obj.email, "signature":obj.signature, "contribution":obj.contribution}
            content = {"err_code":0, "message":"成功查询用户信息", "data":user}
    else:
        content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
    return HttpResponse(json.dumps(content))


def ask_login_user(request):
    ''' 查询当前登录用户，仅用于前端处理

    Return:
        An HttpRepsonse, which contains {"err_code":<int>, "message":<str>, "data":user or None}
    '''

    obj = backend_ask_login_user(request)
    if not obj:
        content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        content = {"err_code":0, "message":"查询成功", "data":obj.username}
    return HttpResponse(json.dumps(content))
    

def message_list(request):
    ''' 获取消息通知列表，兼具删除过期通知消息
    '''
    user = backend_ask_login_user(request)
    if not user:
        content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        obj_list = user.rec_msg.all().order_by('-pub_date')
        msg_list = []
        for o in obj_list:
            # 超过30天则自动删除
            if timezone.now() > o.pub_date + datetime.timedelta(days=30):
                o.delete()
            # 已读且超过7天则自动删除
            elif o.IsReading and timezone.now() > o.pub_date + datetime.timedelta(days=7):
                o.delete()
            else:
                msg = conduct_message(o)
                msg_list.append(msg)
        content = {"err_code":0, "message":"消息获取成功", "data":msg_list}
    return HttpResponse(json.dumps(content))


def message_read(request, msg_id):
    ''' 将某条消息标记为已读
    '''
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        try:
            msg = Message.objects.get(id=msg_id)
            if msg.receiver == user:
                msg.IsReading = True
                msg.save()
                response_content = {"err_code":0, "message":"成功标记已读", "data":None}
            else:
                response_content = {"err_code":-1, "message":"您不是该通知消息的接收者，无法标记", "data":None}
        except Message.DoesNotExist:
            response_content = {"err_code":-1, "message":"该通知消息不存在", "data":None}
    
    return HttpResponse(json.dumps(response_content))


def message_delete(request, msg_id):
    ''' 删除某条消息
    '''
    user = backend_ask_login_user(request)
    if not user:
        response_content = {"err_code":-1, "message":"当前未登录", "data":None}
    else:
        try:
            msg = Message.objects.get(id=msg_id)
            if msg.receiver == user:
                msg.delete()
                response_content = {"err_code":0, "message":"消息已删除", "data":None}
            else:
                response_content = {"err_code":-1, "message":"您不是该消息的接收者，无法删除", "data":None}
        except Message.DoesNotExist:
            response_content = {"err_code":-1, "message":"该消息不存在", "data":None}
    
    return HttpResponse(json.dumps(response_content))


# some assist functions

def make_cookie():
    ''' 随机生成长度为50的cookie value
    '''

    cookie_value = ""
    for i in range(50):
        cookie_value += str(random.randint(0, 9))
    return cookie_value


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


def backend_ask_user(username, password):
    ''' 若存在返回相应的用户，否则返回None

    Arguments:
        username: 用户名或邮箱地址
        password: 密码
    '''
    if User.objects.filter(username=username, password=password).exists():
        return User.objects.filter(username=username, password=password)[0]
    elif User.objects.filter(email=username, password=password).exists():
        return User.objects.filter(email=username, password=password)[0]
    else:
        return None

