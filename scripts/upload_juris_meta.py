import pandas as pd
import numpy as np
from pyrebase.pyrebase import initialize_app, Storage
from pathlib import Path

# ff. imports are for getting secret values from .env file
import os
from dotenv import load_dotenv

from concurrent.futures import ThreadPoolExecutor



def simple_file_upload_test(storage: Storage):
    """
    testing simple .html file upload to firebase storage
    """
    
    # testing simple upload
    sample_path_set_on_cloud = "labor_related_juris_docs/1901-1920/126281645830902.html"
    local_path = "d:/Projects/To Github/LaRJ-Corpus/raw jurisprudence/juris/1901-1920/126281645830902.html"
    storage.child(sample_path_set_on_cloud).put(local_path)

def upload_juris_docs(juris_meta: pd.DataFrame, storage: Storage) -> None:
    """
    file structure of firebase storage would be:
    labor_related_juris_docs
     |- 1901-1920
         |- 2134353.html
         |- 23431251.html
         |- ...
         |- 0652123904.html
     |- 1921-1940
         |- ...
     |- ...
     |- 2021
         |- ...

    non_labor_related_juris_docs
     |- 1901-1920
         |- ...
     |- ...
     |- 2021
         |- ...

    if it is labor related then path_set_on_cloud used will
    be labor_related_juris_docs/{year_range}/{file_name}

    if not labor related then it would be 
    non_labor_related_juris_docs/{year_range}/{file_name}

    """

    def helper(row):
        # answers other than labor related will be put in 
        # non_labor_related_juris_docs/{year_range}/{file_url}
        # path
        answer = row['answer']
        year_range = row['year_range']
        file_name = row['file_name']

        # this is a simple ternary statement that returns 
        # labor_related_juris_docs/{year_range}/{file_name}
        # if doc is labor related, and 
        # non_labor_related_juris_docs/{year_range}/{file_name} 
        # if otherwise
        path_set_on_cloud = f"labor_related_juris_docs/{year_range}/{file_name}" if answer == "LABOR RELATED" else f"non_labor_related_juris_docs/{year_range}/{file_name}"
        local_path = row['abs_file_path']

        storage.child(path_set_on_cloud).put(local_path)
    
    # apply helper function to every row in dataframe
    # by setting axis arg to 1 in order to work on each
    # value of the y/vertical axis
    juris_meta.apply(helper, axis=1)

def upload_juris_docs_concurrently(data: np.ndarray, storage: Storage):
    """
    takes an array of the columns of the converted DataFrame
    and runs a concurrent process of uploading each row to
    firebase storage
    """

    def helper(row):
        # extract the columns of the converted DataFrame
        answer = row[1]
        year_range = row[2]
        file_name = row[4]

        # this is a simple ternary statement that returns 
        # labor_related_juris_docs/{year_range}/{file_name}
        # if doc is labor related, and 
        # non_labor_related_juris_docs/{year_range}/{file_name} 
        # if otherwise
        path_set_on_cloud = f"labor_related_juris_docs/{year_range}/{file_name}" if answer == "LABOR RELATED" else f"non_labor_related_juris_docs/{year_range}/{file_name}"
        local_path = row[0]

        storage.child(path_set_on_cloud).put(local_path)
        print(f"{path_set_on_cloud} {local_path}")
        

    with ThreadPoolExecutor() as executor:
        executor.map(helper, data)


def load_meta_data(url_or_path: str) -> pd.DataFrame:
    """
    reads url of uploaded .csv file in github and
    returns the dataframe
    """

    df = pd.read_csv(url_or_path, index_col=0)

    return df



if __name__ == "__main__":
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path('./').resolve().parent
    load_dotenv(os.path.join(BASE_DIR, '.env'))

    # define config dictionary with credentials
    config = {
        "apiKey": os.environ['FIREBASE_API_KEY'],
        "authDomain": os.environ['FIREBASE_AUTH_DOMAIN'],
        "databaseURL": os.environ['FIREBASE_DATABASE_URL'],
        "projectId": os.environ['FIREBASE_PROJECT_ID'],
        "storageBucket": os.environ['FIREBASE_STORAGE_BUCKET'],
        "messagingSenderId": os.environ['FIREBASE_MESSAGING_SENDER_ID'],
        "appId": os.environ['FIREBASE_APP_ID'],
    }

    # pass credentials dicitonary to access firebase project
    firebase = initialize_app(config=config)
    auth = firebase.auth()

    # return storage object for file retrieval, upload,
    # update, and deletion
    storage = firebase.storage()
    # simple_file_upload_test(storage)

    # read .csv file containing meta data of jurisprudence docs
    df = load_meta_data("https://raw.githubusercontent.com/08Aristodemus24/LaRJ-Corpus/master/raw%20labor%20related%20jurisprudence%20cleaning/juris_meta.csv")
    # upload_juris_docs(df, storage)
    upload_juris_docs_concurrently(df.to_numpy(), storage)

