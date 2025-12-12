
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
from typing import Dict

from grpc import RpcMethodHandler
from grpc import unary_stream_rpc_method_handler
from grpc import unary_unary_rpc_method_handler

import neuro_san.api.grpc.agent_pb2 as agent__pb2
from neuro_san.api.grpc.agent_pb2_grpc import AgentServiceServicer


class AgentServicerToServer:
    """
    Taken from generated gRPC code from the agent_pb2_grpc.py file
    so multiple services of the same service protobuf construction can be serviced
    by the same server with a simple addition of an agent name in the gRPC path.
    """

    def __init__(self, servicer: AgentServiceServicer):
        """
        Constructor
        """
        self.servicer: AgentServiceServicer = servicer

    def build_rpc_handlers(self):
        """
        Constructs a table of RpcMethodHandlers
        to be used for an agent service
        """
        # One entry for each grpc method defined in the agent handling protobuf
        # Note that all methods (as of 8/27/2024) are unary_unary.
        # (Watch generated _grpc.py for changes).
        # pylint: disable=no-member
        rpc_method_handlers: Dict[str, RpcMethodHandler] = {
            'Function': unary_unary_rpc_method_handler(
                    self.servicer.Function,
                    request_deserializer=agent__pb2.FunctionRequest.FromString,
                    response_serializer=agent__pb2.FunctionResponse.SerializeToString,
            ),
            'Connectivity': unary_unary_rpc_method_handler(
                    self.servicer.Connectivity,
                    request_deserializer=agent__pb2.ConnectivityRequest.FromString,
                    response_serializer=agent__pb2.ConnectivityResponse.SerializeToString,
            ),
            'StreamingChat': unary_stream_rpc_method_handler(
                    self.servicer.StreamingChat,
                    request_deserializer=agent__pb2.ChatRequest.FromString,
                    response_serializer=agent__pb2.ChatResponse.SerializeToString,
            ),
        }
        return rpc_method_handlers
