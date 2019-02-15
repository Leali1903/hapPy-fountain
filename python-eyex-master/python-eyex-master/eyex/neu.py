from __future__ import print_function
from api import EyeXInterface
import pygame
from pygame.locals import *
import socket

RED = (255, 0, 0)
RED_LIGHT = (240, 80, 40)

stop = 'stop'


######################### KONSTANTEN & EINSTELLUNGEN #########################
### Eyetracking ###
# Speicherort dll-Datei
lib_location = 'C:/Program Files (x86)/Tobii/Tobii EyeX Interaction/Tobii.EyeX.Client.dll'

# Zugriff auf die dll-Datei des EyeX mittels Function EyeXInterface aus api.py
eye_api = EyeXInterface(lib_location)

### GUI ###
# Pygame initialisieren
pygame.init()
# Textmodul initialisieren
pygame.font.init()

# Bildschirmeinstellungen
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
CENTER = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
# pygame-Fenster fullscreen & = Bildschirmeinstellungen
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)

# Farb- & Texteinstellungen
    # schwarz für Boxen & Texte
BLACK = (0, 0, 0)
    # weiß für Boxen & Texte
WHITE = (255, 255, 255)
HF_BLUE = (79, 154, 196)
HF_BLUE_LIGHT = (120, 200, 200)

# Schriftart & Größe wählen
MYFONT = pygame.font.SysFont('Comic Sans MS', 30)
MYFONT_BIG = pygame.font.SysFont('Comic Sans MS', 70)
# Höhe Schriftart
MYFONT_HEIGHT = MYFONT.get_height()

# Buttoncharakteristika festlegen
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)

# Für das Willkommensfenster
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
#Text für das Endfenster
TEXT_HF = MYFONT_BIG.render('Genieße deinen hapPy(i) fountain-Moment!', False, HF_BLUE)

# Logo
hf_logo = pygame.image.load('happy(i) fountain.jpeg')
hf_logo = pygame.transform.scale(hf_logo, (180, 110))

# Einstellungen für frames pro Sekunde
CLOCK = pygame.time.Clock()
FPS = 360

### SOCKET ###
# Servers hostname oder IP Addresse
HOST = '192.168.1.147'
PORT = 60000

######################### FUNCTIONS #########################


### EYETRACKING ###
# Function zum Auslesen der Koordinaten: Ausgabe zweier Listen von einmal X- und einmal Y- Koordinaten
def eyetracking(coordinates):
    eye_x.append(coordinates.x)
    eye_y.append(coordinates.y)
    return eye_x, eye_y


### GUI ###
# Funktion Textzentralisierung
def text_central(text):
    text_surface = MYFONT.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()


# Funktion interaktiver Klick-Button
def button(action):
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

def stop_button():                                         # Funktion interaktiver Klick-Button
    # Mausposition & click
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Interaktivität & Farbe des Buttons in Abhängigkeit der Mausposition & Click
    if SCREEN_HEIGHT * (7 / 9) + BUTTON_HEIGHT > mouse[1] > SCREEN_HEIGHT * (7 / 9) and SCREEN_WIDTH * (6 / 8) + BUTTON_WIDTH > mouse[0] > SCREEN_WIDTH * (6 / 8):
        pygame.draw.rect(screen, RED_LIGHT, ((SCREEN_WIDTH * (6 / 8)), (SCREEN_HEIGHT * (7 / 9)), BUTTON_WIDTH, BUTTON_HEIGHT))
        if click[0] == 1:
            send_data_stop(stop)
            pygame.quit()
            exit()
    else:
        pygame.draw.rect(screen, RED, ((SCREEN_WIDTH * (6 / 8)), (SCREEN_HEIGHT * (7 / 9)), BUTTON_WIDTH, BUTTON_HEIGHT))

    # Text Button
    textsurf_next, textrect = text_central('HALT STOPP!')
    textrect.center = ((SCREEN_WIDTH * (6 / 8) + (BUTTON_WIDTH / 2)), (SCREEN_HEIGHT * (7 / 9) + (BUTTON_HEIGHT / 2)))
    screen.blit(textsurf_next, textrect)

# Funktion Mousecursor
def mouse_cursor():
    # mousecursor als Regentropfen
    cursor = pygame.image.load('mouse.png').convert_alpha()
    cursor = pygame.transform.scale(cursor, (40, 60))
    # transparenter Originalcursor
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
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
                # nach Klick auf Escape oder q
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    raise SystemExit
        #Bildschirm schwarz füllen
        screen.fill(BLACK)
        # Rechteck um Willkommenstext
        pygame.draw.rect(screen, HF_BLUE, (250, 200, 1400, 350))
        pygame.draw.rect(screen, BLACK, (275, 225, 1350, 300))
        # Willkommenstext einblenden
        text_surf_welcome1, text_rect1 = text_central(TEXT_WELCOME1)
        text_rect1.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (6 * MYFONT_HEIGHT)))
        text_surf_welcome3, text_rect3 = text_central(TEXT_WELCOME3)
        text_rect3.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (2 * MYFONT_HEIGHT)))
        screen.blit(text_surf_welcome1, text_rect1)
        screen.blit(text_surf_welcome3, text_rect3)
        # Erklärung Stimmungsfenster einblenden
        text_surf_mood1, text_rect1 = text_central(TEXT_MOOD1)
        text_rect1.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (2 * MYFONT_HEIGHT)))
        text_surf_mood2, text_rect2 = text_central(TEXT_MOOD2)
        text_rect2.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (4 * MYFONT_HEIGHT)))
        text_surf_mood3, text_rect3 = text_central(TEXT_MOOD3)
        text_rect3.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (6 * MYFONT_HEIGHT)))
        screen.blit(text_surf_mood1, text_rect1)
        screen.blit(text_surf_mood2, text_rect2)
        screen.blit(text_surf_mood3, text_rect3)
        # Button einblenden, wenn Button geclickt dann weiter in den Moodloop
        button(mood_loop)
        # Logo statt Text
        screen.blit(hf_logo, ((SCREEN_WIDTH / 2 - 100), ((SCREEN_HEIGHT / 2) - 220)))
        mouse_cursor()
        pygame.display.update()
        # frames pro Sekunde
        CLOCK.tick(FPS)


