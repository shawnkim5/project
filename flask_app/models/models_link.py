from flask_app.models.models_user import User
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

db = 'projects_db'

class Link:
    def __init__(self, data):
        self.id = data['id']
        self.link = data['link']
        self.user_id = data['user_id']
        self.owner = None
        self.all = None
    

    # create art
    @classmethod
    def create_link(cls, data):
        query = "INSERT INTO arts ( title, description, price, user_id ) VALUES ( %(title)s, %(description)s, %(price)s, %(user_id)s )"
        return connectToMySQL(db).query_db(query, data)

    # user validator
    @staticmethod
    def link_validator(data):
        is_valid = True
        if len(data['link']) < 5:
            flash('link must be longer than 5')
            is_valid = False
        return is_valid

    @classmethod
    def all_links(cls):
        query = 'SELECT * FROM links LEFT JOIN users on users.id = links.user_id'
        results = connectToMySQL(db).query_db(query)
        links = []
        for link in results:
            one_link = cls(link)
            one_link_info = {
            'id' : link['users.id'],
            'email' : link['email'],
            'password' : link['password'],
            'created_at' : link['users.created_at'],
            'updated_at' : link['users.updated_at'],
            }
            painter = User(one_link_info)
            one_link.all = painter
            links.append(one_link)
        return links

    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM links JOIN users on users.id = links.user_id WHERE links.id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        link = cls(results[0])
        owner_data = {
            'id' : results[0]['users.id'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
        }
        link.owner = User(owner_data)
        return link

    # update art
    @classmethod
    def update_link(cls, form_data, link_id):
        query = f"UPDATE links SET title = %(title)s, description = %(description)s, price = %(price)s WHERE id = {link_id}"
        return connectToMySQL(db).query_db(query, form_data)


    # delete art
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM links WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)