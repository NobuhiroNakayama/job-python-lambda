import commands, boto3

def _(cmd):
    return commands.getoutput(cmd)

def search_instance_ids(instance_name):
    targetInstances = []
    
    for reservation in boto3.client('ec2').describe_instances()["Reservations"]:
        for instance in reservation["Instances"]:
            for tag in instance["Tags"]:
                if(tag["Key"] == "Name" and tag["Value"] == instance_name):
                    targetInstances.append(instance)

    return targetInstances

def create_image(instance_name):
    instances = search_instance_ids(instance_name)

    for i in instances:
        instance = boto3.resource('ec2').Instance(i["InstanceId"])
        image_name = _('TZ=JST-9 date +"%Y%m%d%H%M%S"') + "_" + i["InstanceId"] + "_" + instance_name
        image = instance.create_image(Name=image_name,Description=i["InstanceId"])
        tag = image.create_tags(Tags=[{'Key': 'Name', 'Value': instance_name}, {'Key': 'InstanceId', 'Value': i["InstanceId"]},])

def lambda_handler(event, context):
    create_image(event['Name'])
