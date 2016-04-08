import commands, boto3

def _(cmd):
    return commands.getoutput(cmd)

def create_snapshot(gateway_name,volume_name):
    client = boto3.client('storagegateway')
    ec2 = boto3.resource('ec2')
    
    gateways = client.list_gateways()['Gateways']
    
    target_volumes = []

    for gateway in gateways:
        gateway_tags = client.list_tags_for_resource(ResourceARN=gateway['GatewayARN'])['Tags']
        for tag in gateway_tags:
            if (tag["Key"] == "Name" and tag["Value"] == gateway_name):
                volumes = client.list_volumes(GatewayARN=gateway['GatewayARN'])['VolumeInfos']
                for volume in volumes:
                    volume_tags = client.list_tags_for_resource(ResourceARN=volume['VolumeARN'])['Tags']
                    if (tag["Key"] == "Name" and tag["Value"] == volume_name):
                        target_volumes.append(volume)

    for target_volume in target_volumes:
        snapshot_description = _('TZ=JST-9 date +"%Y%m%d%H%M%S"')
        snapshot_id = client.create_snapshot(VolumeARN=target_volume['VolumeARN'],SnapshotDescription=snapshot_description)['SnapshotId']
        snapshot = ec2.Snapshot(snapshot_id)
        snapshot.create_tags(Tags=[{'Key': 'Name','Value': volume_name},{'Key': 'GatewayName','Value': gateway_name},{'Key': 'volume_arn','Value': target_volume['VolumeARN']},])

# for cached volume
def lambda_handler(event, context):
    create_snapshot(event['gateway_name'],event['volume_name'])