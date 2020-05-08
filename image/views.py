import os
import json
from django.utils import timezone
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from account.models import User

# Create your views here.

# HOST = "http://127.0.0.1:8000"
HOST = "http://182.92.131.202:8000"


def upload(request):
    ''' 图片上传
    '''
    if request.method == "POST":
        user = backend_ask_login_user(request)
        if not user:
            response_content = {"err_code":-1, "message":"当前未登录", "data":None}
        else:
            files_list = request.FILES
            index_list = files_list.keys()
            url_list = {}
            for img_index in index_list:
                img_file = files_list[img_index]
                img_name = timezone.now().strftime('%Y%M%d%H%M%S%f') + ".jpg"
                if all([img_index, img_file]):
                    f = open(os.path.join(settings.UPLOAD_ROOT, img_name), 'wb')
                    for i in img_file.chunks():
                        f.write(i)
                    f.close()
                img_url = HOST + "/uploads/" + img_name
                url_list[img_index] = img_url
            response_content = {"err_code":0, "message":"图片上传成功", "data":url_list}
    else:
        response_content = {"err_code":-1, "message":"请求方式错误", "data":None}
    
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
