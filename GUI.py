import pygame                                                  # Pygame-Modul importieren für GUI
from pygame.locals import *

eye_input = 'happy'

###################### EINGABE-GUI ######################

# Pygame initialisieren
pygame.init()
pygame.font.init()                                             # Textmodul initialisieren -> braucht man das?

# Bildschirmeinstellungen
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
CENTER = ((SCREEN_WIDTH % 2), (SCREEN_HEIGHT % 2))
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)      # pygame-Fenster fullscreen & = Bildschirmeinstellungen

# Farb- & Texteinstellungen
BLACK = (0, 0, 0)                                              # schwarz für Boxen & Texte
WHITE = (255, 255, 255)                                        # weiß für Boxen & Texte
HF_BLUE = (79, 154, 196)
HF_BLUE_LIGHT = (120, 200, 200)
MYFONT = pygame.font.SysFont('Comic Sans MS', 30)              # Schriftart & Größe wählen
MYFONT_BIG = pygame.font.SysFont('Comic Sans MS', 70)          # Schriftart & Größe wählen

def text_central(text, MYFONT):                                # Funktion Textzentralisierung
    textsurface = MYFONT.render(text, True, WHITE)
    return textsurface, textsurface.get_rect()


# Funktion interaktive Klick-Buttons
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)

text_next = 'WEITER'


def button_text(text_next):
    textsurf_next, textrect = text_central(text_next, MYFONT)
    textrect.center = ((SCREEN_WIDTH * (6 / 8) + (BUTTON_WIDTH / 2)), (SCREEN_HEIGHT * (7 / 9) + (BUTTON_HEIGHT / 2)))
    screen.blit(textsurf_next, textrect)


def button(action): # ABSTRAKTER GESTALTEN? zB (msg,x,y,w,h,ic,ac,action)
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

    # Text des Buttons
    button_text(text_next)


# Logo
hf_logo = pygame.image.load('happy(i) fountain.jpeg')
hf_logo = pygame.transform.scale(hf_logo, (140, 100))

# 1.) Willkommensfenster
text_welcome = "Herzlich willkommen! hapPy(i) fountain: Dein persönlicher Home-Entertainment Assistent, der über \n" \
               "deine Augenbewegungen gesteuert wird."

# 2.) Erklärung Stimmungsfenster
text_mood = "Bitte wähle im nächsten Schritt deine momentane Stimmung aus, indem du auf die passende Stimmung \n" \
            "schaust. Das rechteck wird sich auf dem Bildschirm bewegen. Bitte verfolge es mit deinem Blick und \n" \
            "schaue es die ganze Zeit an."

# 3.) Fenster: Auswahl Stimmung
# # Graphiken laden & verkleinern
width_moodimage_x = 150
height_moodimage_y = 150
size_moodimage = (width_moodimage_x,height_moodimage_y)

happy = pygame.image.load('happy.png')
happy = pygame.transform.scale(happy, size_moodimage)
sad = pygame.image.load('sad.png')
sad = pygame.transform.scale(sad, size_moodimage)
party = pygame.image.load('party.png')
party = pygame.transform.scale(party, size_moodimage)
chillen = pygame.image.load('chillen.png')
chillen = pygame.transform.scale(chillen, size_moodimage)

# 4.) Endfenster & kontinuierliches Hintergrundbild, abhängig von Stimmung

happy_background = pygame.image.load('freude.jpg')
happy_background = pygame.transform.scale(happy_background, SCREEN_SIZE)
sad_background = pygame.image.load('trauer.jpg')
sad_background = pygame.transform.scale(sad_background, SCREEN_SIZE)
party_background = pygame.image.load('party.jpg')
party_background = pygame.transform.scale(party_background, SCREEN_SIZE)
chillen_background = pygame.image.load('chillen.jpg')
chillen_background = pygame.transform.scale(chillen_background, SCREEN_SIZE)

text_hf = MYFONT_BIG.render('Genieße deinen hapPy(i) fountain-Moment!', False, HF_BLUE)


# GUI anzeigen
clock = pygame.time.Clock()
FPS = 360

# 1.) Willkommenstext
def welcomeloop():
    welcomeExit = False
    while not welcomeExit:

        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                welcomeExit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit

        screen.fill(BLACK)

        textsurf_welcome, textrect = text_central(text_welcome, MYFONT)
        textrect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))

        button(explanationloop)

        screen.blit(textsurf_welcome, textrect)
        screen.blit(hf_logo, (SCREEN_WIDTH*(7/8), 100))
        pygame.display.update()
        clock.tick(FPS)                                          # frames pro Sekunde


