Select track_id, playlist_id, min(created_at) as created_at
from musicprojects_analytics_staging.Stage_Dim_Track_Playlist_Relationship
group by track_id, playlist_id