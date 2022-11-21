Select t1.* ,t4.category
from `musicprojects_analytics.Dim_Tracks` t1
left join `musicprojects.musicprojects_analytics.Dim_Track_Playlist_Relationship` t2
on t1.track_id = t2.track_id
left join `musicprojects_analytics.Dim_Playlist_Category_Relationship` t3
on t2.playlist_id = t3.Playlist_Id
left join `musicprojects.musicprojects_analytics.Dim_Category` t4
on t3.category_id = t4.category_id
WHERE true
QUALIFY ROW_NUMBER() OVER (PARTITION BY track_id) = 1