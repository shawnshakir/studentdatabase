from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'minor'

# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = %s AND passwords = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            if account['username']>='5000':
            #Redirect to professor homepage if username is over 5000
                return redirect(url_for('professor'))
            else:
            # Redirect to student home page
                return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = "Incorrect username/password"
    # Show the login form with message (if any)
    return render_template("index.html", msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythonlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE student_id =(SELECT student_id FROM login WHERE username = %s)', [session['username']])
        students= cursor.fetchone()
        return render_template("home.html", students=students)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythonlogin/profesor - this will be the professor home page, only accessible for loggedin users
@app.route('/pythonlogin/professor')
def professor():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM professors WHERE professor_id =(SELECT professor_id FROM login WHERE username = %s)', [session['username']])
        professors= cursor.fetchone()
        return render_template("professor.html", professors=professors)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



# http://localhost:5000/pythonlogin/coures - this will be the courses page, only accessible for loggedin students
@app.route('/pythonlogin/courses')
def courses():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # x=session['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM s_semesters WHERE student_id =(SELECT student_id FROM login WHERE username = %s)',
                       [session['username']])
        courses = cursor.fetchone()
        return render_template("courses.html", courses=courses)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythonlogin/profcourses - this will be the professors cousrses that they are teaching page, only accessible for loggedin professors
@app.route('/pythonlogin/profcourses')
def profcourses():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM p_semesters WHERE professor_id =(SELECT professor_id FROM login WHERE username = %s)',
                       [session['username']])
        profcourses = cursor.fetchone()
        return render_template("profcourses.html", profcourses=profcourses)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythonlogin/studentsinclass - this will be the students that are listed in each course page, only accessible for loggedin professors
@app.route('/pythonlogin/studentsinclass')
def studentsinclass():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM p_semesters WHERE professor_id =(SELECT professor_id FROM login WHERE username = %s)',
            [session['username']])
        profcourses = cursor.fetchone()
        cursor.execute('SELECT * FROM students WHERE student_id IN (SELECT student_id FROM s_semesters WHERE course_1 = %s OR course_2=%s OR course_3=%s OR course_4=%s OR course_5=%s)',[[profcourses['course_1']],[profcourses['course_1']],[profcourses['course_1']],[profcourses['course_1']],[profcourses['course_1']]])
        mysql.connection.commit()
        studentsinclass=cursor.fetchall()
        return render_template("studentsinclass.html", studentsinclass=studentsinclass, profcourses=profcourses)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythonlogin/studentsinclass2 - this will be the students that are listed in each course page, only accessible for loggedin professors
@app.route('/pythonlogin/studentsinclass2')
def studentsinclass2():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM p_semesters WHERE professor_id =(SELECT professor_id FROM login WHERE username = %s)',
            [session['username']])
        profcourses = cursor.fetchone()
        cursor.execute('SELECT * FROM students WHERE student_id IN (SELECT student_id FROM s_semesters WHERE course_1 = %s OR course_2=%s OR course_3=%s OR course_4=%s OR course_5=%s)',[[profcourses['course_2']],[profcourses['course_2']],[profcourses['course_2']],[profcourses['course_2']],[profcourses['course_2']]])
        mysql.connection.commit()
        studentsinclass=cursor.fetchall()
        return render_template("studentsinclass2.html", studentsinclass=studentsinclass, profcourses=profcourses)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythonlogin/studentsinclass3 - this will be the students that are listed in each course page, only accessible for loggedin professors
@app.route('/pythonlogin/studentsinclass3')
def studentsinclass3():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM p_semesters WHERE professor_id =(SELECT professor_id FROM login WHERE username = %s)',
            [session['username']])
        profcourses = cursor.fetchone()
        cursor.execute('SELECT * FROM students WHERE student_id IN (SELECT student_id FROM s_semesters WHERE course_1 = %s OR course_2=%s OR course_3=%s OR course_4=%s OR course_5=%s)',[[profcourses['course_3']],[profcourses['course_3']],[profcourses['course_3']],[profcourses['course_3']],[profcourses['course_3']]])
        mysql.connection.commit()
        studentsinclass=cursor.fetchall()
        return render_template("studentsinclass3.html", studentsinclass=studentsinclass, profcourses=profcourses)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythonlogin/search - this will be the page that logged in students can search for available classes
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'loggedin' in session:

        #if request.method == "POST":
        if request.method == 'POST' and 'search' in request.form:
            search = request.form['search']
            # search by course code
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * from courses WHERE course_code like %s", [search])
            mysql.connection.commit()
            data = cursor.fetchall()


                #all in the search box will return all the tuples
            if len(data) == 0 and search == 'all':
                cursor.execute("SELECT * from courses")
                mysql.connection.commit()
                data = cursor.fetchall()
            return render_template('search.html', data=data)

        return render_template('search.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/drop/<students_id>/<course_code>', methods=['POST'])
