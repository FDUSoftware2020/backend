from ..models import VerificationCode


def make_verification_code():
    ''' 随机生成4位验证码
    '''

    code = ""
    for i in range(4):
        code += str(random.randint(0, 9))
    return code


def save_verification_code(email, code):
    ''' 保存验证码，email不可为空
    '''

    if not VerificationCode.objects.filter(email=email).exists():
        VerificationCode.objects.create(email=email, code=code, make_time=timezone.now())
    else:
        obj = VerificationCode.objects.filter(email=email)[0]
        obj.code = code
        obj.make_time = timezone.now()
        obj.save()


def check_verification_code(email, code):
    ''' 核对验证码
    
    Returns:
        If the code is error or out of date, return false; otherwise, return true
    '''

    if not VerificationCode.objects.filter(email=email).exists():
        return False
    else:
        obj = VerificationCode.objects.filter(email=email)[0]
        if obj.code != code or timezone.now() > obj.make_time + datetime.timedelta(minutes=10):
            return False
        else:
            return True
