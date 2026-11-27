
CREATE EXTENSION IF NOT EXISTS pg_trgm;


ALTER TABLE games 
ADD COLUMN search_vector tsvector 
GENERATED ALWAYS AS (
    to_tsvector('russian', coalesce(title, '') || ' ' || coalesce(description, ''))
) STORED;


CREATE INDEX idx_games_search ON games USING GIN (search_vector);
CREATE INDEX idx_games_title_trgm ON games USING GIN (title gin_trgm_ops);