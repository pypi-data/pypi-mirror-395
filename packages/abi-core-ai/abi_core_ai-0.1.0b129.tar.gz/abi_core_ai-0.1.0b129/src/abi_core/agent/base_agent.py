"""
Base agent classes for ABI-Core.

This module provides the foundational classes for building AI agents in the
ABI-Core framework. It includes both Pydantic-based models for validation
and traditional class-based agents for runtime execution.
"""

import logging
from abc import ABC
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ModelAgent(BaseModel, ABC):
    """
    Pydantic-based base model for agents.
    
    This class provides validation and serialization capabilities for agent
    configurations using Pydantic. It's useful for agent metadata, configuration
    files, and API interactions.
    
    Attributes:
        agent_name: Unique identifier for the agent
        description: Human-readable description of the agent's purpose
        content_types: List of content types the agent can process (e.g., 'text/plain', 'application/json')
        
    Example:
        >>> class MyAgent(ModelAgent):
        ...     custom_field: str = "value"
        >>> agent = MyAgent(
        ...     agent_name="my-agent",
        ...     description="A custom agent",
        ...     content_types=["text/plain"]
        ... )
    """

    model_config = {
        'arbitrary_types_allowed': True,
        'extra': 'allow',
    }

    agent_name: str = Field(
        description='The name of the agent.',
    )

    description: str = Field(
        description="A brief description of the agent's purpose.",
    )

    content_types: List[str] = Field(
        description='Supported content types (e.g., text/plain, application/json).'
    )


class BaseAgent:
    """
    Base class for runtime agent execution.
    
    This class provides the core functionality for agent lifecycle management,
    including registration, task reception, and state management. All ABI agents
    should inherit from this class or its subclasses.
    
    Attributes:
        agent_name: Unique identifier for the agent
        description: Human-readable description of the agent's purpose
        content_types: List of content types the agent can process
        logger: Logger instance for the agent
        state: Dictionary for maintaining agent state between operations
        
    Example:
        >>> agent = BaseAgent(
        ...     agent_name="example-agent",
        ...     description="An example agent",
        ...     content_types=["text/plain"]
        ... )
        >>> agent.register()
        >>> agent.receive({"task": "process data"})
        >>> agent.clear_state()
    """
    
    def __init__(
        self,
        agent_name: str,
        description: str,
        content_types: Optional[List[str]] = None
    ):
        """
        Initialize a base agent.
        
        Args:
            agent_name: Unique identifier for the agent
            description: Human-readable description of the agent's purpose
            content_types: List of content types the agent can process.
                          Defaults to ["text/plain"] if not provided.
        """
        self.agent_name = agent_name
        self.description = description
        self.content_types = content_types or ["text/plain"]
        self.logger = logging.getLogger(agent_name)
        self.state: Dict[str, Any] = {}

    def register(self) -> None:
        """
        Register the agent with the system.
        
        This method is called when the agent is initialized and ready to
        receive tasks. Override this method to add custom registration logic.
        """
        self.logger.info(f"[{self.agent_name}] Registered.")

    def receive(self, task: Any) -> None:
        """
        Receive and log a task.
        
        This method is called when the agent receives a new task. Override
        this method to implement custom task handling logic.
        
        Args:
            task: The task to be processed. Can be any type depending on
                 the agent's implementation.
        """
        self.logger.info(f"[{self.agent_name}] Received task: {task}")

    def clear_state(self) -> None:
        """
        Clear the agent's internal state.
        
        This method resets the agent's state dictionary. Call this method
        when you need to reset the agent between operations or sessions.
        """
        self.state.clear()
        self.logger.info(f"[{self.agent_name}] State cleared.")

