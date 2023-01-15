# WjAdmin/app/api/user.py
from app.models import User
from app.utils import error


def test(request, data, resp):
    resp['hello'] = 'world'
    return resp


# 注册接口
def register(request, data, resp):
    username = data.get('username')
    password = data.get('password')
    if not all([username, password]):
        return error.REQ_PARAMS_ERROR
    try:
        User.objects.create(username=username, password=password)
    except:
        return error.USERNAME_EXISTS
    return resp


# 登录接口
def login(request, data, resp):
    username = data.get('username')
    password = data.get('password')
    if not all([username, password]):
        return error.REQ_PARAMS_ERROR
    user = User.objects.filter(username=username).first()
    if not user:
        return error.USER_NOT_FOUND
    if user.password != password:
        return error.USER_PASSWORD_ERROR
    request.session["username"] = username
    return resp


# 登出接口
def logout(request, data, resp):
    del request.session['username']
    return resp