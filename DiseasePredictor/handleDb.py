import pyrebase

config = {
    "apiKey": "AIzaSyDG9dtoC0iwj1TNB04cjUJKqM_BRg9erqU",
    "authDomain": "disease-predictor-e446f.firebaseapp.com",
    "databaseURL": "https://disease-predictor-e446f-default-rtdb.firebaseio.com/",
    "projectId": "disease-predictor-e446f",
    "storageBucket": "disease-predictor-e446f.appspot.com",
    "messagingSenderId": "459690692589",
    "appId": "1:459690692589:web:e7e6319809b601945c61e4"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db = firebase.database()

def addUser(user):
    uid, email = user['uid'], user['email']
    data = {'email': email}
    db.child("Data").child(uid).set(data)
    return True

"""
# selecting the column in the database
db.child("users").child("Morty")

# How to save a data
data = {"name": "Mortimer 'Morty' Smith"}
db.child("users").push(data)

# How to update a existing data
db.child("users").child("Morty").update({"name": "Mortiest Morty"})

# Removing existing data
db.child("users").child("Morty").remove()

# retrieving the data
users = db.child("users").get()
print(users.val()) #  retervies  this data => {"Morty": {"name": "Mortimer 'Morty' Smith"}, "Rick": {"name": "Rick Sanchez"}}

# reterving data using loops
all_users = db.child("users").get()
for user in all_users.each():
    print(user.key()) # Morty
    print(user.val()) # {name": "Mortimer 'Morty' Smith"}

# For getting a data in a particular path
all_users = db.child("users").get()

# some Complex queries

# ordering by child
users_by_name = db.child("users").order_by_child("name").get()

# equal to
users_by_score = db.child("users").order_by_child("score").equal_to(10).get()

# starting and ending
users_by_score = db.child("users").order_by_child("score").start_at(3).end_at(10).get()

# limiting form first to last
users_by_score = db.child("users").order_by_child("score").limit_to_first(5).get()

# geting by key
users_by_key = db.child("users").order_by_key().get()

# getting by value
users_by_value = db.child("users").order_by_value().get()
"""