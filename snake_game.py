import pygame
import random
import sys
from dalle_integration import generate_background
import os
from hello import hello

# Initialize the mixer
pygame.mixer.init()

# Load the sound effect
eat_sound = pygame.mixer.Sound("eat_sound.wav")

# Initialize Pygame
pygame.init()

# Define colors used in the game
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
light_blue = (173, 216, 230)  # Light blue for the background

# Game settings
width = 600
height = 400
snake_block = 10
snake_speed = 15

# Ensure the flags directory exists
os.makedirs("flags", exist_ok=True)

# Create the display window for the game
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Create a clock to control the game's frame rate
clock = pygame.time.Clock()

# Define font styles for displaying text
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def draw_snake(snake_list):
    for i, segment in enumerate(snake_list):
        color = (0, 255 - i * 5, 0)  # Gradient effect for the snake
        pygame.draw.rect(display, color, [segment[0], segment[1], snake_block, snake_block])

def ask_country(background):
    width, height = 600, 400
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Select Country')
    font = pygame.font.Font(None, 30)
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (200, 200, 200)

    input_text = ""
    suggestions = []
    dropdown_open = False

    def draw_input_box():
        input_rect = pygame.Rect(width / 4, height / 3, width / 2, 30)
        pygame.draw.rect(display, white, input_rect, 2)  # Change input box color to white
        text_surface = font.render(input_text, True, black)  # Change text color to black
        display.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        if dropdown_open and suggestions:
            for i, suggestion in enumerate(suggestions):
                item_rect = pygame.Rect(input_rect.x, input_rect.y + 30 * (i + 1), input_rect.width, 30)
                pygame.draw.rect(display, grey, item_rect)
                item_surface = font.render(suggestion, True, black)
                display.blit(item_surface, (item_rect.x + 5, item_rect.y + 5))

    # Main loop
    while True:
        display.fill(light_blue)  # Change background color to light blue
        draw_input_box()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text  # Return the input text directly
                elif event.key == pygame.K_ESCAPE:  # Allow exiting the input with ESC
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

                # Update suggestions based on input
                suggestions = []  # No suggestions needed
                dropdown_open = True

def select_flag(country):
    # Select the appropriate flag drawing function based on the country
    display.fill(white)  # Default background if no specific flag is available

def message(msg, color):
    # Display a message on the screen
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])

def gameLoop():
    # Main game loop
    game_over = False
    game_close = False

    # Initial position of the snake
    x1 = width / 2
    y1 = height / 2

    # Change in position for the snake
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Generate initial food position
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Select the country and generate a background using DALL-E
    country = ask_country(pygame.Surface((width, height)))
    background_path = os.path.join("flags", "background.png")
    generate_background(f"A minimalist background with the flag of {country}", background_path)
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (width, height))  # Scale the background to fit the display
    select_flag(country)

    while not game_over:
        display.blit(background, (0, 0))  # Draw the scaled background
        print(f"Snake position: ({x1}, {y1}), Food position: ({foodx}, {foody})")

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

        # Check for collision with the boundaries
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        # Update the snake's position
        x1 += x1_change
        y1 += y1_change

        # Update the snake's body
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check for collision with itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_List)  # Draw the snake

        pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])  # Draw the food
        pygame.display.update()

        # Check if the snake has eaten the food
        if x1 == foodx and y1 == foody:
            print("Food eaten!")
            eat_sound.play()  # Play the sound effect
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1  # Increase the length of the snake

        clock.tick(snake_speed)  # Control the frame rate

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    gameLoop()  # Start the game loop
