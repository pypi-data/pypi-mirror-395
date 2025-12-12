"""
ABI Agent implementation with policy and semantic enrichment.

This module provides the AbiAgent class, which extends BaseAgent with
semantic enrichment and policy evaluation capabilities.
"""

from typing import Any, Dict
from abi_core.agent.base_agent import BaseAgent
from abi_core.agent.policy import evaluate_policy
from abi_core.agent.semantics import enrich_input


class AbiAgent(BaseAgent):
    """
    ABI Agent with semantic enrichment and policy evaluation.
    
    This class extends BaseAgent to provide:
    - Semantic enrichment of input data for agent discovery
    - Policy evaluation for security and compliance
    - Structured input processing pipeline
    
    All ABI agents should inherit from this class to benefit from
    semantic layer integration and policy enforcement.
    
    Example:
        >>> class MyCustomAgent(AbiAgent):
        ...     def process(self, enriched_input):
        ...         query = enriched_input['query']
        ...         return {"result": f"Processed: {query}"}
        ...
        >>> agent = MyCustomAgent(
        ...     agent_name="custom-agent",
        ...     description="A custom agent with policies",
        ...     content_types=["text/plain"]
        ... )
        >>> result = agent.handle_input("Find an agent for data analysis")
    """
    
    def handle_input(self, input_data: Any) -> Dict[str, Any]:
        """
        Handle input with semantic enrichment and policy evaluation.
        
        This method implements the complete input processing pipeline:
        1. Enrich input with semantic context
        2. Evaluate security policies
        3. Process the enriched input
        
        Args:
            input_data: Raw input data (string, dict, or other types)
            
        Returns:
            Dict containing the processing result
            
        Raises:
            Exception: If policy evaluation rejects the input
            
        Example:
            >>> agent = AbiAgent("test-agent", "Test agent", ["text/plain"])
            >>> result = agent.handle_input("Process this data")
        """
        # Enrich input with semantic context
        enriched = enrich_input(input_data)
        
        # Evaluate security policies
        if not evaluate_policy(enriched):
            raise Exception(f"[{self.agent_name}] Policy rejected the input.")
        
        # Process the enriched input
        return self.process(enriched)

    def process(self, enriched_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process enriched input data.
        
        This method must be implemented by subclasses to define the agent's
        core processing logic. The input has already been enriched with
        semantic context and validated against policies.
        
        Args:
            enriched_input: Dictionary containing:
                - query: The processed query string
                - raw_input: Original input data
                - input_type: Type of input (text, structured, etc.)
                - semantic_context: Semantic metadata
                - metadata: Enrichment metadata
                
        Returns:
            Dict containing the processing result
            
        Raises:
            NotImplementedError: If not implemented by subclass
            
        Example:
            >>> class DataAgent(AbiAgent):
            ...     def process(self, enriched_input):
            ...         query = enriched_input['query']
            ...         return {"result": f"Analyzed: {query}"}
        """
        raise NotImplementedError(
            f"process() must be implemented by the subclass. "
            f"Agent: {self.agent_name}"
        )
