import firebase_admin
from firebase_admin import credentials, firestore, messaging

# Path to your Firebase service account key
cred = credentials.Certificate(r'C:\Users\dilll\Backend\backend\cleaning_app\credentials\neatnest-308c4-firebase-adminsdk-8bt91-be2f5d5a1b.json')
firebase_admin.initialize_app(cred)

db = firestore.client()