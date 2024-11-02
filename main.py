import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird with AI")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
BROWN = (139, 69, 19)
FONT = pygame.font.SysFont("Arial", 30)

BIRD_WIDTH, BIRD_HEIGHT = 34, 24
GRAVITY = 0.5
FLAP_STRENGTH = -9
bird_y_velocity = 0
bird_x, bird_y = WIDTH // 4, HEIGHT // 2
bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
bird_color = (255, 223, 0)

PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_COLOR_TOP = DARK_GREEN
PIPE_COLOR_BOTTOM = LIGHT_GREEN
pipe_speed = -3
pipes = []
pipe_spawn_time = 1500
last_pipe_spawn_time = pygame.time.get_ticks() - pipe_spawn_time

GROUND_HEIGHT = 80
ground_x = 0
ground_y = HEIGHT - GROUND_HEIGHT
ground_color = BROWN

background_color = BLUE
background_gradient_color = (135, 206, 250)
background_surface = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    color_blend = pygame.Color(0, 0, 0, 255)
    color_blend.r = int(background_color[0] * (1 - y / HEIGHT) + background_gradient_color[0] * (y / HEIGHT))
    color_blend.g = int(background_color[1] * (1 - y / HEIGHT) + background_gradient_color[1] * (y / HEIGHT))
    color_blend.b = int(background_color[2] * (1 - y / HEIGHT) + background_gradient_color[2] * (y / HEIGHT))
    pygame.draw.line(background_surface, color_blend, (0, y), (WIDTH, y))

score = 0
high_score = 0
game_over = False
show_start_screen = True

bird_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
bird_image.fill(bird_color)
pipe_image_top = pygame.Surface((PIPE_WIDTH, HEIGHT), pygame.SRCALPHA)
pipe_image_top.fill(PIPE_COLOR_TOP)
pipe_image_bottom = pygame.Surface((PIPE_WIDTH, HEIGHT), pygame.SRCALPHA)
pipe_image_bottom.fill(PIPE_COLOR_BOTTOM)
ground_image = pygame.Surface((WIDTH, GROUND_HEIGHT))
ground_image.fill(ground_color)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

def reset_game():
    global bird_y, bird_y_velocity, pipes, score, game_over, last_pipe_spawn_time, show_start_screen
    bird_y = HEIGHT // 2
    bird_y_velocity = 0
    pipes = []
    score = 0
    game_over = False
    show_start_screen = False
    last_pipe_spawn_time = pygame.time.get_ticks() - pipe_spawn_time

def spawn_pipe():
    y_position = random.randint(100, HEIGHT - PIPE_GAP - 100)
    top_pipe = pygame.Rect(WIDTH, y_position - HEIGHT, PIPE_WIDTH, HEIGHT)
    bottom_pipe = pygame.Rect(WIDTH, y_position + PIPE_GAP, PIPE_WIDTH, HEIGHT)
    pipes.append((top_pipe, bottom_pipe))

def draw_pipes():
    for pipe in pipes:
        SCREEN.blit(pipe_image_top, pipe[0].topleft)
        SCREEN.blit(pipe_image_bottom, pipe[1].topleft)

def move_pipes():
    global pipes, score, high_score
    for pipe in pipes:
        pipe[0].x += pipe_speed
        pipe[1].x += pipe_speed
    pipes = [pipe for pipe in pipes if pipe[0].right > 0]
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            return True
    for pipe in pipes:
        if pipe[0].right < bird_x and not pipe[0].colliderect(bird_rect):
            score += 1
            if score > high_score:
                high_score = score
            pipes.remove(pipe)
    return False

def display_score():
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    high_score_text = FONT.render(f"High Score: {high_score}", True, BLACK)
    SCREEN.blit(score_text, (10, 10))
    SCREEN.blit(high_score_text, (10, 40))

def check_ground_collision():
    return bird_rect.bottom >= HEIGHT - GROUND_HEIGHT

def update_bird():
    global bird_y, bird_y_velocity
    bird_y_velocity += GRAVITY
    bird_y += bird_y_velocity
    bird_rect.y = bird_y

def draw_bird():
    SCREEN.blit(bird_image, (bird_x, bird_y))

def draw_ground():
    SCREEN.blit(ground_image, (ground_x, ground_y))

def start_screen():
    SCREEN.blit(background_surface, (0, 0))
    draw_text("Flappy Bird AI", FONT, BLACK, SCREEN, WIDTH // 2 - 80, HEIGHT // 2 - 100)
    draw_text("Press SPACE to Start", FONT, BLACK, SCREEN, WIDTH // 2 - 130, HEIGHT // 2)
    pygame.display.flip()
    while show_start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    return
        clock.tick(FPS)

def ai_decision():
    if pipes:
        next_pipe = None
        for pipe in pipes:
            if pipe[0].x + PIPE_WIDTH > bird_x:
                next_pipe = pipe
                break
        if next_pipe:
            pipe_center_y = next_pipe[0].bottom + PIPE_GAP // 2
            if bird_y > pipe_center_y:
                return True
    return False

def main():
    global bird_y_velocity, last_pipe_spawn_time, game_over, show_start_screen
    running = True
    while running:
        if show_start_screen:
            start_screen()
        SCREEN.blit(background_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_y_velocity = FLAP_STRENGTH
                elif event.key == pygame.K_r and game_over:
                    reset_game()
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_spawn_time > pipe_spawn_time:
            spawn_pipe()
            last_pipe_spawn_time = current_time
        if not game_over:
            if ai_decision():
                bird_y_velocity = FLAP_STRENGTH
            game_over = move_pipes() or check_ground_collision()
            update_bird()
        draw_pipes()
        draw_bird()
        draw_ground()
        display_score()
        if game_over:
            draw_text("Game Over!", FONT, BLACK, SCREEN, WIDTH // 2 - 80, HEIGHT // 2 - 40)
            draw_text("Press R to Restart", FONT, BLACK, SCREEN, WIDTH // 2 - 100, HEIGHT // 2 + 20)
        pygame.display.flip()
        clock.tick(FPS)

main()
