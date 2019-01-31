from __future__ import print_function  # import für ET
from api import EyeXInterface

import pygame                                                  # Pygame-Modul importieren für GUI
from pygame import mixer
from pygame.locals import *
import time

import math
from math import sin,cos,pi, radians


eye_x = []
eye_y = []
eye_input = []

###################### EINGABE-GUI ######################


def text_central(text, MYFONT):                             # Funktion Textzentralisierung
    textsurface = MYFONT.render(text, True, WHITE)
    return textsurface, textsurface.get_rect()


def button(action):                                         # Funktion interaktiver Klick-Button
    # Mausposition & click
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Interaktivität & Farbe des Buttons in Abhängigkeit der Mausposition & Click
    if SCREEN_HEIGHT * (7 / 9) + BUTTON_HEIGHT > mouse[1] > SCREEN_HEIGHT * (7 / 9) and SCREEN_WIDTH * (6 / 8) + BUTTON_WIDTH > mouse[0] > SCREEN_WIDTH * (6 / 8):
        pygame.draw.rect(screen, BLUE_LIGHT, ((SCREEN_WIDTH * (6 / 8)), (SCREEN_HEIGHT * (7 / 9)), BUTTON_WIDTH, BUTTON_HEIGHT))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, BLUE, ((SCREEN_WIDTH * (6 / 8)), (SCREEN_HEIGHT * (7 / 9)), BUTTON_WIDTH, BUTTON_HEIGHT))

    # Text Button
    textsurf_next, textrect = text_central('WEITER', MYFONT)
    textrect.center = ((SCREEN_WIDTH * (6 / 8) + (BUTTON_WIDTH / 2)), (SCREEN_HEIGHT * (7 / 9) + (BUTTON_HEIGHT / 2)))
    screen.blit(textsurf_next, textrect)


def mousecursor():                                          # Funktion Mousecursor
    cursor = pygame.image.load('mouse_cd.png')                                                   # mousecursor raindrop
    # cursor = pygame.image.load('mouse.jpg')                                                    # mousecursor happy fountain
    cursor = pygame.transform.scale(cursor, (40,40))
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))  # transparenter Originalcursor
    screen.blit(cursor, pygame.mouse.get_pos())

# 1.) Willkommensfenster
def welcomeloop():
    welcomeexit = False
    while not welcomeexit:

        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                welcomeexit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):                              # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit

        screen.fill(BLACK)

        # Rechteck um Willkommenstext
        pygame.draw.rect(screen, BLUE, (200, 150, 1500, 350))
        pygame.draw.rect(screen, BLACK, (225, 175, 1450, 300))

        # Willkommenstext
        textsurf_welcome1, textrect1 = text_central(text_welcome1, MYFONT)
        textrect1.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (8 * MYFONT_HEIGHT)))

        # textsurf_welcome2, textrect2 = text_central(text_welcome2, MYFONT_BIG)            # Option: happy(i) fountain Schrift statt Logo
        # textrect2.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (4*MYFONT_HEIGHT)))

        textsurf_welcome3, textrect3 = text_central(text_welcome3, MYFONT)
        textrect3.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (2 * MYFONT_HEIGHT)))

        screen.blit(textsurf_welcome1, textrect1)
        # screen.blit(textsurf_welcome2, textrect2)                                         # Option: happy(i) fountain Schrift statt Logo
        screen.blit(textsurf_welcome3, textrect3)

        # Erklärung Musikfenster

        textsurf_mood1, textrect1 = text_central(text_mood1, MYFONT)
        textrect1.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (2 * MYFONT_HEIGHT)))

        textsurf_mood2, textrect2 = text_central(text_mood2, MYFONT)
        textrect2.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (4 * MYFONT_HEIGHT)))

        textsurf_mood3, textrect3 = text_central(text_mood3, MYFONT)
        textrect3.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (6 * MYFONT_HEIGHT)))

        screen.blit(textsurf_mood1, textrect1)
        screen.blit(textsurf_mood2, textrect2)
        screen.blit(textsurf_mood3, textrect3)

        button(musicloop)

        # screen.blit(hf_logo, (SCREEN_WIDTH*(1/15), SCREEN_HEIGHT - 250))                  # Option: Logo oben rechts
        screen.blit(logo, ((SCREEN_WIDTH / 2 - LOGO_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (7 * MYFONT_HEIGHT + 10))))       # Option: Logo statt Text
        mousecursor()
        pygame.display.update()
        clock.tick(FPS)                                                                     # frames pro Sekunde


