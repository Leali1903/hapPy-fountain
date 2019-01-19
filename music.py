import pygame
import glob, os

pygame.mixer.init()

import os

def find_play_tracks(folder):
    for root, dirs, files in os.walk(folder):  
        for tracks in files:
            if tracks.endswith(".mp3"):
                print(tracks)
                pygame.mixer.music.load(folder + tracks)
                pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
    return tracks

eye_input = 'sad'

if eye_input == 'happy': # in case eyetracking input was happy
    folder = "/home/pi/Music/happy/"
    tracks = find_play_tracks(folder)
elif eye_input == 'chillen': # in case eyetracking input was chillen
    folder = "/home/pi/Music/chillen/"
    tracks = find_play_tracks(folder)
elif eye_input == 'party': # in case eyetracking input was party
    folder = "/home/pi/Music/party/"
    tracks = find_play_tracks(folder)
elif eye_input == 'sad': # in case eyetracking input was sad
    folder = "/home/pi/Music/sad/"
    tracks = find_play_tracks(folder)
else:
    print('Error: No Input received!')


