import os
from typing import Optional, Any, List, Dict
from django.conf import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

class AdemaBaseAgent:
    """
    Base agent class for ADEMA applications.
    Supports switching between Local (Ollama) and Cloud (OpenAI) providers.
    """
    
    def __init__(self):
        self.provider = getattr(settings, 'AI_PROVIDER', 'ollama').lower()
        self.model_name = getattr(settings, 'AI_MODEL', 'llama3')
        self.base_url = getattr(settings, 'AI_BASE_URL', 'http://localhost:11434')
        self.api_key = getattr(settings, 'AI_API_KEY', None)
        
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self) -> BaseChatModel:
        """Initialize the LLM based on configuration."""
        if self.provider == 'openai':
            return ChatOpenAI(
                model=self.model_name,
                api_key=self.api_key
            )
        else:
            # Default to Ollama
            return ChatOllama(
                base_url=self.base_url,
                model=self.model_name
            )
            
    def get_tools(self) -> List[Any]:
        """
        Return a list of tools available to this agent.
        Override this method in subclasses.
        """
        return []
        
    def get_prompt(self) -> ChatPromptTemplate:
        """
        Return the prompt template for the agent.
        Override this method in subclasses.
        """
        return ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

    def run(self, query: str) -> Any:
        """
        Execute the agent with the given query.
        """
        tools = self.get_tools()
        prompt = self.get_prompt()
        
        # If tools are provided, use an agent
        if tools:
            # We use create_tool_calling_agent which works with models that support tool calling
            # For Ollama, ensure you are using a model that supports it (e.g. llama3)
            agent = create_tool_calling_agent(self.llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
            return agent_executor.invoke({"input": query})
        else:
            # Direct LLM call if no tools
            chain = prompt | self.llm
            return chain.invoke({"input": query})
