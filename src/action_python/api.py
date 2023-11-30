import abc
from typing import Any, Final, Sequence, Mapping

from grpclib.client import Channel
from grpclib.server import Stream

from viam.resource.rpc_service_base import ResourceRPCServiceBase
from viam.resource.types import RESOURCE_TYPE_SERVICE, Subtype
from viam.services.service_base import ServiceBase
from viam.utils import sensor_readings_native_to_value, sensor_readings_value_to_native

from .grpc.action_grpc import ActionServiceBase, ActionServiceStub

from .grpc.action_pb2 import StartRequest, StartResponse, StopRequest, StopResponse, IsRunningRequest, IsRunningResponse, StatusRequest, StatusResponse


class Action(ServiceBase):

    SUBTYPE: Final = Subtype("viam-labs", RESOURCE_TYPE_SERVICE, "action")

    # update with actual API methods
    @abc.abstractmethod
    async def start(self) -> str:
        ...

    async def stop(self) -> str:
        ...

    async def is_running(self) -> bool:
        ...

    async def status(self) -> dict:
        ...

class ActionRPCService(ActionServiceBase, ResourceRPCServiceBase):

    RESOURCE_TYPE = Action

    async def Start(self, stream: Stream[StartRequest, StartResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        resp = await service.start()
        await stream.send_message(StartResponse(text=resp))

    async def Stop(self, stream: Stream[StopRequest, StopResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        resp = await service.stop()
        await stream.send_message(StopResponse(text=resp))

    async def IsRunning(self, stream: Stream[IsRunningRequest, IsRunningResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        resp = await service.is_running()
        await stream.send_message(IsRunningResponse(running=resp))

    async def Status(self, stream: Stream[StatusRequest, StatusResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        resp = await service.status()
        
        await stream.send_message(StatusResponse(status=sensor_readings_native_to_value(resp)))

class ActionClient(Action):

    def __init__(self, name: str, channel: Channel) -> None:
        self.channel = channel
        self.client = ActionServiceStub(channel)
        super().__init__(name)

    async def start(self) -> str:
        request = StartRequest(name=self.name)
        response: StartResponse = await self.client.Start(request)
        return response.text

    async def stop(self) -> str:
        request = StopRequest(name=self.name)
        response: StopResponse = await self.client.Stop(request)
        return response.text
    
    async def is_running(self) -> bool:
        request = IsRunningRequest(name=self.name)
        response: IsRunningResponse = await self.client.IsRunning(request)
        return response.running
    
    async def status(self) -> Mapping[str, Any]:
        request = StatusRequest(name=self.name)
        response: StatusResponse = await self.client.Status(request)
        return sensor_readings_value_to_native(response.status)