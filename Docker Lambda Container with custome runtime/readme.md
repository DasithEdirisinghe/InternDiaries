## This is regarding how to develop a docker lambda nodejs runtime on top of a python based image and invoke the lambda function using the AWS latest container image support.

#### Here I have already created the python base image and pushed into the docker hub. You can find the repo [here](https://hub.docker.com/repository/docker/dasithdev/python-app)

The Lambda Runtime Interface Client is a lightweight interface that allows the runtime to receive requests from and send requests to the Lambda service.

**The Lambda NodeJS Runtime Interface Client** is vended through `npm`. You can include this package in your preferred base image to make that base image Lambda compatible.

So make sure to run following command from the working directory to add this dependency to package.json

`npm install aws-lambda-ric --save
`

`task.py` is located in /usr/scr/app dir in the base python image.
