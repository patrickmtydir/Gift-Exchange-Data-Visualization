# Data downloaded from https://www.kaggle.com/datasets/nelgiriyewithana/most-streamed-spotify-songs-2024?resource=download
# Data Cleaning Process:
#1) Remove Duplicates
#2) Remove columns which are not needed
#3) Standardize the Data and Var types

# Making a copy so main table isn't edited before being sure of edits
CREATE TABLE top_songs
LIKE `most streamed spotify songs 2024`;
INSERT top_songs
SELECT *
FROM `most streamed spotify songs 2024`;

# First glance at data
SELECT *
FROM top_songs;

# Lots of columns defined as text. Let's remove duplicates first though

SELECT *, TRIM(Track), TRIM(Artist)
FROM top_songs
WHERE Track != TRIM(Track) OR Artist!= TRIM(Artist);

# Two tracks weren't trimmed. Let's standardize Track and Artist so we can check for duplicates
UPDATE top_songs
SET Track = TRIM(Track), Artist = TRIM(Artist);

SELECT *, TRIM(Track), TRIM(Artist)
FROM top_songs
WHERE Track != TRIM(Track) OR Artist!= TRIM(Artist);

#No more trimable tracks/artists. Now let's check for duplicates

WITH dup_cte AS
(
SELECT LOWER(Track), LOWER(Artist), ROW_NUMBER() OVER ( PARTITION BY LOWER(Track), LOWER(Artist)) AS row_num
FROM top_songs
)
SELECT *
FROM dup_cte
WHERE row_num >1;

# Only one duplicate in the whole dataset, Vampire by Olivia Rodrigo

SELECT *
FROM top_songs
WHERE Track = "vampire";

# It appears that the second entry of Vampire is a duplicate. It has almost the same number of streams, but the rest of the data is far below that of the first entry
DELETE 
FROM top_songs
WHERE ISRC = "USUG12305004";

# Checking that the duplicate is removed
WITH dup_cte AS
(
SELECT LOWER(Track), LOWER(Artist), ROW_NUMBER() OVER ( PARTITION BY LOWER(Track), LOWER(Artist)) AS row_num
FROM top_songs
)
SELECT *
FROM dup_cte
WHERE row_num >1;

# No more duplicates. Now to standardize columns. There are a ton of text columns which could be ints: 
# Release date, Spotify Streams, etc.
# Also, TIDAL POPULARITY appears to be blank for every entry. So, let's check that, then drop that column
SELECT `TIDAL Popularity`
FROM top_songs
WHERE `TIDAL Popularity` != ''; 
# It is blank for every entry, let's drop it
ALTER TABLE top_songs
DROP COLUMN `TIDAL Popularity`;
# Now let's change those variables to be ints. First we need to remove commas
UPDATE top_songs
SET `Spotify Streams` = REPLACE(`Spotify Streams`, ",", ""),
`Spotify Playlist Count` = REPLACE(`Spotify Playlist Count`, ",", ""),
`Spotify Playlist Reach` = REPLACE(`Spotify Playlist Reach`, ",", ""),
`YouTube Views` = REPLACE(`YouTube Views`, ",", ""),
`YouTube Likes` = REPLACE(`YouTube Likes`, ",", ""),
`TikTok Posts` = REPLACE(`TikTok Posts`, ",", ""),
`TikTok Likes` = REPLACE(`TikTok Posts`, ",", ""),
`TikTok Views` = REPLACE(`TikTok Views`, ",", ""),
`YouTube Playlist Reach` = REPLACE(`YouTube Playlist Reach`, ",", ""),
`AirPlay Spins` = REPLACE(`AirPlay Spins`, ",", ""),
`SiriusXM Spins` = REPLACE(`SiriusXM Spins`, ",", ""),
`Deezer Playlist Reach` = REPLACE(`Deezer Playlist Reach`, ",", ""),
`Pandora Streams` = REPLACE(`Pandora Streams`, ",", ""),
`Pandora Track Stations` = REPLACE(`Pandora Track Stations`, ",", ""),
`Soundcloud Streams` = REPLACE(`Soundcloud Streams`, ",", ""),
`Shazam Counts` = REPLACE(`Shazam Counts`, ",", "")
;
# Now let's convert the columns to ints and convert Explicit Track into a Boolean
# You may need to run the following line:
SET SESSION sql_mode = 'NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

ALTER TABLE top_songs
MODIFY COLUMN `Spotify Streams` bigint,
MODIFY COLUMN `Spotify Playlist Count` int,
MODIFY COLUMN `Spotify Playlist Reach` int,
MODIFY COLUMN `YouTube Views` int,
MODIFY COLUMN `YouTube Likes` int,
MODIFY COLUMN `TikTok Posts` int,
MODIFY COLUMN `TikTok Likes` int,
MODIFY COLUMN `TikTok Views` bigint,
MODIFY COLUMN `YouTube Playlist Reach` bigint,
MODIFY COLUMN `AirPlay Spins` int,
MODIFY COLUMN `SiriusXM Spins` int,
MODIFY COLUMN `Deezer Playlist Reach` int,
MODIFY COLUMN `Pandora Streams` int,
MODIFY COLUMN `Pandora Track Stations` int,
MODIFY COLUMN `Soundcloud Streams` bigint,
MODIFY COLUMN `Shazam Counts` int,
MODIFY COLUMN `Explicit Track` Bool;

# Now, let's make the Release Date column a Date column
UPDATE top_songs
SET `Release Date`= STR_TO_DATE(`Release Date`, "%m/%d/%Y");

ALTER TABLE top_songs
MODIFY COLUMN `Release Date` date;

# Now, all our columns are set appropriately. Let's look at the data again

SELECT *
from top_songs;

# At this point, I would eliminate all null entries. However, there are none. The data appears to be clean and ready for analysis

# Data Analysis:
# The first variable which appears interesting is release date. Let's see how many songs from each year are in the data
SELECT Count(Track), SUBSTRING(`Release Date`, 1,4) as Year
FROM top_songs
GROUP BY Year;

# Interestingly enough, 173 of the top songs are from 2023, 123 are from 2022, and 101 are from 2024

#Let's see where my Top 10 Songs from 2024 are on the list
SELECT *
FROM top_songs
WHERE Track = "Creep" OR "Karma Police" OR "Covet" OR "Time in a Bottle" OR "Rooster" OR "One Last Breath" OR "Exit Music (For A Film)" OR "Youngest Daughter" OR "Even Flow" OR "Heart-Shaped Box";

# None of my top 10 songs were in the data. I guess that means my music tastes are not popular




















