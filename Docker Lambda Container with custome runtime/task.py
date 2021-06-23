import sys
import boto3

ACCESS_KEY = 'xxxxxxxxxxxxxx'
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxx'
bucket_name = 'S3bucketname'
fileName = "pythontest.txt"
s3_file_name = fileName

def main():
    f = open(fileName,"w+")

    f.write(" TXT File is created")
   
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

