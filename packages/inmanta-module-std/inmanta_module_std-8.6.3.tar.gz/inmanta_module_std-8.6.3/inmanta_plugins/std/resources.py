"""
Copyright 2016 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

import logging

from inmanta import data
from inmanta.agent.handler import CRUDHandler, HandlerContext, ResourcePurged, provider
from inmanta.resources import (
    IgnoreResourceException,
    ManagedResource,
    PurgeableResource,
    resource,
)

LOGGER = logging.getLogger(__name__)


@resource("std::testing::NullResource", agent="agentname", id_attribute="name")
class Null(ManagedResource, PurgeableResource):
    fields = ("name", "agentname", "fail", "value", "int_value")


@resource("std::AgentConfig", agent="agent", id_attribute="agentname")
class AgentConfig(PurgeableResource):
    """
    A resource that can modify the agentmap for autostarted agents
    """

    fields = ("agentname", "uri", "autostart")

    @staticmethod
    def get_autostart(exp, obj):
        try:
            if not obj.autostart:
                raise IgnoreResourceException()
        except Exception:
            # When this attribute is not set, also ignore it
            raise IgnoreResourceException()
        return obj.autostart


@provider("std::testing::NullResource", name="null")
class NullProvider(CRUDHandler):
    """Does nothing at all"""

    def read_resource(self, ctx: HandlerContext, resource: PurgeableResource) -> None:
        if resource.fail:
            raise Exception("This resource is set to fail")
        ctx.debug("Observed value: %(value)s", value=resource.value)
        ctx.debug("Observed int value: %(value)s", value=resource.int_value)
        return

    def create_resource(self, ctx: HandlerContext, resource: PurgeableResource) -> None:
        ctx.set_created()

    def delete_resource(self, ctx: HandlerContext, resource: PurgeableResource) -> None:
        ctx.set_purged()

    def update_resource(
        self, ctx: HandlerContext, changes: dict, resource: PurgeableResource
    ) -> None:
        ctx.set_updated()


@provider("std::AgentConfig", name="agentrest")
class AgentConfigHandler(CRUDHandler):

    # If this evaluates to True, it means we are running against an ISO (ISO8+) or OSS
    # version that doesn't have the AUTOSTARTED_AGENT_MAP environment configuration
    # option anymore. In that case this handler should not make any changes.
    has_autostarted_agent_map: bool = hasattr(data, "AUTOSTART_AGENT_MAP")

    def _get_map(self) -> dict:
        def call():
            return self.get_client().get_setting(
                tid=self._agent.environment, id=data.AUTOSTART_AGENT_MAP
            )

        value = self.run_sync(call)
        return value.result["value"]

    def _set_map(self, agent_config: dict) -> None:
        def call():
            return self.get_client().set_setting(
                tid=self._agent.environment,
                id=data.AUTOSTART_AGENT_MAP,
                value=agent_config,
            )

        return self.run_sync(call)

    def read_resource(self, ctx: HandlerContext, resource: AgentConfig) -> None:
        if not self.has_autostarted_agent_map:
            ctx.info(
                msg="Not making any changes, because we are running against a version of the Inmanta server"
                " that doesn't have the the autostarted_agent_map configuration option anymore."
                " It's recommended to remove this resource from the configuration model."
            )
            return
        agent_config = self._get_map()
        ctx.set("map", agent_config)

        if resource.agentname not in agent_config:
            raise ResourcePurged()

        resource.uri = agent_config[resource.agentname]

    def create_resource(self, ctx: HandlerContext, resource: AgentConfig) -> None:
        if not self.has_autostarted_agent_map:
            return
        agent_config = ctx.get("map")
        agent_config[resource.agentname] = resource.uri
        self._set_map(agent_config)

    def delete_resource(self, ctx: HandlerContext, resource: AgentConfig) -> None:
        if not self.has_autostarted_agent_map:
            return
        agent_config = ctx.get("map")
        del agent_config[resource.agentname]
        self._set_map(agent_config)

    def update_resource(
        self, ctx: HandlerContext, changes: dict, resource: AgentConfig
    ) -> None:
        if not self.has_autostarted_agent_map:
            return
        agent_config = ctx.get("map")
        agent_config[resource.agentname] = resource.uri
        self._set_map(agent_config)