def drop(students_id,course_code):
    print(students_id)
    print(course_code)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from s_semesters where student_id = %s", [students_id])
    result_set=cursor.fetchall()
    for row in result_set:
        c_1=("{Name}".format(Name=row['course_1']))
        c_2=("{Name}".format(Name=row['course_2']))
        c_3=("{Name}".format(Name=row['course_3']))
        c_4=("{Name}".format(Name=row['course_4']))
        c_5=("{Name}".format(Name=row['course_5']))

    if (c_1 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_1 = '' where student_id = %s ", [students_id])
    elif (c_2 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_2 = '' where student_id = %s ", [students_id])
    elif (c_3 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_3 = '' where student_id = %s ", [students_id])
    elif (c_4 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_4 = '' where student_id = %s ", [students_id])
    elif (c_5 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_5 = '' where student_id = %s ", [students_id])
    else:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM p_semesters WHERE professor_id =(SELECT professor_id FROM login WHERE username = %s)',[session['username']])
    profcourses = cursor.fetchone()
    cursor.execute('SELECT * FROM students WHERE student_id IN (SELECT student_id FROM s_semesters WHERE course_1 = %s OR course_2=%s OR course_3=%s OR course_4=%s OR course_5=%s)',[[profcourses['course_1']],[profcourses['course_1']],[profcourses['course_1']],[profcourses['course_1']],[profcourses['course_1']]])
    mysql.connection.commit()
    studentsinclass=cursor.fetchall()
    return render_template("studentsinclass.html", studentsinclass=studentsinclass, profcourses=profcourses)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/drop2/<students_id>/<course_code>', methods=['POST'])
def drop2(students_id,course_code):
    print(students_id)
    print(course_code)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from s_semesters where student_id = %s", [students_id])
    result_set=cursor.fetchall()
    for row in result_set:
        c_1=("{Name}".format(Name=row['course_1']))
        c_2=("{Name}".format(Name=row['course_2']))
        c_3=("{Name}".format(Name=row['course_3']))
        c_4=("{Name}".format(Name=row['course_4']))
        c_5=("{Name}".format(Name=row['course_5']))

    if (c_1 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_1 = '' where student_id = %s ", [students_id])
    elif (c_2 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_2 = '' where student_id = %s ", [students_id])
    elif (c_3 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_3 = '' where student_id = %s ", [students_id])
    elif (c_4 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_4 = '' where student_id = %s ", [students_id])
    elif (c_5 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_5 = '' where student_id = %s ", [students_id])
    else:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM p_semesters WHERE professor_id =(SELECT professor_id FROM login WHERE username = %s)',[session['username']])
    profcourses = cursor.fetchone()
    cursor.execute('SELECT * FROM students WHERE student_id IN (SELECT student_id FROM s_semesters WHERE course_1 = %s OR course_2=%s OR course_3=%s OR course_4=%s OR course_5=%s)',[[profcourses['course_2']],[profcourses['course_2']],[profcourses['course_2']],[profcourses['course_2']],[profcourses['course_2']]])
    mysql.connection.commit()
    studentsinclass=cursor.fetchall()
    return render_template("studentsinclass2.html", studentsinclass=studentsinclass, profcourses=profcourses)



# http://localhost:5000/python/logout - this will be the logout page
@app.route('/drop3/<students_id>/<course_code>', methods=['POST'])
def drop3(students_id,course_code):
    print(students_id)
    print(course_code)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from s_semesters where student_id = %s", [students_id])
    result_set=cursor.fetchall()
    for row in result_set:
        c_1=("{Name}".format(Name=row['course_1']))
        c_2=("{Name}".format(Name=row['course_2']))
        c_3=("{Name}".format(Name=row['course_3']))
        c_4=("{Name}".format(Name=row['course_4']))
        c_5=("{Name}".format(Name=row['course_5']))

    if (c_1 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_1 = '' where student_id = %s ", [students_id])
    elif (c_2 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_2 = '' where student_id = %s ", [students_id])
    elif (c_3 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_3 = '' where student_id = %s ", [students_id])
    elif (c_4 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_4 = '' where student_id = %s ", [students_id])
    elif (c_5 == course_code):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update s_semesters set course_5 = '' where student_id = %s ", [students_id])
    else:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM p_semesters WHERE professor_id =(SELECT professor_id FROM login WHERE username = %s)',[session['username']])
    profcourses = cursor.fetchone()
    cursor.execute('SELECT * FROM students WHERE student_id IN (SELECT student_id FROM s_semesters WHERE course_1 = %s OR course_2=%s OR course_3=%s OR course_4=%s OR course_5=%s)',[[profcourses['course_3']],[profcourses['course_3']],[profcourses['course_3']],[profcourses['course_3']],[profcourses['course_3']]])
    mysql.connection.commit()
    studentsinclass=cursor.fetchall()
    return render_template("studentsinclass3.html", studentsinclass=studentsinclass, profcourses=profcourses)