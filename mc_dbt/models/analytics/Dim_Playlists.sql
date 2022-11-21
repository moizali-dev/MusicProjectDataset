select playlist_id, playlist_name, min(created_at) as created_at
from musicprojects_analytics_staging.Stage_Dim_Playlists
group by playlist_id, playlist_name