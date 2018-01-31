from mitmproxy import ctx
from urllib.parse import quote
import string
import pymysql as MySQLdb
import json
import requests

mysql_conn = MySQLdb.connect(host="*****",user="root",passwd="*****",db="tnwz",port=3306,charset="UTF8")
mysql_cursor = mysql_conn.cursor()

def response(flow):
    path = flow.request.path
    global quiz
    if path == '/question/bat/findQuiz':
        #读题阶段
        data = json.loads(flow.response.text)
        quiz = data
        question = data['data']['quiz']
        options = data['data']['options']
        ctx.log.info('question : %s, options : %s'%(question, options))
        options = ask(question, options)
        data['data']['options'] = options
        flow.response.text = json.dumps(data)
        return quiz
    elif path == '/question/bat/choose':
        #得到正确答案并传入数据库
        data_ans = json.loads(flow.response.text)
        answer_num = int(data_ans['data']['answer'])
        question = quiz['data']['quiz']
        right_choose = answer_num  - 1
        answer_str = sql_write(quiz,right_choose)
        ctx.log.info('answernum : %d, question: %s answer: %s' % (answer_num, question,answer_str ))



def ask(question, options):
    sql_result = sql_match_result(question)
    if sql_result:
        answer = []
        for option in options:
            if option == sql_result:
                answer.append(option + '[' + '正确'+ ']')
            else:
                answer.append(option)
        return answer
    else:
        url = quote('https://www.baidu.com/s?wd=' + question, safe=string.printable)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        content = requests.get(url, headers=headers).text
        answer = []
        for option in options:
            count = content.count(option)
            ctx.log.info('option : %s, count : %s' % (option, count))
            answer.append(option + '[' + str(count) + ']')
        return answer


def sql_match_result(question):
    #在数据库里搜索题目
    right_answer = ''
    sql_cmd = "select answer_str from quizzes where quiz = %s"
    mysql_cursor.execute(sql_cmd,question)
    results = mysql_cursor.fetchall()
    for row in results:
        right_answer = row[0]
        print("right_answer =%s" % \
              (right_answer))
        if not right_answer == '':
            return right_answer
        else:
            return False

def sql_write(quiz,right_choose):

        question = quiz['data']['quiz']
        type = quiz['data']['type']
        school = quiz['data']['type']
        answer = quiz['data']['options'][right_choose]
        answer_str = ''
        b = False
        for ch in answer:#处理后缀
            if ch == '[':
                break
            answer_str = answer_str + ch
        # for ch in answer:
        #     if ch == ']':
        #         b = True
        #     if b and ch != ']':
        #         s = s + ch

        print('将题目写入数据库中...')
        try:
            mysql_cursor.execute('insert into quizzes(type,school,quiz,answer_str) values("%s","%s","%s", "%s")'%(type,school,question, answer_str))
            mysql_conn.commit()
            print('写入成功')
        except:
            print('该问题已存在数据库中，跳过')

        return answer_str
