create table photoLocation (
    ID integer primary key autoincrement,
    longitude decimal(11,8) not null,
    latitude decimal(11,8) not null
);

create table photo (
	ID integer primary key autoincrement,
    dateAndTime datetime,
    locationID int,
    deviceType varchar(20),
    dataType varchar(6) not null,
    foreign key (locationID) references photoLocation (ID)
);


create table person (
    ID integer primary key autoincrement,
    firstName varchar(20) not null,
    lastName varchar(20) not null
);

create table personInPhoto (
    personID int,
    photoID int,
    foreign key (personID) references person (ID),
    foreign key (photoID) references photo (ID),
    primary key (personID, photoID)
);

create table album (
    ID integer primary key autoincrement,
    albumName varchar(20) not null unique
);

create table photoInAlbum (
    photoID int,
    albumID int,
    foreign key (photoID) references photo (ID),
    foreign key (albumID) references album (ID),
    primary key (photoID, albumID)
);
