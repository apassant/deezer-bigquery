title = "Most popular tracks from Daft Punk"
query = """
SELECT COUNT(tracks.data.id), tracks.data.id, tracks.data.title
FROM 
  [Playlists.Playlists]
WHERE 
  tracks.data.artist.id == 27
GROUP EACH BY 2, 3
ORDER BY 1 DESC
LIMIT 5
"""