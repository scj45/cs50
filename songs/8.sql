-- list names of songs featuring other artists

SELECT name
FROM songs
WHERE name LIKE '%feat.%';
