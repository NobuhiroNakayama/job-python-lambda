import commands, boto3
from datetime import datetime, timedelta

def _(cmd):
    return commands.getoutput(cmd)

def lambda_handler(event, context):
    instance_name = event['Name']
    snapshots = boto3.client('rds').describe_db_snapshots(DBInstanceIdentifier=instance_name,SnapshotType='manual')['DBSnapshots']

    print snapshots
    
    for snapshot in snapshots:
        if int(datetime.now().strftime('%s')) - 2592000 > int(snapshot["SnapshotCreateTime"].strftime('%s')): # If snapshot created time is older than 30 days ago
            # print "delete"
            # 2592000
            response = boto3.client('rds').delete_db_snapshot(DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'])
        else:
            # print "not delete"
            break

