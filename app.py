import sqlalchemy
from model import session
from model import School
from model import Information
from model import Person
from model import Home
from flask import Flask
from flask import request
from flask import jsonify
from pymysql import err
app = Flask(__name__)

def insert_data(name, cno, age, sex, sno, major, grade, sd, province, address, tele, pnum, QQ, wx, email):
    try:
        session.execute(f"call insert_data('{name}', {cno}, {age}, '{sex}', '{sno}', '{major}', '{grade}', '{sd}', '{province}', '{address}', '{tele}', '{pnum}', '{QQ}', '{wx}', '{email}');")
    except:
        session.rollback()
        return (100, '插入失败，记录已存在')
    else:
        return (0, '插入成功')


# insert_data('李书翔',0,100,'男','20171002141','计算机科学与技术','大二','25#203','湖南','永州','1218899','13974696387','372505855','lelexia','lishuxiang@cug.edu.cn')
@app.route('/add', methods=['POST'])
def addRecord():
    name = request.form.get('name')
    age = int(request.form.get('age'))
    cno = int(request.form.get('cno'))
    sex = request.form.get('sex')
    sno = request.form.get('sno')
    major = request.form.get('major')
    grade = request.form.get('grade')
    sd = request.form.get('sd')
    province = request.form.get('province')
    address = request.form.get('address')
    tele = request.form.get('tele')
    pnum = request.form.get('pnum')
    QQ = request.form.get('QQ')
    wx = request.form.get('wx')
    email = request.form.get('email')
    code, msg = insert_data(name,cno,age,sex,sno,major,grade,sd,province,address,tele,pnum,QQ,wx,email)
    ret = {
        'code': code,
        'msg': msg
    }
    return jsonify(ret)

@app.route('/update', methods=['POST'])
def updateRecord():
    name = request.form.get('name')
    age = int(request.form.get('age'))
    old_cno = int(request.form.get('old_cno'))
    new_cno = int(request.form.get('new_cno'))
    sex = request.form.get('sex')
    sno = request.form.get('sno')
    major = request.form.get('major')
    grade = request.form.get('grade')
    sd = request.form.get('sd')
    province = request.form.get('province')
    address = request.form.get('address')
    tele = request.form.get('tele')
    pnum = request.form.get('pnum')
    QQ = request.form.get('QQ')
    wx = request.form.get('wx')
    email = request.form.get('email')
    person = session.query(Person).filter(Person.cno == old_cno).first()
    home = session.query(Home).filter(Home.cno == old_cno).first()
    information = session.query(Information).filter(Information.cno == old_cno).first()
    school = session.query(School).filter(School.cno == old_cno).first()
    home.province = province
    home.address = address
    home.tele = tele
    information.pnum = pnum
    information.QQ = QQ
    information.wx = wx
    information.email = email
    school.sno = sno
    school.major = major
    school.grade = grade
    school.sd = sd
    person.cno = new_cno
    person.name = name
    person.age = age
    person.sex = sex
    code = 0
    msg = ''
    try:
        session.commit()
    except:
        code = 100
        msg = '修改失败'
        session.rollback()
    else:
        code = 0
        msg = '修改成功'
    ret = {
        'code': code,
        'msg': msg
    }
    return jsonify(ret)

@app.route('/delete', methods=['POST'])
def deletePerson():
    cno = int(request.form.get('cno'))
    person = session.query(Person).filter(Person.cno == cno).first()
    if person is not None:
        session.delete(person)
        session.commit()
    ret = {
        'code': 0,
        'msg': '删除成功'
    }
    return jsonify(ret)

@app.route('/get', methods=['POST'])
def getRecord():
    ret={}
    array=[]
    persons = session.query(Person).all()
    for person in persons:
        info={}
        cno = person.cno
        info['cno'] = cno
        info['name'] = person.NAME
        info['age'] = person.age
        info['sex'] = person.sex
        home = session.query(Home).filter(Home.cno == cno).first()
        info['province'] = home.province
        info['address'] = home.address
        info['tele'] = home.tele
        information = session.query(Information).filter(Information.cno == cno).first()
        info['pnum'] = information.pnum
        info['QQ'] = information.QQ
        info['wx'] = information.wx
        info['email'] = information.email
        school = session.query(School).filter(School.cno == cno).first()
        info['sno'] = school.sno
        info['major'] = school.major
        info['grade'] = school.grade
        info['sd'] = school.sd
        array.append(info)
    ret['code'] = 0
    ret['data'] = array
    return jsonify(ret)