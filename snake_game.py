import pygame
import random
from kyrgyzstan_flag import draw_kyrgyzstan_flag
import sys

# Initialize Pygame
pygame.init()

# Define colors used in the game
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Define the colors for the gay pride flag
pride_colors = [
    (255, 0, 0),    # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130)    # Purple
]

# Game settings
width = 600
height = 400
snake_block = 10
snake_speed = 15

# Create the display window for the game
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Create a clock to control the game's frame rate
clock = pygame.time.Clock()

# Define font styles for displaying text
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def draw_dropdown(countries, selected_country, dropdown_open):
    # Draw the dropdown menu for country selection
    dropdown_rect = pygame.Rect(width / 4, height / 3, width / 2, 30)
    pygame.draw.rect(display, black, dropdown_rect)
    font = pygame.font.SysFont("bahnschrift", 20)
    text = font.render(selected_country, True, white)
    display.blit(text, (dropdown_rect.x + 5, dropdown_rect.y + 5))

    # If the dropdown is open, draw the list of countries
    if dropdown_open:
        for i, country in enumerate(countries):
            item_rect = pygame.Rect(width / 4, height / 3 + 30 * (i + 1), width / 2, 30)
            if country == selected_country:
                # Highlight selected country with pride colors
                for j, color in enumerate(pride_colors):
                    pygame.draw.rect(display, color, item_rect.move(0, 0), item_rect.width, item_rect.height // len(pride_colors))
            else:
                pygame.draw.rect(display, blue, item_rect)
            item_text = font.render(country, True, white)
            display.blit(item_text, (item_rect.x + 5, item_rect.y + 5))

def ask_country():
    # Prompt the user to select a country from the dropdown
    countries = ["Kyrgyzstan", "USA", "Canada", "Germany", "France"]
    selected_country = countries[0]
    dropdown_open = False

    while True:
        display.fill(white)
        draw_dropdown(countries, selected_country, dropdown_open)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    dropdown_open = not dropdown_open
                if event.key == pygame.K_RETURN and not dropdown_open:
                    return selected_country
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if dropdown_open:
                    for i, country in enumerate(countries):
                        item_rect = pygame.Rect(width / 4, height / 3 + 30 * (i + 1), width / 2, 30)
                        if item_rect.collidepoint(mouse_pos):
                            selected_country = country
                            dropdown_open = False
                            break
                else:
                    dropdown_open = True  # Open dropdown if clicked outside

def draw_kyrgyzstan_flag_wrapper():
    # Wrapper function to draw the Kyrgyzstan flag
    draw_kyrgyzstan_flag(display, width, height)

# Mapping of country names to their flag drawing functions
country_flags = {
    "kyrgyzstan": draw_kyrgyzstan_flag_wrapper,
}

def select_flag(country):
    # Select the appropriate flag drawing function based on the country
    return country_flags.get(country.lower(), draw_kyrgyzstan_flag_wrapper)

def our_snake(snake_block, snake_list):
    # Draw the snake on the display
    for x in snake_list:
        pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])

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

    # Ask user to select a country and get the corresponding flag drawing function
    country = ask_country()
    draw_flag = select_flag(country)

    frame_count = 0

    while not game_over:
        frame_count += 1
        print(f"Frame: {frame_count}, Snake position: ({x1}, {y1}), Food position: ({foodx}, {foody})")

        while game_close:
            display.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
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

        # Check for collision with the boundaries
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        # Update the snake's position
        x1 += x1_change
        y1 += y1_change
        display.fill(white)
        draw_flag()  # Draw the selected country's flag
        pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])  # Draw the food
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check for collision with itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)  # Draw the snake

        pygame.display.update()

        # Check if the snake has eaten the food
        if x1 == foodx and y1 == foody:
            print("Food eaten!")
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1  # Increase the length of the snake

        clock.tick(snake_speed)  # Control the frame rate

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    gameLoop()  # Start the game loop
