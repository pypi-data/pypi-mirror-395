import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
from sfn_llm_client import CostCallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

class BaseLangChainAgent(ABC):
    def __init__(self, cfg: BaseModel, retries: int = 3):
        self.retries = retries
        self.cb = CostCallbackHandler(logger=logging.getLogger(__name__))
        self.llm = self._load(cfg)

    def _load(self, cfg):
        config_dict = cfg.model_dump(); provider = config_dict.pop("provider")
        models = {"openai": ChatOpenAI} 
        if provider not in models: raise ValueError(f"Unsupported: {provider}")
        return models[provider](**config_dict)

    def route_with_langchain(self, system_prompt, user_prompt, schema: BaseModel = None):
        self.cb.reset()
        model = self.llm.with_structured_output(schema) if schema else self.llm
        chain = ChatPromptTemplate.from_messages([("system", "{system}"), ("user", "{user}")]) | model.with_retry(stop_after_attempt=self.retries, wait_exponential_jitter=True, retry_if_exception_type=(TimeoutError, ConnectionError),)
        
        result = chain.invoke({"system": system_prompt, "user": user_prompt}, config={"callbacks": [self.cb]})
        return result if schema else result.content, {"total_tokens": self.cb.total_tokens, "prompt_tokens": self.cb.prompt_tokens, "completion_tokens": self.cb.completion_tokens, "total_cost_usd": self.cb.total_cost}

