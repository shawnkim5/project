from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL

db = 'projects_db'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # get one user
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    # user validator
    @staticmethod
    def user_validator(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address')
            is_valid = False
        connection = connectToMySQL(db)
        query = "SELECT *  FROM users WHERE email = %(email)s"
        results = connection.query_db(query, data)
        if len(results) != 0:
            flash('This email is already being used', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must contain at least 8 characters', 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('password does not match')
            is_valid = False
        return is_valid

    #Check to see if user is already in the db
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Create user
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s )"
        return connectToMySQL(db).query_db(query, data)