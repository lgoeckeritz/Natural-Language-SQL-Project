-- Insert some sample data into the location table
INSERT INTO photoLocation (longitude, latitude) VALUES
(-111.658531, 40.233844), -- Provo, UT
(-122.419416, 37.774929), -- San Francisco, CA
(-0.127758, 51.507351), -- London, UK
(139.691706, 35.689487), -- Tokyo, JP
(31.235712, 30.044420); -- Cairo, EG

-- Insert some sample data into the person table
INSERT INTO person (firstName, lastName) VALUES
('Alice', 'Smith'),
('Bob', 'Jones'),
('Charlie', 'Brown'),
('David', 'Lee'),
('Emma', 'Watson');

-- Insert some sample data into the photo table
INSERT INTO photo (dateAndTime, locationID, deviceType, dataType) VALUES
('2024-01-01 12:00:00', 1, 'iPhone 12', 'JPEG'),
('2024-01-02 13:00:00', 2, 'Samsung Galaxy S21', 'PNG'),
('2024-01-03 14:00:00', 3, 'Canon EOS 5D Mark IV', 'RAW'),
('2024-01-04 15:00:00', 4, 'Nikon D850', 'TIFF'),
('2024-01-05 16:00:00', 5, 'Sony Alpha a7 III', 'GIF');

-- Insert some sample data into the personInPhoto table
INSERT INTO personInPhoto (personID, photoID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(1, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 1);

-- Insert some sample data into the album table
INSERT INTO album (albumName) VALUES
('New Year 2024'),
('Travel 2024'),
('Family 2024'),
('Friends 2024'),
('Pets 2024');

-- Insert some sample data into the photoInAlbum table
INSERT INTO photoInAlbum (photoID, albumID) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(1, 2),
(2, 2),
(3, 2),
(4, 2),
(5, 2),
(1, 3),
(2, 4),
(3, 5),
(4, 3),
(5, 4);
