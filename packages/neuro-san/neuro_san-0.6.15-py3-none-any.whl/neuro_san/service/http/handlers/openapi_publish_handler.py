
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

import json

from neuro_san.service.http.handlers.base_request_handler import BaseRequestHandler


class OpenApiPublishHandler(BaseRequestHandler):
    """
    Handler class for neuro-san OpenAPI service spec publishing"concierge" API call.
    """

    def get(self):
        """
        Implementation of GET request handler
        for "publish my OpenAPI specification document" call.
        """
        metadata: Dict[str, Any] = self.get_metadata()
        self.application.start_client_request(metadata, "/api/v1/docs")
        try:
            with open(self.openapi_service_spec_path, "r", encoding='utf-8') as f_out:
                result_dict: Dict[str, Any] = json.load(f_out)
            # Return json data to the HTTP client
            self.set_header("Content-Type", "application/json")
            self.write(result_dict)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.process_exception(exc)
        finally:
            self.do_finish()
            self.application.finish_client_request(metadata, "/api/v1/docs")
