# WjAdmin/app/api/analysis.py
from app.models import Question, Answer
from django.db import connection
from django.db.models import Q
from app.utils import error

# 根据问题id获取统计情况
def _get_question_analysis(q_id):
    result = []
    cursor = connection.cursor()
    cursor.execute(
        'select A.id,count(B.submitId),A.title from app_options A left join app_answer B on A.id=B.answer where A.questionId=%s group by A.id' % q_id)
    rows = cursor.fetchall()
    total = 0
    for id, count, title in rows:
        total += count
    for id, count, title in rows:
        if total == 0:
            percent = 0
        else:
            percent = '%.1f' % ((count / total) * 100)
        result.append({
            'option': title,
            'count': count,
            'percent': str(percent) + '%'
        })
    print('q_id=', q_id)
    print('result=', result)
    return result


# 数据统计
def data_analysis(request, data, resp):
    wjId = data.get('wjId')
    if not wjId:
        return error.REQ_PARAMS_ERROR
    detail = []
    questions = Question.objects.filter(wjId=wjId)
    for question in questions:
        questionTitle = question.title
        questionType = question.type
        questionId = question.id
        if questionType == "radio" or questionType == "checkbox":
            result = _get_question_analysis(question.id)
        else:
            result = ''

        detail.append({
            "title": questionTitle,
            "type": questionType,
            "result": result,
            "questionId": questionId
        })
    resp['detail'] = detail
    return resp
# WjAdmin/app/api/analysis.py
# 获取文本回答详情
def get_text_answer_detail(request, data, resp):
    questionId = data.get('questionId')
    pageSize = data.get('pageSize', 10)
    currentPage = data.get('currentPage', 1)
    if not questionId:
        return error.REQ_PARAMS_ERROR
    answer = Answer.objects.filter(~Q(answerText=''), questionId=questionId, answerText__isnull=False)
    total = answer.count()
    answer = answer[(currentPage - 1) * pageSize:currentPage * pageSize]
    result = []
    for item in answer:
        result.append({'context': item.answerText})
    resp['detail'] = result
    resp['total'] = total
    return resp