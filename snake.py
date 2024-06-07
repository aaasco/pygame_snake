import pygame
import random
import numpy as np

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

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game with AI')

        self.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.food = self.generate_food()
        self.score = 0
        self.running = True

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if food not in self.snake:
                return food

    def update(self):
        if not self.running:
            return

        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or
            new_head[1] < 0 or new_head[1] >= GRID_SIZE or
            new_head in self.snake):
            self.running = False
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.generate_food()
            self.score += 1
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)

        for x, y in self.snake:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        fx, fy = self.food
        pygame.draw.rect(self.screen, RED, pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

    def compute_distance_map(self):
        distance_map = np.full((GRID_SIZE, GRID_SIZE), np.inf)
        fx, fy = self.food
        distance_map[fx][fy] = 0

        updated = True
        while updated:
            updated = False
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if distance_map[x][y] < np.inf:
                        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                                if distance_map[nx][ny] > distance_map[x][y] + 1:
                                    distance_map[nx][ny] = distance_map[x][y] + 1
                                    updated = True
        return distance_map

    def get_best_move(self):
        distance_map = self.compute_distance_map()
        head_x, head_y = self.snake[0]
        possible_moves = [UP, DOWN, LEFT, RIGHT]
        best_move = min(possible_moves, key=lambda move: distance_map[head_x + move[0]][head_y + move[1]]
                        if 0 <= head_x + move[0] < GRID_SIZE and 0 <= head_y + move[1] < GRID_SIZE else np.inf)
        return best_move

    def ai_move(self):
        if self.running:
            self.direction = self.get_best_move()
            self.update()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.ai_move()
            self.draw()
            clock.tick(10)  # 10 FPS

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
