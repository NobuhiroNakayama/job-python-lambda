import commands, boto3

def _(cmd):
    return commands.getoutput(cmd)

def search_snapshots(volume_name):

    #client = boto3.client('sts')
    #account = client.get_caller_identity()['Account']
    
    snapshots = boto3.client('ec2').describe_snapshots(OwnerIds=['************',])["Snapshots"]

    targetSnapshots = []
    for snapshot in sorted(snapshots, key=lambda x: x["StartTime"]):
        try:
            for tag in snapshot["Tags"]:
                if (tag["Key"] == "Name" and tag["Value"] == volume_name):
                    targetSnapshots.append(snapshot)
        except:
            print "no Tag!"

    return targetSnapshots

def delete_snapshots(targetSnapshots, deleteCount):
    count = deleteCount
    ec2 = boto3.resource('ec2')
    
    for targetSnapshot in targetSnapshots:
        if count > 0:
            ec2.Snapshot(targetSnapshot["SnapshotId"]).delete()
            count -= 1
        else:
            return

def lambda_handler(event, context):
    targetSnapshots = search_snapshots(event['volume_name'])
    deleteCount = len(targetSnapshots) - int(event['generation_number'])
    delete_snapshots(targetSnapshots,deleteCount)