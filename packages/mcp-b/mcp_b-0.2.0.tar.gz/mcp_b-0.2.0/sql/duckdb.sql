-- ============================================
-- MCP-B (Master Client Bridge) DUCKDB SCHEMA
-- Analytics layer for MCP-B + AMUM + QCI + ETHIC + SmartACE
-- ============================================

-- Required extensions:
-- INSTALL http_client FROM community;
-- INSTALL vss;
-- LOAD http_client;
-- LOAD vss;

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
-- OLLAMA / LLM MACROS (SmartACE)
-- ============================================

-- Base Ollama API endpoint
CREATE OR REPLACE MACRO ollama_base() AS 'http://localhost:11434';

-- Generic Ollama chat completion
CREATE OR REPLACE MACRO ollama_chat(model_name, prompt) AS (
    SELECT json_extract_string(
        http_post(
            ollama_base() || '/api/generate',
            headers := MAP {'Content-Type': 'application/json'},
            body := json_object(
                'model', model_name,
                'prompt', prompt,
                'stream', false
            )
        ).body,
        '$.response'
    )
);

-- Ollama chat with messages format (for multi-turn)
CREATE OR REPLACE MACRO ollama_chat_messages(model_name, messages_json) AS (
    SELECT http_post(
        ollama_base() || '/api/chat',
        headers := MAP {'Content-Type': 'application/json'},
        body := json_object(
            'model', model_name,
            'messages', json(messages_json),
            'stream', false
        )
    ).body
);

-- Ollama chat WITH tools (function/tool calling)
CREATE OR REPLACE MACRO ollama_chat_with_tools(model_name, messages_json, tools_json) AS (
    SELECT http_post(
        ollama_base() || '/api/chat',
        headers := MAP {'Content-Type': 'application/json'},
        body := json_object(
            'model', model_name,
            'messages', json(messages_json),
            'tools', json(tools_json),
            'stream', false
        )
    ).body
);

-- Extract tool calls from Ollama response
CREATE OR REPLACE MACRO extract_tool_calls(response_body) AS (
    SELECT json_extract(response_body, '$.message.tool_calls')
);

-- Extract text response from Ollama response
CREATE OR REPLACE MACRO extract_response(response_body) AS (
    SELECT json_extract_string(response_body, '$.message.content')
);

-- Ollama embeddings
CREATE OR REPLACE MACRO ollama_embed(model_name, text_input) AS (
    SELECT json_extract(
        http_post(
            ollama_base() || '/api/embeddings',
            headers := MAP {'Content-Type': 'application/json'},
            body := json_object(
                'model', model_name,
                'prompt', text_input
            )
        ).body,
        '$.embedding'
    )::FLOAT[]
);

-- ============================================
-- EMBEDDING / VECTOR MACROS
-- ============================================

-- Text to embedding (default model: nomic-embed-text)
CREATE OR REPLACE MACRO embed(text_input) AS (
    ollama_embed('nomic-embed-text', text_input)
);

-- Cosine similarity between two vectors
CREATE OR REPLACE MACRO cosine_sim(vec1, vec2) AS (
    list_cosine_similarity(vec1, vec2)
);

-- Semantic similarity score between two texts
CREATE OR REPLACE MACRO semantic_score(query_text, doc_text) AS (
    cosine_sim(embed(query_text), embed(doc_text))
);

-- ============================================
-- AGENTIC / SmartACE MACROS
-- ============================================

-- Agent call: Send prompt with system message and tools
CREATE OR REPLACE MACRO agent_call(model_name, system_prompt, user_prompt, tools_json) AS (
    SELECT ollama_chat_with_tools(
        model_name,
        json_array(
            json_object('role', 'system', 'content', system_prompt),
            json_object('role', 'user', 'content', user_prompt)
        ),
        tools_json
    )
);

-- Check if response contains tool calls
CREATE OR REPLACE MACRO has_tool_calls(response_body) AS (
    SELECT json_extract(response_body, '$.message.tool_calls') IS NOT NULL
        AND json_array_length(json_extract(response_body, '$.message.tool_calls')) > 0
);

