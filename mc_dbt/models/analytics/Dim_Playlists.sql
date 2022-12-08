select playlist_id, max(playlist_name) as playlist_name, min(created_at) as created_at
from musicprojects_analytics_staging.Stage_Dim_Playlists
group by playlist_id