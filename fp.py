
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("arminnovators-e1fb9-firebase-adminsdk-cv698-20460a9f9b.json")  # Replace with your credentials file
firebase_admin.initialize_app(cred)

db = firestore.client()
bus_collection = db.collection('TrackBus') 
bus_name = "test1"

def upDate(count):
        if bus_doc.exists:
                # If the document exists, update the passenger count with the new value
                bus_doc_ref.update({'PassengersCount': count})
        else:
               bus_doc_ref.set({'PassengersCount': count})