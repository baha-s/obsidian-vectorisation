import pygame
import time
import random

# Initialize Pygame
pygame.init()

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

def draw_kyrgyzstan_flag():
    # Set flag dimensions (3:5 ratio)
    flag_width = width
    flag_height = int(flag_width * 3 / 5)
    offset_y = (height - flag_height) // 2

    # Draw the red background
    display.fill(red)

    # Draw the yellow sun
    center_x = width // 2
    center_y = height // 2
    sun_radius = min(width, height) // 4
    pygame.draw.circle(display, kyrgyzstan_yellow, (center_x, center_y), sun_radius)

    # Draw sun rays
    for i in range(40):
        angle = i * (360 / 40)
        start_x = center_x + int(sun_radius * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).x)
        start_y = center_y + int(sun_radius * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).y)
        end_x = center_x + int(sun_radius * 1.15 * pygame.math.Vector2(1, 0).rotate(angle).x)
        end_y = center_y + int(sun_radius * 1.15 * pygame.math.Vector2(1, 0).rotate(angle).y)
        pygame.draw.line(display, kyrgyzstan_yellow, (start_x, start_y), (end_x, end_y), 3)

    # Draw the tunduk (yurt ring) symbol
    tunduk_radius = sun_radius * 0.4
    pygame.draw.circle(display, red, (center_x, center_y), tunduk_radius)
    for i in range(4):
        angle = i * 90 + 45
        start_x = center_x + int(tunduk_radius * pygame.math.Vector2(1, 0).rotate(angle).x)
        start_y = center_y + int(tunduk_radius * pygame.math.Vector2(1, 0).rotate(angle).y)
        end_x = center_x + int(tunduk_radius * 1.4 * pygame.math.Vector2(1, 0).rotate(angle).x)
        end_y = center_y + int(tunduk_radius * 1.4 * pygame.math.Vector2(1, 0).rotate(angle).y)
        pygame.draw.line(display, red, (start_x, start_y), (end_x, end_y), 5)

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
        draw_kyrgyzstan_flag()  # Draw the Kyrgyzstan flag as the background
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

gameLoop()
