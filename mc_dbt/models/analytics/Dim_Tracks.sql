Select *
from musicprojects_analytics_staging.Stage_Dim_Tracks
WHERE true
QUALIFY ROW_NUMBER() OVER (PARTITION BY track_id) = 1