# 2.) Musikfenster
def musicloop():
    musicexit = False
    while not musicexit:

        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                musicexit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:            # Klicken = nächste Loop (oder lieber nach Zeit, zB 5 Sekunden?)
                musicexit = True
                musicloopmove()
                eye_input = data_comparison(eye_x, eye_y)
                endloop(eye_input)

        screen.fill(BLACK)

        # Musikicon: Startpositionen (berechnet aus Screensize & Zentrierung)
        #x = 3 * width_image_x
        #y = 0.5 * SCREEN_HEIGHT - (height_image_y / 2)
        x = center_of_rotation_x + radius * cos(angle)  # Starting position x
        y = center_of_rotation_y - radius * sin(angle)  # Starting position y

        coords_1 = center_of_rotation_x - 500, center_of_rotation_y - 300
        coords_2 = center_of_rotation_x + 250, center_of_rotation_y - 300
        screen.blit(music, (coords_1[0], coords_1[1]))
        screen.blit(music2, (coords_2[0], coords_2[1]))

        pygame.display.update()
        clock.tick(FPS)                                          # frames pro Sekunde

def move_coords_right(angle, radius, coords):
    theta = math.radians(angle)
    return coords[0] + radius * math.cos(theta), coords[1] + radius * math.sin(theta)

def move_coords_left(angle, radius, coords):
    theta = math.radians(angle)
    return coords[0] - radius * math.cos(theta), coords[1] + radius * math.sin(theta)

# Musikicon bewegen
def musicloopmove():


    fps = 30
    coords_1 = center_of_rotation_x-500, center_of_rotation_y-300
    coords_2 = center_of_rotation_x+250, center_of_rotation_y - 300
    angle = 0
    #rect = pygame.Rect(*coords, 20, 20)
    #music = pygame.image.load('musicon.png')
    speed = 50
    next_tick = 500
    #music = pygame.transform.scale(music, (150, 150))
    musicmoveexit = False

    while not musicmoveexit:
        time_start = time.clock()
        if 0 + time_start <= time.clock() < 2 + time_start:
            pygame.event.get()
            eye_api.on_event += [lambda coordinates: eyetracking(coordinates)]  # START des Eyetrackings
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                musicexit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:  # Klicken = nächste Loop (oder lieber nach Zeit, zB 5 Sekunden?)
                musicexit = True
                musicloopmove()

        clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                musicmoveexit = False


        ticks = pygame.time.get_ticks()
        if ticks > next_tick:
            next_tick += speed
            angle += 1
            coords_1 = move_coords_right(angle, 4, coords_1)
            coords_2 = move_coords_left(angle, 4, coords_2)
            #rect.topleft = coords

        screen.fill(BLACK)
        # screen.fill((0, 150, 0), rect)
        screen.blit(music, (coords_1[0], coords_1[1]))
        screen.blit(music2, (coords_2[0], coords_2[1]))
        # pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)


       # if time.clock() > 8:
           # eye_input = data_comparison(eye_x, eye_y)
        if time.clock() > 20:
            #endloop(eye_input)
            musicmoveexit = True




# 4.) Endfenster
def endloop(data):
    endexit = False
    while not endexit:

        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endexit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit

        if data == 'party':
            screen.fill(BLACK)
            screen.blit(party_background, (0, 0))
            screen.blit(text, (100, 100))
            screen.blit(logo, (SCREEN_WIDTH*(6/8), 100))

            pygame.display.update()
            clock.tick()

            pygame.mixer.music.load('Kygo-Stay-Intro.mp3')
            pygame.mixer.music.play()

        elif data == 'chillen':
            screen.fill(BLACK)
            screen.blit(chillen_background, (0, 0))
            screen.blit(text, (100, 100))
            screen.blit(logo, (SCREEN_WIDTH * (6 / 8), 100))

            pygame.display.update()
            clock.tick()

            pygame.mixer.music.load('08.Dark Blue Echoes.mp3')
            pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            # Einstellungen zum Beenden der GUI
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endexit = True
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                        pygame.quit()
                        raise SystemExit

            pygame.time.Clock().tick(10)


