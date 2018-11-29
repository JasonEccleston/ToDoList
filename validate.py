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

class validate():

    def validation(session,user_id):
        try:
            username = session['username']
        except:
            abort(403)#forbidden
        try:
            db = pymysql.connect(
                settings.DB_HOST,
                settings.DB_USER,
                settings.DB_PASSWD,
                settings.DB_DATABASE,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            args = [username]
            cursor.callproc("getUserListId",args)
            #going to compare this for validation below.
            userId = cursor.fetchone()
            cursor.close()
            db.close()
        except:
            abort(500)#server error
        if userId is None:
            abort(403)#forbidden
        if not user_id == userId['listId']:
            abort(403)#forbidden session id does not match endpoint id

    def validateListById(session,user_id,item_id):
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
            cursor.callproc("getItemListId",args)
            #going to compare this for validation below.
            listId = cursor.fetchone()
            cursor.close()
            db.close()
        except:
            abort(500)#server error
        try:
            if listId is None:
                abort(403)#forbidden
            if not user_id == listId['listId']:
                abort(403)#forbidden session id does not match endpoint id
        except:
            abort(403)
