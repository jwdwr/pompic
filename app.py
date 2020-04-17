import os
from uuid import uuid1
import boto3

from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def index():
  return "You are dreaming."

@app.route('/save', methods=['POST'])
def save():
  entry = request.json
  dream_id = entry.get('dream_id') or str(uuid1())

  event = request.environ['serverless.event']
  user_id = event['requestContext']['identity']['cognitoIdentityId']

  # save to database
  dream = {
    "user_id": user_id,
    "dream_id": dream_id,
    "metadata": entry['metadata']
  }
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table('dreams')
  table.put_item(Item=dream)

  # generate upload url + params
  s3_client = boto3.client('s3')
  bucket = os.environ.get('DREAMS_BUCKET')
  key = user_id + '/' + dream_id
  conditions = [{"acl": "private"}]

  return s3_client.generate_presigned_post(bucket, key, Conditions=conditions)

@app.route('/list', methods=['GET'])
def list():
  return {"dreams": dynamo_client.scan(TableName='dreams')['Items']}
