
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
from neuro_san.service.generic.async_agent_service_provider import AsyncAgentServiceProvider


class AgentAuthorizer:
    """
    Abstract interface implementing some policy
    of allowing to route incoming requests to an agent.
    """

    def allow(self, agent_name) -> AsyncAgentServiceProvider:
        """
        :param agent_name: name of an agent
        :return: instance of AsyncAgentService if routing requests is allowed for this agent;
                 None otherwise
        """
        raise NotImplementedError
