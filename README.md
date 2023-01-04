# Data Requirements

- Create datasets using star schema methodology that have audio features of tracks by genre from Spotify API
- There are 13 audio features for each track, including confidence measures like `acousticness, liveness, speechiness and instrumentalness`, perceptual measures like `energy, loudness, danceability and valence (positiveness)`, and descriptors like `duration, tempo, key, time signature and mode`.
- The Genres are `'Hip-Hop':0, 'Pop':1, 'Country':2, 'Rock':3, 'R&B':4, 'Dance/Electronic':5, 'Indie':6, 'Sleep':7, 'Jazz':8, 'Soul':9, 'Metal':10'`
- The datasets get automatically validated and updated on a weekly basis

# Design and Flow Architecture

![ETL](https://github.com/moizali-dev/MusicProjectDataset/blob/main/images/etl.png?raw=true)

# Learnings

- Created an OOP class for Spotify API and Spotify Token Update to get information from Spotify API
- Creating a staging layer and analytics layer to leverage the schema concept
- Transformations and tests done using dbt
- Using Airflow and Docker to orchestrate the runs

# Challenges and Solutions

- Spotify API token access expires in an hour
    - https://stackoverflow.com/questions/65435932/spotify-api-authorization-code-flow-with-python
    - Created a class (`tokenupdate.py`) that updates the env variable in a set amount of time i.e. every 15mins it will be updated
    - The class also has a method to update the token right before the script begins (so that user doesnt have to do it manually)
- Increase the speed of API calls (33104 tracks in one hour)
- Spotify call has a limit and returns a 429 response
    - Use the header from the `response.header` to get the time limit required to sleep
- Integrating dbt to airflow
    - Had to pass the ~/.dbt/profile and change the ENV DBT to the path where the file can be found
- When the sleep method is called on a 429 response then the code skips that `track_id`. It should come back to the same `track_id` again
- If the `music_classification_main.py` fails then all the information gathered so far is lost
- If the `MusicalOrchestration` runs again in the same day, then the file loaded in the gcp bucket is replaced. 
- Figure out the disributions of genres data being added over time

# Experiments

- Test out batch API calls instead of iterating through each track one by one
- Can each DAG be one playlist and run in parallel?
