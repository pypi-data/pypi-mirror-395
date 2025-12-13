"""Databricks Guard implementation."""
from dataclasses import dataclass

from virtueai.models import VirtueAIModel, DatabricksDbModel, VirtueAIResponseStatus, VirtueAIResponse
from openai import OpenAI
from .together_safety_model import TogetherSafetyModel
from virtueai.models import SafetyModel
import logging
import os
from virtueai.utils import init_logger
@dataclass
class GuardDatabricksConfig:
    databricks_api_key: str
    databricks_url: str
    databricks_db_model: DatabricksDbModel | str
    safety_model: VirtueAIModel
    virtueai_api_key: str | None = None
    max_tokens: int = 256
    safety_check_query: bool = True
    safety_check_response: bool = True

class GuardDatabricks:
    def __init__(self, config: GuardDatabricksConfig):
        init_logger()
        self.config = config
        logging.debug(f"[DEBUG] Initializing GuardDatabricks with config: {self.config}")
        try:
            self.databricks_client = OpenAI(
                api_key=self.config.databricks_api_key,
                base_url=self.config.databricks_url,
            )
        except Exception as e:
            logging.error(f"Error initializing Databricks client: {e}")
            raise e

        if self.config.virtueai_api_key:
            # self.together_client = Together(api_key=self.config.virtueai_api_key)
            self.safety_model: SafetyModel = TogetherSafetyModel(api_key=self.config.virtueai_api_key, safety_model=self.config.safety_model)
        else:
            self.safety_model: SafetyModel = None

    def databricks_chat(self, messages: list[dict]) -> str:
        # Call Databricks model
        try:
            model = self.config.databricks_db_model
            if isinstance(self.config.databricks_db_model, DatabricksDbModel):
                model = str(self.config.databricks_db_model.value)
            completion = self.databricks_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=self.config.max_tokens,
            )
            assistant_output = completion.choices[0].message.content

            # Handle potential list structure returned by some models
            if isinstance(assistant_output, list):
                assistant_output = " ".join(
                    item.get("text", "")
                    for item in assistant_output
                    if item.get("type") == "text"
                )

            return assistant_output
        except Exception as e:
            logging.error(f"Error calling Databricks model: {e}")
            raise e

    async def __safety_check(self, query: str) -> bool:
        if self.safety_model:
            try:
                return await self.safety_model(query)
            except Exception as e:
                logging.error(f"Error calling Safety model: {e}")
                return False
        else:
            return False

    async def __call__(
        self,
        messages,
    ) -> VirtueAIResponse:
        user_content = " ".join(m["content"] for m in messages if m["role"] == "user")
        logging.debug(f"GuardDatabricks Messages: {messages}")

        if self.config.safety_check_query:
            logging.debug(f"Safety check query: {user_content}")
            if not await self.__safety_check(user_content):
                return VirtueAIResponse(status=VirtueAIResponseStatus.UNSAFE, message="Sorry, I can't help with that.")
       
        # Databricks chat
        assistant_output = self.databricks_chat(messages)
        logging.debug(f"Assistant_output from databricks_chat: {assistant_output}")

        # Safety-check the model's response if flag enabled (treat output as a standalone user message)
        if self.config.safety_check_response:
            logging.debug(f"Safety check response: {assistant_output}")
            if not await self.__safety_check(assistant_output):
                return VirtueAIResponse(status=VirtueAIResponseStatus.UNSAFE, message="Sorry, I can't help with that.")

        logging.debug(f"Returning VirtueAIResponse with validated_output: {assistant_output}")
        return VirtueAIResponse(status=VirtueAIResponseStatus.SUCCESS, validated_output=assistant_output)
