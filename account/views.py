import json, random
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import User, VerificationCode

# Create your views here.

def register(request):
    ''' 实现用户注册功能，须以POST方式

    Arguments:
       request: It should contains {"username":<str>, "password":<str>} in the body.
    
    Return:
        HttpRepsonse, which contains {"err_code":<int>, "message":<str>} as below
         0 --> 注册成功
        -1 --> 注册失败, message是相关错误信息
    '''

    if request.method == "POST":
        content = json.loads(request.body)
        username = content.get("username")
        password = content.get("password")
        if username == "" or password == "":
            content = {"err_code":-1, "message":"用户名或密码为空"}
        elif User.objects.filter(username=username).exists():
            content = {"err_code":-1, "message":"该用户名已存在"}
        else:
            User.objects.create(username=username, password=password)
            content = {"err_code":0, "message":"注册成功"}
    else:
        content = {"err_code":-1, "message":"请求方式错误"}

    return HttpResponse(json.dumps(content))
    

def login(request):
    ''' 实现登录功能，须以POST方式. If successful, cookie would be set.

    Arguments:
       request: It should contains {"username":<str>, "password":<str>} in the body.
    
    Return:
        HttpRepsonse, which contains {"err_code":<int>, "message":<str>} as below
         0 --> 登录成功
        -1 --> 登录失败, message是相关错误信息
    '''

    if request.method == "POST":
        content = json.loads(request.body)
        username = content.get("username")
        password = content.get("password")
        if User.objects.filter(username=username, password=password).exists():
            cookie_value = make_cookie()
            # save cookie_value in user
            user = User.objects.get(username=username, password=password)
            user.cookie_value = cookie_value
            user.save()
            # conduct response
            content = {"err_code":0, "message":"登录成功"}
            response = HttpResponse(json.dumps(content))
            response.set_cookie("cookie_value", cookie_value, max_age=6*60*60)  
            return response
        else:
            content = {"err_code":-1, "message":"用户名或密码错误"}
            return HttpResponse(json.dumps(content))
    else:
        content = {"err_code":-1, "message":"请求方式错误"}
        return HttpResponse(json.dumps(content))


def logout(request):
    ''' 退出登录

    Arguments:
        request: no data in the body
    
    Return:
        An empty HtttpResponse, whose cookie is deleted.
    '''
    
    response = HttpResponse()
    response.delete_cookie("cookie_value")
    return response


def verify(request):
    ''' 对于注册过程，生成、发送、保存验证码, 须以POST方式

    Arguments:
        request: It should contains {"email":<str>} in the body
    
    Return:
        An empty HttpResponse
    '''

    if request.method == "POST":
        content = json.loads(request.body)
        email = content.get("email")
        code = make_verification_code()
        # save to Verification
        VerificationCode.create(email=email, code=code)
        # send email
        subject = "FSDN论坛"
        message = "欢迎使用FSDN论坛，您本次操作的验证码是{}。此验证码十分钟内有效。".format(code)
        send_mail(subject, message, "fdc_forum@163.com", [email], fail_silently=False)

    return HttpResponse()



# some assist functions

def make_cookie(length = 50):
    ''' 随机生成cookie value

    Arguments:
        length: 生成随机字符串的长度
    
    Return:
        生成的随机字符串，即cookie value
    '''

    cookie_value = ""
    for i in range(length):
        cookie_value += str(random.randint(0, 9))
    return cookie_value


def make_verification_code():
    ''' 随机生成4位验证码
    '''

    code = ""
    for i in range(4):
        code += str(random.randint(0, 9))
    return code


def ask_user(request):
    ''' 查询当前登录用户

    Return:
        已登录时，返回登录对象即an object of class User;
        未登录时，返回None
    '''

    cookie_value = request.COOKIES.get("cookie_value")
    if not cookie_value:
        return None
    else:
        user = User.objects.get(cookie_value=cookie_value)
        if not user:
            return None
        else:
            return user
