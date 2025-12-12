
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

from langchain_core.language_models.base import BaseLanguageModel

from neuro_san.internals.run_context.langchain.llms.llm_policy import LlmPolicy


class LangChainLlmResources:
    """
    Class for representing a LangChain model
    together with run-time policy necessary for model usage by the service.
    """

    def __init__(self, model: BaseLanguageModel, llm_policy: LlmPolicy = None):
        """
        Constructor.
        :param model: Language model used.
        :param llm_policy: optional LlmPolicy object to manage connections to LLM host.
        """
        self.model: BaseLanguageModel = model
        self.llm_policy: LlmPolicy = llm_policy

    def get_model(self) -> BaseLanguageModel:
        """
        :return: the BaseLanguageModel
        """
        return self.model

    def get_llm_policy(self) -> LlmPolicy:
        """
        :return: the LlmPolicy used by the model
        """
        return self.llm_policy

    async def delete_resources(self):
        """
        Release the run-time resources used by the model
        """
        if self.llm_policy is not None:
            await self.llm_policy.delete_resources()
