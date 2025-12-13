-- ============================================
-- MCB-DATABRIDGE SURREALDB SCHEMA
-- Complete schema for MCB + AMUM + QCI + ETHIC
-- ============================================

-- ============================================
-- MCB AGENTS
-- ============================================
DEFINE TABLE mcb_agents SCHEMAFULL;
DEFINE FIELD name ON mcb_agents TYPE string;
DEFINE FIELD agent_id ON mcb_agents TYPE string;
DEFINE FIELD binary_state ON mcb_agents TYPE string;
DEFINE FIELD capabilities ON mcb_agents TYPE array;
DEFINE FIELD created_at ON mcb_agents TYPE datetime DEFAULT time::now();
DEFINE FIELD last_seen ON mcb_agents TYPE datetime;
DEFINE INDEX idx_agent_id ON mcb_agents FIELDS agent_id UNIQUE;

-- ============================================
-- MCB MESSAGES (INQC Protocol)
-- ============================================
DEFINE TABLE mcb_messages SCHEMAFULL;
DEFINE FIELD raw_message ON mcb_messages TYPE string;
DEFINE FIELD source_id ON mcb_messages TYPE string;
DEFINE FIELD dest_id ON mcb_messages TYPE string;
DEFINE FIELD binary_state ON mcb_messages TYPE string;
DEFINE FIELD command ON mcb_messages TYPE string 
    ASSERT $value IN ['I', 'N', 'Q', 'C'];
DEFINE FIELD payload ON mcb_messages TYPE object;
DEFINE FIELD timestamp ON mcb_messages TYPE datetime DEFAULT time::now();
DEFINE INDEX idx_source ON mcb_messages FIELDS source_id;
DEFINE INDEX idx_dest ON mcb_messages FIELDS dest_id;
DEFINE INDEX idx_command ON mcb_messages FIELDS command;

-- ============================================
-- AMUM ALIGNMENT SESSIONS
-- ============================================
DEFINE TABLE amum_sessions SCHEMAFULL;
DEFINE FIELD session_id ON amum_sessions TYPE string;
DEFINE FIELD user_id ON amum_sessions TYPE string;
DEFINE FIELD phase ON amum_sessions TYPE string 
    ASSERT $value IN ['divergent_3', 'expand_6', 'converge_9', 'complete'];
DEFINE FIELD intent ON amum_sessions TYPE string;
DEFINE FIELD options ON amum_sessions TYPE array;
DEFINE FIELD selected ON amum_sessions TYPE int;
DEFINE FIELD created_at ON amum_sessions TYPE datetime DEFAULT time::now();
DEFINE INDEX idx_session ON amum_sessions FIELDS session_id;
DEFINE INDEX idx_user ON amum_sessions FIELDS user_id;

-- ============================================
-- ETHIC PRINCIPLES
-- ============================================
DEFINE TABLE ethic_principles SCHEMAFULL;
DEFINE FIELD name ON ethic_principles TYPE string;
DEFINE FIELD category ON ethic_principles TYPE string ASSERT $value IN [
    'human_dignity', 'transparency', 'accountability', 
    'fairness', 'privacy', 'safety', 'sustainability', 'autonomy'
];
DEFINE FIELD description ON ethic_principles TYPE string;
DEFINE FIELD source ON ethic_principles TYPE string;
DEFINE FIELD priority ON ethic_principles TYPE int;
DEFINE FIELD active ON ethic_principles TYPE bool DEFAULT true;
DEFINE INDEX idx_category ON ethic_principles FIELDS category;

-- ============================================
-- ETHIC VIOLATIONS
-- ============================================
DEFINE TABLE ethic_violations SCHEMAFULL;
DEFINE FIELD principle_id ON ethic_violations TYPE string;
DEFINE FIELD severity ON ethic_violations TYPE string 
    ASSERT $value IN ['block', 'warn', 'log'];
DEFINE FIELD context ON ethic_violations TYPE object;
DEFINE FIELD resolved ON ethic_violations TYPE bool DEFAULT false;
DEFINE FIELD timestamp ON ethic_violations TYPE datetime DEFAULT time::now();
DEFINE INDEX idx_principle ON ethic_violations FIELDS principle_id;
DEFINE INDEX idx_severity ON ethic_violations FIELDS severity;

