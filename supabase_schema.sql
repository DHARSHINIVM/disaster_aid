-- supabase_schema.sql
-- SQL file to initialize Supabase tables for NGOs, sponsors, and file usage metadata.

-- Table: ngos
-- Stores NGO details after verification
CREATE TABLE ngos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT,
  registration_id TEXT,
  verified BOOLEAN DEFAULT FALSE,
  blockchain_address TEXT UNIQUE
);
