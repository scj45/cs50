-- names of all people who starred in Toy Story

SELECT name -- find names
FROM people
WHERE id IN
(
    SELECT person_id -- find stars
    FROM stars
    WHERE movie_id =
    (
        SELECT id -- find movie
        FROM movies
        WHERE title = 'Toy Story'
    )
);
