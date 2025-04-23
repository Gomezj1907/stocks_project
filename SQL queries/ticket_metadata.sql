CREATE TABLE IF NOT EXISTS tickers_metadata (
    id SERIAL PRIMARY KEY,
    ticker TEXT UNIQUE,
    name TEXT,
    sector TEXT,
    country TEXT,
    source_index TEXT
);


ALTER TABLE tickers_metadata
ADD CONSTRAINT unique_ticker UNIQUE (ticker);

Select * from tickers_metadata;

