# WjAdmin/app/utils/error.py 错误信息定义

SYSTEM_ERROR = {
    'code': 99,
    'msg': '系统运行错误'
}
USER_CHECK_FAIL = {
    'code': 100,
    'msg': '身份验证失败，请重新登录'
}
API_ERROR = {
    'code': 101,
    'msg': 'api有误'
}
REQ_PARAMS_ERROR = {
    'code': 102,
    'msg': '请求参数有误'
}
UPDATE_VERSION = {
    'code': 103,
    'msg': '请更新到最新版本'
}
REQ_TYPE_ERROR = {
    'code': 104,
    'msg': '请求方式有误'
}
USER_NOT_FOUND = {
    'code': 105,
    'msg': '用户不存在'
}
PERMISSION_DENIED = {
    'code': 106,
    'msg': '权限不足'
}
RESP_DATA_ERROR = {
    'code': 107,
    'msg': '返回数据有误'
}
CONTENT_NOT_FOUND = {
    'code': 404,
    'msg': '内容未找到'
}
NETWORK_ERROR = {
    'code': 901,
    'msg': '网络错误'
}
USERNAME_EXISTS = {
    'code': 601,
    'msg': '用户名已存在'
}
USER_PASSWORD_ERROR = {
    'code': 602,
    'msg': '账号或密码错误'
}
WJ_NOT_PUBLISH = {
    'code': 603,
    'msg': '问卷未发布'
}
ERROR_ANSWER_MUST_QUESTION = {
    'code': 603,
    'msg': '有必填题目未作答'
}