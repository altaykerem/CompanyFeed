import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('C:/Users/HP/Downloads/company-feed-firebase-adminsdk.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://databaseName.firebaseio.com'
})
print(default_app.name)
