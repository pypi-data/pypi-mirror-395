import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
from sfn_llm_client import CostCallbackHandler
from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

class BaseLangChainAgent(ABC):
    def __init__(self, cfg: BaseModel, retries: int = 3):
        self.retries = retries
        self.cb = CostCallbackHandler(logger=logging.getLogger(__name__))
        self.llm = self._load(cfg)

    def _load(self, cfg):
        d = cfg.model_dump(); p = d.pop("provider")
        m = {"openai": ChatOpenAI} 
        if p not in m: raise ValueError(f"Unsupported: {p}")
        return m[p](**d)

    def route_with_langchain(self, sys, usr, schema: BaseModel = None):
        self.cb.reset()
        mod = self.llm.with_structured_output(schema) if schema else self.llm
        chain = ChatPromptTemplate.from_messages([("system", "{s}"), ("user", "{u}")]) | mod.with_retry(stop_after_attempt=self.retries, wait_exponential_jitter=True, retry_if_exception_type=(TimeoutError, ConnectionError),)
        
        res = chain.invoke({"s": sys, "u": usr}, config={"callbacks": [self.cb]})
        return res if schema else res.content, {"total_tokens": self.cb.total_tokens, "prompt_tokens": self.cb.prompt_tokens, "completion_tokens": self.cb.completion_tokens, "total_cost_usd": self.cb.total_cost}