-- ============================================
-- QCI QUANTUM COHERENCE STATES
-- ============================================
DEFINE TABLE qci_states SCHEMAFULL;
DEFINE FIELD agent_id ON qci_states TYPE string;
DEFINE FIELD rov_q ON qci_states TYPE float;
DEFINE FIELD coherence_level ON qci_states TYPE float;
DEFINE FIELD signal_strength ON qci_states TYPE float;
DEFINE FIELD breathing_cycle ON qci_states TYPE string 
    ASSERT $value IN ['inhale', 'exhale', 'hold'];
DEFINE FIELD binary_state ON qci_states TYPE string;
DEFINE FIELD timestamp ON qci_states TYPE datetime DEFAULT time::now();
DEFINE INDEX idx_agent ON qci_states FIELDS agent_id;

-- ============================================
-- RELATIONSHIPS
-- ============================================

-- Agent connections
DEFINE TABLE connects TYPE RELATION;
DEFINE FIELD established_at ON connects TYPE datetime DEFAULT time::now();
DEFINE FIELD connection_type ON connects TYPE string;
DEFINE FIELD binary_state ON connects TYPE string;

-- Agent has QCI state
DEFINE TABLE has_qci TYPE RELATION;

-- Agent follows ETHIC principle
DEFINE TABLE follows_ethic TYPE RELATION;
DEFINE FIELD priority ON follows_ethic TYPE int;

-- AMUM triggers MCB message
DEFINE TABLE triggers_mcb TYPE RELATION;
DEFINE FIELD alignment_phase ON triggers_mcb TYPE string;
DEFINE FIELD mcb_command ON triggers_mcb TYPE string;

-- QCI enables ETHIC
DEFINE TABLE enables TYPE RELATION;
DEFINE FIELD reason ON enables TYPE string;

-- ============================================
-- CORE ETHIC PRINCIPLES (Seed Data)
-- ============================================

CREATE ethic_principles:human_first SET
    name = "Human First",
    category = "human_dignity",
    description = "AI serves humans, not the other way around",
    source = "marcel_facebook",
    priority = 10;

CREATE ethic_principles:no_harm SET
    name = "No Harm",
    category = "safety",
    description = "AI must not cause harm to humans or environment",
    source = "anthropic",
    priority = 10;

CREATE ethic_principles:transparency SET
    name = "Transparency",
    category = "transparency",
    description = "Be clear about AI involvement, no deception",
    source = "eu_ai_act",
    priority = 9;

CREATE ethic_principles:respect_creativity SET
    name = "Respect Creativity",
    category = "autonomy",
    description = "AI enhances human creativity, doesn't replace it",
    source = "marcel_facebook",
    priority = 8;

CREATE ethic_principles:sustainable_ai SET
    name = "Sustainable AI",
    category = "sustainability",
    description = "Efficient over wasteful, prefer local models when possible",
    source = "woai",
    priority = 7;

CREATE ethic_principles:inclusive_design SET
    name = "Inclusive Design",
    category = "fairness",
    description = "Design for all, check for bias",
    source = "eu_ai_act",
    priority = 8;

CREATE ethic_principles:data_privacy SET
    name = "Data Privacy",
    category = "privacy",
    description = "Minimal data collection, secure storage, user consent",
    source = "eu_ai_act",
    priority = 9;

CREATE ethic_principles:sandbox_default SET
    name = "Sandbox Default",
    category = "safety",
    description = "Untrusted code runs in sandbox, always",
    source = "woai",
    priority = 10;

CREATE ethic_principles:user_override SET
    name = "User Override",
    category = "autonomy",
    description = "User can always override AI decisions",
    source = "marcel_facebook",
    priority = 9;

CREATE ethic_principles:explainability SET
    name = "Explainability",
    category = "accountability",
    description = "Decisions should be traceable and explainable",
    source = "anthropic",
    priority = 8;
