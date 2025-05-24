import pygame
import time
from snake import Snake
from food import Food
import csv
from datetime import datetime

# kleuren
kleur_achtergrond = (0, 0, 0)
kleur_tekst = (0, 255, 0)
kleur_score = (144, 238, 144)

# schermgrootte
breedte = 800
hoogte = 600
veld_grootte = 20

# Snelheid van het spel
spel_snelheid = 10

# Initialiseren van de pygame-module
pygame.init()

# Creëer een venster met opgegeven breedte en hoogte
venster = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption('Snake')


def sla_op_in_csv(score, tijdstip):
    with open('highscores.csv', mode='a',
              newline='') as file:  # dit opent de file, mode = 'a' staat voor append (toevoegen)
        writer = csv.writer(file)  # maak een object dat we kunnen gebruiken om iets in de file te schrijven
        writer.writerow([score, tijdstip])  # voeg een rij toe aan de file met de waardes

def haal_hoogste_score_op():
    try:  # zorgt er voor dat als het bestand niet bestaat, we niet crashen
        with open('highscores.csv', mode='r') as file:  # open het bestand en sla het op in de file variabele
            reader = csv.reader(file)  # maak er een csv-lezer van
            scores = list(reader)  # vorm die lezer om naar een 2-dimensionale lijst (= een lijst met lijsten)
            hoogste_score = max(
                int(row[0]) for row in scores)  # Zoek het maximum van alle tweede waardes (de leeftijden)
            return hoogste_score

    except FileNotFoundError:  # als de file niet gevonden wordt gewoon rustig blijven ;)
        return 0

# Functie om de score op het scherm te tonenµ

def toon_score(score, venster):
    font = pygame.font.Font(None, 36)
    scoretekst = font.render(f"Score: {score}", True, kleur_tekst)
    venster.blit(scoretekst, (10, 10))

# Start de hoofdloop van het spel
def game_lus():
    global kleur_score
    food = Food(breedte, hoogte)
    snake = Snake(breedte//2, hoogte//2)
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.x_verandering == 0:
                    snake.x_verandering = -veld_grootte
                    snake.y_verandering = 0
                elif event.key == pygame.K_RIGHT and snake.x_verandering == 0:
                    snake.x_verandering = veld_grootte
                    snake.y_verandering = 0
                elif event.key == pygame.K_UP and snake.y_verandering == 0:
                    snake.y_verandering = -veld_grootte
                    snake.x_verandering = 0
                elif event.key == pygame.K_DOWN and snake.y_verandering == 0:
                    snake.y_verandering = veld_grootte
                    snake.x_verandering = 0
                elif event.key == pygame.K_p:
                    gepauzeerd = True
                    pauze_font = pygame.font.Font(None, 36)
                    pauze_tekst = pauze_font.render("Pauze (Druk op P om door te gaan)", True, kleur_tekst)
                    venster.blit(pauze_tekst, (breedte // 2 - pauze_tekst.get_width() // 2, hoogte //2))
                    pygame.display.update()
                    while gepauzeerd:
                        for pauze_event in pygame.event.get():
                            if pauze_event.type == pygame.KEYDOWN and pauze_event.key == pygame.K_p:
                                gepauzeerd = False
                elif event.key == pygame.K_s:
                    score =+ 2000


        snake.beweeg()
        if snake.is_buiten_veld(breedte, hoogte) or snake.raakt_zichzelf():
            game_over = True

        venster.fill(kleur_achtergrond)  # Vul het scherm met een zwarte achtergrond
        food.teken(venster)
        snake.teken(venster, kleur_score)
        toon_score(score, venster)

        if snake.x == food.x and snake.y == food.y:
            food.plaats_voedsel()
            snake.lengte_slang += 1
            score += 10
            if score == 10:
                kleur_score = (240, 128, 0)

        pygame.display.update()
        time.sleep(1 / spel_snelheid)

    print(f"Jouw score is {score}")
    sla_op_in_csv(score, datetime.now())
    hoogste_score = haal_hoogste_score_op()
    print(f"De hoogste score is {hoogste_score}")


# Start de hoofdloop van het spel
game_lus()
