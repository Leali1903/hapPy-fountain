import pygame                                                  # Pygame-Modul importieren für GUI
from pygame.locals import *

# Pygame initialisieren
pygame.init()
pygame.font.init()                                             # Textmodul initialisieren -> braucht man das?


# Bildschirmeinstellungen
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
CENTER = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)      # pygame-Fenster fullscreen & = Bildschirmeinstellungen

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

# Logo
hf_logo = pygame.image.load('happy(i) fountain.jpeg')
hf_logo = pygame.transform.scale(hf_logo, (180, 110))


# 1.) Willkommensfenster
# Willkommenstext
text_welcome1 = "Herzlich willkommen!"
text_welcome2 = "hapPy(i) fountain:"
text_welcome3 = "Dein persönlicher Home-Entertainment Assistent, der über deine Augen gesteuert wird."

# Erklärung Stimmungsfenster
text_mood1 = "Bitte wähle im nächsten Schritt deine Stimmung aus, indem du auf die passende Stimmung schaust."
text_mood2 = "Das Symbol wird sich auf dem Bildschirm bewegen."
text_mood3 = "Bitte verfolge es mit deinem Blick und schaue es die ganze Zeit an."

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


# frames pro Sekunde
clock = pygame.time.Clock()
FPS = 360

# Stimmungen bewegen (innerhalb Screens) ALS SIE NOCH OHNE FUNCTION WAREN HAT ES FUNLKTIONIERT!!!
moodmoveexit = False
while not moodmoveexit:

        # Einstellungen zum Beenden der GUI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            moodmoveexit = True
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                pygame.quit()
                raise SystemExit

    screen.fill(BLACK)

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

    x = 20
    y = 10

    if y_party < SCREEN_HEIGHT:             # Grenze des Screens, an der die Stimmungs-Images stehen bleiben sollen
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





