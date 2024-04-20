FROM ubuntu:24.04

RUN apt update && apt install -y socat libgmp-dev

WORKDIR /

COPY kekogram /kekogram
RUN chmod +x /kekogram

CMD ["socat", "TCP-LISTEN:2112,reuseaddr,fork", "EXEC:/kekogram"]
