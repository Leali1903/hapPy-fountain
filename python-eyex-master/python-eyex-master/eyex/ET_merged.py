from __future__ import print_function               # import für ET
from api import EyeXInterface

import pygame                                       # import für GUI
from pygame.locals import *

import numpy as np                                  # import für Abgleich

import socket                                       # für Socket (senden von Abgleich-Daten an Pi)

######################### KONSTANTEN & EINSTELLUNGEN #########################
### Eyetracking ###
lib_location = 'C:/Program Files (x86)/Tobii/Tobii EyeX Interaction/Tobii.EyeX.Client.dll'          # Speicherort dll-Datei
eye_api = EyeXInterface(lib_location)               # Zugriff auf die dll-Datei des EyeX mittels Function EyeXInterface aus api.py

### GUI ###
# Pygame initialisieren
pygame.init()

# Textmodul initialisieren -> braucht man das?
pygame.font.init()

# Bildschirmeinstellungen
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
CENTER = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)      # pygame-Fenster fullscreen & = Bildschirmeinstellungen

# Farb- & Texteinstellungen
BLACK = (0, 0, 0)                                              # schwarz für Boxen & Texte
WHITE = (255, 255, 255)                                        # weiß für Boxen & Texte
HF_BLUE = (79, 154, 196)
HF_BLUE_LIGHT = (120, 200, 200)

MYFONT = pygame.font.SysFont('Comic Sans MS', 30)              # Schriftart & Größe wählen
MYFONT_BIG = pygame.font.SysFont('Comic Sans MS', 70)          # Schriftart & Größe wählen

MYFONT_HEIGHT = MYFONT.get_height()                            # Höhe Schriftart

# Button
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)

# 1.) Willkommensfenster
# Willkommenstext
TEXT_WELCOME1 = "Herzlich willkommen!"
TEXT_WELCOME2 = "hapPy(i) fountain:"
TEXT_WELCOME3 = "Dein persönlicher Home-Entertainment Assistent, der über deine Augen gesteuert wird."

# Erklärung Stimmungsfenster
TEXT_MOOD1 = "Bitte wähle im nächsten Schritt deine Stimmung aus, indem du auf die passende Stimmung schaust."
TEXT_MOOD2 = "Das Symbol wird sich auf dem Bildschirm bewegen."
TEXT_MOOD3 = "Bitte verfolge es mit deinem Blick und schaue es die ganze Zeit an."

# 2.) Fenster: Auswahl Stimmung
# Graphiken laden & verkleinern
WIDTH_MOOD_IMAGE_X = 150
HEIGHT_MOOD_IMAGE_Y = 150
SIZE_MOOD_IMAGE = (WIDTH_MOOD_IMAGE_X, HEIGHT_MOOD_IMAGE_Y)

happy = pygame.image.load('happy.png')
happy = pygame.transform.scale(happy, SIZE_MOOD_IMAGE)
sad = pygame.image.load('sad.png')
sad = pygame.transform.scale(sad, SIZE_MOOD_IMAGE)
party = pygame.image.load('party.png')
party = pygame.transform.scale(party, SIZE_MOOD_IMAGE)
chillen = pygame.image.load('chillen.png')
chillen = pygame.transform.scale(chillen, SIZE_MOOD_IMAGE)

# 3.) Endfenster & kontinuierliches Hintergrundbild, abhängig von Stimmung
# Graphiken laden & verkleinern
happy_background = pygame.image.load('freude.jpg')
happy_background = pygame.transform.scale(happy_background, SCREEN_SIZE)
sad_background = pygame.image.load('trauer.jpg')
sad_background = pygame.transform.scale(sad_background, SCREEN_SIZE)
party_background = pygame.image.load('party.jpg')
party_background = pygame.transform.scale(party_background, SCREEN_SIZE)
chillen_background = pygame.image.load('chillen.jpg')
chillen_background = pygame.transform.scale(chillen_background, SCREEN_SIZE)

TEXT_HF = MYFONT_BIG.render('Genieße deinen hapPy(i) fountain-Moment!', False, HF_BLUE)

# Logo
hf_logo = pygame.image.load('happy(i) fountain.jpeg')
hf_logo = pygame.transform.scale(hf_logo, (180, 110))

# frames pro Sekunde
CLOCK = pygame.time.Clock()
FPS = 360

### SOCKET ###
HOST = '172.16.107.164'  # The server's hostname or IP address
PORT = 60005

######################### FUNCTIONS #########################


### EYETRACKING ###
def eyetracking(coordinates):           # Function zum Auslesen der Koordinaten
    eye_x.append(coordinates.x) # Liste der x-Koordinaten
    eye_y.append(coordinates.y)  # Liste der y-Koordinaten
    return eye_x, eye_y


### GUI ###
def text_central(text):                             # Funktion Textzentralisierung
    text_surface = MYFONT.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()


