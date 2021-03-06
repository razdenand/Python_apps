from app import app
from flask import render_template, request, redirect, url_for, session
from Classes import *
import requests
import random
import smtplib
import time

answer3 = 0
key = 1
ans = ['answer', 'answer1', 'answer2']
answer = ['a3', 'b1', 'c1']
values = 1
true_vals = 0
que = 0
final = []

@app.route('/main', methods=['GET'])
def main():
    return render_template('base.html')


@app.route('/add', methods=["POST"])
def add():
    data = request.form['add']
    db.q_fetchall("insert into kek (name, phone) values('{0}', '134');".format(data))
    return redirect(url_for('total'))


@app.route('/dele', methods=["POST"])
def dele():
    data = request.form['del']
    db.q_fetchall("delete from kek where name='{0}'".format(data))
    return redirect(url_for('total'))


@app.route('/lol', methods=["POST"])
def lol():
    data = request.form['lol']


@app.route('/total', methods=['GET'])
def total():
    query = db.q_fetchall('select * from kek;')
    final_list = []
    for x in query:
        final_list.append(x['name'])
    return render_template('show_val.html', posts=final_list)


@app.route('/question', methods=["POST"])
def question():
    buf = 0
    try:
        for a in request.form:
            if request.form[a] in answer:
                buf += 1
                print(request.form[a])
        return render_template('index.html', ans=buf)
    except Exception as ex:
        return render_template('index.html', ans=str(ex))


@app.route('/hm', methods=["POST"])
def hm():
    data = requests.get('http://cppquiz.org/static/published.json').json()
    data2 = request.form.get('kek')
    id = request.form.get('id')
    question = data['questions'][int(id)]['question']
    answer = data['questions'][int(id)]['result']
    answer1 = data['questions'][int(id)]['answer']
    lol = question.split('\r\n')
    global true_vals
    global que
    que += 1
    pob = ''
    res = request.form.get('additional')
    if answer == 'OK' and answer == data2:
        if res == data['questions'][int(id)]['answer']:
            true_vals += 1
            ans = db.q_fetchall('select count(*) as k from quest;')
            pob = 'Верно!'
            value = ans[0]['k'] - 1
            final.append(value)
        else:
            pob = 'Неверно!'
    elif answer != 'OK' and answer == data2:
        ans = db.q_fetchall('select count(*) as k from quest;')
        value = ans[0]['k'] - 1
        final.append(value)
        true_vals += 1
        pob = 'Верно!'
    else:
        pob = 'Неверно!'
    if session['visits'] < 11:
        req_data = {'answer': data['questions'][int(id)]['result'],
                    'explanation': data['questions'][int(id)]['explanation']}
        if pob == 'Верно!':
            return render_template('buf.html', val=session['visits'], pob=pob)
        else:
            return render_template('buf.html', answer=req_data['answer'], exp=req_data['explanation'],
                                   val=session['visits'], pob=pob,
                                   tr=true_vals, id=id, answer1=answer1)
    else:
        return render_template('final.html', val=f"Вы правильно ответили на {true_vals} из 10 вопросов:", mass=final)


@app.route('/', methods=["GET", "POST"])
def mainn():
    global true_vals
    global values
    global final
    final = []
    true_vals = 0
    db.q_fetchall('delete from quest;')
    values = 0
    data = requests.get('http://cppquiz.org/static/published.json').json()
    for i in range(10):
        is_in_table = True
        while is_in_table == True:
            lole = random.randint(0, 124)
            if db.q_fetchall('select id from quest where id={}'.format(lole)) == ():
                is_in_table = False
                question = data['questions'][lole]['question']
                lol = question.split('\r\n')
                # session['question'][i] = lol
                # session['id'][i] = lole
    session['visits'] = 0
    return render_template('main.html')


@app.route('/quiz', methods=["POST", "GET"])
def quiz():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # чтение и обновление данных сессии
    else:
        session['visits'] = 1  # настройка данных сессии
    data = requests.get('http://cppquiz.org/static/published.json').json()
    is_in_table = True
    while is_in_table:
        lole = random.randint(0, 124)
        if db.q_fetchall('select id from quest where id={}'.format(lole)) == ():
            is_in_table = False

    global values
    global true_vals
    global que
    values += 1
    if values == 12:
        values = 1
        true_vals = 0

    count = db.q_fetchall('select count(id) from quest;')
    if count[0]['count(id)'] == 10:
        db.q_fetchall('delete from quest;')
    db.q_fetchall('insert into quest (id) values({})'.format(lole))
    question = data['questions'][lole]['question']
    id = data['questions'][lole]['id']
    lol = question.split('\r\n')
    username = request.args.get('id')
    data2 = request.form.get('kek')
    if session['visits'] < 11:
        return render_template("q2.html", key=lol, id=lole, val=session['visits'])
    else:
        return render_template('final.html', val=f"Вы правильно ответили на {true_vals} из 10 вопросов:", mass=final)


@app.route('/buf', methods=["POST", "GET"])
def buf():
    pass


@app.route('/mail', methods=["POST", "GET"])
def ans():
    global true_vals
    session['visits'] = 0
    mail = request.form.get('mail')
    if mail != '' and '@' in mail and '.' in mail:
        cpp_articles = 'Basic language C++ materials:\n' \
                       'Stroustrup: The C++ Programming Language (4th Edition)\n' \
                       'https://ru.cppreference.com/w/ - website with basic C ++ documentation\n' \
                       'Specialization Art of development in modern C ++ - course on Coursera\n'

        smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
        smtpObj.starttls()
        smtpObj.login('noreply.2021@mail.ru', 'daniil123450705')
        smtpObj.sendmail("noreply.2021@mail.ru", "{}".format(mail), "{}".format(cpp_articles))
        smtpObj.quit()
        global values
        true_vals = 0
        values = 0
        session.pop('visits', None)
        global final
        final = []
    else:
        return render_template('final.html', message='Неправильный формат почтового ящика, повторите попытку!')

    return redirect(url_for('mainn'))


# реализовать рассылку писем
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
