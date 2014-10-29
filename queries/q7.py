title = "Top-artists by number of tracks"
query = """
SELECT COUNT(tracks.data.artist.id) as c, tracks.data.artist.id, tracks.data.artist.name
FROM 
    [Playlists.Playlists]
WHERE 
    rating == 5
GROUP EACH BY 2, 3
ORDER BY 1 DESC
LIMIT 5
"""