def button(action):                                         # Funktion interaktiver Klick-Button
    # Mausposition & click
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Interaktivität & Farbe des Buttons in Abhängigkeit der Mausposition & Click
    if SCREEN_HEIGHT * (7 / 9) + BUTTON_HEIGHT > mouse[1] > SCREEN_HEIGHT * (7 / 9) and SCREEN_WIDTH * (6 / 8) + BUTTON_WIDTH > mouse[0] > SCREEN_WIDTH * (6 / 8):
        pygame.draw.rect(screen, HF_BLUE_LIGHT, ((SCREEN_WIDTH * (6 / 8)), (SCREEN_HEIGHT * (7 / 9)), BUTTON_WIDTH, BUTTON_HEIGHT))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, HF_BLUE, ((SCREEN_WIDTH * (6 / 8)), (SCREEN_HEIGHT * (7 / 9)), BUTTON_WIDTH, BUTTON_HEIGHT))

    # Text Button
    textsurf_next, textrect = text_central('WEITER')
    textrect.center = ((SCREEN_WIDTH * (6 / 8) + (BUTTON_WIDTH / 2)), (SCREEN_HEIGHT * (7 / 9) + (BUTTON_HEIGHT / 2)))
    screen.blit(textsurf_next, textrect)


def mouse_cursor():                                          # Funktion Mousecursor
    cursor = pygame.image.load('mouse.png').convert_alpha()                                      # mousecursor raindrop
    cursor = pygame.transform.scale(cursor, (40, 60))
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))  # transparenter Originalcursor
    screen.blit(cursor, pygame.mouse.get_pos())


# 1.)  Willkommensfenster
def welcome_loop():
    welcome_exit = False
    while not welcome_exit:
        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                welcome_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):                              # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit

        screen.fill(BLACK)

        # Rechteck um Willkommenstext
        pygame.draw.rect(screen, HF_BLUE, (250, 200, 1400, 350))
        pygame.draw.rect(screen, BLACK, (275, 225, 1350, 300))

        # Willkommenstext
        text_surf_welcome1, text_rect1 = text_central(TEXT_WELCOME1)
        text_rect1.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (6 * MYFONT_HEIGHT)))

        text_surf_welcome3, text_rect3 = text_central(TEXT_WELCOME3)
        text_rect3.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (2 * MYFONT_HEIGHT)))

        screen.blit(text_surf_welcome1, text_rect1)
        screen.blit(text_surf_welcome3, text_rect3)

        # Erklärung Stimmungsfenster
        text_surf_mood1, text_rect1 = text_central(TEXT_MOOD1)
        text_rect1.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (2 * MYFONT_HEIGHT)))

        text_surf_mood2, text_rect2 = text_central(TEXT_MOOD2)
        text_rect2.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (4 * MYFONT_HEIGHT)))

        text_surf_mood3, text_rect3 = text_central(TEXT_MOOD3)
        text_rect3.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (6 * MYFONT_HEIGHT)))

        screen.blit(text_surf_mood1, text_rect1)
        screen.blit(text_surf_mood2, text_rect2)
        screen.blit(text_surf_mood3, text_rect3)

        button(mood_loop)

        screen.blit(hf_logo, ((SCREEN_WIDTH / 2 - 100), ((SCREEN_HEIGHT / 2) - 220)))       # Option: Logo statt Text
        mouse_cursor()
        pygame.display.update()
        CLOCK.tick(FPS)                                                                     # frames pro Sekunde


# 2.) Stimmungfenster
def mood_loop():
    mood_exit = False
    while not mood_exit:
        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mood_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:            # Klicken = nächste Loop (oder lieber nach Zeit, zB 5 Sekunden?)
                mood_exit = True
                mood_loop_move()
                eye_input = data_comparison(eye_x, eye_y)
                send_data(eye_input)
                print(eye_input)
                ### passender Bildschirmschoner ###
                endloop(eye_input)

        screen.fill(BLACK)

        # Stimmungen anzeigen: Startpositionen (berechnet aus Screensize & Zentrierung)
        x_happy = 0.5 * SCREEN_WIDTH - WIDTH_MOOD_IMAGE_X
        y_happy = 0.5 * SCREEN_HEIGHT - HEIGHT_MOOD_IMAGE_Y
        x_sad = 0.5 * SCREEN_WIDTH
        y_sad = 0.5 * SCREEN_HEIGHT - HEIGHT_MOOD_IMAGE_Y
        x_party = 0.5 * SCREEN_WIDTH - WIDTH_MOOD_IMAGE_X
        y_party = 0.5 * SCREEN_HEIGHT
        x_chillen = 0.5 * SCREEN_WIDTH
        y_chillen = 0.5 * SCREEN_HEIGHT

        screen.blit(happy, (x_happy, y_happy))
        screen.blit(sad, (x_sad, y_sad))
        screen.blit(party, (x_party, y_party))
        screen.blit(chillen, (x_chillen, y_chillen))

        pygame.display.update()
        CLOCK.tick(FPS)                                          # frames pro Sekunde


