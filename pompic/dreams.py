import os
from uuid import uuid1
from flask import Blueprint, request

from .db import DynamoTable
from .s3 import S3Bucket

bp = Blueprint('dreams', __name__, url_prefix='/dreams')

@bp.route('/save', methods=['POST'])
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
  dreams_table = DynamoTable('dreams')
  dreams_table.put_item(dream)

  # generate upload url + params
  bucket = S3Bucket(os.environ.get('DREAMS_BUCKET'), user_id)
  return bucket.presigned_post(dream_id)

@bp.route('/list', methods=['GET'])
def list():
  dreams_table = DynamoTable('dreams')
  dreams = dreams_table.get_items()
  return {"dreams": dreams}
