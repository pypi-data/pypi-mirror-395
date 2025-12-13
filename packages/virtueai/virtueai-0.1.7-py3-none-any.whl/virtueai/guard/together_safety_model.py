import logging
from together import AsyncTogether
from virtueai.models import VirtueAIModel, SafetyModel
import asyncio
from openai.types.chat import ChatCompletion

class TogetherSafetyModel(SafetyModel):
    def __init__(self, api_key: str, safety_model: VirtueAIModel):
        self.together_client = AsyncTogether(api_key=api_key)
        self.safety_model = safety_model.value

    async def __call__(self, query: str) -> bool:
        return await self.safety_check(query)

    async def safety_check(self, query: str) -> bool:
        try:
            logging.debug(f"Calling VirtueAI safety model with query: {query}")
            response: ChatCompletion = await self.together_client.chat.completions.create(
                model=self.safety_model,
                messages=[{"role": "user", "content": query}],
            )
            verdict = response.choices[0].message.content.strip().lower()
            logging.debug(f"VirtueAI safety model verdict: {verdict}")
            return verdict.startswith("safe")
        except Exception as exc:  # Fallback: if safety model fails, err on safe side
            return False
