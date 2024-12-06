-- list in alphabetical order titles of all movies with release date on or after 2018

SELECT title
FROM movies
WHERE year >= 2018
ORDER BY title;
