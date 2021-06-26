import boto3

# Create SQS client
sqs = boto3.client(‘sqs’)
queue_url = ‘URL of the queue'

#AMI details
AMI = ‘ami-xxxxxxx’
INSTANCE_TYPE = ‘t2.micro’
KEY_NAME = ‘xxxx’
SUBNET_ID = ‘xxxxxx’
ec2 = boto3.resource(‘ec2’)

def lambda_handler(event, context):

  body = event[“Records”][0][‘body’]
  messageId = event[“Records”][0][‘messageId’]

  userData1 = f”#!/bin/bash \n echo ‘message id : {messageId} , body : {body}’ > /home/ec2-user/message.txt \n”
  
  #script to terminate the instance
  userData2 = “””touch /home/ec2-user/file
  cat << EOF > /home/ec2-user/file
  aws configure set aws_access_key_id xxxxxx
  aws configure set aws_secret_access_key xxxxxx
  aws configure set default.region xxxxx
  ec2InstanceId=$(ec2-metadata — instance-id | cut -d “ “ -f 2)
  aws ec2 terminate-instances — instance-ids $(ec2-metadata — instance-id | cut -d “ “ -f 2)
  EOF
  chmod +x /home/ec2-user/file”””
  
  userDataEncoded = userData1+userData2
  
  #create instance
  instance = ec2.create_instances(
  ImageId=AMI,
  InstanceType=INSTANCE_TYPE,
  KeyName=KEY_NAME,
  SubnetId=SUBNET_ID,
  MaxCount=1,
  MinCount=1,
  UserData=userDataEncoded
  )
  
  print(“New instance created:”, instance[0].id)
  return userDataEncoded
