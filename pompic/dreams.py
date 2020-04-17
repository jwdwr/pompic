import os
from uuid import uuid1
from flask import Blueprint, request

from .db import DynamoTable
from .s3 import S3Bucket
from .aws import AWS

bp = Blueprint('dreams', __name__, url_prefix='/dreams')


@bp.route('/save', methods=['POST'])
def save():
  ''' save dream metadata to DB and return URL to upload dream data '''
  entry = request.json
  dream_id = entry.get('dream_id') or str(uuid1())

  # save to database
  dream = {"id": dream_id, "metadata": entry.metadata}
  table = DynamoTable(os.environ.get('DREAMS_TABLE'), AWS().get_user_id())
  table.put_item(dream)

  # generate upload url + params
  bucket = S3Bucket(os.environ.get('DREAMS_BUCKET'), AWS().get_user_id())
  return bucket.presigned_post(dream_id)

@bp.route('/get/<id>', methods=['GET'])
def get(id):
  ''' get dream data + metadata '''
  dreams_table = DynamoTable(os.environ.get('DREAMS_TABLE'), AWS().get_user_id())
  return dreams_table.get_by_id(id)

@bp.route('/list', methods=['GET'])
def list():
  ''' get all dreams '''
  dreams_table = DynamoTable('dreams', AWS().get_user_id())
  dreams = dreams_table.get_items()
  return {"dreams": dreams}
