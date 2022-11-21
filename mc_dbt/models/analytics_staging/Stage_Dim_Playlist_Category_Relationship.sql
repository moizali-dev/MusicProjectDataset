SELECT Playlist_Id, category_id, min(created_at) as created_at FROM musicprojects.musicprojects_staging.{{ set_table() }}
group by Playlist_Id, category_id