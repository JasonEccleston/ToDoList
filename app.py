#!/usr/bin/env python3
import sys
#import MySQLdb as mydb
import pymysql.cursors
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import settings # Our server and db settings, stored in settings.py
from validate import validate as valid

app = Flask(__name__)
# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)



####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

class SignUp(Resource):
	def post(self):
		if not request.json:
			abort(400) # bad request
		# Parse the json
		parser = reqparse.RequestParser()
		try:
			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			parser.add_argument('displayName', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		# Already logged in
		try:
			ldapServer = Server(host=settings.LDAP_HOST)
			ldapConnection = Connection(ldapServer,
				raise_exceptions=True,
				user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
				password = request_params['password'])
			ldapConnection.open()
			ldapConnection.start_tls()
			ldapConnection.bind()
			# At this point we have successfully authenticated.
			session['username'] = request_params['username']
			response = {'status': 'success' }
			responseCode = 201
            #db = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass=pymysql.cursor.DictCursor)
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4')

			cursor = db.cursor()
			cursor2 = db.cursor()
			#Checks to see if list exists for given user
			args = [request_params['username']]
			cursor.callproc("checkForList", args)
			args = [request_params['displayName']]
			cursor2.callproc("checkDisplayName", args)

			#checks if username is already in db
			if not cursor.fetchall():
				#check if displayname is already in db
				#if both of these cond are false then we add
				#the user
				if not cursor2.fetchall():
					args = [request_params['username'], request_params['displayName']]
					cursor.callproc("addList", args)
				else:
					responseCode = 400
					response = {'status': 'Display name already in use'}
			else:
				responseCode = 400
				response = {'status': 'Account already created'}

			cursor.close()
			cursor2.close()
			db.commit()
			db.close()
			ldapConnection.unbind()

		except (LDAPException):
			response = {'status': 'Access denied'}
			responseCode = 403


		return make_response(jsonify(response), responseCode)

####################################################################################
#
# Routing: GET and POST using Flask-Session
#
class SignIn(Resource):
	#
	# Login, start a session and set/return a session cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Casper", "password": "cr*ap"}'
	#  	-c cookie-jar http://info3103.cs.unb.ca:61340/signin
	#
	def post(self):
		if not request.json:
			abort(400) # bad request
		# Parse the json
		parser = reqparse.RequestParser()
		try:
			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()

		except:
			abort(400)
		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4')

			cursor = db.cursor()

			args = [request_params['username']]
			cursor.callproc("checkForList", args)
			if not cursor.fetchall():
				cursor.close()
				db.close()
				abort(404)

			cursor.close()
			db.close()
		except:
			abort(404) # bad request

		# Already logged in
		if request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				# At this point we have successfully authenticated.
				session['username'] = request_params['username']
				response = {'status': 'success' }
				responseCode = 201

			except (LDAPException):
				response = {'status': 'Access denied'}
				responseCode = 403
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)

	# GET: Check for a login
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	http://info3103.cs.unb.ca:61340/signin
	def get(self):
		if 'username' in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	def delete(self):
		if session:
			session.clear()
			response = {'status':'success'}
			responseCode = 204
			success = True

		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response),responseCode) # turn set into json and return it

class Users(Resource):
	def get(self):
		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)

			cursor = db.cursor()

			cursor.callproc("getUsers")
			rows = cursor.fetchall()

			if rows is None:
				abort(404)

			users = []
			for row in rows:
				users.append(row)

			response = {
				"users" : users
			}
			cursor.close()
			db.close()
		except:
			abort(500)

		return make_response(jsonify(response), 200)

