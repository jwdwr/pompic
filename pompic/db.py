import boto3

class DynamoTable:
  def __init__(self, table_name):
    self.db = boto3.resource('dynamodb')
    self.load_table(table_name)

  def load_table(self, table_name):
    self.table = self.db.Table(table_name) # pylint: disable=no-member

  def put_item(self, item):
    return self.table.put_item(Item=item)

  def get_items(self):
    return self.table.scan().get('Items')