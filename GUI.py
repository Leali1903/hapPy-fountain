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
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)      # pygame-Fenster fullscreen & auf Bildschirmeinstellungen gesetzt

# Farb- & Texteinstellungen
BLACK = (0, 0, 0)                                              # schwarz für Boxen & Texte
WHITE = (255, 255, 255)                                        # weiß für Boxen & Texte
HF_BLUE = (79, 154, 196)
MYFONT = pygame.font.SysFont('Comic Sans MS', 30)              # Schriftart & Größe wählen
MYFONT_BIG = pygame.font.SysFont('Comic Sans MS', 70)              # Schriftart & Größe wählen


# 1.) Willkommensfenster
# # Text
posX = SCREEN_HEIGHT*1/8
posY = SCREEN_HEIGHT*1/8
position = (posX, posY)

text_1 = ["Herzlich willkommen!", "hapPy(i) fountain: Dein persönlicher Home-Entertainment Assistent", "der über deine Augenbewegungen gesteuert wird.", "Bitte schaue auf den Start-Button."]

# label_1 =[]
# for line in text_1:
#      label.append(MYFONT.render(text_1, False, text_colour))
# return label, position
# for line in range(len(label)):
#     screen.blit(label(line), (position[0], (position[1]+(line*fontsize)+(15*line)), (position[1]+(line*fontsize)+(15*line))))

# Start-Button: Text, Textfarbe, Schriftgröße, Schriftart, Rechteck, Rechtecksfarbe, Verankerung
startbutton_text = "START"


# 2.) Erklärung Stimmungsfenster
# # Text
text_mood = "Bitte wähle im nächsten Schritt deine momentane Stimmung aus, indem du auf die passende Stimmung schaust. Das rechteck wird sich auf dem Bildschirm bewegen. Bitte verfolge es mit deinem Blick und schaue es die ganze Zeit an."

#
#
# # 3.) Fenster: Auswahl Stimmung
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

x_happy = 0.5*SCREEN_WIDTH - width_moodimage_x                    # Startpositionen (berechnet aus Screensize & Zentrierung)
y_happy = 0.5*SCREEN_HEIGHT - height_moodimage_y
x_sad = 0.5*SCREEN_WIDTH
y_sad = 0.5*SCREEN_HEIGHT - height_moodimage_y
x_party = 0.5*SCREEN_WIDTH - width_moodimage_x
y_party = 0.5*SCREEN_HEIGHT
x_chillen = 0.5*SCREEN_WIDTH
y_chillen = 0.5*SCREEN_HEIGHT

x = 20                                                           # für die Bewegung der Images
y = 10

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


# 5.) Weiter-Button
#def next_button():
 #   = "WEITER"

# 6) Logo
hf_logo = pygame.image.load('happy(i) fountain.jpeg')
hf_logo = pygame.transform.scale(hf_logo, (140, 100))



# GUI anzeigen
clock = pygame.time.Clock()
FPS = 360

guiExit = False
while not guiExit:

    # Einstellungen zum Beenden der GUI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            guiExit = True
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_ESCAPE):  # nach Klick auf Escape oder q
                pygame.quit()
                raise SystemExit

    # 1.) Willkommenstext
    screen.fill(BLACK)

    # #textsurface_1 = myfont.render(text_1, False, text_colour)
    # #screen.blit(textsurface_1, (500, 500))
    # for line in text_1:
    #     label_1.append(myfont.render(text_1, False, text_colour))
    # # return label, position
    # for line in range(len(label_1)):
    #     screen.blit(label_1(line), (
    #     position[0], (position[1] + (line * fontsize) + (15 * line)), (position[1] + (line * fontsize) + (15 * line))))
    #
    pygame.draw.rect(screen, WHITE, ((SCREEN_WIDTH*(6/8)), (SCREEN_HEIGHT*(7/9)), 200, 100))

    screen.blit(hf_logo, (SCREEN_WIDTH*(7/8), 100))
    pygame.display.update()

    # 2.) Erklärung Stimmungsfenster
    screen.fill(BLACK)

    screen.blit(hf_logo, (SCREEN_WIDTH * (7 / 8), 100))
    pygame.display.update()

    # 3.) Stimmungfenster
    ## Stimmungen anzeigen


    screen.blit(happy, (x_happy, y_happy))
    screen.blit(sad, (x_sad, y_sad))
    screen.blit(party, (x_party, y_party))
    screen.blit(chillen, (x_chillen, y_chillen))

    pygame.display.update()

    ## Stimmungen bewegen

    x_happy = x_happy - x
    y_happy = y_happy - y
    x_sad = x_sad + x
    y_sad = y_sad - y
    x_party = x_party - x
    y_party = y_party + y
    x_chillen = x_chillen + x
    y_chillen = y_chillen + y

    screen.blit(happy, (x_happy, y_happy))
    screen.blit(sad, (x_sad, y_sad))
    screen.blit(party, (x_party, y_party))
    screen.blit(chillen, (x_chillen, y_chillen))

    pygame.display.update()

    if y_party > (SCREEN_HEIGHT-200):                            # Grenze des Screens, an der die Stimmungs-Images stehen bleiben sollen
        # guiExit = True                                         # TUN SIE ABER NICHT?!?!?!
        screen.blit(happy, (x_happy, y_happy))
        screen.blit(sad, (x_sad, y_sad))
        screen.blit(party, (x_party, y_party))
        screen.blit(chillen, (x_chillen, y_chillen))

    pygame.display.update()

    # 4.) Endfenster
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

