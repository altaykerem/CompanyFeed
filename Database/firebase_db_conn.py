import os
import codecs
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

private = codecs.decode(os.environ.get('firebase_private_key'), 'unicode_escape')
cred_json = {
  "type": "service_account",
  "project_id": "company-feed",
  "private_key_id": os.environ.get('firebase_private_kID'),
  "private_key": private,
  "client_email": "firebase-adminsdk-f1ufm@company-feed.iam.gserviceaccount.com",
  "client_id": os.environ.get('firebase_cID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ.get('firebase_client_cert_url')
}

cred = credentials.Certificate(cred_json)


def get_parameters():
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    param_ref = db.collection('runtime').document('parameters')
    params = param_ref.get()
    firebase_admin.delete_app(app)
    return params.to_dict()


def get_mailing_list():
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    users = db.collection('users').get()
    mailing_dict = {}
    for user in users:
        mailing_dict[user.id] = user.to_dict()['mail']
    firebase_admin.delete_app(app)
    return mailing_dict


def get_functions():
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    func_ref = db.collection('runtime').document('functionalities')
    params = func_ref.get()
    firebase_admin.delete_app(app)
    return params.to_dict()
