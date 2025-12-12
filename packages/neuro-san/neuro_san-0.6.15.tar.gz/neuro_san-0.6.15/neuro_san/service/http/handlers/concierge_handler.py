
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
"""
See class comment for details
"""
from typing import Any
from typing import Dict

from neuro_san.interfaces.concierge_session import ConciergeSession
from neuro_san.internals.network_providers.agent_network_storage import AgentNetworkStorage
from neuro_san.service.http.handlers.base_request_handler import BaseRequestHandler
from neuro_san.session.direct_concierge_session import DirectConciergeSession


class ConciergeHandler(BaseRequestHandler):
    """
    Handler class for neuro-san "concierge" API call.
    """

    def get(self):
        """
        Implementation of GET request handler for "concierge" API call.
        """
        metadata: Dict[str, Any] = self.get_metadata()
        self.application.start_client_request(metadata, "/api/v1/list")
        network_storage_dict: Dict[str, AgentNetworkStorage] = self.server_context.get_network_storage_dict()
        public_storage: AgentNetworkStorage = network_storage_dict.get("public")
        try:
            data: Dict[str, Any] = {}
            session: ConciergeSession = DirectConciergeSession(public_storage, metadata=metadata)
            result_dict: Dict[str, Any] = session.list(data)

            # Return response to the HTTP client
            self.set_header("Content-Type", "application/json")
            self.write(result_dict)

        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.process_exception(exc)
        finally:
            self.do_finish()
            self.application.finish_client_request(metadata, "/api/v1/list")
