import boto3

class S3Bucket:
  def __init__(self, bucket_name, user_id):
    self.s3 = boto3.client('s3')
    self.bucket_name = bucket_name
    self.user_id = user_id

  def presigned_post(self, key):
    full_key = self.user_id + '/' + key
    conditions = [{"acl": "private"}]
    return self.s3.generate_presigned_post(self.bucket_name, full_key, Conditions=conditions)