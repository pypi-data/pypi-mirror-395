-- ============================================
-- MCB-DATABRIDGE DUCKDB SCHEMA
-- Analytics layer for MCB + AMUM + QCI + ETHIC
-- ============================================

-- ============================================
-- MCB AGENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS mcb_agents (
    id INTEGER PRIMARY KEY,
    agent_id VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL,
    binary_state BIT(16) DEFAULT B'0000000000000001',
    capabilities JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP
);

-- ============================================
-- MCB MESSAGES TABLE (INQC Protocol)
-- ============================================
CREATE TABLE IF NOT EXISTS mcb_messages (
    id INTEGER PRIMARY KEY,
    raw_message TEXT,
    source_id VARCHAR NOT NULL,
    dest_id VARCHAR NOT NULL,
    binary_state BIT(16),
    command CHAR(1) CHECK (command IN ('I', 'N', 'Q', 'C')),
    payload JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- AMUM SESSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS amum_sessions (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR NOT NULL,
    user_id VARCHAR,
    phase VARCHAR CHECK (phase IN ('divergent_3', 'expand_6', 'converge_9', 'complete')),
    intent TEXT,
    options JSON,
    selected INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ETHIC PRINCIPLES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS ethic_principles (
    id INTEGER PRIMARY KEY,
    principle_id VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL,
    category VARCHAR CHECK (category IN (
        'human_dignity', 'transparency', 'accountability',
        'fairness', 'privacy', 'safety', 'sustainability', 'autonomy'
    )),
    description TEXT,
    source VARCHAR CHECK (source IN ('marcel_facebook', 'anthropic', 'eu_ai_act', 'woai')),
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ETHIC VIOLATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS ethic_violations (
    id INTEGER PRIMARY KEY,
    principle_id VARCHAR REFERENCES ethic_principles(principle_id),
    severity VARCHAR CHECK (severity IN ('block', 'warn', 'log')),
    context JSON,
    resolved BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- QCI STATES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS qci_states (
    id INTEGER PRIMARY KEY,
    agent_id VARCHAR NOT NULL,
    rov_q DOUBLE,
    coherence_level DOUBLE CHECK (coherence_level BETWEEN 0 AND 1),
    signal_strength DOUBLE,
    breathing_cycle VARCHAR CHECK (breathing_cycle IN ('inhale', 'exhale', 'hold')),
    binary_state BIT(16),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- AGENT CONNECTIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS agent_connections (
    id INTEGER PRIMARY KEY,
    source_agent VARCHAR NOT NULL,
    dest_agent VARCHAR NOT NULL,
    connection_type VARCHAR,
    binary_state BIT(16),
    established_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (source_agent, dest_agent)
);

-- ============================================
-- MCB PARSING MACROS
-- ============================================

-- Parse source ID from MCB message
CREATE OR REPLACE MACRO mcb_parse_source(msg) AS (
    regexp_extract(msg, '^(\w+)\s+\w+', 1)
);

-- Parse destination ID from MCB message
CREATE OR REPLACE MACRO mcb_parse_dest(msg) AS (
    regexp_extract(msg, '^\w+\s+(\w+)', 1)
);

-- Parse binary state from MCB message
CREATE OR REPLACE MACRO mcb_parse_state(msg) AS (
    regexp_extract(msg, '([01]{16})', 1)
);

-- Parse INQC command from MCB message
CREATE OR REPLACE MACRO mcb_parse_command(msg) AS (
    regexp_extract(msg, '•\s*([INQC])$', 1)
);

-- Parse payload JSON from MCB message
CREATE OR REPLACE MACRO mcb_parse_payload(msg) AS (
    regexp_extract(msg, '•\s*(\{.*\})\s*•', 1)
);

-- Encode MCB message
CREATE OR REPLACE MACRO mcb_encode(source, dest, state, payload, cmd) AS (
    source || ' ' || dest || ' ' || state || ' • ' || 
    COALESCE(json_serialize(payload), '{}') || ' • ' || cmd
);

-- ============================================
-- BINARY STATE MACROS
-- ============================================

-- Check if specific bit is set
CREATE OR REPLACE MACRO binary_has_flag(state, bit_position) AS (
    get_bit(state::BIT(16), bit_position) = 1
);

-- Check if connected (bit 0)
CREATE OR REPLACE MACRO is_connected(state) AS (
    binary_has_flag(state, 0)
);

-- Check if authenticated (bit 1)
CREATE OR REPLACE MACRO is_authenticated(state) AS (
    binary_has_flag(state, 1)
);

-- Check if encrypted (bit 2)
CREATE OR REPLACE MACRO is_encrypted(state) AS (
    binary_has_flag(state, 2)
);

-- Count active flags
CREATE OR REPLACE MACRO count_flags(state) AS (
    bit_count(state::BIT(16))
);

-- ============================================
-- QCI CALCULATION MACROS
-- ============================================

-- Calculate ROV/Q ratio
CREATE OR REPLACE MACRO qci_rov_q(resonance, quality) AS (
    CASE WHEN quality > 0 THEN resonance / quality ELSE 0 END
);

-- Calculate signal strength
CREATE OR REPLACE MACRO qci_signal(base, coherence, multiplier) AS (
    base * coherence * COALESCE(multiplier, 1.0)
);

-- Convert coherence to binary state
CREATE OR REPLACE MACRO coherence_to_binary(coherence, bits) AS (
    repeat('1', CAST(coherence * bits AS INTEGER)) || 
    repeat('0', bits - CAST(coherence * bits AS INTEGER))
);

-- ============================================
-- ETHIC CHECK MACROS
-- ============================================

-- Check if action is ethical (returns principle violations)
CREATE OR REPLACE MACRO ethic_check(action_name, has_consent, is_sandboxed, is_destructive) AS (
    SELECT principle_id, name, category
    FROM ethic_principles
    WHERE active = TRUE
    AND (
        (principle_id = 'data_privacy' AND has_consent = FALSE)
        OR (principle_id = 'sandbox_default' AND is_sandboxed = FALSE)
        OR (principle_id = 'user_override' AND is_destructive = TRUE)
    )
);

-- ============================================
-- SEED DATA: ETHIC PRINCIPLES
-- ============================================

INSERT INTO ethic_principles (principle_id, name, category, description, source, priority) VALUES
    ('human_first', 'Human First', 'human_dignity', 'AI serves humans, not the other way around', 'marcel_facebook', 10),
    ('no_harm', 'No Harm', 'safety', 'AI must not cause harm to humans or environment', 'anthropic', 10),
    ('transparency', 'Transparency', 'transparency', 'Be clear about AI involvement, no deception', 'eu_ai_act', 9),
    ('respect_creativity', 'Respect Creativity', 'autonomy', 'AI enhances human creativity, doesnt replace it', 'marcel_facebook', 8),
    ('sustainable_ai', 'Sustainable AI', 'sustainability', 'Efficient over wasteful, prefer local models', 'woai', 7),
    ('inclusive_design', 'Inclusive Design', 'fairness', 'Design for all, check for bias', 'eu_ai_act', 8),
    ('data_privacy', 'Data Privacy', 'privacy', 'Minimal data collection, secure storage, user consent', 'eu_ai_act', 9),
    ('sandbox_default', 'Sandbox Default', 'safety', 'Untrusted code runs in sandbox, always', 'woai', 10),
    ('user_override', 'User Override', 'autonomy', 'User can always override AI decisions', 'marcel_facebook', 9),
    ('explainability', 'Explainability', 'accountability', 'Decisions should be traceable and explainable', 'anthropic', 8)
ON CONFLICT (principle_id) DO NOTHING;

-- ============================================
-- VIEWS
-- ============================================

-- Agent network view with QCI states
CREATE OR REPLACE VIEW agent_network AS
SELECT 
    a.agent_id,
    a.name,
    a.binary_state,
    q.coherence_level,
    q.breathing_cycle,
    COUNT(DISTINCT c1.dest_agent) as outgoing_connections,
    COUNT(DISTINCT c2.source_agent) as incoming_connections
FROM mcb_agents a
LEFT JOIN qci_states q ON a.agent_id = q.agent_id
LEFT JOIN agent_connections c1 ON a.agent_id = c1.source_agent
LEFT JOIN agent_connections c2 ON a.agent_id = c2.dest_agent
GROUP BY a.agent_id, a.name, a.binary_state, q.coherence_level, q.breathing_cycle;

-- Message flow summary
CREATE OR REPLACE VIEW message_flow AS
SELECT 
    source_id,
    dest_id,
    command,
    COUNT(*) as message_count,
    MAX(timestamp) as last_message
FROM mcb_messages
GROUP BY source_id, dest_id, command
ORDER BY message_count DESC;

-- Ethic compliance summary
CREATE OR REPLACE VIEW ethic_compliance AS
SELECT 
    p.category,
    p.name,
    p.priority,
    COUNT(v.id) as violation_count,
    SUM(CASE WHEN v.resolved THEN 1 ELSE 0 END) as resolved_count
FROM ethic_principles p
LEFT JOIN ethic_violations v ON p.principle_id = v.principle_id
WHERE p.active = TRUE
GROUP BY p.category, p.name, p.priority
ORDER BY p.priority DESC;
