CREATE OR REPLACE VIEW vw_latest_us_prices AS
SELECT *
FROM fuel_prices_us_states
WHERE price_date = (SELECT MAX(price_date) FROM fuel_prices_us_states);

CREATE OR REPLACE VIEW vw_latest_oil_prices AS
SELECT o.*
FROM oil_prices o
JOIN (
  SELECT benchmark, MAX(price_date) AS max_date
  FROM oil_prices
  GROUP BY benchmark
) x
ON o.benchmark = x.benchmark AND o.price_date = x.max_date;
