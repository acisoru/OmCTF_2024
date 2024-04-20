FROM golang:1.21 as build_base

WORKDIR /app 

COPY . /app

#RUN ls && sleep 10

RUN CGO_ENABLED=0 go build -tags netgo,osusergo,static_build -o /shop /app/cmd

FROM alpine:3.18.4

COPY --from=build_base /shop /shop

CMD ["/shop"]
