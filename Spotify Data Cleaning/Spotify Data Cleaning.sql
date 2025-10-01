# Data downloaded from https://www.kaggle.com/datasets/nelgiriyewithana/most-streamed-spotify-songs-2024?resource=download
# Data Cleaning Process:
#1) Remove Duplicates
#2) Remove columns which are not needed
#3) Standardize the Data and Var types

# Please note that I had to load the file into VS code and change the encoding to `UTF-8 with BOM` in order for the data to import appropriately
SET GLOBAL local_infile = 1;

CREATE TABLE most_streamed_spotify_songs_2024 (
    `Track` VARCHAR(255),
    `Album_Name` VARCHAR(255),
    `Artist` VARCHAR(255),
    `Release_Date` VARCHAR(20),
    `ISRC` VARCHAR(20),
    `All_Time_Rank` INT,
    `Track_Score` DECIMAL(10,2),
    `Spotify_Streams` BIGINT NULL,
    `Spotify_Playlist_Count` INT NULL,
    `Spotify_Playlist_Reach` BIGINT NULL,
    `Spotify_Popularity` INT NULL,
    `YouTube_Views` BIGINT NULL,
    `YouTube_Likes` BIGINT NULL,
    `TikTok_Posts` INT NULL,
    `TikTok_Likes` BIGINT NULL,
    `TikTok_Views` BIGINT NULL,
    `YouTube_Playlist_Reach` BIGINT NULL,
    `Apple_Music_Playlist_Count` INT NULL,
    `AirPlay_Spins` BIGINT NULL,
    `SiriusXM_Spins` BIGINT NULL,
    `Deezer_Playlist_Count` INT NULL,
    `Deezer_Playlist_Reach` BIGINT NULL,
    `Amazon_Playlist_Count` INT NULL,
    `Pandora_Streams` BIGINT NULL,
    `Pandora_Track_Stations` INT NULL,
    `Soundcloud_Streams` BIGINT NULL,
    `Shazam_Counts` BIGINT NULL,
    `TIDAL_Popularity` INT NULL,
    `Explicit_Track` BOOL NULL
)
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

LOAD DATA LOCAL INFILE 'C:\\Users\\patri\\OneDrive - Florida State University\\SQL\\Projects\\Spotify\\Most Streamed Spotify Songs 2024.csv'
INTO TABLE most_streamed_spotify_songs_2024
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    Track,
    Album_Name,
    Artist,
    Release_Date,
    ISRC,
    All_Time_Rank,
    Track_Score,
    @Spotify_Streams,
    @Spotify_Playlist_Count,
    @Spotify_Playlist_Reach,
    @Spotify_Popularity,
    @YouTube_Views,
    @YouTube_Likes,
    @TikTok_Posts,
    @TikTok_Likes,
    @TikTok_Views,
    @YouTube_Playlist_Reach,
    @Apple_Music_Playlist_Count,
    @AirPlay_Spins,
    @SiriusXM_Spins,
    @Deezer_Playlist_Count,
    @Deezer_Playlist_Reach,
    @Amazon_Playlist_Count,
    @Pandora_Streams,
    @Pandora_Track_Stations,
    @Soundcloud_Streams,
    @Shazam_Counts,
    @TIDAL_Popularity,
    @Explicit_Track
)
SET 
    Spotify_Streams = NULLIF(@Spotify_Streams, ''),
    Spotify_Playlist_Count = NULLIF(@Spotify_Playlist_Count, ''),
    Spotify_Playlist_Reach = NULLIF(@Spotify_Playlist_Reach, ''),
    Spotify_Popularity = NULLIF(@Spotify_Popularity, ''),
    YouTube_Views = NULLIF(@YouTube_Views, ''),
    YouTube_Likes = NULLIF(@YouTube_Likes, ''),
    TikTok_Posts = NULLIF(@TikTok_Posts, ''),
    TikTok_Likes = NULLIF(@TikTok_Likes, ''),
    TikTok_Views = NULLIF(@TikTok_Views, ''),
    YouTube_Playlist_Reach = NULLIF(@YouTube_Playlist_Reach, ''),
    Apple_Music_Playlist_Count = NULLIF(@Apple_Music_Playlist_Count, ''),
    AirPlay_Spins = NULLIF(@AirPlay_Spins, ''),
    SiriusXM_Spins = NULLIF(@SiriusXM_Spins, ''),
    Deezer_Playlist_Count = NULLIF(@Deezer_Playlist_Count, ''),
    Deezer_Playlist_Reach = NULLIF(@Deezer_Playlist_Reach, ''),
    Amazon_Playlist_Count = NULLIF(@Amazon_Playlist_Count, ''),
    Pandora_Streams = NULLIF(@Pandora_Streams, ''),
    Pandora_Track_Stations = NULLIF(@Pandora_Track_Stations, ''),
    Soundcloud_Streams = NULLIF(@Soundcloud_Streams, ''),
    Shazam_Counts = NULLIF(@Shazam_Counts, ''),
    TIDAL_Popularity = NULLIF(@TIDAL_Popularity, ''),
    Explicit_Track = NULLIF(@Explicit_Track, '');

