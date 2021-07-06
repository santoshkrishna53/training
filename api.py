from flask import Blueprint, render_template, abort, request
import json
import time
from google.cloud import storage
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials,auth
from firebase_admin import firestore
import os
from functools import wraps
# credential_path = "storage.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app()
db = firestore.client()



def authorize_user(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not 'Authorization' in request.headers:
                print("No header Authorization")
                abort(401)
            user = None
            data = request.headers['Authorization']
            authToken = str(data)
            try:
              user = auth.verify_id_token(authToken)
            except Exception as identifier:
                print(identifier)
                abort(401)

            return f(user,*args, **kws)            
    return decorated_function

gcs_upload_object = Blueprint('gcs_upload_object', __name__)
@gcs_upload_object.route('/gcs_upload_object', methods=['GET','POST'])
def gcs_upload():
  filename = request.form.get('filename')
  f=request.files["file"]
  storage_client = storage.Client()
  bucket = storage_client.bucket('training-bucket-53')
  print(filename)
  blob = bucket.blob(filename)
  blob.upload_from_string(f.read())
  resp = {
  'status' : 'success'
  }
  return json.dumps(resp)

get_files = Blueprint('get_files', __name__)
@get_files.route('/get_files', methods=['GET','POST'])
@authorize_user
def get_docs(user,*args, **kws):
  print("user" , user['email'])
  email = user['email']
  user_docs = []
  docs = db.collection(u'training').stream()
  for doc in docs:
    # print(f'{doc.id} => {doc.to_dict()}')
    data = doc.to_dict()
    # print(data)
    if(data['email'] == email):
      user_docs.append({
        'filename': doc.id,
        'data' : data
      })
  return json.dumps (
    {
      'docs' : user_docs
    }
  )

  


  








        

