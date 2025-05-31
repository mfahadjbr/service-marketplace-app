-- Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT 1
);

-- Providers table
CREATE TABLE IF NOT EXISTS providers (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    business_name TEXT,
    service_type TEXT,
    hourly_rate REAL,
    location TEXT,
    working_hours TEXT,
    rating REAL DEFAULT 0.0,
    reviews_count INTEGER DEFAULT 0,
    is_verified BOOLEAN DEFAULT 0,
    image TEXT DEFAULT '/images/placeholder.jpg',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT 1
); 