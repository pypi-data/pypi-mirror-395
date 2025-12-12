
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


class KeywordNetworkValidator(AbstractNetworkValidator):
    """
    AgentNetworkValidator that looks for correct keywords in an agent network
    """

    def __init__(self):
        """
        Constructor
        """
        self.logger: Logger = getLogger(self.__class__.__name__)

    def validate_name_to_spec_dict(self, name_to_spec: Dict[str, Any]) -> List[str]:
        """
        Validate the agent network, specifically in the form of a name -> agent spec dictionary.

        :param name_to_spec: The name -> agent spec dictionary to validate
        :return: List of errors indicating agents and missing keywords
        """
        errors: List[str] = []

        self.logger.info("Validating agent network keywords...")

        # Currently, only required "instructions" for non-function agents.
        for agent_name, agent in name_to_spec.items():
            if agent.get("instructions") == "":
                error_msg = f"{agent_name} 'instructions' cannot be empty."
                errors.append(error_msg)

        # Only warn if there is a problem
        if len(errors) > 0:
            self.logger.warning(str(errors))

        return errors
