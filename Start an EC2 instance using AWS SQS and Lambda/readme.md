# Getting started with AWS SQS and Lambda Trigger to start an ec2 instance

[Read my medium article for complete explanation](https://dasith-dev.medium.com/intern-diaries-1-d7307d93367)

## The summary of what we wanted to achieve here was :

  1.  Send objects to the FIFO queue using the S3 bucket in a sequence manner
  2.  When the FIFO queue received a message lambda function will trigger
  3.  The function will start a new EC2 instance (Here we used t2.micro instance and we need one instance per processing of an object)
  4.  After the processing part is done automatically terminate the instance
   
#### NOTE: This procedure was done actually for testing purposes, not for production purposes.
AWS SQS, Lambda function, and EC2 are some main services provide by AWS, and for this particular task, I and my mentor decided to use these services to achieve our target.

Here I am not going to tell you about how to set up the AWS account. Instead, I'll dive into the concepts of SQS and lambda function. 
Below I have given a small definition for both SQS and Lambda by referring to Amazon Documentation

**Amazon Simple Queue Service** (Amazon SQS) offers a secure, durable, and available hosted queue that lets you integrate and decouple distributed software systems and components. It provides a generic web services API that you can access using any programming language that the AWS SDK supports. Amazon SQS supports both standard and FIFO queues.

**AWS Lambda** is a serverless compute service that lets you run code without provisioning or managing servers, creating workload-aware cluster scaling logic, maintaining event integrations, or managing runtimes. With Lambda, you can run code for virtually any type of application or backend service — all with zero administration. Just upload your code as a ZIP file or container image, and Lambda automatically and precisely allocates compute execution power and runs your code based on the incoming request or event, for any scale of traffic. You can set up your code to automatically trigger from over 200 AWS services and SaaS applications or call it directly from any web or mobile app. You can write Lambda functions in your favorite language (Node.js, Python, Go, Java, and more) and use both serverless and container tools, such as AWS SAM or Docker CLI, to build, test, and deploy your functions.

In this task, we use the S3 bucket to push objects to the queue and we used the FIFO queue for the task as the FIFO manner was crucial when processing the objects.

#### To use all the AWS services make sure you have the right access and permission to the services.
- Make sure to create ‘roles’ using IAM especially for lambda events that use triggers.
- After getting relevant access you can simply create SQS using Amazon SQS.
- Before creating the lambda function I created an IAM role for the lambda function that has a lambda function execution permission and full access SQS permissions.
- Then using the AWS lambda console I created a lambda function.

To invoke the function I created a lambda SQS trigger with a batch size of 1 (Because we want to trigger the function when a new message is pushed into the queue)

### So what is happening inside the function? 😕

```python
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
  ```


**Boto3** is the name of the Python SDK for AWS. It allows you to directly create, update, and delete AWS resources from your Python scripts.

Make sure to pass the proper AMI details

#AMI details
```python
AMI = ‘ami-xxxxxxx’
INSTANCE_TYPE = ‘t2.micro’
KEY_NAME = ‘xxxx’
SUBNET_ID = ‘xxxxxx’
```

#### lambda_handler(event, context) is the function that executes when the event is triggered.

In the lambda function console you can configure these:

  1.  The Handler is set to lambda_function.lambda_handler
  2.  lambda_function.py is the name of our .py file
  3.  lambda_handler is the name of the function in our code
  
event argument is the data that's passed to the function upon execution. Here A message arriving on an SQS Queue is the event and we can access the specific message using:
#### event[“Records”][0]

context arg is the data about the execution environment of the function

**ec2.create_instances()** method create a new instance according to the params provided.
```python
instance = ec2.create_instances(
  ImageId=AMI,
  InstanceType=INSTANCE_TYPE,
  KeyName=KEY_NAME,
  SubnetId=SUBNET_ID,
  MaxCount=1,
  MinCount=1,
  UserData=userDataEncoded
  )
```

### UserData

When you launch an instance in Amazon EC2, you have the option of passing user data to the instance that can be used to perform common automated configuration tasks and even run scripts after the instance starts.
Here I add UserData to the instance using the bash command so I can save the message ID and message body in a text file.

```python
userData1 = f”#!/bin/bash \n echo ‘message id : {messageId} , body : {body}’ > /home/ec2-user/message.txt \n”
```

### Terminating the Instance

As I mentioned earlier in summary we wanted to terminate the instance after the processing is done. So what I did was write a bash script to terminate the instance and pass the script to the instance via userData. So after processing the object we can execute that bash script.

```python
userData2 = “””touch /home/ec2-user/file
cat << EOF > /home/ec2-user/file
aws configure set aws_access_key_id xxxxxx
aws configure set aws_secret_access_key xxxxxx
aws configure set default.region xxxxx
ec2InstanceId=$(ec2-metadata — instance-id | cut -d “ “ -f 2)
aws ec2 terminate-instances — instance-ids $(ec2-metadata — instance-id | cut -d “ “ -f 2)
EOF
chmod +x /home/ec2-user/file”””
```

Here I created a bash file named “file”. But to terminate an instance it should configure the AWS details. So make sure to fill in the proper aws_access_key and secret_key values along with the region.
After processing the object just execute the bash file by typing ./file
So the particular instance will terminate automatically.

### Testing

You can create a custom test plan using the lambda function console or test via simply sending an SQS message. I'll explain the second approach.
To test this you can simply send a message to the FIFO queue using SQS console. { When sending messages make sure to put the same group ID (Messages that belong to the same message group are processed in a FIFO manner. However, messages in different message groups might be processed out of order) and different duplicate ID for every message }
By monitoring the EC2 console you could see that new instances are being created and the FIFO queue becomes empty because when the function is triggered the particular message also will be automatically deleted.

### THANK YOU
