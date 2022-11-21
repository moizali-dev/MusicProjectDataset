select id as track_id, danceability, energy, cast(key as INT64) as key, loudness, cast(mode as INT64) as mode, 
speechiness, acousticness, instrumentalness, liveness, valence, tempo, 
cast(duration_ms as INT64) as duration_ms, 
cast(time_signature as INT64) as time_signature, Name, Artist, created_at
FROM musicprojects.musicprojects_staging.{{ set_table() }}
where id is not null and Name is not null and Artist is not null