#!/usr/bin/env python

import time
import sqlite3
from http import cookies
import json

try:
	conn = sqlite3.connect("feed.dat")
	conn.execute('''CREATE TABLE ooks 
		(user text not null,
		dt text not null,
		ook text not null);''')
	conn.commit()
	conn.close()
	print("Feed database created.")
except:
	pass

try:
	conn = sqlite3.connect("users.dat")
	conn.execute('''CREATE TABLE users
		(userName text unique not null,
		password text not null,
		email text not null);''')
	conn.commit()
	conn.close()
	print("Users database created.")
except:
	pass

print("Monkey 1.0 is ready to fling!")

def addOok(self, data):
	cookie = self.headers['cookie']
	cookie = cookie.split(';')
	uName = cookie[0].split('=')
	conn = sqlite3.connect("feed.dat")
	d = time.strftime("%b %d %Y %H:%M:%S", time.gmtime())
	conn.execute("INSERT INTO ooks (user, dt, ook) VALUES (?,?,?);", (uName[1],d,data))
	conn.commit()
	conn.close()
	print("Ook added to database.")

def logOok(data):
	print(data)

def showOoks(self):
	try:
		feedArray = []
		conn = sqlite3.connect("feed.dat")
		o = conn.execute("SELECT user, dt, ook from ooks ORDER BY dt DESC LIMIT 5")
		for row in o:
			feedArray.append({'Username':row[0], 'Date':row[1], 'Data':row[2]})
		json.dump(feedArray, self.remote)
		conn.commit()
		conn.close()
		print("Showing Feed.")
	except:
		pass

def deleteAllOoks():
	try:
		conn = sqlite3.connect("feed.dat")
		conn.execute("DROP TABLE ooks")
		conn.commit()
		conn.close()
		print("Feed table deleted.")
	except:
		pass

def deleteAllUsers():
	try:
		conn = sqlite3.connect("users.dat")
		conn.execute("DROP TABLE users")
		conn.commit()
		conn.close()
		print("Users table deleted.")
	except:
		pass

def createNewUser(u, p, m):
	try:
		conn = sqlite3.connect("users.dat")
		conn.execute("INSERT INTO users (userName, password, email) VALUES (?,?,?);", (u,p,m))
		conn.commit()
		conn.close()
		print("User created.")
	except:
		print("FAILED!!!")

def setCookieLogIn(self, user, password):
	if (findUserAndPass(user, password) == True):

		self.send_header('Set-Cookie', 'username=' + user + ';')
		self.send_header('Set-Cookie', 'signedIn=True')
		print("Signed In!")

	else:
		print("Invalid password or username.")


def setCookieSignUp(self, user, password, email):
	if (checkForUsername(user) == False):
		createNewUser(user, password, email)
		self.send_header('Set-Cookie', 'username=' + user + ';')
		self.send_header('Set-Cookie', 'signedIn=True')

	else:
		print("Failed to sign up user.")

def setCookieLogout(self):
	cookie = self.headers['cookie']
	if not cookie:
		return

	self.send_header('Set-Cookie', 'username=None' + ';')
	self.send_header('Set-Cookie', 'signedIn=False')
	print("Logged Out!")

def findUserAndPass(username, password):
	conn = sqlite3.connect("users.dat")
	c = conn.execute("SELECT userName, password from users")

	for row in c:
		if (username == row[0] and password == row[1]):
			conn.close()
			return True
	conn.close()
	return False

def checkForUsername(username):
	conn = sqlite3.connect("users.dat")
	c = conn.execute("SELECT userName from users")

	for row in c:
		if (username == row[0]):
			conn.close()
			return True
	conn.close()
	return False

def displayCookie(self):
	cookie = self.headers['cookie']
	if cookie:
		cookie = cookie.split(';')
		uName = cookie[0].split('=')
		signedIn = cookie[1].split('=')
		
	if (not cookie or signedIn[1] ==  'False'):
	    self.remote.write('''<form class="login" action="login.html">
	        <fieldset>
	        <legend>Log in!</legend>
	        <label for="username">Name</label>
	        <input name="username"></br>
	        <label for="password">Password</label>
	        <input type="password" name="password"></br>
	        <input type="submit" value="Log in!">
	        </fieldset>
	    </form>
	    
	    
	    <form class="signup" action="signup.html">
	            <fieldset>
	                <legend>Sign up!</legend>
	                <label for="username">Name
	                <input name="username"></br>
	                <label for="password1">Password
	                <input type="password" name="password1"></br>
	                <label for="email">E-mail
	                <input name="email"></br>
	                <input type="submit" value="Create!">
	            </fieldset>
	    </form>''')
	else:
	    self.remote.write('''<form class="logout" action="logout.html">
	        <fieldset>
	        <legend>Signed in!</legend>
	        <p>Welcome, ''' + uName[1] + '''!</p>
	        <input type="submit" value="Sign Out!">
	        </fieldset>
	    </form>''')

def showOokInput(self):
	cookie = self.headers['cookie']
	if not cookie:
		return

	cookie = cookie.split(';')
	signedIn = cookie[1].split('=')

	if (signedIn[1] == 'True'):
	    self.remote.write('''<form action="sendToFeed.html">
	        <label for="ook">
	        <input name="ook" size=120></br>
	        <input type="submit" value="OOK!!">
	    </form>''')