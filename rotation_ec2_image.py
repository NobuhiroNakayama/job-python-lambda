import commands, boto3

def _(cmd):
    return commands.getoutput(cmd)

def search_images(instance_name):
    images = boto3.client('ec2').describe_images(Owners=["self"])["Images"]

    targetImages = []
    for image in sorted(images, key=lambda x: x["CreationDate"]):
        try:
            for tag in image["Tags"]:
                if (tag["Key"] == "Name" and tag["Value"] == instance_name):
                    targetImages.append(image)
                    print "appended!"
        except:
            print "no Tag!"

    return targetImages

def delete_images(targetImages, deleteCount):
    count = deleteCount
    for targetImage in targetImages:
        if count > 0:
            ec2 = boto3.resource('ec2')
            ec2.Image(targetImage["ImageId"]).deregister()
            for block in targetImage["BlockDeviceMappings"]:
                ec2.Snapshot(block["Ebs"]["SnapshotId"]).delete()
            count -= 1
            print "deleted!"
        else:
            return

def lambda_handler(event, context):
    targetImages = search_images(event['instance_name'])
    deleteCount = len(targetImages) - int(event['generation_number'])
    delete_images(targetImages,deleteCount)
