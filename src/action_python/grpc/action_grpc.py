# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: action.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import google.api.annotations_pb2
import google.protobuf.struct_pb2
from . import action_pb2


class ActionServiceBase(abc.ABC):

    @abc.abstractmethod
    async def Start(self, stream: 'grpclib.server.Stream[action_pb2.StartRequest, action_pb2.StartResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Stop(self, stream: 'grpclib.server.Stream[action_pb2.StopRequest, action_pb2.StopResponse]') -> None:
        pass

    @abc.abstractmethod
    async def IsRunning(self, stream: 'grpclib.server.Stream[action_pb2.IsRunningRequest, action_pb2.IsRunningResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Status(self, stream: 'grpclib.server.Stream[action_pb2.StatusRequest, action_pb2.StatusResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/viamlabs.services.action.v1.ActionService/Start': grpclib.const.Handler(
                self.Start,
                grpclib.const.Cardinality.UNARY_UNARY,
                action_pb2.StartRequest,
                action_pb2.StartResponse,
            ),
            '/viamlabs.services.action.v1.ActionService/Stop': grpclib.const.Handler(
                self.Stop,
                grpclib.const.Cardinality.UNARY_UNARY,
                action_pb2.StopRequest,
                action_pb2.StopResponse,
            ),
            '/viamlabs.services.action.v1.ActionService/IsRunning': grpclib.const.Handler(
                self.IsRunning,
                grpclib.const.Cardinality.UNARY_UNARY,
                action_pb2.IsRunningRequest,
                action_pb2.IsRunningResponse,
            ),
            '/viamlabs.services.action.v1.ActionService/Status': grpclib.const.Handler(
                self.Status,
                grpclib.const.Cardinality.UNARY_UNARY,
                action_pb2.StatusRequest,
                action_pb2.StatusResponse,
            ),
        }


class ActionServiceStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Start = grpclib.client.UnaryUnaryMethod(
            channel,
            '/viamlabs.services.action.v1.ActionService/Start',
            action_pb2.StartRequest,
            action_pb2.StartResponse,
        )
        self.Stop = grpclib.client.UnaryUnaryMethod(
            channel,
            '/viamlabs.services.action.v1.ActionService/Stop',
            action_pb2.StopRequest,
            action_pb2.StopResponse,
        )
        self.IsRunning = grpclib.client.UnaryUnaryMethod(
            channel,
            '/viamlabs.services.action.v1.ActionService/IsRunning',
            action_pb2.IsRunningRequest,
            action_pb2.IsRunningResponse,
        )
        self.Status = grpclib.client.UnaryUnaryMethod(
            channel,
            '/viamlabs.services.action.v1.ActionService/Status',
            action_pb2.StatusRequest,
            action_pb2.StatusResponse,
        )
