from flask import Flask, jsonify, request, render_template
import mysql.connector
import os
import matplotlib.pyplot as plt
import base64
import mpld3
from io import BytesIO


conn = mysql.connector.connect(
    host='localhost', username='root', password='12345678', database='Project1')

app = Flask(__name__)

uno = 0
studname = ""
grade = 0
academic1 = []
academic2 = []
childnop = 0


@app.route('/')
def index():
    return render_template('Firstpage.html')


if conn.is_connected:
    print("Database connected")

else:
    print("Not connected")

    conn.commit()
    conn.close()


@app.route('/login_form', methods=['POST'])
def getValue():
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')

    my_cursor = conn.cursor(buffered=True)

    my_cursor.execute(
        "select Username,Password from user_info1 where UserType='Admin'")
    rows = my_cursor.fetchone()

    if uname == rows[0] and pwd == rows[1]:
        my_cursor.close()
        conn.close()
        return render_template('mod2.html')
    else:
        my_cursor.close()
        conn.close()
        return "Wrong Credentials"


@app.route('/next_page', methods=['GET'])
def next_page():
    return render_template('mod3.html')


@app.route('/next_page1', methods=['POST'])
def next_page1():
    return render_template('mod4.html')


@app.route('/next_page2', methods=['POST'])
def next_page2():
    return render_template('mod5.html')


@app.route('/next_page3', methods=['GET'])
def next_page3():
    return render_template('mod6.html')


@app.route('/next_page4', methods=['POST'])
def next_page4():
    conn = mysql.connector.connect(
        host='localhost', username='root', password='12345678', database='Project1')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    contact = request.form.get('contact')
    address = request.form.get('address')
    noofkids = request.form.get('noofkids')
    relation = request.form.get('relation')
    username = request.form.get('username')
    password = request.form.get('password')
    usertype = "User"
    userno = 1

    print(fname)
    my_cursor = conn.cursor()

    insert_query = "insert into user_info1(UserNo, FirstName, LastName, Email, Contact, Address, No_of_kids, UserType, Username, Password, Relation) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    my_cursor.execute(insert_query, (str(userno+1), str(fname), str(lname), str(email), str(contact),
                      str(address), str(noofkids), str(usertype), str(username), str(password), str(relation)))

    conn.commit()
    my_cursor.close()
    conn.close()


@app.route('/login_form1', methods=['POST'])
def get_value2():

    global uno
    global studname
    conn = mysql.connector.connect(
        host='localhost', username='root', password='12345678', database='Project1')

    uname = request.form.get('uname1')
    pwd = request.form.get('pwd1')

    my_cursor = conn.cursor()
    sqlst1 = "select u.UserNo,c.FirstName,c.LastName,u.FirstName,u.Username,u.Password from user_info1 as u, Child as c where u.UserNo = c.UserNo and u.Username = %s"
    my_cursor.execute(sqlst1, (uname,))
    res = my_cursor.fetchall()

    first_names = [record[1] for record in res]
    username = [record[4] for record in res]
    psd = [record[5] for record in res]

    print(first_names)
    studname = first_names
    print(res)

    sqlst2 = "select UserNo from user_info1 where Username = %s"
    my_cursor.execute(sqlst2, (uname, ))
    res1 = my_cursor.fetchone()

    uno = res1[0]

    for row in res:
        print(row)

    if not res:
        print("if")
        my_cursor.close()
        conn.close()
        return render_template("mod8.html", val=0, uname=uname)

    else:
        print("else")
        if uname == username[0] and pwd == psd[0]:
            my_cursor.close()
            conn.close()
            return render_template('mod8.html', val=1, first_names=first_names, uname=uname)
        else:
            my_cursor.close()
            conn.close()
            return "No child present you need to add a child"


@app.route('/About')
def About():
    return render_template('/About.html')


@app.route('/Contact')
def Contact():
    return render_template('/Contact.html')


@app.route('/ChildAdd')
def ChildAdd():
    return render_template('/ChildAdd.html')


@app.route('/mod9', methods=['GET', 'POST'])
def mod9():

    global grade
    global studname
    global academic1
    global childnop

    conn = mysql.connector.connect(
        host='localhost', username='root', password='12345678', database='Project1')

    mystr = request.args.get('input', )
    print(mystr)
    print(type(mystr))

    # str2 = str(mystr)
    # print("mystr is " + str2)

    studname = mystr

    my_cursorf = conn.cursor()
    sqlstatement = "select Grade, ChildNo from Child where FirstName=%s"

    my_cursorf.execute(sqlstatement, (mystr, ))
    result = my_cursorf.fetchone()

    print("Executing SQL statement: " + sqlstatement)
    print("Parameters: " + str((mystr,)))

    print("Query result: " + str(result))

    my_cursorf.close()
    conn.commit()
    conn.close()

    if result is not None:
        print("if")
        grade = result[0]
        print(grade)
        childno1 = result[1]
        print(childno1)
        childnop = childno1
        conn = mysql.connector.connect(
            host='localhost', username='root', password='12345678', database='Project1')
        my_cursorf = conn.cursor()
        sqlstatement2 = "select SubjectName, Marks, ExamDate from Subject where Childno = %s"
        my_cursorf.execute(sqlstatement2, (childno1, ))
        result2 = my_cursorf.fetchmany(size=5)

        if result2 is not None:
            academic1 = result2
            for i in result2:
                print(i[0])
                print(i[1])
                print(i[2])
            print("Fetch")
        else:
            print("None")
        return render_template("mod9.html")
    else:
        print("else")
        grade = None
        return render_template("mod9.html")


