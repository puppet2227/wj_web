# WjAdmin/app/api/wj.py
import datetime
from app.models import Wj, Question, Options, Submit, Answer
from app.utils import error
from django.db import transaction
from django.db.models import Q
from django.db import transaction
# WjAdmin/app/api/wj.py
# 添加修改问卷
def add_wj(request, data, resp):
    title = data.get('title')  # 问卷标题
    desc = data.get('desc')  # 问卷描述
    id = data.get('id')  # 问卷id 可为空
    username = request.session.get('username')
    if not title:
        return error.REQ_PARAMS_ERROR
    if id:
        res = Wj.objects.filter(username=username, id=id).first()
        if not res:
            return error.CONTENT_NOT_FOUND
        res.title = title
        res.desc = desc
        res.save()
    else:
        res = Wj.objects.create(username=username, title=title, desc=desc, status=0)
    resp['id'] = res.id
    return resp
# 获取问卷列表
def get_wj_list(request, data, resp):
    username = request.session.get('username')
    objs = Wj.objects.filter(username=username).order_by('-id')
    detail = []
    for item in objs:
        detail.append({
            'id': item.id,
            'title': item.title,
            'desc': item.desc,
            'status': item.status
        })
    resp['detail'] = detail
    return resp
# 删除问卷
def delete_wj(request, data, resp):
    username = request.session.get('username')
    id = data.get('id')  # 问卷id
    if not id:
        return error.REQ_PARAMS_ERROR
    # 删除问卷
    Wj.objects.filter(username=username, id=id).delete()
    objs = Question.objects.filter(wjId=id)  # 查询所有关联问题
    for item in objs:
        Options.objects.filter(questionId=item.id).delete()  # 删除问题关联的选项
    objs.delete()  # 删除问卷所有关联问题
    Submit.objects.filter(wjId=id).delete()  # 删除该问卷的提交信息
    Answer.objects.filter(wjId=id).delete()  # 删除该问题的所有回答
    return resp
# 发布问卷
def push_wj(request, data, resp):
    username = request.session.get('username')
    wjId = data.get('wj_id')
    status = data.get('status')  # 0暂停问卷 1发布问卷
    if wjId and username and status in [0, 1]:
        res = Wj.objects.filter(id=wjId, username=username)
        if res.exists():  # 该题目是此用户创建的 有权限
            res.update(status=status)
        else:  # 该题目不是此用户创建的 无权限
            return error.PERMISSION_DENIED
    else:
        return error.REQ_PARAMS_ERROR
    resp['status'] = status
    return resp
# 添加题目/更新题目
@transaction.atomic
def add_question(request, data, resp):
    username = request.session.get('username')
    wj_id = data.get('wjId')  # 问卷id
    q_info = data.get('qInfo', {})
    q_id = q_info.get('id')  # 题目id 可为空
    q_title = q_info.get('title')  # 题目标题
    q_type = q_info.get('type')  # 题目类型
    options = q_info.get('options', [])  # 选项
    must = q_info.get('must', False)  # 是否必填
    attrs = q_info.get('attrs', {})
    row = attrs.get('row')
    if not all([wj_id, q_title, q_type]):
        return error.REQ_PARAMS_ERROR
    if type(options) != list:
        return error.REQ_PARAMS_ERROR
    # 校验问卷权限
    wj = Wj.objects.filter(username=username, id=wj_id).first()
    if not wj:
        return error.PERMISSION_DENIED
    if q_id:
        # 修改题目
        newIds = []
        for temp in options:
            newIds.append(temp['id'])  # 将更新后的选项id记录
        # 把不在更新后的选项id中的选项删除
        Options.objects.filter(~Q(id__in=newIds), questionId=q_id).delete()
        # 更新题目
        Question.objects.filter(wjId=wj_id, id=q_id).update(title=q_title, type=q_type, must=must, row=row)
        # 更新选项
        for option in options:
            if option['id'] != 0:  # 选项为已有的 更新
                Options.objects.filter(questionId=q_id, id=option['id']).update(title=option['title'])
            else:  # 选项为新增的 添加
                Options.objects.create(questionId=q_id, title=option['title'])
    else:
        # 新增题目
        resObj = Question.objects.create(wjId=wj_id, title=q_title, type=q_type, row=row, must=must)
        q_id = resObj.id
        # 添加选项
        if q_type == 'radio' or q_type == 'checkbox':  # 单选或者多选
            for item in options:
                Options.objects.create(questionId=q_id, title=item['title'])
    return resp
