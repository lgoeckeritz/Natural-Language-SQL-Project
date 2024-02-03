# Natural-Language-SQL-Project

In this project we designed a database to act as a photo storage device, similar to GooglePhotos. The database contains tables for people, pictures and photo albums, as well as tables used for appropriate many-many relationsips. Information such as date and time, location, device used, etc are included for the photos. Names are included for people tagged in photos. Albums have unique titles.


Zero vs Single shot prompt engineering

In our experience we found that zero shot was more effective. We found that our single shot queries were more prone to errors. We realize that this was probably due to our own error and trying to use more complex queries for the single shot prompts. If we did multi shot it probably would have worked better and better with more examples from which to try and decipher our queries. 