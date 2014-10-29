title = "Related to Harder Better Faster Stronger, non Daft-Punk"
query = """
SELECT COUNT(b.tracks.data.title), b.tracks.data.id, b.tracks.data.artist.name, b.tracks.data.title
FROM 
  FLATTEN([Playlists.Playlists], tracks.data) a
LEFT JOIN 
  EACH FLATTEN([Playlists.Playlists], tracks.data) b 
  ON a.id == b.id 
WHERE 
  a.tracks.data.id == 3129775
  AND b.tracks.data.artist.id != 27
GROUP EACH BY 2, 3, 4
ORDER BY 1 DESC
LIMIT 5
"""