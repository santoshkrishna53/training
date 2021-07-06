import os
from flask import Flask, Blueprint, send_from_directory, render_template,request,make_response
import logging
from flask_cors import CORS
from api import gcs_upload_object,get_files

app = Flask(__name__)
cors = CORS(app)
app = Flask(__name__, static_folder='appdev/dist/appdev')
CORS(app)
appdev = Blueprint('appdev', __name__,
                    template_folder='appdev/dist/appdev')
app.register_blueprint(appdev)
app.register_blueprint(gcs_upload_object , url_prefix='/api')
app.register_blueprint(get_files , url_prefix='/api')



@app.route('/assets/<path:filename>')
def custom_static_for_assets(filename):
    return send_from_directory('appdev/dist/appdev/assets', filename)


@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory('appdev/dist/appdev/', filename)


@app.route('/')
def index():
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run()