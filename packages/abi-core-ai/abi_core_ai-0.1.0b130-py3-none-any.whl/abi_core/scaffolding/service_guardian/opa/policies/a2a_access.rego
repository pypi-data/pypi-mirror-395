package a2a_access

import future.keywords.if
import future.keywords.in

# ============================================
# A2A ACCESS CONTROL POLICY
# ============================================
# Controls agent-to-agent communication
# Validates if source agent can communicate with target agent

# Default deny
default allow := false

# ============================================
# VALIDATION MODE
# ============================================

validation_mode := input.validation_mode

# Disabled mode - always allow
allow if {
    validation_mode == "disabled"
}

# ============================================
# AGENT VALIDATION
# ============================================

# Extract agent information
source_agent := input.source_agent
target_agent := input.target_agent

# Validate agent names exist
agents_identified if {
    source_agent.name != ""
    source_agent.name != "unknown"
    target_agent.name != ""
    target_agent.name != "unknown"
}

# ============================================
# COMMUNICATION RULES
# ============================================

# Allow if agents are in allowed communication pairs
allow if {
    agents_identified
    is_allowed_communication
}

# Check if communication is allowed based on rules
is_allowed_communication if {
    some rule in communication_rules
    rule.source == source_agent.name
    rule.target == target_agent.name
}

# Allow bidirectional communication
is_allowed_communication if {
    some rule in communication_rules
    rule.source == target_agent.name
    rule.target == source_agent.name
    rule.bidirectional == true
}

# Allow if source has wildcard permission
is_allowed_communication if {
    some rule in communication_rules
    rule.source == source_agent.name
    rule.target == "*"
}

# Allow if target accepts from anyone
is_allowed_communication if {
    some rule in communication_rules
    rule.source == "*"
    rule.target == target_agent.name
}

# ============================================
# COMMUNICATION RULES DATABASE
# ============================================

communication_rules := [
    # Orchestrator can talk to everyone
    {"source": "orchestrator", "target": "*", "bidirectional": false},
    
    # Planner can talk to orchestrator
    {"source": "planner", "target": "orchestrator", "bidirectional": true},
    
    # Semantic layer can be accessed by all agents
    {"source": "*", "target": "semantic-layer", "bidirectional": false},
    
    # Example: specific agent pairs
    # {"source": "data-agent", "target": "analytics-agent", "bidirectional": true},
    # {"source": "ui-agent", "target": "orchestrator", "bidirectional": false},
]

# ============================================
# DENY REASONS
# ============================================

deny_reason := reason if {
    not agents_identified
    reason := "Source or target agent not properly identified"
}

deny_reason := reason if {
    agents_identified
    not is_allowed_communication
    reason := sprintf(
        "Communication not allowed: %s -> %s",
        [source_agent.name, target_agent.name]
    )
}

# ============================================
# AUDIT INFORMATION
# ============================================

audit_info := {
    "source_agent": source_agent.name,
    "target_agent": target_agent.name,
    "timestamp": input.communication.timestamp,
    "message_length": input.communication.message_length,
    "allowed": allow,
    "reason": deny_reason,
    "validation_mode": validation_mode
}
