import pygame  
import sys  
import random  
import math  
  
# Initialize Pygame  
pygame.init()  
  
# Set up the display  
screen = pygame.display.set_mode((1600, 760))  
pygame.display.set_caption('Clicker Game')  
  
# Load the button image  
button_image = pygame.image.load('button_image.png').convert_alpha()  # Ensure the file exists in the directory  
original_button_rect = button_image.get_rect(center=(800, 380))  
  
# Load Fredoka font  
fredoka_font_path = 'FredokaOne-Regular.ttf'  # Ensure this file is in the same directory  
font = pygame.font.Font(fredoka_font_path, 74)  
popup_font = pygame.font.Font(fredoka_font_path, 150)  
  
money = 0  # Starting money  
hovering = False  
tween_time = 0  
tween_duration = 15  # Faster animation by reducing duration  
click_multiplier = 1  
popup_visible = False  
popup_time = 0  
particles = []  
  
# Auto-clicker settings  
auto_click_rate = 0  # Start with no auto-clicks  
auto_click_timer = 0  
auto_click_cost = 100  # Cost to purchase or upgrade the auto-clicker  
  
multipliers = {  
    'Dc': 1e33, 'No': 1e30, 'Oc': 1e27, 'Sp': 1e24, 'Sx': 1e21,  
    'Qi': 1e18, 'Qa': 1e15, 'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3  
}  
  
def format_large_number(number):  
    """ Format large numbers with appropriate suffix. """  
    for suffix, size in multipliers.items():  
        if number >= size:  
            return f"{number/size:.2f}{suffix}"  
    return str(number)  
  
def quart_ease_out(t):  
    return 1 - (1 - t) ** 4  
  
# Main game loop  
clock = pygame.time.Clock()  
running = True  
while running:  
    dt = clock.tick(60) / 1000  # Delta time in seconds  
    screen.fill((0, 0, 0))  # Fill the screen with black  
  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        elif event.type == pygame.MOUSEBUTTONDOWN:  
            if original_button_rect.collidepoint(event.pos):  
                if random.random() <= 0.1:  # 10% chance to double the click value  
                    click_multiplier *= 2  
                    popup_visible = True  
                    popup_time = 60  # Display popup for 60 frames  
                    for _ in range(20):  # Create 20 particles  
                        particles.append([event.pos[0], event.pos[1], random.uniform(-2, 2), random.uniform(-2, 2), 100])  
                money += click_multiplier  
  
            # Check if user wants to buy or upgrade the auto-clicker  
            if 50 < event.pos[0] < 250 and 100 < event.pos[1] < 200 and money >= auto_click_cost:  
                money -= auto_click_cost  
                auto_click_rate += 1  # Increase click rate  
                auto_click_cost *= 2  # Increase cost for next upgrade  
  
    # Auto-clicker logic  
    auto_click_timer += dt  
    if auto_click_rate > 0 and auto_click_timer >= 1 / auto_click_rate:  
        money += click_multiplier  
        auto_click_timer = 0  
  
    # Detect hover  
    mouse_pos = pygame.mouse.get_pos()  
    hovering = original_button_rect.collidepoint(mouse_pos)  
  
    # Tweening logic for hover  
    tween_time = min(tween_time + 1, tween_duration) if hovering else max(tween_time - 1, 0)  
    scale_factor = 1 + 0.2 * math.sin(tween_time / tween_duration * math.pi / 2)  
    new_width = int(original_button_rect.width * scale_factor)  
    new_height = int(original_button_rect.height * scale_factor)  
    scaled_image = pygame.transform.scale(button_image, (new_width, new_height))  
    button_rect = scaled_image.get_rect(center=original_button_rect.center)  
  
    # Draw the button image  
    screen.blit(scaled_image, button_rect.topleft)  
  
    # Render and display the money  
    money_text = font.render(f'Money: {format_large_number(money)}', True, (255, 255, 255))  
    screen.blit(money_text, (50, 50))  
  
    # Render and display the auto-clicker upgrade option  
    upgrade_text = font.render(f'Auto-Clicker: {format_large_number(auto_click_cost)}', True, (255, 255, 255))  
    screen.blit(upgrade_text, (50, 100))  
  
    # Handle popup text  
    if popup_visible:  
        t = 1 - (popup_time / 60)  
        scale = quart_ease_out(t)  
        current_size = int(150 * scale)  
        popup_text = popup_font.render('DOUBLE!', True, (255, 255, 255))  
        popup_text = pygame.transform.scale(popup_text, (popup_text.get_width(), current_size))  
        screen.blit(popup_text, (800 - popup_text.get_width() // 2, 50))  
        popup_time -= 1  
        if popup_time <= 0:  
            popup_visible = False  
  
    # Update and draw particles  
    for particle in particles:  
        particle[0] += particle[2]  
        particle[1] += particle[3]  
        particle[4] -= 1  
        pygame.draw.circle(screen, (255, 255, 255), (int(particle[0]), int(particle[1])), 5)  
        if particle[4] <= 0:  
            particles.remove(particle)  
  
    # Update the display  
    pygame.display.flip()  
  
# Quit Pygame  
pygame.quit()  
sys.exit()  
