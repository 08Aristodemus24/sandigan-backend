from pathlib import Path

# ff. imports are for getting secret values from .env file
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))


from django.shortcuts import render
from django.http import HttpResponse
from pyrebase.pyrebase import initialize_app

config = {
    "apiKey": os.environ['FIREBASE_API_KEY'],
    "authDomain": os.environ['FIREBASE_AUTH_DOMAIN'],
    "databaseURL": os.environ['FIREBASE_DATABASE_URL'],
    "projectId": os.environ['FIREBASE_PROJECT_ID'],
    "storageBucket": os.environ['FIREBASE_STORAGE_BUCKET'],
    "messagingSenderId": os.environ['FIREBASE_MESSAGING_SENDER_ID'],
    "appId": os.environ['FIREBASE_APP_ID'],
    "measurementId": os.environ['FIREBASE_MEASUREMENT_ID'],
}

firebase = initialize_app(config)
auth = firebase.auth()
database = firebase.database()


# Create your views here.
def index(request):
    # retrieve data using keys of database since database
    # is jsut a potentially large json file
    owner = database.child('meta-data').child('owner').get().val()
    app_name = database.child('meta-data').child('app-name').get().val()

    sample_template = f"""
    <h1>Philippine Jurisprudence API<h1>
    <p>owner: {owner}<p>
    <p>app name: {app_name}<p>
    """
    return HttpResponse(sample_template)