@app.route('/childform', methods=['POST'])
def childform():

    conn = mysql.connector.connect(
        host='localhost', username='root', password='12345678', database='Project1')
    fname = request.form.get('firstName')
    lname = request.form.get('lastName')
    dob = request.form.get('dob')
    wt = request.form.get('wt')
    ht = request.form.get('ht')
    grade = request.form.get('grade')

    my_cursor = conn.cursor()
    query1 = "select max(ChildNo) from Child"
    my_cursor.execute(query1)
    res = my_cursor.fetchone()
    childno = res[0]
    # print(childno)
    print(uno)

    insert_query = "insert into Child(ChildNo,FirstName,LastName,DOB,wt,ht,Grade,UserNo) values (%s,%s,%s,%s,%s,%s,%s,%s)"

    my_cursor.execute(insert_query, (str(childno+1), str(fname),
                      str(lname), str(dob), str(wt), str(ht), str(grade), str(uno)))

    # query2 = "select UserNo from user_info1 where UserName=%s"

    # my_cursor.execute(query2, (uname11,))
    # res1 = my_cursor.fetchone()
    # userno = res1[0]
    # print(userno)

    conn.commit()
    my_cursor.close()
    conn.close()

    return "One child added"


@app.route('/mod11', methods=['GET', 'POST'])
def mod11():

    global grade
    global studname
    global academic1

    return render_template("mod11.html", grade=grade, studname=studname, academic1=academic1)


@app.route('/mod12', methods=['GET'])
def mod12():

    global studname
    global academic2
    global childnop

    conn = mysql.connector.connect(
        host='localhost', username='root', password='12345678', database='Project1')

    selected_value = request.args.get('value')

    print(f"Selected value = ", selected_value)

    my_cursor = conn.cursor()
    query2 = "select SubjectName, Marks, ExamDate from Subject where Year(ExamDate) = %s and ChildNo = %s"

    my_cursor.execute(query2, (selected_value, childnop, ))

    result3 = my_cursor.fetchmany(size=5)

    if result3 is not None:
        academic2 = result3
        for j in result3:
            print(j[0])
            print(j[1])
            print(j[2])
            print("Academic2 Fetch")
        else:
            print("None")
            return render_template("mod12.html", grade=grade, studname=studname, academic2=academic2)
    else:
        print("else")
        return render_template("mod12.html", grade=grade, studname=studname, academic2=academic2)


@app.route('/mod13', methods=['GET', 'POST'])
def mod13():
    global academic2
    global grade
    global studname

    return render_template("mod13.html", studname=studname, grade=grade, academic2=academic2)


@app.route('/bargraphsubject', methods=['GET', 'POST'])
def bargraphsubject():

    global studname
    global childnop

    conn = mysql.connector.connect(
        host='localhost', username='root', password='12345678', database='Project1')

    my_cursor = conn.cursor()

    selected_value1 = request.args.get('value2')

    print(f"Selected value in bargraphsubject = ", selected_value1)

    subjectName = "Maths"

    myquery2 = "select SubjectName, Marks from Subject where Year(ExamDate) = %s and Childno=%s and SubjectName=%s;"

    my_cursor.execute(myquery2, (selected_value1, childnop, subjectName, ))

    result4 = my_cursor.fetchmany(size=10)

    mydata = []

    if result4 is not None:
        for i in result4:
            mydata.append(i[1])

    print("Mydata is ", mydata)

    subjectName = "Science"

    myquery3 = "select SubjectName, Marks from Subject where Year(ExamDate) = %s and Childno=%s and SubjectName=%s;"

    my_cursor.execute(myquery3, (selected_value1, childnop, subjectName, ))

    result5 = my_cursor.fetchmany(size=10)

    mydata1 = []

    if result5 is not None:
        for i in result5:
            mydata1.append(i[1])

    print("Mydata1 is ", mydata1)

    subjectName = "PE"

    myquery4 = "select SubjectName, Marks from Subject where Year(ExamDate) = %s and Childno=%s and SubjectName=%s;"

    my_cursor.execute(myquery4, (selected_value1, childnop, subjectName, ))

    result6 = my_cursor.fetchmany(size=10)

    mydata2 = []

    if result6 is not None:
        for i in result6:
            mydata2.append(i[1])

    print("Mydata1 is ", mydata2)

    return render_template("bargraphsubject.html", studname=studname, mydata=mydata, mydata1=mydata1, mydata2=mydata2)


if __name__ == '__main__':
    app.run(debug=True)