-- Convert MCP tool schema to Ollama tool format
CREATE OR REPLACE MACRO mcp_to_ollama_tool(tool_name, description, input_schema_json) AS (
    SELECT json_object(
        'type', 'function',
        'function', json_object(
            'name', tool_name,
            'description', description,
            'parameters', json(input_schema_json)
        )
    )
);

-- Simple chat helper (default model)
CREATE OR REPLACE MACRO chat(prompt) AS (
    ollama_chat('llama3.2', prompt)
);

-- RAG query: Answer question based on context
CREATE OR REPLACE MACRO rag_query(question, context) AS (
    ollama_chat('llama3.2',
        'Answer based on the following context:\n\n' || context ||
        '\n\nQuestion: ' || question
    )
);

-- ============================================
-- QCI + EMBEDDING INTEGRATION
-- ============================================

-- Calculate coherence between two agents based on their descriptions
CREATE OR REPLACE MACRO agent_coherence(agent1_desc, agent2_desc) AS (
    semantic_score(agent1_desc, agent2_desc)
);

-- Find most coherent agent for a task
CREATE OR REPLACE MACRO find_coherent_agent(task_description) AS (
    SELECT agent_id, name, semantic_score(task_description, capabilities::VARCHAR) as coherence
    FROM mcb_agents
    ORDER BY coherence DESC
    LIMIT 1
);

-- ============================================
-- INQC + LLM INTEGRATION
-- ============================================

-- Generate INQC response using LLM
CREATE OR REPLACE MACRO inqc_llm_query(source, dest, query_payload) AS (
    mcb_encode(
        source, dest, '1011101010111111',
        json_object('response', ollama_chat('llama3.2', query_payload)),
        'Q'
    )
);

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

-- ============================================
-- ETHICS-MODEL ANALYSIS TABLES
-- (from bjoernbethge/ethics-model)
-- ============================================

