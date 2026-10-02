"""
This file registers the model with the Python SDK.
"""

from viam.resource.registry import Registry, ResourceRegistration

from .api import ActionClient, ActionRPCService, Action

Registry.register_api(ResourceRegistration(Action, ActionRPCService, lambda name, channel: ActionClient(name, channel)))
