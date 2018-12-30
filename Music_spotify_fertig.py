import spotipy
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json


client_credentials_manager = SpotifyClientCredentials(client_id='f8cb48bb9bd0490ea739c35ede219adf', client_secret='e3480061bd7b4e63ac8de04b856b0b18')


# util.prompt_for_user_token('123leaali456','user-modify-playback-state',client_id='f8cb48bb9bd0490ea739c35ede219adf',client_secret='e3480061bd7b4e63ac8de04b856b0b18',redirect_uri='http://localhost/')


spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#if len(sys.argv) > 1:
#    name = ' '.join(sys.argv[1:])
#else:
#    name = 'Radiohead'

#results = spotify.search(q='artist:' + name, type='artist')
#items = results['artists']['items']
#if len(items) > 0:
#    artist = items[0]
#    print(artist['name'], artist['images'][0]['url'])


# defining where to search
SEARCH_PLAYLIST_ENDPOINT ='https://api.spotify.com/v1/search?type=playlist'
AUDIO_FEATURES_ENDPOINT = 'https://api.spotify.com/v1/audio-features/{id}'


def generate_token():
    """ Generate the token."""
    credentials = SpotifyClientCredentials(client_id='f8cb48bb9bd0490ea739c35ede219adf', client_secret='e3480061bd7b4e63ac8de04b856b0b18')
    token = credentials.get_access_token()
    return token


# function for searching for playlist by name
def search_playlist(name):
    token = generate_token()
    myparams = {'type': 'playlilst'}
    myparams['q'] = name
    resp = requests.get(SEARCH_PLAYLIST_ENDPOINT, params=myparams, headers={"Authorization": "Bearer {}".format(token)})
    return resp.json()


# function for playing songs from the playlist
def get_audio_features(track_id):
    token = generate_token()
    url = AUDIO_FEATURES_ENDPOINT.format(id=track_id)
    resp = requests.get(url, headers={"Authorization": "Bearer {}".format(token)})
    return resp.json()


# input variable from eyetracking
eye_input = 'happy'

# loop for differentiating between the 4 input modi and what will be triggered in spotify
if eye_input == 'happy': # in case eyetracking input was happy
    playlist = search_playlist('Happy Beats')
    items = playlist['playlists']['items'][0]['tracks']
    for i in items:
        get_audio_features(i) # play all songs in playlist
elif eye_input == 'chillen': # in case eyetracking input was chillen
    playlist = search_playlist('STEVIE MC CRORIE - Best Of') 
    items = playlist['playlists']['items'][0]['tracks']
    for i in items:
        get_audio_features(i) # play all songs in playlist
elif eye_input == 'party': # in case eyetracking input was party
    playlist = search_playlist('Sonne, Mond und Sterne 2018')
    items = playlist['playlists']['items'][0]['tracks']
    for i in items:
        get_audio_features(i) # play all songs in playlist
elif eye_input == 'sad': # in case eyetracking input was sad
    playlist = search_playlist('Sad Songs')
    items = playlist['playlists']['items'][0]['tracks']
    for i in items:
        get_audio_features(i) # play all songs in playlist
else:
    print('Error: No Input received!')