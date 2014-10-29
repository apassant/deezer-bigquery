title = "Related to Rihanna"
query = """
SELECT COUNT(b.tracks.data.artist.id), b.tracks.data.artist.name, 
FROM 
  FLATTEN([Playlists.Playlists], tracks.data) a
LEFT JOIN 
  EACH FLATTEN([Playlists.Playlists], tracks.data) b 
  ON a.id == b.id
WHERE 
  a.tracks.data.artist.id == 564
  AND b.tracks.data.artist.id != 564
GROUP EACH BY 2
ORDER BY 1 DESC
LIMIT 5
"""