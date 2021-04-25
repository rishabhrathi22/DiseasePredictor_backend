import pyrebase
import datetime
import json

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


# function to add user to database
def addUser(user):
    uid, email = user['uid'], user['email']
    data = {'email': email, 'pastRecords': {'diabetes': False, 'pneumonia': False}}

    isPresent = db.child('Data').child(uid)
    if (isPresent.get().val() == None):
        print("First time user")
        db.child("Data").child(uid).set(data)
    else:
        print("Already registered.")

    return True


# function to add diabetes record to database
def addDiabatesRecord(uid, inputData, result):
    isPresent = db.child('Data').child(uid)
    if (isPresent.get().val() == None):
        return False

    try:
        diabetesRecords = db.child('Data').child(uid).child('pastRecords').child('diabetes').get().val()
        res = {
            "RandomForestNormal": "Yes" if result["RandomForestNormal"]==1 else "No",
            "RandomForestUnskewed": "Yes" if result["RandomForestUnskewed"]==1 else "No",
            "KNNUnskewed": "Yes" if result["KNNUnskewed"]==1 else "No",
            "Prediction": "have diabetes" if result["Ones"]>1 else "does not have diabetes"
        }
        if result.get("GBM")!=None:
            res["GBM"] = "Yes" if result["GBM"]==1 else "No"
            res["Prediction"] = "have diabetes" if result["Ones"]>2 else "does not have diabetes"

        data = {
            "date": datetime.datetime.now().strftime("%d-%m-%Y"),
            "input": inputData,
            "result": res
        }

        # first record
        if diabetesRecords == False:
            db.child('Data').child(uid).child('pastRecords').child('diabetes').child(1).set(data)
        # new records
        else:
            last = len(diabetesRecords)
            db.child('Data').child(uid).child('pastRecords').child('diabetes').child(last).set(data)

    except Exception as e:
        print(e)

    return True


# function to add pneumonia record to database
def addPneumoniaRecord(uid, inputImage, result):
    isPresent = db.child('Data').child(uid)
    if (isPresent.get().val() == None):
        return False

    try:
        pneumoniaRecords = db.child('Data').child(uid).child('pastRecords').child('pneumonia').get().val()
        res = {
            "Prediction": "have pneumonia" if result["Prediction"]==1 else "does not have pneumonia",
            "Accuracy": str(result["Accuracy"])
        }

        data = {
            "date": datetime.datetime.now().strftime("%d-%m-%Y"),
            "input": inputImage,
            "result": res
        }

        # first record
        if pneumoniaRecords == False:
            db.child('Data').child(uid).child('pastRecords').child('pneumonia').child(1).set(data)
        # new records
        else:
            last = len(pneumoniaRecords)
            db.child('Data').child(uid).child('pastRecords').child('pneumonia').child(last).set(data)

    except Exception as e:
        print(e)

    return True


# function to get diabetes past records
def getDiabetesPastRecords(uid):
    diabetesRecords = db.child('Data').child(uid).child('pastRecords').child('diabetes').get().val()
    if diabetesRecords == False:
        return []
    return diabetesRecords[1:]


# function to get pneumonia past records
def getPneumoniaPastRecords(uid):
    pneumoniaRecords = db.child('Data').child(uid).child('pastRecords').child('pneumonia').get().val()
    if pneumoniaRecords == False:
        return []
    return pneumoniaRecords[1:]

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

# retrieving data using loops
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