# 删除问题
@transaction.atomic
def delete_question(request, data, resp):
    username = request.session.get('username')
    q_id = data.get('q_id')
    if not q_id:
        return error.REQ_PARAMS_ERROR
    q = Question.objects.filter(id=q_id).first()
    if not q:
        return error.CONTENT_NOT_FOUND
    q_wj_id = q.wjId  # 该题目所属的问卷id
    wj = Wj.objects.filter(id=q_wj_id).first()
    if not wj:
        return error.CONTENT_NOT_FOUND
    # 判断是否有权限删除（是否是本人创建）
    s_username = wj.username
    if s_username != username:
        return error.PERMISSION_DENIED
    Question.objects.filter(id=q_id).delete()  # 删除问题
    Options.objects.filter(questionId=q_id).delete()  # 删除关联选项
    return resp
# 获取问题列表
def get_question_list(request, data, resp):
    wj_id = data.get('wj_id')
    if not wj_id:
        return error.REQ_PARAMS_ERROR
    wj = Wj.objects.filter(id=wj_id).first()
    if not wj:
        return error.CONTENT_NOT_FOUND
    obj = Question.objects.filter(wjId=wj_id)
    detail = []
    for item in obj:
        temp = {}
        temp['title'] = item.title
        temp['type'] = item.type
        temp['id'] = item.id  # 问题id
        temp['attrs'] = {
            'row': item.row
        }
        temp['must'] = item.must
        # 获取选项
        temp['options'] = []
        if temp['type'] in ['radio', 'checkbox']:  # 如果是单选或者多选
            optionItems = Options.objects.filter(questionId=item.id)
            for optionItem in optionItems:
                temp['options'].append({'title': optionItem.title, 'id': optionItem.id})

        detail.append(temp)
    resp['detail'] = detail
    return resp
# WjAdmin/app/api/wj.py
# 获取问卷信息
def get_wj_info(request, data, resp):
    wj_id = data.get('wj_id')
    if not wj_id:
        return error.REQ_PARAMS_ERROR
    wj = Wj.objects.filter(id=wj_id).first()
    if not wj:
        return error.CONTENT_NOT_FOUND
    detail = {
        'title': wj.title,
        'desc': wj.desc,
        'status': wj.status
    }
    resp['detail'] = detail
    return resp
# WjAdmin/app/api/wj.py
# 提交问卷
def submit_wj(request, data, resp):
    wjId = data.get('wj_id')
    useTime = data.get('use_time')
    answers = data.get('answers', {})
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        ip = request.META.get('REMOTE_ADDR')
    if not wjId:
        return error.REQ_PARAMS_ERROR
    wj = Wj.objects.filter(id=wjId).first()
    if not wj:
        return error.CONTENT_NOT_FOUND
    if wj.status == 0:
        return error.WJ_NOT_PUBLISH

    # 校验必填项
    qs = Question.objects.filter(wjId=wjId)

    for q in qs:
        answer = answers.get(str(q.id))
        print('anser=',answer)
        # 校验必填题目
        if q.must:
            if q.type == 'checkbox' and str(answer) == '[]':
                return error.ERROR_ANSWER_MUST_QUESTION
            elif not answer:
                return error.ERROR_ANSWER_MUST_QUESTION

    # 记录提交信息
    submitInfo = Submit.objects.create(
        wjId=wjId,
        submitTime=datetime.datetime.now(),
        submitIp=ip,
        useTime=useTime
    )

    for q in qs:
        answer = answers.get(str(q.id))
        if q.type == 'text':
            Answer.objects.create(
                questionId=q.id,
                submitId=submitInfo.id,
                wjId=wjId,
                type=q.type,
                answerText=answer
            )
        else:
            if q.type == 'checkbox':
                for value in answer:
                    Answer.objects.create(
                        questionId=q.id,
                        submitId=submitInfo.id,
                        wjId=wjId,
                        type=q.type,
                        answer=value
                    )
            else:
                Answer.objects.create(
                    questionId=q.id,
                    submitId=submitInfo.id,
                    wjId=wjId,
                    type=q.type,
                    answer=answer
                )
    return resp
