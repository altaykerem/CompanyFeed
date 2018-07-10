import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred_json = {
  "type": "service_account",
  "project_id": "company-feed",
  "private_key_id": os.environ.get('firebase_private_kID'),
  "private_key": os.environ.get('firebase_private_key'),
  "client_email": "firebase-adminsdk-f1ufm@company-feed.iam.gserviceaccount.com",
  "client_id": os.environ.get('firebase_cID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ.get('firebase_client_cert_url')
}
print(cred_json)
cred = credentials.Certificate(json.dumps(cred_json))


def get_parameters():
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    param_ref = db.collection('runtime').document('parameters')
    params = param_ref.get()

    return params.to_dict()
