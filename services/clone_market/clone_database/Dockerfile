FROM ubuntu@sha256:67211c14fa74f070d27cc59d69a7fa9aeff8e28ea118ef3babc295a0428a6d21

WORKDIR /app

RUN apt-get update && apt-get install -y \
  build-essential \
  libboost-all-dev \
  uuid-dev

RUN apt update && apt install -y protobuf-compiler
RUN apt install -y libgrpc-dev libgrpc++-dev libprotobuf-dev protobuf-compiler-grpc
RUN apt install nlohmann-json3-dev wget
ADD server ./server
ADD http_server ./http_server
COPY conf.txt .

EXPOSE 50051

CMD ["sh", "-c", "./server 50051 & ./http_server"]
