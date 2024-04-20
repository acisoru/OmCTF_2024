# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import clone_market_pb2 as clone__market__pb2


class CloneMarketStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SignIn = channel.unary_unary(
                '/clone_market.CloneMarket/SignIn',
                request_serializer=clone__market__pb2.SignInRequest.SerializeToString,
                response_deserializer=clone__market__pb2.SignInResponse.FromString,
                )
        self.SignOut = channel.unary_unary(
                '/clone_market.CloneMarket/SignOut',
                request_serializer=clone__market__pb2.SignOutRequest.SerializeToString,
                response_deserializer=clone__market__pb2.SignOutResponse.FromString,
                )
        self.SignUp = channel.unary_unary(
                '/clone_market.CloneMarket/SignUp',
                request_serializer=clone__market__pb2.SignUpRequest.SerializeToString,
                response_deserializer=clone__market__pb2.SignUpResponse.FromString,
                )
        self.GetClones = channel.unary_unary(
                '/clone_market.CloneMarket/GetClones',
                request_serializer=clone__market__pb2.GetClonesRequest.SerializeToString,
                response_deserializer=clone__market__pb2.GetClonesResponse.FromString,
                )
        self.CreateClone = channel.unary_unary(
                '/clone_market.CloneMarket/CreateClone',
                request_serializer=clone__market__pb2.CreateCloneRequest.SerializeToString,
                response_deserializer=clone__market__pb2.CreateCloneResponse.FromString,
                )
        self.CreateCloneFromURL = channel.unary_unary(
                '/clone_market.CloneMarket/CreateCloneFromURL',
                request_serializer=clone__market__pb2.CreateCloneFromURLRequest.SerializeToString,
                response_deserializer=clone__market__pb2.CreateCloneFromURLResponse.FromString,
                )
        self.Ping = channel.unary_unary(
                '/clone_market.CloneMarket/Ping',
                request_serializer=clone__market__pb2.PingRequest.SerializeToString,
                response_deserializer=clone__market__pb2.PingResponse.FromString,
                )
        self.GetCloneByUUID = channel.unary_unary(
                '/clone_market.CloneMarket/GetCloneByUUID',
                request_serializer=clone__market__pb2.GetCloneByUUIDRequest.SerializeToString,
                response_deserializer=clone__market__pb2.GetCloneByUUIDResponse.FromString,
                )


class CloneMarketServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SignIn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SignOut(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SignUp(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetClones(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateClone(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateCloneFromURL(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCloneByUUID(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CloneMarketServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SignIn': grpc.unary_unary_rpc_method_handler(
                    servicer.SignIn,
                    request_deserializer=clone__market__pb2.SignInRequest.FromString,
                    response_serializer=clone__market__pb2.SignInResponse.SerializeToString,
            ),
            'SignOut': grpc.unary_unary_rpc_method_handler(
                    servicer.SignOut,
                    request_deserializer=clone__market__pb2.SignOutRequest.FromString,
                    response_serializer=clone__market__pb2.SignOutResponse.SerializeToString,
            ),
            'SignUp': grpc.unary_unary_rpc_method_handler(
                    servicer.SignUp,
                    request_deserializer=clone__market__pb2.SignUpRequest.FromString,
                    response_serializer=clone__market__pb2.SignUpResponse.SerializeToString,
            ),
            'GetClones': grpc.unary_unary_rpc_method_handler(
                    servicer.GetClones,
                    request_deserializer=clone__market__pb2.GetClonesRequest.FromString,
                    response_serializer=clone__market__pb2.GetClonesResponse.SerializeToString,
            ),
            'CreateClone': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateClone,
                    request_deserializer=clone__market__pb2.CreateCloneRequest.FromString,
                    response_serializer=clone__market__pb2.CreateCloneResponse.SerializeToString,
            ),
            'CreateCloneFromURL': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateCloneFromURL,
                    request_deserializer=clone__market__pb2.CreateCloneFromURLRequest.FromString,
                    response_serializer=clone__market__pb2.CreateCloneFromURLResponse.SerializeToString,
            ),
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=clone__market__pb2.PingRequest.FromString,
                    response_serializer=clone__market__pb2.PingResponse.SerializeToString,
            ),
            'GetCloneByUUID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCloneByUUID,
                    request_deserializer=clone__market__pb2.GetCloneByUUIDRequest.FromString,
                    response_serializer=clone__market__pb2.GetCloneByUUIDResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'clone_market.CloneMarket', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CloneMarket(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SignIn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clone_market.CloneMarket/SignIn',
            clone__market__pb2.SignInRequest.SerializeToString,
            clone__market__pb2.SignInResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SignOut(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clone_market.CloneMarket/SignOut',
            clone__market__pb2.SignOutRequest.SerializeToString,
            clone__market__pb2.SignOutResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SignUp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clone_market.CloneMarket/SignUp',
            clone__market__pb2.SignUpRequest.SerializeToString,
            clone__market__pb2.SignUpResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetClones(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clone_market.CloneMarket/GetClones',
            clone__market__pb2.GetClonesRequest.SerializeToString,
            clone__market__pb2.GetClonesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateClone(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clone_market.CloneMarket/CreateClone',
            clone__market__pb2.CreateCloneRequest.SerializeToString,
            clone__market__pb2.CreateCloneResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateCloneFromURL(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clone_market.CloneMarket/CreateCloneFromURL',
            clone__market__pb2.CreateCloneFromURLRequest.SerializeToString,
            clone__market__pb2.CreateCloneFromURLResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clone_market.CloneMarket/Ping',
            clone__market__pb2.PingRequest.SerializeToString,
            clone__market__pb2.PingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCloneByUUID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clone_market.CloneMarket/GetCloneByUUID',
            clone__market__pb2.GetCloneByUUIDRequest.SerializeToString,
            clone__market__pb2.GetCloneByUUIDResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
