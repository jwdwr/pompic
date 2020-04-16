import os
from uuid import uuid1

import boto3
s3_client = boto3.client('s3')

from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def index():
  return "You are dreaming."

@app.route('/save', methods=['POST'])
def save():
  entry = request.json

  # generate upload url + params
  bucket = os.environ.get('DREAMS_BUCKET')
  key = str(uuid1())
  conditions = [{"acl": "private"}]

  return s3_client.generate_presigned_post(bucket, key, Conditions=conditions)
