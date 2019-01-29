import pygame                                                  # Pygame-Modul importieren für GUI
from pygame import mixer
from pygame.locals import *
import time

import math
from math import sin,cos,pi, radians


eye_input = 'happy'

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

        screen.fill(BLACK)

        # Musikicon: Startpositionen (berechnet aus Screensize & Zentrierung)
        #x = 3 * width_image_x
        #y = 0.5 * SCREEN_HEIGHT - (height_image_y / 2)
        x = center_of_rotation_x + radius * cos(angle)  # Starting position x
        y = center_of_rotation_y - radius * sin(angle)  # Starting position y

        screen.blit(music, (x, y))
        pygame.display.update()
        clock.tick(FPS)                                          # frames pro Sekunde

def move_coords(angle, radius, coords):
    theta = math.radians(angle)
    return coords[0] + radius * math.cos(theta), coords[1] + radius * math.sin(theta)

# Musikicon bewegen
def musicloopmove():

    time.clock()
    fps = 30
    coords = 400, 200
    angle = 0
    rect = pygame.Rect(*coords, 20, 20)
    #music = pygame.image.load('musicon.png')
    speed = 50
    next_tick = 500
    #music = pygame.transform.scale(music, (150, 150))
    musicmoveexit = False

    while not musicmoveexit:

        clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                musicmoveexit = True

        ticks = pygame.time.get_ticks()
        if ticks > next_tick:
            next_tick += speed
            angle += 1
            coords = move_coords(angle, 2, coords)
            rect.topleft = coords

        screen.fill((0, 0, 30))
        # screen.fill((0, 150, 0), rect)
        screen.blit(music, (coords[0], coords[1]))
        # pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)

        if time.clock() > 15:
            musicmoveexit = True
            endloop()



# 4.) Endfenster
def endloop():
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

        screen.fill(BLACK)
        screen.blit(party_background, (0, 0))
        screen.blit(text, (100, 100))
        screen.blit(logo, (SCREEN_WIDTH*(6/8), 100))

        pygame.display.update()
        clock.tick()

        pygame.mixer.music.load('Kygo-Stay-Intro.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


# Pygame initialisieren
pygame.init()
pygame.font.init()                                             # Textmodul initialisieren -> braucht man das?
mixer.init()                                                   # Soundmodul initialisieren


# Bildschirmeinstellungen
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1000
CENTER = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)      # pygame-Fenster fullscreen & = Bildschirmeinstellungen

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

music = pygame.image.load('musicon.png')
music = pygame.transform.scale(music, size_image)

# 3.) Endfenster & kontinuierliches Hintergrundbild
# Graphiken laden & verkleinern
party_background = pygame.image.load('party.jpg')
party_background = pygame.transform.scale(party_background, SCREEN_SIZE)

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

