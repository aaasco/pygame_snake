import pygame
import random

# Configuration du jeu
GRID_SIZE = 20
CELL_SIZE = 20
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialisation du jeu
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Snake')
font = pygame.font.Font(None, 36)

def init_game():
    snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
    direction = random.choice([UP, DOWN, LEFT, RIGHT])
    food = generate_food(snake)
    score = 0
    running = True
    return screen, snake, direction, food, score, running

def generate_food(snake):
    while True:
        food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if food not in snake:
            return food

def update(snake, direction, food, score, running):
    if not running:
        return snake, food, score, running

    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or
        new_head in snake):
        running = False
        return snake, food, score, running

    snake.insert(0, new_head)

    if new_head == food:
        food = generate_food(snake)
        score += 100
    else:
        snake.pop()

    return snake, food, score, running

def draw(screen, snake, food, score, message):
    screen.fill(BLACK)

    # Dessiner le serpent
    for i, (x, y) in enumerate(snake):
        # Changer la couleur de dessin de la tête
        if i == 0:
            pygame.draw.rect(screen, WHITE, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        else:
            pygame.draw.rect(screen, GREEN, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Dessiner la nourriture
    fx, fy = food
    pygame.draw.rect(screen, RED, pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Afficher le score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Afficher le message
    if message:
        message_text = font.render(message, True, WHITE)
        text_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(message_text, text_rect)

    # Ajouter le message "Press SPACE to restart" à côté de "You Win!" et "Game Over"
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()

def get_best_move(snake, food):
    head_x, head_y = snake[0]
    fx, fy = food

    # Calcul des distances
    distances = {
        UP: abs(head_x - fx) + abs(head_y - 1 - fy),
        DOWN: abs(head_x - fx) + abs(head_y + 1 - fy),
        LEFT: abs(head_x - 1 - fx) + abs(head_y - fy),
        RIGHT: abs(head_x + 1 - fx) + abs(head_y - fy)
    }

    # Initialisation du meilleur mouvement avec une grande distance
    best_move = None
    best_distance = float('inf')

    # Vérifie les mouvements possibles et évite de se mordre la queue
    for direction in [UP, DOWN, LEFT, RIGHT]:
        new_head = (head_x + direction[0], head_y + direction[1])
        if (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE and new_head not in snake):
            distance = distances[direction]
            if distance < best_distance:
                best_move = direction
                best_distance = distance

    return best_move

def ai_move(snake, direction, food, score, running):
    if running:
        new_direction = get_best_move(snake, food)
        if new_direction:  # Vérifie si un mouvement sûr a été trouvé
            direction = new_direction
        snake, food, score, running = update(snake, direction, food, score, running)
    return snake, direction, food, score, running

def run():
    screen, snake, direction, food, score, running = init_game()
    clock = pygame.time.Clock()
    message = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not running:
                screen, snake, direction, food, score, running = init_game()
                message = ""

        if running:
            snake, direction, food, score, running = ai_move(snake, direction, food, score, running)
            if score >= 2500:
                message = "You Win!"
                running = False
            elif not running:
                message = "Game Over"

        draw(screen, snake, food, score, message)
        clock.tick(10)  # 10 FPS

if __name__ == "__main__":
    run()
