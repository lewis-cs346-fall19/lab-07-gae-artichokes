import webapp2
import MySQLdb
import passwords
import random
class MainPage (webapp2.RequestHandler):
	def get(self):
		if (self.request.cookies.get("cookie_name")==None):
			#if no cookie has been set
			rand = "%032x" % random.getrandbits(128)
			self.response.set_cookie("cookie_name", rand, max_age=1800)
			conn = MySQLdb.connect(unix_socket=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWORD,db="lab07")
			cursor = conn.cursor()
			cursor.execute("INSERT INTO sessions(id) VALUES(%s);",(rand,))
			cursor.close()
			conn.commit()
			session_id = rand
		else:
			#if one has
			session_id = self.request.cookies.get("cookie_name")
		conn = MySQLdb.connect(unix_socket=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWORD,db="lab07")
		cursor = conn.cursor()
		cursor.execute("SELECT user FROM sessions WHERE id=%s",(session_id,))
		results = cursor.fetchall()
		cursor.close()
		if results.isempty():
			#no user set
			self.response.headers["Content-Type"] = "text/html"
			self.response.write('<html><body><form action="main.py" method="POST"><input type = text name="user" required><input type=hidden name=session_id value=%s><input type = submit></form></body></html>',(session_id,))
		else:
			#user is set
			user = results[0][0]
			conn = MySQLdb.connect(unix_socket=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWORD,db="lab07")
			cursor = conn.cursor()
			cursor.execute("SELECT number FROM users WHERE user=%s;",(user,))
			results2 = cursor.fetchall()
			if results.isempty():
				#user not yet set in users table
				cursor.execute("INSERT INTO users(user,number) VALUES(%s,%s);",(user,0))
				num = 0
			else:
				#user is set in users table
				num = results2[0][0]
			cursor.close()
			conn.commit()
			self.response.headers["Content-Type"] = "text/html"
			self.response.write('''<html><body>User: %s<br>Num: %s<br><form action="main.py" method = "POST"><input type=hidden name="incr_user" value=%s><input type=hidden name="num" value=%s>
					<input type=submit value ="INCREMENT"></form></body><html>''',(user,num,user,num))
	def post(self):
		if (self.request.get("user")!=None):
			#adding new user to sessions
			user = self.request.get("user")
			session_id = self.request.get("session_id")
			conn = MySQLdb.connect(unix_socket=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWORD,db="lab07")
			cursor = conn.cursor()
			cursor.execute("UPDATE sessions SET user=%s WHERE id=%s;",(user,session_id))
			cursor.close()
			conn.commit()
			self.response.headers["Status"] = "302 Redirect"
			self.response.headers["Location"] = "main.py"
		else:
			#incrementing user's number
			user = self.request.get("incr_user")
			num = self.request.get("num")
			conn = MySQLdb.connect(unix_socket=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWORD,db="lab07")
			cursor = conn.cursor()
			cursor.execute("SELECT FROM users WHERE user=%s;", (user,))
			if cursor.fetchall().isempty():
				cursor.execute("UPDATE users SET number=%s WHERE user=%s;",(num+1,user))
				#keeps usernames unique, if already used, user will be asked for a username again
			cursor.close()
			conn.commit()
			self.response.headers["Status"] = "302 Redirect"
			self.response.headers["Location"] = "main.py"
app = webapp2.WSGIApplication([("/",MainPage),],debug=True)
