import boto3
from boto3.dynamodb.conditions import Key, Attr

class DynamoTable:
  ''' a dynamodb table. partitioned by user_id '''

  def __init__(self, table_name, user_id):
    self.db = boto3.resource('dynamodb')
    self.table = self.db.Table(table_name) # pylint: disable=no-member
    self.user_id = user_id

  def put_item(self, item):
    item['user_id'] = self.user_id
    return self.table.put_item(Item=item)

  def get_items(self):
    return self.table.scan().get('Items')

  def get_by_id(self, id):
    ''' get a single object from dynamo based on id '''
    items = self.table.query(
      KeyConditionExpression=Key('id').eq(id) & Key('user_id').eq(self.user_id)
      ).get('Items')
    return items and items[0]