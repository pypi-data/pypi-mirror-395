
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

import html

from typing import Union


class RequestsUtil:
    """
    Utility helper class for MCP requests processing.
    """

    @staticmethod
    def safe_request_id(request_id: Union[int, str]) -> str:
        """
        Return HTML-safe representation of user request id to be sent back in MCP response.
        :param request_id: MCP request id (as received from user);
        :return: HTML-escaped request id string
        """
        if isinstance(request_id, str):
            return html.escape(request_id)
        # Do not escape integers, just return as-is
        # otherwise, MCP client gets confused and could reject this response
        if isinstance(request_id, int):
            return request_id
        return "invalid"

    @staticmethod
    def safe_message(msg: str) -> str:
        """
        Return HTML-safe representation of string message to be sent back in MCP response.
        :param msg: message string;
        :return: HTML-escaped message string
        """
        return html.escape(msg)
