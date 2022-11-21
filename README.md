# Data Requirements

- Music features by Genre
- Can be static or add more songs with a date stamp

# Learning
- Created an OOP class for Spotify API and Spotify Token Update
- Creating a staging layer and analytics layer to leverage the schema concept
- Transformations and tests done using dbt
- Using Airflow and Docker to orchestrate the runs

# Challenges and Solutions

- Spotify API token access expires in an hour
    - https://stackoverflow.com/questions/65435932/spotify-api-authorization-code-flow-with-python
    - Created a Class script that updates the env variable in a set amount of time i.e. every 15mins it will be updated
    - The class also has a method to update the token right before the script begins (so that user doesnt have to do it manually)
- Should the output from the script be saved in cloud storage, transformed and fed into big query or should it be transformed locally first?
- Increase the speed of API calls (33104 tracks in one hour)
- Spotify call has a limit and returns a 429 response
    - Use the header from the `response.header` to get the time limit required to sleep
- Integrating dbt to airflow
    - Had to pass the ~/.dbt/profile and change the ENV DBT to the path where the file can be found
- When the sleep method is called on a 429 response then the code skips that `track_id`. It should come back to the same `track_id` again
- If the `music_classification_main.py` fails then all the information gathered so far is lost

# Experiments

- Test out batch API calls instead of iterating through each track one by one
- Can each DAG be one playlist and run in parallel?

