"""
Pong game created using Python and Pygame.
Player vs AI, use UP and DOWN arrow keys to control paddle.
First to 5 points Wins.

AUTHOR: JIAXI KANG
"""


import pygame
import time
import random

pygame.init()

display_width = 900
display_height = 600
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

def draw_Rect(x, y, width, height, color):
# This function draws rectangles to be used as the buttons in this program
    pygame.draw.rect(gameDisplay, color, (x, y, width, height))

def draw_Ball(x, y, radius, color):
# This function draws the ball used in the pong game
    pygame.draw.circle(gameDisplay, color, (x, y), radius)
    
def draw_Borders():
# This function draws the borders of the pong game
    pygame.draw.line(gameDisplay, black, (display_width/2, 0), (display_width/2, display_height), 2)
    pygame.draw.lines(gameDisplay, black, True, [(0,0),(0, display_height - 2), (display_width - 2, display_height - 2), (display_width - 2, 0)], 2)

def display_Text(text, size, x_center, y_center, color):
# This function displays text onto the current frame
    shownText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, shownText, color)
    TextRect.center = (x_center, y_center)
    gameDisplay.blit(TextSurf, TextRect)
    
def text_objects(text, font, color):
# Helper function of the display_Text function
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def draw_Buttons(text, text_size, rect_x, rect_y, width, height, text_color, rect_color):
# This function draws both the button and text displayed on the button
    pygame.draw.rect(gameDisplay, rect_color, (rect_x, rect_y, width, height))
    display_Text(text, text_size, rect_x + width/2, rect_y + height/2, text_color)
    
def wall_Collision(ball_y):
# This function determines if the ball has collided with a wall
    if ball_y <= 10 or ball_y >= display_height -10:
        return True
    else:
        return False

def paddle_Collision(ball_x, ball_y, p_x, p_y):
# This function determines if the ball has collided with a paddle
    if p_y + 10 <= ball_y <= p_y + 90 and p_x <= ball_x <= p_x + 15:
        return "center hit"

    if p_y < ball_y < p_y + 10 and p_x <= ball_x <= p_x + 15 or \
       p_y + 90 < ball_y < p_y + 100 and p_x <= ball_x <= p_x + 15:
        return "corner hit"
    
def computer_Movement(ball_x, ball_y, p_x, p_y):
#This function dictates how the computer paddle will move in response to the ball
    if ball_x > display_width / 2:
        if ball_y > p_y + 50:
            return "move down"
        else:
            return "move up"
    else:
        return "don't move"

def goal_Score(ball_x):
# This function determines if a goal has been scored be either a player or computer
    if ball_x < 0:
        return "computer"
    if ball_x > display_width:
        return "player"

def game_start():
    gameDisplay.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    display_Text("Welcome to pong!", 30, display_width/2, 100, black)
    display_Text("Use up and down arrow keys play against a computer", 30, display_width/2, 140, black)
    display_Text("First to 5 points wins!", 30, display_width/2, 180, black)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if display_width/2 - 100 < mouse[0] < display_width/2 + 100 and display_height - 350 < mouse[1] < display_height - 250:
        draw_Buttons("BEGIN", 40, display_width/2 - 100, display_height - 350, 200, 100, white, green)
        if click[0]:
            return False
    else:
        draw_Buttons("BEGIN", 40, display_width/2 - 100, display_height - 350, 200, 100, white, blue)
    
    pygame.display.update()
    return True

def game_end(player):
    gameDisplay.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    display_Text(player + " has won!", 50, display_width/2, 150, black)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if display_width/2 - 100 < mouse[0] < display_width/2 + 100 and display_height - 350 < mouse[1] < display_height - 250:
        draw_Buttons("Restart", 40, display_width/2 - 100, display_height - 350, 200, 100, white, green)
        if click[0]:
            game_loop()
    else:
        draw_Buttons("Restart", 40, display_width/2 - 100, display_height - 350, 200, 100, white, blue)

    if display_width/2 - 100 < mouse[0] < display_width/2 + 100 and display_height - 200 < mouse[1] < display_height - 100:
        draw_Buttons("Quit", 40, display_width/2 - 100, display_height - 200, 200, 100, white, red)
        if click[0]:
            pygame.quit()
            quit()
    else:
        draw_Buttons("Quit", 40, display_width/2 - 100, display_height - 200, 200, 100, white, blue)

    pygame.display.update()
    