# 2.) Stimmungfenster
def mood_loop():
    mood_exit = False
    while not mood_exit:
        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mood_exit = True
            if event.type == pygame.KEYDOWN:
                # nach Klick auf Escape oder q, beenden
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    raise SystemExit
            # Klicken = nächste Loop (oder lieber nach Zeit, zB 5 Sekunden?)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mood_exit = True
                mood_loop_move()
        # Bildschirm schwarz füllen
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
        # Aktualisierung des Screens
        pygame.display.update()
        # frames pro Sekunde
        CLOCK.tick(FPS)


# Stimmungen bewegen
def mood_loop_move():
    mood_move_exit = False
    while not mood_move_exit:
        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mood_move_exit = True
            if event.type == pygame.KEYDOWN:
                # nach Klick auf Escape oder q, beenden
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    raise SystemExit
        # Bildschirm schwarz einfärben
        screen.fill(BLACK)
        # Startpostionen definieren
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
        #Koordinaten/Pixel um die sich die Icons pro screen-blit bewegen sollen
        x = 2
        y = 1

        moving_exit = False
        while not moving_exit:
            pygame.event.get()
            # START des Eyetrackings falls Person vor Eyetracker
            eye_api.on_event += [lambda coordinates: eyetracking(coordinates)]
            screen.fill(BLACK)
            # Grenze des Screens, an der die Stimmungs-Images stehen bleiben sollen
            if x_happy > 0 and y_happy > 0:
                # Bewegung der einzelnen Icons
                x_happy -= x
                y_happy -= y
                x_sad += x
                y_sad -= y
                x_party -= x
                y_party += y
                x_chillen += x
                y_chillen += y
            else:
                # Berechnungen des Inputs
                eye_input = data_comparison(eye_x, eye_y)
                # Senden des Inputs an den Pi
                send_data(eye_input)
                ### passender Bildschirmschoner ###
                endloop(eye_input)
                # Verlassen des Loops
                moving_exit = True
                mood_move_exit = True
            # Updaten der neuen Postionen der Icons
            screen.blit(happy, (x_happy, y_happy))
            screen.blit(sad, (x_sad, y_sad))
            screen.blit(party, (x_party, y_party))
            screen.blit(chillen, (x_chillen, y_chillen))
            # Anzeigen der neuen Postionen
            pygame.display.update()
            # frames pro Sekunde
            CLOCK.tick(50)


# 4.) Endfenster
def endloop(data):
    endexit = False
    while not endexit:
        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endexit = True
            if event.type == pygame.KEYDOWN:
                # nach Klick auf Escape oder q, beenden
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    raise SystemExit
        # Aufruf des zur Stimmung gehörenden Hintergrunds
        if data == 'happy':
            screen.blit(happy_background, (0, 0))
        elif data == 'sad':
            screen.blit(sad_background, (0, 0))
        elif data == 'party':
            screen.blit(party_background, (0, 0))
        elif data == 'chillen':
            screen.blit(chillen_background, (0, 0))

        stop_button()

        mouse_cursor()


        # Logo einblenden
        screen.blit(TEXT_HF, (100, 100))
        screen.blit(hf_logo, (SCREEN_WIDTH*(7/8), 100))
        #Updaten des Displays
        pygame.display.update()
        # frames pro Sekunde
        CLOCK.tick(FPS)


### Abgleich ###
def data_comparison(data_x, data_y):
    # Berechnen der Differenzen zwischen x- und y-Koordinaten am Anfang und Ende der GUI Bewegung
    eye_movement_x = data_x[0] - data_x[-1]
    eye_movement_y = data_y[0] - data_y[-1]
    # Anpassung des Inputs an Blickdifferenzen
    if eye_movement_x > 0 and eye_movement_y > 0:
        eye_input = 'happy'
    elif eye_movement_x < 0 and eye_movement_y > 0:
        eye_input = 'sad'
    elif eye_movement_x < 0 and eye_movement_y < 0:
        eye_input = 'chillen'
    elif eye_movement_x > 0 and eye_movement_y < 0:
        eye_input = 'party'
    # Weitergabe des Inputs
    return eye_input


### SOCKET ###
def send_data(data_input):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data_input.encode('utf-8'))
        data = s.recv(1024)


def send_data_stop(stop_input):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT+1))
        s.sendall(stop_input.encode('utf-8'))
        data = s.recv(1024)


######################### AUSFÜHRUNG: EYETRACKING UND GUI #########################
#Initialisierung leerer Listen für Berechnungen
eye_x = []
eye_y = []
eye_input = []

welcome_loop()

### Abgleich ###
#eye_data = data_comparison(eye_x, eye_y)

### Socket ###
#send_data(eye_data)

### passender Bildschirmschoner ###
