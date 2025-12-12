
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
from typing import List

from logging import getLogger
from logging import Logger

from neuro_san.internals.validation.network.abstract_network_validator import AbstractNetworkValidator


class UrlNetworkValidator(AbstractNetworkValidator):
    """
    AbstractNetworkValidator that looks for correct URLs in an agent network
    """

    def __init__(self, external_agents: List[str] = None, mcp_servers: List[str] = None):
        """
        Constructor

        :param external_agents: A list of valid /external_agent referencess
        :param mcp_servers: A list of MCP servers, as read in from a mcp_info.hocon file
        """
        self.logger: Logger = getLogger(self.__class__.__name__)
        self.external_agents: List[str] = external_agents
        self.mcp_servers: List[str] = mcp_servers

    def validate_name_to_spec_dict(self, name_to_spec: Dict[str, Any]) -> List[str]:
        """
        Validate the agent network, specifically in the form of a name -> agent spec dictionary.
        Check if URL of MCP servers and external_agents are valid.

        :param name_to_spec: The name -> agent spec dictionary to validate
        :return: List of errors indicating invalid URL
        """
        errors: List[str] = []

        # Compile list of urls to check
        urls: List[str] = []
        if self.external_agents:
            urls.extend(self.external_agents)
        if self.mcp_servers:
            urls.extend(self.mcp_servers)

        self.logger.info("Validating URLs for MCP tools and subnetwork...")

        for agent_name, agent in name_to_spec.items():
            if agent.get("tools"):
                tools: List[str] = agent.get("tools")
                if tools:
                    safe_tools: List[str] = self.remove_dictionary_tools(tools)
                    self.check_safe_urls(agent_name, safe_tools, urls, errors)

        return errors

    def check_safe_urls(self, agent_name: str, safe_tools: List[str], urls: List[str], errors: List[str]):
        """
        Check that urls are valid

        :param agent_name: Name of agent
        :param safe_tools: List of tools
        :param urls: List of URLs
        :param errors: List of errors. Potentially modified on exit.
        """
        for tool in safe_tools:
            # pylint: disable=too-many-boolean-expressions
            if self.is_url_or_path(tool) and \
                    tool not in urls and \
                    not tool.startswith("http://") and \
                    not tool.startswith("https://") and \
                    not tool.endswith("mcp") and \
                    not tool.endswith("mcp/"):
                error_msg = f"Agent '{agent_name}' has invalid URL or path in tools." + \
                            f" Invalid tool: '{tool}' urls: {urls}"
                errors.append(error_msg)
