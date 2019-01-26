import pygame  # Pygame-Modul importieren für GUI
from pygame.locals import *


###################### EINGABE-GUI ######################

def text_central(text, MYFONT):  # Funktion Textzentralisierung
    textsurface = MYFONT.render(text, True, WHITE)
    return textsurface, textsurface.get_rect()


def button_next(action):  # ABSTRAKTER GESTALTEN? zB (msg,x,y,w,h,ic,ac,action)
    # Mausposition & click
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Interaktivität & Farbe des Buttons in Abhängigkeit der Mausposition & Click
    if SCREEN_HEIGHT * (7 / 9) + BUTTON_HEIGHT > mouse[1] > SCREEN_HEIGHT * (7 / 9) and SCREEN_WIDTH * (
            6 / 8) + BUTTON_WIDTH > mouse[0] > SCREEN_WIDTH * (6 / 8):
        pygame.draw.rect(screen, HF_BLUE_LIGHT,
                         ((SCREEN_WIDTH * (6 / 8)), (SCREEN_HEIGHT * (7 / 9)), BUTTON_WIDTH, BUTTON_HEIGHT))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, HF_BLUE,
                         ((SCREEN_WIDTH * (6 / 8)), (SCREEN_HEIGHT * (7 / 9)), BUTTON_WIDTH, BUTTON_HEIGHT))

    # Text Button
    textsurf_next, textrect = text_central('WEITER', MYFONT)
    textrect.center = ((SCREEN_WIDTH * (6 / 8) + (BUTTON_WIDTH / 2)), (SCREEN_HEIGHT * (7 / 9) + (BUTTON_HEIGHT / 2)))
    screen.blit(textsurf_next, textrect)


def button_mood(action):  # ABSTRAKTER GESTALTEN? zB (msg,x,y,w,h,ic,ac,action)
    # Mausposition & click
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    click_output = 'None'
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # pos = pygame.mouse.get_pos()
            # if 960 > mouse[1] > 860 and 540 > mouse[0] > 440:
            click_output = 'happy'
            endloop(click_output)

    return click_output

    # Interaktivität & Farbe des Buttons in Abhängigkeit der Mausposition & Click
    # if 960 > mouse[1] > 860 and 540 > mouse[0] > 440:
    #   click_input = 'happy'
    # return click_input

    # elif SCREEN_HEIGHT * (7 / 9) + BUTTON_HEIGHT > mouse[1] > SCREEN_HEIGHT * (7 / 9) and SCREEN_WIDTH * (6 / 8) + BUTTON_WIDTH > mouse[0] > SCREEN_WIDTH * (6 / 8):
    #   click_input = 'sad'
    # elif SCREEN_HEIGHT * (7 / 9) + BUTTON_HEIGHT > mouse[1] > SCREEN_HEIGHT * (7 / 9) and SCREEN_WIDTH * (6 / 8) + BUTTON_WIDTH > mouse[0] > SCREEN_WIDTH * (6 / 8):
    #   click_input = 'party'
    # elif SCREEN_HEIGHT * (7 / 9) + BUTTON_HEIGHT > mouse[1] > SCREEN_HEIGHT * (7 / 9) and SCREEN_WIDTH * (6 / 8) + BUTTON_WIDTH > mouse[0] > SCREEN_WIDTH * (6 / 8):
    #   click_input = 'chillen'


def mousecursor():
    cursor = pygame.image.load('mouse.png').convert_alpha()  # mousecursor raindrop
    # cursor = pygame.image.load('mouse.jpg')                    # mousecursos happyfountain
    cursor = pygame.transform.scale(cursor, (40, 60))
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0),
                            (0, 0, 0, 0, 0, 0, 0, 0))  # transparenter Originalcursor
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
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit

        screen.fill(BLACK)

        # Rechteck um Willkommenstext
        pygame.draw.rect(screen, HF_BLUE, (250, 200, 1400, 350))
        pygame.draw.rect(screen, BLACK, (275, 225, 1350, 300))

        # Willkommenstext
        textsurf_welcome1, textrect1 = text_central(text_welcome1, MYFONT)
        textrect1.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (6 * 43)))  # 43 = Font-Size von MYFONT

        # textsurf_welcome2, textrect2 = text_central(text_welcome2, MYFONT_BIG)            # Option: happy(i) fountain Schrift statt Logo
        # textrect2.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (4*43)))

        textsurf_welcome3, textrect3 = text_central(text_welcome3, MYFONT)
        textrect3.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) - (2 * 43)))

        screen.blit(textsurf_welcome1, textrect1)
        # screen.blit(textsurf_welcome2, textrect2)                                         # Option: happy(i) fountain Schrift statt Logo
        screen.blit(textsurf_welcome3, textrect3)

        # Erklärung Stimmungsfenster

        textsurf_mood1, textrect1 = text_central(text_mood1, MYFONT)
        textrect1.center = ((SCREEN_WIDTH / 2), ((SCREEN_HEIGHT / 2) + (2 * 43)))

        screen.blit(textsurf_mood1, textrect1)

        button_next(moodloop)

        # screen.blit(hf_logo, (SCREEN_WIDTH*(1/15), SCREEN_HEIGHT - 250))                  # Option: Logo oben rechts
        screen.blit(hf_logo, ((SCREEN_WIDTH / 2 - 100), ((SCREEN_HEIGHT / 2) - 220)))  # Option: Logo statt Text
        mousecursor()
        pygame.display.update()
        clock.tick(FPS)  # frames pro Sekunde


