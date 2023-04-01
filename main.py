import pygame
import os
from pygame import mixer

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 860, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')
pygame.event.pump()

FPS = 60
user = 1


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

CC_SIZE = 140


COORDINATE_MAPPING_RECT = {
    1:pygame.Rect(215, 155, CC_SIZE, CC_SIZE),
    2:pygame.Rect(355, 155, CC_SIZE, CC_SIZE),
    3:pygame.Rect(495, 155, CC_SIZE, CC_SIZE),
    4:pygame.Rect(215, 295, CC_SIZE, CC_SIZE),
    5:pygame.Rect(355, 295, CC_SIZE, CC_SIZE),
    6:pygame.Rect(495, 295, CC_SIZE, CC_SIZE),
    7:pygame.Rect(215, 435, CC_SIZE, CC_SIZE),
    8:pygame.Rect(355, 435, CC_SIZE, CC_SIZE),
    9:pygame.Rect(495, 435, CC_SIZE, CC_SIZE),
}

COORDS = {
    0:(-69, -420),
    1:(215, 155),
    2:(355, 155),
    3:(495, 155),
    4:(215, 295),
    5:(355, 295),
    6:(495, 295),
    7:(215, 435),
    8:(355, 435),
    9:(495, 435),
}

CIRCLE_IMG = pygame.image.load(os.path.join('Assets', 'Circle.png'))
CROSS_IMG = pygame.image.load(os.path.join('Assets', 'Cross.png'))

CIRCLE = pygame.transform.scale(CIRCLE_IMG, (150, 150))
CROSS = pygame.transform.scale(CROSS_IMG, (150, 150))

BG_IMG = pygame.image.load(os.path.join("Assets", 'bg.png'))
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))

BOX_IMG = pygame.image.load(os.path.join("Assets", 'box.png'))
BOX =  pygame.transform.scale(BOX_IMG, (480, 480))

LOGO_IMG = pygame.image.load(os.path.join("Assets", 'tictactoe.png'))
LOGO = pygame.transform.scale(LOGO_IMG, (274, 101))

PLAYERS_TURN_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 96)

PLAYER1_WIN = pygame.USEREVENT + 1
PLAYER2_WIN = pygame.USEREVENT + 2

PLAYER1SOUND = pygame.mixer.Sound(os.path.join("Assets", 'player1.wav'))
PLAYER2SOUND = pygame.mixer.Sound(os.path.join("Assets", 'player2.wav'))
GAMEOVERSOUND = pygame.mixer.Sound(os.path.join("Assets", 'game-over.wav'))


def draw_window(user, clicked_number, blitdic):
    WIN.blit(BG_IMG, (0, 0))                                       
    WIN.blit(BOX,(WIDTH//2 - 480/2, HEIGHT//2 - 480/2 + 50))    
    WIN.blit(LOGO, (WIDTH//2 - 274/2, 20))
    
    if user == 1:
        draw_player1_turn = PLAYERS_TURN_FONT.render("PLAYER 1", 1, WHITE)
        WIN.blit(draw_player1_turn, (40-20, HEIGHT//2))

    elif user == 2:
        draw_player2_turn = PLAYERS_TURN_FONT.render("PLAYER 2", 1, WHITE)
        WIN.blit(draw_player2_turn, (690-20, HEIGHT//2))
    
    for i in range(len(row)):
        if row[i] == 'X':
            blitdic[i] = CROSS

        if row[i] == 'O':
            blitdic[i] = CIRCLE

    for blocks in blitdic:
        WIN.blit(blitdic[blocks], COORDS[blocks])
        
    pygame.display.update()


def check(winner_text):
    allalpha = all(isinstance(item, str) for item in row)
    if allalpha:
        winner_text = 'Game Tied!'
        return winner_text
    
    if row[1] == row[2] == row[3] == 'O' or row[4] == row[5] == row[6] == 'O' or row[7] == row[8] == row[9] == 'O' or row[1] == row[4] == row[7] == 'O' or row[2] == row[5] == row[8] == 'O' or row[3] == row[6] == row[9] == 'O' or row[1] == row[5] == row[9] == 'O' or row[3] == row[5] == row[7] == 'O':
        winner_text = 'Player 2 Won!'
        return winner_text
        
    if row[1] == row[2] == row[3] == 'X' or row[4] == row[5] == row[6] == 'X' or row[7] == row[8] == row[9] == 'X' or row[1] == row[4] == row[7] == 'X' or row[2] == row[5] == row[8] == 'X' or row[3] == row[6] == row[9] == 'X' or row[1] == row[5] == row[9] == 'X' or row[3] == row[5] == row[7] == 'X':
        winner_text = 'Player 1 Won!'
        return winner_text
    
def main(user):
    clock = pygame.time.Clock()
    clicked_number = 0

    global run
    run = True
    winner_text = ""

    global row
    row = ['ay', 1, 2, 3,
              4, 5, 6,
              7, 8, 9]

    blitdic = {0:CROSS}

    pygame.display.update()

    while run:
        clock.tick(FPS)
        click_pos = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:    
                    click_pos = pygame.mouse.get_pos()

            for blocks in COORDINATE_MAPPING_RECT:
                clickx, clicky = click_pos
                click_rect = pygame.Rect(clickx, clicky, 1, 1)
                if COORDINATE_MAPPING_RECT[blocks].colliderect(click_rect):
                    clicked_number = blocks

                    if user == 1 and clicked_number in row:
                        row[clicked_number] = 'X'
                        user = 2
                        pygame.mixer.Sound.play(PLAYER1SOUND)
                        pygame.mixer.music.stop()

                    elif user == 2 and clicked_number in row:
                        row[clicked_number] = 'O'                     
                        user = 1
                        pygame.mixer.Sound.play(PLAYER2SOUND)
                        pygame.mixer.music.stop()

                win = check(winner_text)

        draw_window(user, clicked_number, blitdic)        

        if win != None:
            pygame.mixer.Sound.play(GAMEOVERSOUND)
            pygame.mixer.music.stop()
            draw_window(user, clicked_number, blitdic)
            

        if win == "Game Tied!":
            draw_win = WINNER_FONT.render("Game Tied", 1, RED)
            WIN.blit(draw_win, (WIDTH//2 - 240, HEIGHT//2 - 20))
            pygame.display.update()
            pygame.time.delay(2000)
            main(user)

        if win == "Player 1 Won!":
            draw_win = WINNER_FONT.render("Player 1 Won!", 1, RED)
            WIN.blit(draw_win, (WIDTH//2 - 300, HEIGHT//2- 20))
            pygame.display.update()
            pygame.time.delay(2000)
            main(user)
            

        if win == "Player 2 Won!":
            draw_win = WINNER_FONT.render("Player 2 Won!", 1, RED)
            WIN.blit(draw_win, (WIDTH//2 - 300, HEIGHT//2 - 20))
            pygame.display.update()
            pygame.time.delay(2000)
            main(user)
        
if __name__ == '__main__':
    main(user)