# Making a copy so main table isn't edited before being sure of edits
CREATE TABLE top_songs
LIKE most_streamed_spotify_songs_2024;

INSERT top_songs
SELECT *
FROM most_streamed_spotify_songs_2024;

# First glance at data
SELECT *
FROM top_songs;

# Let's remove duplicates first. First let's check if we need to trim tracks or artists 

SELECT *, TRIM(Track), TRIM(Artist)
FROM top_songs
WHERE Track != TRIM(Track) OR Artist!= TRIM(Artist);

# All tracks and artist names appear to not have trailing or leading spaces

#Now let's check for duplicates

WITH dup_cte AS
(
SELECT LOWER(Track), LOWER(Artist), ROW_NUMBER() OVER ( PARTITION BY LOWER(Track), LOWER(Artist)) AS row_num
FROM top_songs
)
SELECT *
FROM dup_cte
WHERE row_num >1;

# There are many duplicates in the dataset, let's clean them

ALTER TABLE top_songs
ADD COLUMN id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;


WITH dup_cte AS 
(
SELECT id, ROW_NUMBER() OVER ( PARTITION BY Track, Artist ORDER BY id) AS row_num
FROM top_songs
)
DELETE t
FROM top_songs t
JOIN dup_cte d ON t.id = d.id
WHERE d.row_num > 1;

# Checking that the duplicates are removed
WITH dup_cte AS
(
SELECT LOWER(Track), LOWER(Artist), ROW_NUMBER() OVER ( PARTITION BY LOWER(Track), LOWER(Artist)) AS row_num
FROM top_songs
)
SELECT *
FROM dup_cte
WHERE row_num >1;

# No more duplicates. Now to standardize columns and trim the dataset
# TIDAL POPULARITY appears to be blank for every entry. So, let's check that, then drop that column
SELECT TIDAL_Popularity
FROM top_songs
WHERE TIDAL_Popularity != ''; 
# It is blank for every entry, let's drop it
ALTER TABLE top_songs
DROP COLUMN TIDAL_Popularity;

# Now, let's make the Release Date column a Date column
UPDATE top_songs 
SET Release_Date= STR_TO_DATE(Release_Date, "%m/%d/%Y");

ALTER TABLE top_songs
MODIFY COLUMN Release_Date date;

# Now, all our columns are set appropriately. Let's look at the data again

SELECT *
from top_songs;

# At this point, I would eliminate all null entries if it were neccessary. However, it is safer to keep them as null, so that if the data is used to calculate anything, the null values do not skew the data towards 0. 

# Data Analysis:
# The first variable which appears interesting is release date. Let's see how many songs from each year are in the data
SELECT Count(Track), SUBSTRING(Release_Date, 1,4) as Year
FROM top_songs
GROUP BY Year;

# Interestingly enough, 1124 of the top songs are from 2023, 681 are from 2022, and 669 are from 2024

#Let's see where my Top 10 Songs from 2024 are on the list
SELECT *
FROM top_songs
WHERE Track LIKE "Creep" OR "Karma Police" OR "Covet" OR "Time in a Bottle" OR "Rooster" OR "One Last Breath" OR "Exit Music (For A Film)" OR "Youngest Daughter" OR "Even Flow" OR "Heart-Shaped Box";

# None of my top 10 songs were in the data, I guess that means my music tastes were not popular in 2024 

# The data is now cleaned and ready for analysis!




















