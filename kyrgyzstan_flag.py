import pygame

def draw_kyrgyzstan_flag(display, width, height):
    # Colors
    red = (230, 0, 0)  # Kyrgyzstan flag red
    kyrgyzstan_yellow = (255, 210, 0)  # Kyrgyzstan flag yellow

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
