CREATE TABLE IF NOT EXISTS oil_prices (
    id SERIAL PRIMARY KEY,
    price_date DATE,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    benchmark VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS fuel_prices_us_states (
    id SERIAL PRIMARY KEY,
    price_date DATE,
    state VARCHAR(100),
    abbr VARCHAR(10),
    region VARCHAR(50),
    regular DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS fuel_prices_world (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100),
    region VARCHAR(100),
    city VARCHAR(100),
    fuel_type VARCHAR(50),
    price DOUBLE PRECISION,
    unit VARCHAR(20),
    currency VARCHAR(20),
    last_update VARCHAR(50),
    source VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dashboard_kpis (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value VARCHAR(255)
);
