import sqlite3

conn = sqlite3.connect("chinook.db")
curs = conn.cursor()


num_tracks = "SELECT COUNT(*) FROM tracks;"

print(f"Num tracks: {curs.execute(num_tracks).fetchone()[0]}")

# what tracks are in the most playlists? (top 10)

query = """
SELECT tracks.Name, albums.Title, COUNT(pt.TrackId)
FROM playlist_track as pt
LEFT JOIN tracks 
ON tracks.TrackId = pt.TrackId
LEFT JOIN albums
ON tracks.AlbumId = albums.AlbumId
GROUP BY pt.TrackId
ORDER BY 2 DESC
LIMIT 10;
"""
print("--- MOST POPULAR TRACKS ---")
track_popularity = curs.execute(query).fetchall()
for track in track_popularity:
    print(track)

# number of albums per artist

query = """
SELECT artists.Name, COUNT(DISTINCT albums.AlbumId)
FROM albums
LEFT JOIN artists 
ON artists.ArtistId = albums.ArtistId
GROUP BY albums.ArtistId
ORDER BY 2 DESC
LIMIT 10;
"""
print("--- MOST ALBUMS PER ARTIST ---")
album_count = curs.execute(query).fetchall()
for artist in album_count:
    print(artist)

curs.close()