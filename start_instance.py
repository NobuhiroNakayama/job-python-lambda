import boto3

INSTANCE_ID = 'i-********'
client = boto3.client('ec2')

def lambda_handler(event, context):
    details = client.describe_instances(
        InstanceIds=[
            INSTANCE_ID,
        ]
    )
    if details['Reservations'][0]['Instances'][0]['State']['Name'] == 'stopped':
        response = client.start_instances(
            InstanceIds=[
                INSTANCE_ID,
            ]
        )
        print response
