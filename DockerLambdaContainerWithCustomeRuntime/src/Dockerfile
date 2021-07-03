FROM dasithdev/python-app:latest

# Create app directory
WORKDIR /usr/src/node

# Install app dependencies
RUN apt-get update
RUN apt-get -y install curl dirmngr apt-transport-https lsb-release ca-certificates vim
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
    apt-get install -y \
    autoconf \
    libtool \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev


# Bundle app source
COPY . .

RUN npm install

EXPOSE 8080

ENTRYPOINT ["npx", "aws-lambda-ric"]
CMD [ "server.lambdaHandler" ]
