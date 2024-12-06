-- list all movies released in 2010 and their ratings in rating descending order

SELECT title, rating
FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE movies.year = 2010
ORDER BY rating DESC, title;
