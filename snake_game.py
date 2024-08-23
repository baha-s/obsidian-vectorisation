import pygame
import time
import random
import sys

# Initialize Pygame
pygame.init()

def ask_country():
    print("Where are you from? (Enter the name of your country)")
    return input().strip().lower()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (230, 0, 0)  # Kyrgyzstan flag red
green = (0, 255, 0)
blue = (0, 0, 102)
sky_blue = (0, 191, 255)  # Sky blue for the background
gold = (255, 215, 0)  # Gold for the sun
skin_color = (255, 224, 189)  # Skin tone for explosion
nipple_color = (255, 192, 203)  # Light pink for nipples
kyrgyzstan_yellow = (255, 210, 0)  # Kyrgyzstan flag yellow

# Game settings
width = 600
height = 400
snake_block = 10
snake_speed = 15

# Create the display
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Clock
clock = pygame.time.Clock()

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load sound
eat_sound = pygame.mixer.Sound("eat_sound.wav")  # Ensure you have this sound file in the same directory

from kyrgyzstan_flag import draw_kyrgyzstan_flag

def draw_kyrgyzstan_flag_wrapper():
    draw_kyrgyzstan_flag(display, width, height)

# Move this dictionary after all flag drawing functions are defined
country_flags = {
    "kyrgyzstan": draw_kyrgyzstan_flag_wrapper,
    # Add more countries and their corresponding flag drawing functions here
}

def select_flag(country):
    return country_flags.get(country, draw_kyrgyzstan_flag)  # Default to Kyrgyzstan flag if country not found

# Game settings
width = 600
height = 400
snake_block = 10
snake_speed = 15

# Create the display
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Clock
clock = pygame.time.Clock()

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load sound
eat_sound = pygame.mixer.Sound("eat_sound.wav")  # Ensure you have this sound file in the same directory

from kyrgyzstan_flag import draw_kyrgyzstan_flag

def draw_kyrgyzstan_flag_wrapper():
    draw_kyrgyzstan_flag(display, width, height)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])

def your_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    display.blit(value, [0, 0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])

def explosion_effect(x, y):
    for radius in range(10, 50, 5):  # Create an expanding explosion
        # Draw two circles to resemble a pair of boobs
        pygame.draw.circle(display, skin_color, (int(x - radius // 2), int(y)), radius)  # Left circle
        pygame.draw.circle(display, skin_color, (int(x + radius // 2), int(y)), radius)  # Right circle
        # Draw nipples
        pygame.draw.circle(display, nipple_color, (int(x - radius // 2), int(y)), radius // 5)  # Left nipple
        pygame.draw.circle(display, nipple_color, (int(x + radius // 2), int(y)), radius // 5)  # Right nipple
        pygame.display.update()
        time.sleep(0.05)  # Delay for effect
        draw_kyrgyzstan_flag()  # Redraw the flag to clear the explosion effect

def gameLoop():
    country = ask_country()
    draw_flag = select_flag(country)
    
    print("Starting game loop...")  # Debugging statement
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        print("Game loop iteration...")  # Debugging statement

        while game_close == True:
            display.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        draw_flag()  # Draw the selected flag as the background
        pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1
            eat_sound.play()  # Play sound when food is eaten
            
            # Start explosion effect in a separate thread
            explosion_effect(foodx, foody)  # Trigger explosion effect

        clock.tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()
