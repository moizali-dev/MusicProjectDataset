select id as track_id, Playlist_Id as playlist_id, min(created_at) as created_at
from musicprojects.musicprojects_staging.{{ set_table() }}
group by track_id, playlist_id