def game_loop():
    start = True
    end = False
    ball_x = display_width/2
    ball_y = display_height/2
    ball_size = 10

    ball_x_change = 0
    ball_y_change = 0
    
    while ball_x_change == 0 or ball_y_change == 0:
        rand_mult_x = 0
        rand_mult_y = 0
        while rand_mult_x == 0:
            rand_mult_x = random.randrange(-1, 1)
        while rand_mult_y == 0:
            rand_mult_y = random.randrange(-1, 1)
        ball_x_change = 4 * rand_mult_x
        ball_y_change = 4 * rand_mult_y

    paddle_speed = 5
    
    p1_x = 50
    p1_y = display_height/2 - 35
    p1_y_change = 0
    
    p2_x = display_width - 50
    p2_y = display_height/2 - 35
    p2_y_change = 0

    score_p = 0
    score_c = 0

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p1_y_change = - paddle_speed
                        
                if event.key == pygame.K_DOWN:
                    p1_y_change = paddle_speed
    
            if event.type == pygame.KEYUP:
                p1_y_change = 0
            
        while start == True:
            if not game_start():
                start = False
      
        gameDisplay.fill(white)

        draw_Borders()
        draw_Ball(ball_x, ball_y, ball_size, black)    
        draw_Rect(p1_x, p1_y, 15, 100, black)
        draw_Rect(p2_x, p2_y, 15, 100, black)
        
        ball_x += ball_x_change
        ball_y += ball_y_change


        p1_y += p1_y_change
        p2_y += p2_y_change
        
        if not (0 < p1_y < display_height - 100):
            p1_y_change = 0
        
        if wall_Collision(ball_y) == True:
            ball_y_change *= -1

        if paddle_Collision(ball_x, ball_y, p1_x, p1_y) == "corner hit":
            ball_x += 5
            ball_x_change = random.randrange(5, 8)

        elif paddle_Collision(ball_x, ball_y, p1_x, p1_y) == "center hit":
            ball_x += 5
            ball_x_change *= -1

        if paddle_Collision(ball_x, ball_y, p2_x, p2_y) == "corner hit":
            ball_x -= 5
            ball_x_change = random.randrange(-8, -5)

        elif paddle_Collision(ball_x, ball_y, p2_x, p2_y) == "center hit":
            ball_x -= 5
            ball_x_change *= -1

        if computer_Movement(ball_x, ball_y, p2_x, p2_y) == "move down":
            if p2_y + 100 < display_height:
                p2_y_change = paddle_speed
            else:
                p2_y_change = 0

        elif computer_Movement(ball_x, ball_y, p2_x, p2_y) == "move up":
            if p2_y > 0:
                p2_y_change = -paddle_speed
            else:
                p2_y_change = 0
        else:
            p2_y_change = 0

        if goal_Score(ball_x) == "computer":
            score_c += 1
            ball_x = display_width / 2
            ball_y = display_height / 2
            ball_x_change = random.randrange(3, 5)
            time.sleep(1)

        if goal_Score(ball_x) == "player":
            score_p += 1
            ball_x = display_width / 2
            ball_y = display_height / 2
            ball_x_change = random.randrange(-5, -3)
            time.sleep(1)

        display_Text("Player: " + str(score_p), 20, display_width/2 - 70, 20, blue)
        display_Text("Computer: " + str(score_c), 20, display_width/2 + 80, 20, red)

        if score_c == 5:
            while True:
                game_end("Computer")

        if score_p == 5:
            while True:
                game_end("Player")
                
                
                    
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    game_loop()
