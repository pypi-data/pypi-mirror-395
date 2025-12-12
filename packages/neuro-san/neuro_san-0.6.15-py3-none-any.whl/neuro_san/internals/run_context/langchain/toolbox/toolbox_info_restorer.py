
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

import json

from pyparsing.exceptions import ParseException
from pyparsing.exceptions import ParseSyntaxException

from leaf_common.persistence.easy.easy_hocon_persistence import EasyHoconPersistence
from leaf_common.persistence.interface.restorer import Restorer

from neuro_san import TOP_LEVEL_DIR


class ToolboxInfoRestorer(Restorer):
    """
    Implementation of the Restorer interface to read in a ToolboxInfo dictionary
    instance given a hocon file name.
    """

    def restore(self, file_reference: str = None):
        """
        :param file_reference: The file reference to use when restoring.
                Default is None, implying the file reference is up to the
                implementation.
        :return: an object from some persisted store
        """
        config: Dict[str, Any] = None

        use_file: str = file_reference

        if file_reference is None or len(file_reference) == 0:
            # Read from the default
            use_file = TOP_LEVEL_DIR.get_file_in_basis("internals/run_context/langchain/toolbox/toolbox_info.hocon")

        try:
            if use_file.endswith(".json"):
                config = json.load(use_file)
            elif use_file.endswith(".hocon"):
                hocon = EasyHoconPersistence(full_ref=use_file, must_exist=True)
                config = hocon.restore()
            else:
                raise ValueError(f"file_reference {use_file} must be a .json or .hocon file")
        except (ParseException, ParseSyntaxException, json.decoder.JSONDecodeError) as exception:
            message = f"""
There was an error parsing the toolbox_info file "{use_file}".
See the accompanying ParseException (above) for clues as to what might be
syntactically incorrect in that file.
"""
            raise ParseException(message) from exception

        return config