def data_comparison(data_x, data_y):
    #gui_movement()

    eye_movement_x = data_x[0] - data_x[-1]
    eye_movement_y = data_y[0] - data_y[-1]

    if eye_movement_x < 0 and eye_movement_y < 0:
        eye_input = 'chillen'
    elif eye_movement_x > 0 and eye_movement_y < 0:
        eye_input = 'party'
    else:
        print('No Input')

    return eye_input


### EYETRACKING ###
def eyetracking(coordinates):           # Function zum Auslesen der Koordinaten
    eye_x.append(coordinates.x) # Liste der x-Koordinaten
    eye_y.append(coordinates.y)  # Liste der y-Koordinaten
    return eye_x, eye_y


### Eyetracking ###
lib_location = 'C:/Program Files (x86)/Tobii/Tobii EyeX Interaction/Tobii.EyeX.Client.dll'          # Speicherort dll-Datei
eye_api = EyeXInterface(lib_location)               # Zugriff auf die dll-Datei des EyeX mittels Function EyeXInterface aus api.py




# Pygame initialisieren
pygame.init()
pygame.font.init()                                             # Textmodul initialisieren -> braucht man das?
mixer.init()                                                   # Soundmodul initialisieren


# Bildschirmeinstellungen
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
CENTER = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)      # pygame-Fenster fullscreen & = Bildschirmeinstellungen

# Farb- & Texteinstellungen
BLACK = (0, 0, 0)                                              # schwarz für Boxen & Texte
WHITE = (255, 255, 255)                                        # weiß für Boxen & Texte
BLUE = (0, 159, 196)
BLUE_LIGHT = (0, 227, 233)

MYFONT = pygame.font.SysFont('Comic Sans MS', 30)              # Schriftart & Größe wählen
MYFONT_BIG = pygame.font.SysFont('Comic Sans MS', 70)          # Schriftart & Größe wählen

MYFONT_HEIGHT = MYFONT.get_height()                            # Höhe Schriftart

# Button
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)

# Logo
LOGO_WIDTH = 325
LOGO_HEIGHT = 200
logo = pygame.image.load('logo_museyec.png')
logo = pygame.transform.scale(logo, (LOGO_WIDTH, LOGO_HEIGHT))


# 1.) Willkommensfenster
# Willkommenstext
text_welcome1 = "Herzlich willkommen!"
text_welcome2 = "Museyec"
text_welcome3 = "Dein persönlicher Home-Entertainment Musik-Assistent, der über deine Augen gesteuert wird."

# Erklärung Musikfenster
text_mood1 = "Bitte schalte im nächsten Schritt die Musik an, indem du auf das Symbol schaust."
text_mood2 = "Das Symbol wird sich auf dem Bildschirm bewegen."
text_mood3 = "Bitte verfolge es mit deinem Blick und schaue es die ganze Zeit an."

# 2.) Fenster: Auswahl Stimmung
# Graphiken laden & verkleinern
width_image_x = 150
height_image_y = 150
size_image = (width_image_x, height_image_y)

music = pygame.image.load('chillen.png')
music = pygame.transform.scale(music, size_image)
music2 = pygame.image.load('party.png')
music2 = pygame.transform.scale(music2, size_image)

# 3.) Endfenster & kontinuierliches Hintergrundbild
# Graphiken laden & verkleinern
party_background = pygame.image.load('party.jpg')
party_background = pygame.transform.scale(party_background, SCREEN_SIZE)
chillen_background = pygame.image.load('chillen.jpg')
chillen_background = pygame.transform.scale(chillen_background, SCREEN_SIZE)

text = MYFONT_BIG.render('Genieße deinen Museyec-Moment!', False, BLUE)


# frames pro Sekunde
clock = pygame.time.Clock()
FPS = 360

# kreis

center_of_rotation_x = SCREEN_WIDTH / 2
center_of_rotation_y = SCREEN_HEIGHT / 2
radius = 100
angle = radians(45)  # pi/4 # starting angle 45 degrees
omega = 0.1  # Angular velocity
x = center_of_rotation_x + radius * cos(angle)  # Starting position x
y = center_of_rotation_y - radius * sin(angle)  # Starting position y

# Start
welcomeloop()

