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

# Define the colors for the pride flag
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

class DropDown:

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    self.main = self.options[self.active_option]
                    return self.main
        return None

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

    # Dropdown for selecting the country
    dropdown = DropDown(
        [blue, green], [white, yellow],
        width // 4, height // 3, width // 2, 40,
        pygame.font.SysFont(None, 30), 
        "Select Country", ["Kyrgyzstan", "USA", "Canada", "Germany", "France"]
    )
    
    selected_country = None
    while selected_country is None:
        display.fill(white)
        event_list = pygame.event.get()
        selected_country = dropdown.update(event_list)
        dropdown.draw(display)
        pygame.display.update()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Get the corresponding flag drawing function
    draw_flag = select_flag(selected_country)

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
