import pygame
import glob, os

pygame.mixer.init()

import os

def find_tracks(folder):
    for root, dirs, files in os.walk(folder):  
        for tracks in files:
            if tracks.endswith(".mp3"):
                print(tracks)
            else: print('No mp3-files found')
    return tracks
def play_tracks(folder):
    for track in tracks: 
        pygame.mixer.music.load(folder + track)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
    
    

eye_input = 'happy'

if eye_input == 'happy': # in case eyetracking input was happy
    folder = "/home/pi/Music/happy/"
    tracks = find_tracks(folder)
    play_tracks(folder)
elif eye_input == 'chillen': # in case eyetracking input was chillen
    find_tracks("/home/pi/Music/chillen")
    pygame.mixer.music.load(tracks)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
elif eye_input == 'party': # in case eyetracking input was party
    find_tracks("/home/pi/Music/party")
    pygame.mixer.music.load(tracks)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
elif eye_input == 'sad': # in case eyetracking input was sad
    pfind_tracks("/home/pi/Music/sad")
    pygame.mixer.music.load(tracks)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
else:
    print('Error: No Input received!')