CREATE TABLE IF NOT EXISTS ethics_analysis (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    ethics_score DOUBLE CHECK (ethics_score BETWEEN 0 AND 1),
    manipulation_score DOUBLE CHECK (manipulation_score BETWEEN 0 AND 1),
    framing_type VARCHAR CHECK (framing_type IN (
        'loss_gain', 'moral', 'episodic_thematic',
        'problem_solution', 'conflict_consensus', 'urgency_deliberation'
    )),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS framework_analysis (
    id INTEGER PRIMARY KEY,
    ethics_id INTEGER REFERENCES ethics_analysis(id),
    framework VARCHAR CHECK (framework IN (
        'deontological', 'utilitarian', 'virtue', 'narrative', 'care'
    )),
    score DOUBLE CHECK (score BETWEEN 0 AND 1),
    reasoning TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS manipulation_detection (
    id INTEGER PRIMARY KEY,
    ethics_id INTEGER REFERENCES ethics_analysis(id),
    technique VARCHAR CHECK (technique IN (
        'emotional_appeal', 'false_dichotomy', 'appeal_to_authority',
        'bandwagon', 'loaded_language', 'cherry_picking',
        'straw_man', 'slippery_slope'
    )),
    detected BOOLEAN,
    confidence DOUBLE CHECK (confidence BETWEEN 0 AND 1),
    evidence TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ETHICS-MODEL LLM ANALYSIS MACROS
-- ============================================

-- Build the ethics analysis prompt
CREATE OR REPLACE MACRO ethics_prompt(text_input) AS (
    'Analyze the following text for ethical considerations.

TEXT: ' || text_input || '

MORAL FRAMEWORKS to consider:
- Deontological ethics (Kant): Evaluate based on duty, rules, and moral obligations.
- Utilitarian ethics (Mill): Evaluate based on consequences and outcomes.
- Virtue ethics (Aristotle): Evaluate based on character and virtues.
- Narrative ethics: Evaluate based on storytelling and framing.
- Care ethics (Gilligan): Evaluate based on relationships and responsibility.

MANIPULATION TECHNIQUES to detect:
- emotional_appeal: Uses emotions instead of logic to persuade
- false_dichotomy: Presents only two options when more exist
- appeal_to_authority: Claims truth because an authority says so
- bandwagon: Claims correctness because many believe it
- loaded_language: Uses emotionally charged words
- cherry_picking: Selects only favorable evidence
- straw_man: Misrepresents an argument
- slippery_slope: Claims extreme consequences without evidence

Respond with JSON:
{
    "ethics_score": 0.0-1.0,
    "frameworks": {
        "deontological": {"score": 0.0-1.0, "reasoning": "..."},
        "utilitarian": {"score": 0.0-1.0, "reasoning": "..."},
        "virtue": {"score": 0.0-1.0, "reasoning": "..."},
        "narrative": {"score": 0.0-1.0, "reasoning": "..."},
        "care": {"score": 0.0-1.0, "reasoning": "..."}
    },
    "manipulation": {
        "emotional_appeal": {"detected": true/false, "confidence": 0.0-1.0, "evidence": "..."},
        "false_dichotomy": {"detected": true/false, "confidence": 0.0-1.0, "evidence": "..."},
        "appeal_to_authority": {"detected": true/false, "confidence": 0.0-1.0, "evidence": "..."},
        "bandwagon": {"detected": true/false, "confidence": 0.0-1.0, "evidence": "..."},
        "loaded_language": {"detected": true/false, "confidence": 0.0-1.0, "evidence": "..."},
        "cherry_picking": {"detected": true/false, "confidence": 0.0-1.0, "evidence": "..."},
        "straw_man": {"detected": true/false, "confidence": 0.0-1.0, "evidence": "..."},
        "slippery_slope": {"detected": true/false, "confidence": 0.0-1.0, "evidence": "..."}
    },
    "framing_type": "loss_gain|moral|episodic_thematic|problem_solution|conflict_consensus|urgency_deliberation|null"
}'
);

-- Run ethics analysis via LLM (returns JSON)
CREATE OR REPLACE MACRO ethics_analyze(text_input) AS (
    ollama_chat('llama3.2', ethics_prompt(text_input))
);

-- Extract ethics score from analysis
CREATE OR REPLACE MACRO ethics_score(analysis_json) AS (
    json_extract(analysis_json, '$.ethics_score')::DOUBLE
);

-- Extract framework score from analysis
CREATE OR REPLACE MACRO framework_score(analysis_json, framework_name) AS (
    json_extract(analysis_json, '$.frameworks.' || framework_name || '.score')::DOUBLE
);

-- Check if manipulation detected
CREATE OR REPLACE MACRO manipulation_detected(analysis_json, technique_name) AS (
    json_extract(analysis_json, '$.manipulation.' || technique_name || '.detected')::BOOLEAN
);

-- Get manipulation confidence
CREATE OR REPLACE MACRO manipulation_confidence(analysis_json, technique_name) AS (
    json_extract(analysis_json, '$.manipulation.' || technique_name || '.confidence')::DOUBLE
);

-- Quick ethics check (returns score only)
CREATE OR REPLACE MACRO quick_ethics(text_input) AS (
    ethics_score(ethics_analyze(text_input))
);

-- Check for any manipulation (returns true if any detected)
CREATE OR REPLACE MACRO has_manipulation(analysis_json) AS (
    manipulation_detected(analysis_json, 'emotional_appeal') OR
    manipulation_detected(analysis_json, 'false_dichotomy') OR
    manipulation_detected(analysis_json, 'appeal_to_authority') OR
    manipulation_detected(analysis_json, 'bandwagon') OR
    manipulation_detected(analysis_json, 'loaded_language') OR
    manipulation_detected(analysis_json, 'cherry_picking') OR
    manipulation_detected(analysis_json, 'straw_man') OR
    manipulation_detected(analysis_json, 'slippery_slope')
);

-- ============================================
-- ETHICS ANALYSIS VIEW
-- ============================================

CREATE OR REPLACE VIEW ethics_summary AS
SELECT
    e.id,
    e.ethics_score,
    e.manipulation_score,
    e.framing_type,
    COUNT(DISTINCT CASE WHEN m.detected THEN m.technique END) as manipulation_count,
    AVG(f.score) as avg_framework_score,
    e.timestamp
FROM ethics_analysis e
LEFT JOIN framework_analysis f ON e.id = f.ethics_id
LEFT JOIN manipulation_detection m ON e.id = m.ethics_id
GROUP BY e.id, e.ethics_score, e.manipulation_score, e.framing_type, e.timestamp
ORDER BY e.timestamp DESC;
