from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 
from flask import flash

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('login_registration').query_db( query, data )
    
    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('login_registration').query_db( query, data )
        user = results[0]
        return user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_registration').query_db( query, data )
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(data):
        is_valid = True

        name_regex = re.compile(r'[A-Za-z]{2,50}$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex = re.compile(r'[A-Za-z0-9]{8,15}$')

        if not name_regex.match(data['first_name']):
            is_valid = False
            flash("First name must contain at least two characters and contain only letters")

        if not name_regex.match(data['last_name']):
            is_valid = False
            flash("Last name must contain at least two characters and contain only letters")

        if not email_regex.match(data['email']):
            is_valid = False
            flash("Invalid email address")

        if not password_regex.match(data['password']):
            id_valid = False
            flash("Password must contain letters and numbers between 8-15 characters")

        if data['confirm_password'] != data['password']:
            is_valid = False
            flash("Passwords must match")
        
        return is_valid

    

        
        