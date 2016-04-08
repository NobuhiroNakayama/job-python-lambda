import commands, boto3
from datetime import datetime, timedelta

def _(cmd):
    return commands.getoutput(cmd)

def delete_snapshots(instance_name):
    snapshots = boto3.client('rds').describe_db_snapshots(DBInstanceIdentifier=instance_name,SnapshotType='manual')['DBSnapshots']
    
    for snapshot in snapshots:
        if int(datetime.now().strftime('%s')) - 2592000 > int(snapshot["SnapshotCreateTime"].strftime('%s')): # If snapshot created time is older than 30 days ago, delete snapshot
            # print "delete"
            # 2592000 sec = 30 day
            response = boto3.client('rds').delete_db_snapshot(DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'])    

def lambda_handler(event, context):
    delete_snapshots(event['Name'])
    