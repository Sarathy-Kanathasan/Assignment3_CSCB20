# required imports
# the sqlite3 library allows us to communicate with the sqlite database
import sqlite3
# we are adding the import 'g' which will be used for the database
from flask import Flask, render_template, request, g,session, redirect, url_for, escape

# the database file we are going to communicate with
DATABASE = './logindatabase.db'

# connects to the database
def get_db():
    # if there is a database, use it
    db = getattr(g, '_database', None)
    if db is None:
        # otherwise, create a database to use
        db = g._database = sqlite3.connect(DATABASE)
    return db
	


# converts the tuples from get_db() into dictionaries
# (don't worry if you don't understand this code)
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# given a query, executes and returns the result
# (don't worry if you don't understand this code)
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(sqlcode, newvalues):
	cur=get_db()
	cur.execute(sqlcode, newvalues)
	cur.commit()
	cur.close()
	return

# tells Flask that "this" is the current running app
app = Flask(__name__)
app.secret_key=b'abbas'

# this function gets called when the Flask app shuts down
# tears down the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # close the database if we are connected to it
        db.close()

@app.route('/')
def index():
	#return render_template('login.html', error=error)
	if 'username' in session:
		return render_template('index.html', status = session['status'])
	elif 'username' not in session:
		return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
	err = 0
	if request.method=='POST':
		sql = """
			SELECT *
			FROM users
			"""
		results = query_db(sql, args=(), one=False)
		for result in results:
			if result[1]==request.form['username']:
				if result[2]==request.form['password']:
					session['username']=request.form['username']
					session['status']=result[3]
					session['id'] = result[0]

					welcome_name = result[1]
					print(welcome_name)
					return render_template('index.html',welcome_name = welcome_name)
		err = 1								
		return render_template('login.html', error = err )
	
	elif 'username' in session:
		return redirect(url_for('index'))
	else:
		return render_template('login.html', error = err)

@app.route('/index')		
def home():
	return render_template('index.html')

@app.route('/lectures')		
def lectures():
	return render_template('lectures.html')

@app.route('/zoomrecordings')		
def zoomrecordings():
	return render_template('zoomrecordings.html')

@app.route('/Assignments')		
def Assignments():
	return render_template('Assignments.html')

@app.route('/Labs')		
def Labs():
	return render_template('Labs.html')

@app.route('/Calendar')		
def Calendar():
	return render_template('Calendar.html')

@app.route('/links')		
def links():
	return render_template('links.html')

@app.route('/courseteam')		
def courseteam():
	return render_template('courseteam.html')

@app.route('/remark', methods=['GET', 'POST'])
def remark():
	if session['status'] == 0:
		sql = """
			SELECT name, mark, assignment, remarkstatus
			FROM marks
			WHERE id = ?
			"""
	if session['status'] == 1:
		sql12 = """
			SELECT *
			FROM remark
			"""
		remarkreq = query_db(sql12,args=(),one=False)
		if request.method == "POST":
			id = request.form['id']
			assignment = request.form['assignment']
			sql = """
				UPDATE marks SET remarkstatus="CLOSED" WHERE id=? AND assignment=?
				"""
			feedlist = (id, assignment)
			insert_db(sql, feedlist)
	return render_template('instructorremarkview.html', remarkreq=remarkreq )