# Stimmungen bewegen
def mood_loop_move():
    mood_move_exit = False

    while not mood_move_exit:
        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mood_move_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit

        screen.fill(BLACK)

        x_happy = 0.5 * SCREEN_WIDTH - WIDTH_MOOD_IMAGE_X
        y_happy = 0.5 * SCREEN_HEIGHT - HEIGHT_MOOD_IMAGE_Y
        x_sad = 0.5 * SCREEN_WIDTH
        y_sad = 0.5 * SCREEN_HEIGHT - HEIGHT_MOOD_IMAGE_Y
        x_party = 0.5 * SCREEN_WIDTH - WIDTH_MOOD_IMAGE_X
        y_party = 0.5 * SCREEN_HEIGHT
        x_chillen = 0.5 * SCREEN_WIDTH
        y_chillen = 0.5 * SCREEN_HEIGHT

        screen.blit(happy, (x_happy, y_happy))
        screen.blit(sad, (x_sad, y_sad))
        screen.blit(party, (x_party, y_party))
        screen.blit(chillen, (x_chillen, y_chillen))

        x = 2
        y = 1

        moving_exit = False
        while not moving_exit:
            pygame.event.get()
            eye_api.on_event += [lambda coordinates: eyetracking(coordinates)]          # START des Eyetrackings
            screen.fill(BLACK)
            if x_happy > 0 and y_happy > 0:  # Grenze des Screens, an der die Stimmungs-Images stehen bleiben sollen
                x_happy -= x
                y_happy -= y

                x_sad += x
                y_sad -= y

                x_party -= x
                y_party += y

                x_chillen += x
                y_chillen += y

            elif y_happy <= 0:
                x_happy = x_happy
                y_happy = y_happy

                x_sad = x_sad
                y_sad = y_sad

                x_party = x_party
                y_party = y_party

                x_chillen = x_chillen
                y_chillen = y_chillen

                moving_exit = True
                mood_move_exit = True

            screen.blit(happy, (x_happy, y_happy))
            screen.blit(sad, (x_sad, y_sad))
            screen.blit(party, (x_party, y_party))
            screen.blit(chillen, (x_chillen, y_chillen))

            pygame.display.update()
            CLOCK.tick(50)  # frames pro Sekunde
            # mood_move_exit = True


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

        if data == 'happy':
            screen.blit(happy_background, (0, 0))
        elif data == 'sad':
            screen.blit(sad_background, (0, 0))
        elif data == 'party':
            screen.blit(party_background, (0, 0))
        elif data == 'chillen':
            screen.blit(chillen_background, (0, 0))

        screen.blit(TEXT_HF, (100, 100))
        screen.blit(hf_logo, (SCREEN_WIDTH*(7/8), 100))
        pygame.display.update()
        CLOCK.tick(FPS)                                          # frames pro Sekunde


### Abgleich ###
def gui_movement():
    for i in range(1,391):
        gui_x_happy.append(810-2*i)
        gui_y_happy.append(390-i)
        gui_x_party.append(810 - 2 * i)
        gui_y_party.append(540 + i)
        gui_x_chillen.append(960 + 2 * i)
        gui_y_chillen.append(540 + i)
        gui_x_sad.append(960 + 2 * i)
        gui_y_sad.append(390 - i)
    return gui_x_happy, gui_y_happy, gui_x_party, gui_y_party, gui_x_chillen, gui_y_chillen, gui_x_sad, gui_y_sad


def correlation(x, y):
    sd_x = np.sqrt(np.var(x))
    sd_y = np.sqrt(np.var(y))
    return np.cov(x,y)/(sd_x * sd_y)


def data_comparison(data_x, data_y):
    gui_movement()

    eye_movement_x = data_x[0] - data_x[-1]
    eye_movement_y = data_y[0] - data_y[-1]

    if eye_movement_x > 0 and eye_movement_y > 0:
        eye_input = 'happy'
    elif eye_movement_x < 0 and eye_movement_y > 0:
        eye_input = 'sad'
    elif eye_movement_x < 0 and eye_movement_y < 0:
        eye_input = 'chillen'
    elif eye_movement_x > 0 and eye_movement_y < 0:
        eye_input = 'party'

    return eye_input


### SOCKET ###
def send_data(data_input):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data_input.encode('utf-8'))
        data = s.recv(1024)


######################### AUSFÜHRUNG: EYETRACKING UND GUI #########################
eye_x = []
eye_y = []
gui_x_happy = []
gui_y_happy = []
gui_x_party = []
gui_y_party = []
gui_x_chillen = []
gui_y_chillen = []
gui_x_sad = []
gui_y_sad = []
eye_input = []

welcome_loop()

### Abgleich ###
#eye_input = data_comparison(eye_x, eye_y)

### Socket ###
#send_data(eye_input)

### passender Bildschirmschoner ###
endloop(eye_input)