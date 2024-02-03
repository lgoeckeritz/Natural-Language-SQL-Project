# Natural-Language-SQL-Project

In this project we designed a database to act as a photo storage device, similar to GooglePhotos. The database contains tables for people, pictures and photo albums, as well as tables used for appropriate many-many relationsips. Information such as date and time, location, device used, etc are included for the photos. Names are included for people tagged in photos. Albums have unique titles.

Successful Question:

David lee and Emma watson are always involved in pictures of each other. If there is a picture of emma without david lee, that means that david took the picture. If there is a picture of david without emma, then emma took the picture. If both david and emma are in a picture, then david took the picture. Between david and emma, who took more pictures?

GPT SQL Response:

SELECT Photographer.firstName, Photographer.lastName,
COUNT(Photographer.ID) AS NumberOfPhotos
FROM (
SELECT person.ID, person.firstName, person.lastName, photo.ID AS photoID
FROM person
JOIN personInPhoto ON person.ID = personInPhoto.personID
JOIN photo ON photo.ID = personInPhoto.photoID
WHERE person.firstName = 'David' AND person.lastName = 'Lee'

    UNION ALL

    SELECT person.ID, person.firstName, person.lastName, photo.ID AS photoID
      FROM person
      JOIN personInPhoto ON person.ID = personInPhoto.personID
      JOIN photo ON photo.ID = personInPhoto.photoID
     WHERE person.firstName = 'Emma' AND person.lastName = 'Watson'
       AND photo.ID NOT IN (
         SELECT photo.ID
           FROM photo
           JOIN personInPhoto ON personInPhoto.photoID = photo.ID
           JOIN person ON person.ID = personInPhoto.personID
          WHERE person.firstName = 'David' AND person.lastName = 'Lee'
       )

) AS Photographer
GROUP BY Photographer.ID
ORDER BY NumberOfPhotos DESC
LIMIT 1;

SQL Result:
[('Emma', 'Watson', 3)]

Friendly Response:
David took more pictures.

Unsuccessful Question:

Who is the most popular?

GPT SQL Response:

SELECT COUNT(DISTINCT pip_other.personID) AS unique_people_with_emma_watson
FROM personInPhoto pip_emma
JOIN personInPhoto pip_other ON pip_emma.photoID = pip_other.photoID
JOIN person p_emma on pip_emma.personID = p_emma.ID
WHERE
p_emma.firstName = 'Emma' AND p_emma.lastName = 'Watson'
AND pip_other.personID != pip_emma.personID;

SQL Result:
[(4,)]

Friendly Response:
Certainly, the individual with the identifier "4" is the most popular based on the context you've provided.

This one was too heavily influenced my our single shot prompt which lead it to just ask about emma watson instead of answering the question.

Zero vs Single shot prompt engineering

In our experience we found that zero shot was more effective. We found that our single shot queries were more prone to errors. We realize that this was probably due to our own error and trying to use more complex queries for the single shot prompts. If we did multi shot it probably would have worked better and better with more examples from which to try and decipher our queries.