@app.route('/Marks', methods=['GET', 'POST'])
def Marks():
	if session['status'] == 0:
		sql = """
			SELECT name, mark, assignment, remarkstatus
			FROM marks
			WHERE id = ?
			"""
		viewmarks = query_db(sql, [int(session['id'])], one = False )
		sql1 = """
			SELECT assignment
			FROM marks 
			WHERE id = ?
			"""
		assignments = query_db(sql1, [int(session['id'])], one = False)
		#If remark is requested, enter information into remarks db
		if request.method=="POST":
			id = int(session['id'])
			name = str(session['username'])
			assignment = request.form['assignment']
			justification = str(request.form['justification'])
			sql3 = """
				UPDATE marks SET remarkstatus="OPEN" WHERE id=? AND assignment=?
				"""
			feedlist2 = (id, assignment)
			cur=get_db()
			cur.execute(sql3, feedlist2)
			cur.commit()
			sql2 = """
				INSERT INTO remark(id, name, assignment, justification) VALUES (?,?,?,?)
				"""
			feedlist = (id, name, assignment, justification)
			insert_db(sql2, feedlist)
		#return render_template('marksstudent.html')
		return render_template('marksstudent.html', viewmarks=viewmarks, uname  = session['username'], assignments=assignments)
	elif session['status'] == 1:
		sql = """
			SELECT id, name, mark, assignment
			FROM marks
			"""
		viewmarks= query_db(sql,args=(),one=False)	# runs the sql query using the method query_db to get the relevnat info 		
		if request.method=="POST":
			id = int(request.form['id'])
			name = request.form['name']
			mark = int(request.form['grade'])
			assignment = request.form['assignment']
			feedlist = (id, name, mark, assignment)
			sql1 = """
				INSERT INTO marks(id, name, mark, assignment) VALUES (?,?,?,?)
				"""
			insert_db(sql1, feedlist) #need error if id, name, or grade missing
		return render_template('marksinstructor.html', viewmarks=viewmarks) #returns the tmeplate aswell as the marks that should be viewed

@app.route('/AnonymousFeedback', methods=['GET', 'POST'])		
def AnonymousFeedback():
	
	if session['status'] == 0:
		sql = """
			SELECT username
			FROM users
			WHERE type = 1
			""" #select all teacher names
		instructors = query_db(sql, args=(), one=False)
		if request.method=="POST":
			sql1 = """
				INSERT INTO afeed(q1, q2, q3, q4, ainfo, instructor) VALUES (?,?,?,?,?,?)
				"""
			q1 = request.form['q1']
			q2 = request.form['q2']
			q3 = request.form['q3']
			q4 = request.form['q4']
			ainfo = request.form['addi']
			instructor = request.form['instructor']
			feedlist = (q1, q2, q3, q4, ainfo, instructor)
			insert_db(sql1, feedlist)
		return render_template("anonymousfeedbackstudent.html", instructors=instructors)
	elif session['status'] == 1:
		sql="""
			SELECT *
			FROM afeed
			WHERE instructor = ?
			"""
		feedback = query_db(sql, [str(session['username'])],one=False)
		return render_template('anonymousfeedbackinstructor.html', feedback=feedback)

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('status', None)
	return redirect(url_for('login'))
	

@app.route('/create_acc', methods = ['GET', 'POST'])
def create_acc():
	usernamechecker = 0
	empty = 0
	if request.method=="POST":
		fname = request.form['fname'] #store the new value that they enter in to the variable newfeed
		lname = request.form['fname']
		uname = request.form['username']
		passw = request.form['password']
		types = request.form['type']
		check_types = ""
		check_types = str(types)
		usernamechecker = 0
		empty = 0
		print(check_types)
		if fname == "" or lname == "" or passw == "" or check_types == "" :
			empty = 1
			return render_template('create_acc.html' , checker = usernamechecker, empty_err = empty)



		#query db for username
		unames = query_db("SELECT *  FROM users WHERE username = ? " , [uname] )
		if len(unames) > 1:
			usernamechecker = 1
			#return redirect(url_for('login'))
			return render_template('create_acc.html' , checker = usernamechecker, empty_err = empty)
		
		#query db for largest index
		ind = query_db("SELECT id from users")
		ids = max(ind)
		id = ids[0]
		id = id+1
		

		print(len(unames))
		# add sql  queries
		sql = """
			INSERT INTO users(id, username, password, type ) VALUES (?,?,?,?)
			"""
		newfeed = (id,uname,passw,types) #store the new value that they enter in to the variable newfeed


		insert_db(sql, newfeed)
	return render_template('create_acc.html',checker = usernamechecker, empty_err = empty)



if __name__=="__main__":
	app.run(debug=True,host='0.0.0.0')


	
#set FLASK_APP=app.py
#flask run
