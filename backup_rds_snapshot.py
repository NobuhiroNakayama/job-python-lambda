import commands, boto3

def _(cmd):
    return commands.getoutput(cmd)

def create_snapshot(instance_name):
    client = boto3.client('rds')
    try:
        response = client.describe_db_instances(DBInstanceIdentifier=instance_name)
    except:
        print "Error occurred. There is not " + instance_name + "."
        return
    
    snapshot_name = instance_name + "-" + _('TZ=JST-9 date +"%Y%m%d%H%M%S"')

    response = client.create_db_snapshot(DBSnapshotIdentifier=snapshot_name,DBInstanceIdentifier=instance_name)

def lambda_handler(event, context):
    create_snapshot(event['Name'])