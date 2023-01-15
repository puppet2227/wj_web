# WjAdmin/app/views.py
import json
import datetime
import decimal
from django.shortcuts import HttpResponse
from app.utils import error
from app.utils import my_log
from WjAdmin.settings import NO_AUTH_API
from app import api

log = my_log.log

class MyJSONEncoder(json.JSONEncoder):
    """
    将date datetime decimal类型转换为json
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, datetime.time):
            return o.strftime("%H:%M:%S")
        super(MyJSONEncoder, self).default(o)


def return_resp(resp):
    """
    返回格式化的json
    """
    s = json.dumps(resp, cls=MyJSONEncoder)
    return HttpResponse(s)

def check_no_auth(api_module, api_name):
    """
    校验不需要授权的接口
    """
    # todo 开发测试直接返回True
    return True

    no_auth = NO_AUTH_API.get(api_module, [])
    if '*' in no_auth:
        return True
    if api_name in no_auth:
        return True
    return False


def api_handle(request):
    """
    统一处理函数
    """
    if request.method != 'POST':
        return return_resp(error.REQ_TYPE_ERROR)
    path = request.path
    sub_path = path.replace('/api', '')
    try:
        api_module = sub_path.split('/')[1]
        print('api_module=', api_module)
        api_list = eval(f'dir(api.{api_module})')
    except:
        return return_resp(error.API_ERROR)
    print('api_list=', api_list)
    try:
        api_name = sub_path.split('/')[2]
        print('api_name=', api_name)
    except:
        return return_resp(error.API_ERROR)
    if api_name not in api_list:
        return return_resp(error.API_ERROR)
    # 执行api处理函数
    resp = {'code': 0, 'msg': 'success'}
    try:
        data = json.loads(request.body)
    except:
        return return_resp(error.REQ_PARAMS_ERROR)
    no_auth_flag = check_no_auth(api_module, api_name)
    if not no_auth_flag:
        user_id = request.session.get('username')
        if not user_id:
            return return_resp(error.USER_CHECK_FAIL)
        data['username'] = user_id
    try:
        log.info('请求data=%s' % data)
        log.info(f'请求api_module={api_module}，api_name={api_name}')
        resp = eval(f'api.{api_module}.{api_name}(request, data, resp)')
        log.info('resp=%s' % resp)
    except Exception as e:
        print('error', e)
        log.error('error', exc_info=True)
        return return_resp(error.SYSTEM_ERROR)
    if not resp or type(resp) != dict:
        return return_resp(error.RESP_DATA_ERROR)
    return HttpResponse(json.dumps(resp, cls=MyJSONEncoder))