
# Copyright © 2023-2025 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

from grpc import Channel
from grpc import UnaryUnaryMultiCallable
from grpc import UnaryStreamMultiCallable

import neuro_san.api.grpc.agent_pb2 as agent__pb2


# pylint: disable=too-many-instance-attributes
class AgentServiceStub:
    """
    The service comprises all the exchanges to the backend in support of agent services.
    """

    def __init__(self, agent_name: str = ""):
        """
        Constructor.
        """
        self._agent_name: str = agent_name

        # Stub methods. These all happen to be the same kind of method, but
        # note that thare are more defined on grpc.Channel if needed (see the source).
        # pylint: disable=invalid-name
        self.Function: UnaryUnaryMultiCallable = None
        self.Connectivity: UnaryUnaryMultiCallable = None
        self.StreamingChat: UnaryStreamMultiCallable = None

    def set_agent_name(self, agent_name: str):
        """
        Exclusively called by ForwardedAgentSession.

        :param agent_name: the agent name to set
        """
        self._agent_name = agent_name

    def get_agent_name(self) -> str:
        """
        Exclusively called by tests.
        :return: the agent_name
        """
        return self._agent_name

    def __call__(self, channel: Channel):
        """
        Because of how service stubs are used to being passed around
        like a class, we use __call__() to short circuit a constructor-like
        call to use an actual instance.
        """

        # Prepare the service name given the agent name
        service_name: str = self.prepare_service_name(self._agent_name)

        # Below comes from generated _grpc.py code for the Stub,
        # with the modification of the service name going into the args.
        # One member variable for each grpc method.
        # pylint: disable=no-member
        self.Function = channel.unary_unary(
                f"/{service_name}/Function",
                request_serializer=agent__pb2.FunctionRequest.SerializeToString,
                response_deserializer=agent__pb2.FunctionResponse.FromString,
                )
        self.Connectivity = channel.unary_unary(
                f"/{service_name}/Connectivity",
                request_serializer=agent__pb2.ConnectivityRequest.SerializeToString,
                response_deserializer=agent__pb2.ConnectivityResponse.FromString,
                )
        self.StreamingChat = channel.unary_stream(
                f"/{service_name}/StreamingChat",
                request_serializer=agent__pb2.ChatRequest.SerializeToString,
                response_deserializer=agent__pb2.ChatResponse.FromString,
                )

        return self

    @staticmethod
    def prepare_service_name(agent_name: str) -> str:
        """
        Prepares the full grpc service name given the name of the agent
        :param agent_name: The string agent name
        :return: A service name that specifies the agent name as part of the routing.
        """

        # Prepare the service name on a per-agent basis
        service_name: str = ""

        # The agent name adds the voodoo to handle the request routing for each
        # agent on the same server.
        if agent_name is not None and len(agent_name) > 0:
            if len(service_name) > 0:
                service_name += "."
            service_name += f"{agent_name}"

        # This string comes from the service definition within agent.proto
        service_name += ".AgentService"

        return service_name
