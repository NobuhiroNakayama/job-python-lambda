import commands, boto3

def _(cmd):
    return commands.getoutput(cmd)

def lambda_handler(event, context):
    images = boto3.client('ec2').describe_images(Owners=["self"])["Images"]

    targetImages = []
    for image in sorted(images, key=lambda x: x["CreationDate"]):
        try:
            for tag in image["Tags"]:
                if (tag["Key"] == "Name" and tag["Value"] == event['TARGET_INSTANCE_NAME']):
                    targetImages.append(image)
                    print "appended!"
        except:
            print "no Tag!"

    delete_count = len(targetImages) - int(event['GEM_NUM'])

    for targetImage in targetImages:
        if delete_count > 0:
            ec2 = boto3.resource('ec2')
            ec2.Image(targetImage["ImageId"]).deregister()
            for block in targetImage["BlockDeviceMappings"]:
                ec2.Snapshot(block["Ebs"]["SnapshotId"]).delete()
            delete_count -= 1
            print "deleted!"
        else:
            break
