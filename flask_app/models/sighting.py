from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Sighting:

    DB = "sasquatch_mysql"

    def __init__(self,sighting):

        self.id = sighting["id"]
        self.location = sighting["location"]
        self.happenings = sighting["happenings"]
        self.date = sighting["date"]
        self.number = sighting["number"]
        
        self.created_at = sighting["created_at"]
        self.updated_at = sighting["updated_at"]
        self.user_id = sighting["user_id"]

        self.creator = None

    @classmethod
    def is_valid(cls, sighting):
        valid = True

        if len(sighting["location"]) <= 0 or len(sighting["happenings"]) <= 0 or len(sighting["date"]) <= 0 or len(sighting["number"]) <= 0:
            valid = False
            flash("All fields required", "sighting")
            return valid
        if len(sighting["location"]) < 3:
            valid = False
            flash("Location must be at least 3 characters", "sighting")
        if len(sighting["happenings"]) < 10:
            flash("Happenings cannot be less than 10 characters", "sighting")
        if len(sighting["date"]) < 3:
            valid = False
            flash("Date must be at least 3 characters", "sighting")
        if len(sighting["number"]) < 1:
            valid = False
            flash("Number of sasquatches cannot be less than 1", "sighting")
        return valid
    
    @classmethod
    def get_by_id(cls, sighting_id):
        
        data = {
            "id": sighting_id
        }
        query = "SELECT * from sightings WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all_with_creator(cls):
        query = "SELECT * from sightings JOIN users on sightings.user_id = users.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        all_sightings = []
        for row in results:

            one_sighting = cls(row)
            one_sighting_user_info = {

                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            user = User(one_sighting_user_info) 
            one_sighting.creator = user 
            all_sightings.append(one_sighting)
        
        return all_sightings
    
    @classmethod
    def get_one(cls, sighting_id):
        query = """
                SELECT * from sightings 
                JOIN users on sightings.user_id = users.id
                WHERE sightings.id = %(id)s;
                """
        data = {
            "id": sighting_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        sighting=cls(results[0])
        for row in results:
            user_data = {
                "id": row["users.id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            user = User(user_data) 
            sighting.creator = user 

        return sighting

    #@classmethod
    #def get_one(cls, sighting_id):
        
        #data = {
            #"id": sighting_id
        #}
        #query = "SELECT * from sightings WHERE id = %(id)s;"
        #results = connectToMySQL(cls.DB).query_db(query, data)
        #return cls(results[0])


    @classmethod
    def create(cls, sighting):

        query = """
                INSERT into sightings (location, happenings, date, number, user_id)
                VALUES (%(location)s, %(happenings)s, %(date)s, %(number)s, %(user_id)s);"""

        result = connectToMySQL(cls.DB).query_db(query, sighting)
        return result


    @classmethod
    def update_sighting(cls, sighting):

        query = """
                UPDATE sightings
                SET location = %(location)s, happenings = %(happenings)s, date = %(date)s, number = %(number)s
                WHERE id = %(id)s;"""

        result = connectToMySQL(cls.DB).query_db(query, sighting)
        return result
    
    @classmethod
    def delete_sighting(cls, sighting):
        data = {
            "id": sighting
        }
        query = """
                DELETE FROM sightings WHERE id=%(id)s
                    """
        return connectToMySQL(cls.DB).query_db(query, data)
    
