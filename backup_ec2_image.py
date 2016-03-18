import commands, boto3

def _(cmd):
    return commands.getoutput(cmd)

def create_image(instance_name):
    instance_id = ""
    for reservation in boto3.client('ec2').describe_instances()["Reservations"]:
        for instance in reservation["Instances"]:
            for tag in instance["Tags"]:
                if(tag["Key"] == "Name" and tag["Value"] == instance_name):
                    instance_id = instance["InstanceId"]

    if instance_id != "":
        instance = boto3.resource('ec2').Instance(instance_id)
        image_name = _('TZ=JST-9 date +"%Y%m%d%H%M%S"') + "_" + instance_name
        image = instance.create_image(Name=image_name,Description=instance_id)
        tag = image.create_tags(Tags=[{'Key': 'Name', 'Value': instance_name}, {'Key': 'InstanceId', 'Value': instance_id},])

def lambda_handler(event, context):
    create_image(event['Name'])
