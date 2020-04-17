from flask import request

class AWS:
  def __init__(self):
    self.event = request.environ['serverless.event']

  def get_user_id(self):
    return self.event['requestContext']['identity']['cognitoIdentityId']
