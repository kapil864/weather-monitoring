-- SQLite
WITH WeatherCounts AS (
  SELECT city, wethercondition, COUNT(*) AS count
  FROM daily
  GROUP BY city, wethercondition
)
SELECT city, wethercondition
FROM WeatherCounts
WHERE count = (
  SELECT MAX(count)
  FROM WeatherCounts AS WC2
  WHERE WC2.city = WeatherCounts.city
);