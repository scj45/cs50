-- number of movies with rating of 10

SELECT COUNT(title)
FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE ratings.rating = 10;
