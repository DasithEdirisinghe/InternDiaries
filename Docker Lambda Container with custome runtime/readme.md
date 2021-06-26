### This is regarding how to develop a docker lambda nodejs runtime on top of a python based image and invoke the lambda function using the AWS latest container image support.

[Read this article to get complete insight](https://dasith-dev.medium.com/create-a-docker-container-image-with-custom-lambda-runtime-c1c73944d87e)

# 1

#### Here I have already created the python base image and pushed into the docker hub. You can find the repo [here](https://hub.docker.com/repository/docker/dasithdev/python-app)

Here I have used Lambda RIC to make the image lambda compatible.
**The Lambda Runtime Interface Client** is a lightweight interface that allows the runtime to receive requests from and send requests to the Lambda service.

The Lambda NodeJS Runtime Interface Client is vended through `npm`. You can include this package in your preferred base image to make that base image Lambda compatible.

So make sure to run following command from the working directory to add this dependency to package.json
In case of an error try to install other dependencies which are in dockerfile

`npm install aws-lambda-ric --save
`

In case of an error try to install below dependencies and reinstall Nodejs RIC

```
    autoconf

    libtool 
    
    g++
    
    make
    
    cmake
    
    libcurl4-openssl-dev
```

# 2

* Then build the docker image using Dockerfile
* Tag the image
* Push the image into the AWS ECR

# 3

* Create a Lambda Function using Pushed container image
* Choose relevant function invocation event


