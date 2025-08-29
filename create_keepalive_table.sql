-- Create a simple table to store keepalive pings
CREATE TABLE IF NOT EXISTS keepalive_pings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ping_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add an index on ping_time for better performance
CREATE INDEX IF NOT EXISTS idx_keepalive_pings_ping_time ON keepalive_pings(ping_time);

-- Optional: Create a policy to allow public access (since this is just for keepalive)
-- You can remove this if you prefer to keep RLS enabled
ALTER TABLE keepalive_pings DISABLE ROW LEVEL SECURITY;
