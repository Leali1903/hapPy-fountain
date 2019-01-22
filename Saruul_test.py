# Funktion zum suchen und abspielen der Tracks
def find_play_tracks(folder):
    tracks = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".mp3"):
                print(file)
                tracks.append(file)
    return tracks
   
def play_tracks(tracks):
    tracksIterator = iter(tracks)
    firstTrack = next(tracksIterator)
    pygame.mixer.music.load(firstTrack)
    pygame.mixer.music.play()
    for track in tracksIterator:
        pygame.mixer.music.queue(track)
    
 
    

###################### STEUERUNG JE NACH INPUT ######################

# Einschalten des pygame-mixers für die Musik
pygame.mixer.init()

# Inputschleife
if eye_input == 'happy':
    ### BRUNNEN ###
    os.system(ON)
    time.sleep(60)  # rausnehmen weil nach Liedern ausgeschaltet
    os.system(OFF)
    ### MUSIK ###
    folder = "/home/pi/Music/happy/"
    tracks = find_tracks(folder)
    play_tracks(tracks)
     next_track_index = 0
    # ### LED LICHTERKETTE ###
    while True:  # weil es sich immer weiter bewegen soll.
         cycle(0.001, wheel_color)  # Farbübergänge in bunt in Kreisform
         if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load(folder + tracks[next_track_index])
            pygame.mixer.music.play()
            next_track_index += 1
         if next_track_index >= len(tracks):
            break
    # ### LED LICHTERKETTE ###
    while True:  # weil es sich immer weiter bewegen soll.
         cycle(0.001, wheel_color)  # Farbübergänge in bunt in Kreisform
