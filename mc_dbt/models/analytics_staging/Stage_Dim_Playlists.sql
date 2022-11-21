select Playlist_Id as playlist_id, Playlist_name as playlist_name, min(created_at) as created_at
from musicprojects.musicprojects_staging.{{ set_table() }}
where Playlist_Id is not null and Playlist_name is not null
group by Playlist_Id, Playlist_name