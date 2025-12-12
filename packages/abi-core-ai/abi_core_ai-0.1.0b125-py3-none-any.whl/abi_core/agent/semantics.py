"""
Semantic enrichment for agent inputs.

This module provides semantic enrichment capabilities for agent inputs,
focusing on agent discovery and semantic context enhancement.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def enrich_input(input_data: Any) -> Dict[str, Any]:
    """
    Enrich input data with semantic context for agent discovery.
    
    This function prepares input data for semantic processing by:
    - Normalizing the input format
    - Adding metadata for agent discovery
    - Preparing context for semantic layer routing
    
    Args:
        input_data: Raw input data (can be string, dict, or other types)
        
    Returns:
        Dict containing enriched input with semantic metadata
        
    Example:
        >>> enriched = enrich_input("Find an agent for data analysis")
        >>> print(enriched['query'])
        'Find an agent for data analysis'
        >>> print(enriched['intent'])
        'agent_discovery'
    """
    # Normalize input to dict format
    if isinstance(input_data, str):
        enriched = {
            'query': input_data,
            'raw_input': input_data,
            'input_type': 'text'
        }
    elif isinstance(input_data, dict):
        enriched = {
            'query': input_data.get('query', str(input_data)),
            'raw_input': input_data,
            'input_type': 'structured'
        }
    else:
        enriched = {
            'query': str(input_data),
            'raw_input': input_data,
            'input_type': 'unknown'
        }
    
    # Add semantic metadata for agent discovery
    enriched['semantic_context'] = {
        'intent': 'agent_discovery',
        'requires_routing': True,
        'discovery_enabled': True
    }
    
    # Add timestamp and tracking
    from datetime import datetime
    enriched['metadata'] = {
        'enriched_at': datetime.utcnow().isoformat(),
        'enrichment_version': '1.0.0'
    }
    
    logger.debug(f"Input enriched for agent discovery: {enriched['query'][:50]}...")
    
    return enriched


def extract_intent(query: str) -> str:
    """
    Extract intent from a query for agent discovery.
    
    Args:
        query: User query string
        
    Returns:
        Detected intent (e.g., 'search', 'execute', 'analyze')
    """
    query_lower = query.lower()
    
    # Simple intent detection (can be enhanced with NLP)
    if any(word in query_lower for word in ['find', 'search', 'discover', 'locate']):
        return 'search'
    elif any(word in query_lower for word in ['execute', 'run', 'perform', 'do']):
        return 'execute'
    elif any(word in query_lower for word in ['analyze', 'process', 'compute']):
        return 'analyze'
    else:
        return 'general'


def prepare_for_semantic_layer(enriched_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare enriched data for semantic layer processing.
    
    Args:
        enriched_data: Enriched input data
        
    Returns:
        Data formatted for semantic layer consumption
    """
    return {
        'query': enriched_data['query'],
        'intent': extract_intent(enriched_data['query']),
        'context': enriched_data.get('semantic_context', {}),
        'metadata': enriched_data.get('metadata', {})
    }
