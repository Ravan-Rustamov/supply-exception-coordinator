-- CREATE EXTENSION IF NOT EXISTS pgvector;

CREATE TABLE IF NOT EXISTS cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL DEFAULT 'NEW',
    exception_type TEXT,
    supplier_id TEXT,
    po_number TEXT,
    state JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS case_events (
    id BIGSERIAL PRIMARY KEY,
    case_id TEXT REFERENCES cases(case_id),
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id TEXT,
    agent_name TEXT,
    input_tokens INT,
    output_tokens INT,
    cost_usd NUMERIC(8,5),
    latency_ms INT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id TEXT PRIMARY KEY,
    name TEXT,
    email_domain TEXT,
    reliability_score NUMERIC(4,3),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);
CREATE INDEX IF NOT EXISTS idx_case_events_case_id ON case_events(case_id);
