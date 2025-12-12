
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

from typing import Any
from typing import Dict

from leaf_common.session.abstract_service_session import AbstractServiceSession
from leaf_common.time.timeout import Timeout

from neuro_san.api.grpc import concierge_pb2 as concierge_messages
from neuro_san.api.grpc.concierge_pb2_grpc import ConciergeServiceStub
from neuro_san.interfaces.concierge_session import ConciergeSession


class GrpcConciergeSession(AbstractServiceSession, ConciergeSession):
    """
    Implementation of ConciergeSession that talks to a gRPC service.
    """

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, host: str = None,
                 port: str = None,
                 timeout_in_seconds: int = 30,
                 metadata: Dict[str, str] = None,
                 security_cfg: Dict[str, Any] = None,
                 umbrella_timeout: Timeout = None):
        """
        Creates a ConciergeSession that connects to the
        Concierge Service and delegates its implementations to the service.

        :param host: the service host to connect to
                        If None, will use a default
        :param port: the service port
                        If None, will use a default
        :param timeout_in_seconds: timeout to use when communicating
                        with the service
        :param metadata: A grpc metadata of key/value pairs to be inserted into
                         the header. Default is None. Preferred format is a
                         dictionary of string keys to string values.
        :param security_cfg: An optional dictionary of parameters used to
                        secure the TLS and the authentication of the gRPC
                        connection.  Supplying this implies use of a secure
                        GRPC Channel.  Default is None, uses insecure channel.
        :param umbrella_timeout: A Timeout object under which the length of all
                        looping and retries should be considered
        """
        use_host: str = "localhost"
        if host is not None:
            use_host = host

        use_port: str = str(self.DEFAULT_GRPC_PORT)
        if port is not None:
            use_port = port

        service_stub = ConciergeServiceStub
        AbstractServiceSession.__init__(self, "Concierge",
                                        service_stub,
                                        use_host, use_port,
                                        timeout_in_seconds, metadata,
                                        security_cfg, umbrella_timeout,
                                        timeout_in_seconds)

    def list(self, request_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        :param request_dict: A dictionary version of the ConciergeRequest
                    protobuf structure. Has the following keys:
                        <None>
        :return: A dictionary version of the ConciergeResponse
                    protobuf structure. Has the following keys:
                "agents" - the sequence of dictionaries describing available agents
        """
        # pylint: disable=no-member
        return self.call_grpc_method(
            "list",
            self._list_from_stub,
            request_dict,
            concierge_messages.ConciergeRequest())

    @staticmethod
    def _list_from_stub(stub, timeout_in_seconds,
                        metadata, credentials, *args):
        """
        Global method associated with the session that calls List
        given a grpc Stub already set up with a channel (socket) to call with.
        """
        response = stub.List(*args, timeout=timeout_in_seconds,
                             metadata=metadata,
                             credentials=credentials)
        return response
