import os
import sys
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from datetime import datetime

from pythonscripts.utils.spotifyclient import SpotifyClient
from pythonscripts.utils.tokenupdate import TokenUpdate
from pythonscripts.utils.gbq import BigQuery

def main(categories_lst = []):
    # Get the token from the link here: https://developer.spotify.com/console/get-playlist/?playlist_id=&market=&fields=&additional_types=
    startTime = datetime.now()

    tu = TokenUpdate(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"], datetime.now())
    tu.update_token(firsttime="Yes")
    sc = SpotifyClient(os.environ["SPOTIFY_TOKEN"],os.environ["SPOTIFY_USER"])

    categories_lst = ["Rock" ,"Pop","Country","Hip-Hop","R&B","Indie","Jazz","Soul","Dance/Electronic","Sleep","Metal"]
    df = pd.DataFrame()

    # Track list from Dim_Track model
    gbq = BigQuery()


    sql_string = """
    Select distinct track_id
    from musicprojects.musicprojects_analytics_staging.Stage_Dim_Tracks
    """

    tracks_lst = gbq.read_query_to_df(sql_string,project_id="musicprojects")['track_id'].unique()

    ## Start of query

    categories = sc.get_categories()
    for category in categories:
        if category.name in categories_lst:

            # Get playlists for the category
            try:
                playlists = sc.get_categories_playlist(category.id, 40)

                # Get tracks for the playlist
                for playlist in playlists:

                    try:  

                        # update token
                        tu.update_token()
                        
                        sc._set_authorization_token(os.environ["SPOTIFY_TOKEN"])

                        # get tracks
                        print(f"Working on {playlist.name} and genre: {category.name}")
                        track_lst = sc.get_playlist_tracks(playlist.id)

                        for trackLst in track_lst:

                            if trackLst.id not in tracks_lst:
                                print(f"Working on {playlist.name} and genre: {category.name} and tracklst: {trackLst}")
                                result = sc.get_track_features(trackLst.id)
                                temp_df = pd.DataFrame(result, index=['i',])
                                temp_df["category"] = category.name
                                temp_df["category_id"] = category.id
                                temp_df["Name"] = trackLst.name
                                temp_df["Artist"] = trackLst.artist
                                temp_df["Playlist_Id"] = playlist.id
                                temp_df["Playlist_name"] = playlist.name
                                temp_df["created_at"] = datetime.now()

                                if df.empty:
                                    df = temp_df
                                else:
                                    df = pd.concat([df,temp_df])  
                    
                    except Exception as e: 
                        print(e)
                        print(f"FAILED -- Playlist Name: {playlist.name}, Playlist ID: {playlist.id} and Genre: {category.name}")
                        pass

            except Exception as e:
                print(e)
                print(f"FAILED -- Playlist Name: {playlist.name}")
                print(df.shape)

    df.to_csv("Music_Classification_Dataset_test_new.csv", index=False)

if __name__=="__main__":
    main()