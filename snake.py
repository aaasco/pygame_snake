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

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')

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
        score += 1
    else:
        snake.pop()

    return snake, food, score, running

def draw(screen, snake, food):
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        snake, direction, food, score, running = ai_move(snake, direction, food, score, running)
        draw(screen, snake, food)
        clock.tick(10)  # 10 FPS

    pygame.quit()

if __name__ == "__main__":
    run()
