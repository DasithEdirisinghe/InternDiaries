import sys
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAYCVXP4N2A5KIILGR'
SECRET_KEY = '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'
bucket_name = 'nodepythonduebucket'
fileName = "pythontest.txt"
s3_file_name = fileName

def main():
    f = open(fileName,"w+")

    f.write(" TXT File is created")
    
    print(f.name)
    
    f.close()

def upload_to_aws(local_file, bucket, s3_file):
    

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

    

if __name__ == "__main__":
    main()
    f = open(fileName,"r+")
    upload_to_aws(f.name, bucket_name, s3_file_name)