# 2.) Stimmungfenster
def moodloop():
    moodexit = False
    while not moodexit:
        # Einstellungen zum Beenden der GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                moodexit = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                    pygame.quit()
                    raise SystemExit

        screen.fill(BLACK)

        # Stimmungen anzeigen (berechnet aus Screensize & Zentrierung)
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

        click_input = 'None'
        click_output = button_mood(endloop())

        mousecursor()
        pygame.display.update()
        clock.tick(FPS)  # frames pro Sekunde


# 4.) Endfenster
def endloop(input):
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

        if input == 'happy':
            screen.blit(happy_background, (0, 0))
        elif input == 'sad':
            screen.blit(sad_background, (0, 0))
        elif input == 'party':
            screen.blit(party_background, (0, 0))
        elif input == 'chillen':
            screen.blit(chillen_background, (0, 0))

        screen.blit(text_hf, (100, 100))
        screen.blit(hf_logo, (SCREEN_WIDTH * (7 / 8), 100))
        pygame.display.update()
        clock.tick(FPS)  # frames pro Sekunde


# Pygame initialisieren
pygame.init()
pygame.font.init()  # Textmodul initialisieren -> braucht man das?

# Bildschirmeinstellungen
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
CENTER = ((SCREEN_WIDTH % 2), (SCREEN_HEIGHT % 2))
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)  # pygame-Fenster fullscreen & = Bildschirmeinstellungen

# Farb- & Texteinstellungen
BLACK = (0, 0, 0)  # schwarz für Boxen & Texte
WHITE = (255, 255, 255)  # weiß für Boxen & Texte
HF_BLUE = (79, 154, 196)
HF_BLUE_LIGHT = (120, 200, 200)

MYFONT = pygame.font.SysFont('Comic Sans MS', 30)  # Schriftart & Größe wählen
MYFONT_BIG = pygame.font.SysFont('Comic Sans MS', 70)  # Schriftart & Größe wählen

z = MYFONT.get_height()  # MYFONT-Höhe = 43
print(z)

# Logo
hf_logo = pygame.image.load('happy(i) fountain.jpeg')
hf_logo = pygame.transform.scale(hf_logo, (180, 110))

# Funktion interaktive Klick-Buttons
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)

# 1.) Willkommensfenster
# Willkommenstext
text_welcome1 = "Herzlich willkommen!"
text_welcome2 = "hapPy(i) fountain:"
text_welcome3 = "Dein persönlicher Home-Entertainment Assistent."

# Erklärung Stimmungsfenster
text_mood1 = "Bitte wähle im nächsten Schritt deine Stimmung aus, indem du auf die passende Stimmung klickst."

# 2.) Fenster: Auswahl Stimmung
# Graphiken laden & verkleinern
width_moodimage_x = 150
height_moodimage_y = 150
size_moodimage = (width_moodimage_x, height_moodimage_y)

happy = pygame.image.load('happy.png')
happy = pygame.transform.scale(happy, size_moodimage)
sad = pygame.image.load('sad.png')
sad = pygame.transform.scale(sad, size_moodimage)
party = pygame.image.load('party.png')
party = pygame.transform.scale(party, size_moodimage)
chillen = pygame.image.load('chillen.png')
chillen = pygame.transform.scale(chillen, size_moodimage)

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

text_hf = MYFONT_BIG.render('Genieße deinen hapPy(i) fountain-Moment!', False, HF_BLUE)

# GUI anzeigen
clock = pygame.time.Clock()
FPS = 360

welcomeloop()



