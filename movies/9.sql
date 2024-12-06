-- list names of all people who starred in a movie released in 2004 by birth year

SELECT name -- find name
FROM people
WHERE id IN
(
    SELECT person_id -- find stars
    FROM stars
    WHERE movie_id IN
    (
        SELECT id -- find 2004 movies
        FROM movies
        WHERE year = 2004
    )
)
ORDER BY birth;