class UserId(Resource):
	#get will return the users row in lists
	def get(self,user_id):
		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)

			cursor = db.cursor()
			args = [user_id]
			cursor.callproc("getUser",args)
			rows = cursor.fetchall()

			if rows is None:
				abort(404)
			user = []
			for row in rows:
				user.append(row)

			response = {
				"user-info" : user
			}
		except:
			abort(500)
		finally:
			cursor.close()
			db.close()

		return make_response(jsonify(response), 200)

	#put will update displayname
	def put(self,user_id):
		parser = reqparse.RequestParser()
		try:
			# Check for required attributes in json document, create a dictionary
			parser.add_argument('displayName', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400)
		try:
			username = session['username']
		except:
			abort(403)#forbidden

		valid.validation(session,user_id)

		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
			cursor = db.cursor()
			args =[user_id,request_params['displayName']]
			cursor.callproc("updateDisplayName",args)
			db.commit()
			cursor.close()
			db.close()
			response = {"status" :"successfully updated"}
			responseCode = 200
		except:
			abort(500)

		return make_response(jsonify(response), 200)


	#deletes the user
	def delete(self,user_id):
		valid.validation(session,user_id)

		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
			cursor = db.cursor()
			args =[user_id]
			cursor.callproc("deleteUsersList",args)
			cursor.callproc("deleteUser", args)
			db.commit()
			cursor.close()
			db.close()
			responseCode = 204
		except:
			abort(500)
		return make_response(jsonify({"status":"success"}),responseCode)

class UserList(Resource):
	#returns the list elements for that user
	def get(self,user_id):
		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
			cursor = db.cursor()
			args = [user_id]
			cursor.callproc("getUsersList",args)

			rows = cursor.fetchall()

			if rows is None:
				abort(404)

			listItems = []
			for row in rows:
				listItems.append(row)

			response = {
				"listItems" : listItems
			}
			cursor.close()
			db.close()
		except:
			abort(500)

		return make_response(jsonify(response), 200)

	def post(self, user_id):

		if not request.json:
			abort(400)#bad request
		try:
			username = session['username']
		except:
			abort(403)#forbidden
		try:
			parser = reqparse.RequestParser()
			#check for required attributes on the ToDo lists
			parser.add_argument('item', type=str, required=True)
			request_params = parser.parse_args()
			item = request_params['item']
		except:
			abort(400)

		valid.validation(session,user_id)

		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
			cursor = db.cursor()
			args = [username,item]
			cursor.callproc("addListItem", args)

			db.commit()
			cursor.close()
			db.close()
		except:
			abort(500)
		responseCode = 201
		return make_response(jsonify({"status":"success"}),responseCode)

	#deletes the users list
	def delete(self, user_id):
		try:
			username = session['username']
		except:
			abort(403)#forbidden

		valid.validation(session,user_id)

		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
			cursor = db.cursor()
			args = [user_id]
			cursor.callproc("deleteUsersList", args)
			db.commit()
			cursor.close()
			db.close()
		except:
			abort(500)
		return make_response(jsonify({"status":"success"}),204)


class ItemId(Resource):

	def get(self, user_id, item_id):
		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
			cursor = db.cursor()
			print(item_id)
			args = [item_id]
			cursor.callproc("getListItem",args)

			row = cursor.fetchone()
			print(row)
			if row is None:
				abort(404)

			item = row

			cursor.close()
			db.close()
		except:
			abort(500)

		return make_response(jsonify(item), 200)

	def delete(self, user_id, item_id):
		try:
			username = session['username']
		except:
			abort(403)#forbidden#legacy code block ignore

		valid.validation(session,user_id)
		valid.validateListById(session,user_id,item_id)

		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)

			cursor = db.cursor()
			args = [item_id]
			cursor.callproc("deleteListItem",args)
			db.commit()
			cursor.close()
			db.close()
		except:
			abort(500)#server error

		return make_response(jsonify({"status":"success"}),204)


	def put(self,user_id,item_id):
		try:
			username = session['username']
		except:
			abort(403)#forbidden

		valid.validation(session,user_id)
		valid.validateListById(session,user_id,item_id)
		try:
			db = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
			parser = reqparse.RequestParser()
				#check for required attributes on the ToDo lists

			parser.add_argument('item', type=str, required=True)
			request_params = parser.parse_args()
			item = request_params['item']

			cursor = db.cursor()
			args = [item_id,item]
			cursor.callproc("updateListItem",args)
			db.commit()
			cursor.close()
			db.close()
		except:
			abort(500)#server error

		responseCode = 200
		return make_response(jsonify({"status":"successfully updated"}),responseCode)




####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(SignUp, '/signup')
api.add_resource(Users, '/users')
api.add_resource(UserId, '/users/<int:user_id>')
api.add_resource(UserList, '/users/<int:user_id>/list')
api.add_resource(ItemId, '/users/<int:user_id>/list/items/<int:item_id>')



#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
   	app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.APP_DEBUG)
