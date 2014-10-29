title = "Top-artists by playlists appearance"
query = """
SELECT COUNT(id) as c, tracks.data.artist.id, tracks.data.artist.name
FROM (
 SELECT id, tracks.data.artist.id, tracks.data.artist.name
 FROM [Playlists.Playlists]
 GROUP EACH BY 1, 2, 3
)
GROUP EACH BY 2, 3
ORDER BY c DESC
LIMIT 5
"""