# 2.) Erklärung Stimmungsfenster
INTRO_DURATION = 4 # how long to play intro in seconds
TICK = USEREVENT + 1 # event type
pygame.time.set_timer(TICK, 1000) # fire the event (tick) every second
time_in_seconds = 0

def explanationloop():
    explanationExit = False
    while not explanationExit:

        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                explanationExit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit


        screen.fill(BLACK)

        textsurf_mood, textrect = text_central(text_mood, MYFONT)
        textrect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))

        button(moodloop)

        screen.blit(textsurf_mood, textrect)
        screen.blit(hf_logo, (SCREEN_WIDTH * (7 / 8), 100))
        pygame.display.update()
        clock.tick(FPS)                                          # frames pro Sekunde


# 3.) Stimmungfenster
def moodloop():
    moodExit = False
    while not moodExit:

        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                moodExit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:            # Klicken = nächste Loop (oder lieber nach Zeit, zB 5 Sekunden?)
                moodExit = True
                moodloopmove()

        screen.fill(BLACK)

        ## Stimmungen anzeigen
        # # Startpositionen (berechnet aus Screensize & Zentrierung)
        x_happy = 0.5 * SCREEN_WIDTH - width_moodimage_x
        y_happy = 0.5 * SCREEN_HEIGHT - height_moodimage_y
        x_sad = 0.5 * SCREEN_WIDTH
        y_sad = 0.5 * SCREEN_HEIGHT - height_moodimage_y
        x_party = 0.5 * SCREEN_WIDTH - width_moodimage_x
        y_party = 0.5 * SCREEN_HEIGHT
        x_chillen = 0.5 * SCREEN_WIDTH
        y_chillen = 0.5 * SCREEN_HEIGHT

        screen.blit(happy, (x_happy, y_happy))
        screen.blit(sad, (x_sad, y_sad))
        screen.blit(party, (x_party, y_party))
        screen.blit(chillen, (x_chillen, y_chillen))

        pygame.display.update()
        clock.tick(FPS)                                          # frames pro Sekunde




## Stimmungen bewegen (innerhalb Screens) ALS SIE NOCH OHNE FUNCTION WAREN HAT ES FUNLKTIONIERT!!!
def moodloopmove():
    moodmoveExit = False
    while not moodmoveExit:

    # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                moodmoveExit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit

        x_happy = 0.5 * SCREEN_WIDTH - width_moodimage_x
        y_happy = 0.5 * SCREEN_HEIGHT - height_moodimage_y
        x_sad = 0.5 * SCREEN_WIDTH
        y_sad = 0.5 * SCREEN_HEIGHT - height_moodimage_y
        x_party = 0.5 * SCREEN_WIDTH - width_moodimage_x
        y_party = 0.5 * SCREEN_HEIGHT
        x_chillen = 0.5 * SCREEN_WIDTH
        y_chillen = 0.5 * SCREEN_HEIGHT

        x = 20
        y = 10

        if y_party < SCREEN_HEIGHT:  # Grenze des Screens, an der die Stimmungs-Images stehen bleiben sollen
            x_happy -= x
            y_happy -= y

            x_sad += x
            y_sad -= y

            x_party -= x
            y_party += y

            x_chillen += x
            y_chillen += y


        else:
            x_happy = x_happy
            y_happy = y_happy

            x_sad = x_sad
            y_sad = y_sad

            x_party = x_party
            y_party = y_party

            x_chillen = x_chillen
            y_chillen = y_chillen

        screen.blit(happy, (x_happy, y_happy))
        screen.blit(sad, (x_sad, y_sad))
        screen.blit(party, (x_party, y_party))
        screen.blit(chillen, (x_chillen, y_chillen))

        pygame.display.update()
        clock.tick(FPS)                                          # frames pro Sekunde


# 4.) Endfenster
def endloop():
    endExit = False
    while not endExit:

        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endExit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit

        screen.fill(BLACK)
        pygame.display.update()

        if eye_input == 'happy':
            screen.blit(happy_background, (0, 0))
        elif eye_input == 'sad':
            screen.blit(sad_background, (0, 0))
        elif eye_input == 'party':
            screen.blit(party_background, (0, 0))
        elif eye_input == 'chillen':
            screen.blit(chillen_background, (0, 0))

        screen.blit(text_hf, (100, 100))
        screen.blit(hf_logo, (SCREEN_WIDTH*(7/8), 100))
        pygame.display.update()
        clock.tick(FPS)                                          # frames pro Sekunde


welcomeloop()

