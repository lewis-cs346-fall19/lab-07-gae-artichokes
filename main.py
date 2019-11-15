import webapp2
import MySQLdb
import passwords
class MainPage (webapp2.RequestHandler):
	def get(self):
		conn = MySQLdb.connect(unix_socket=passwords.SQL_HOST,user=passwords.SQL_USER,passwd=passwords.SQL_PASSWORD,db="lab07")
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM things;")
		results = cursor.fetchall()
		cursor.close()
		self.response.headers["Content-Type"] = "text/html"
		str = "<table>"
		for thing in results:
			str+="<tr>"
			for attr in thing:
				str+="<td>"+attr+"</td>"
			str+="</tr>"
		str+="</table>"
		self.response.write(str)

app = webapp2.WSGIApplication([("/",MainPage),],debug=True)
