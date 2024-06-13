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

def init_game(): # Fonction pour initialiser le jeu
    snake = [(GRID_SIZE // 2, GRID_SIZE // 2)] # Créer un serpent avec une seule partie au milieu de l'écran
    direction = random.choice([UP, DOWN, LEFT, RIGHT]) # Choisir une direction aléatoire
    food = generate_food(snake) # Générer la nourriture
    score = 0 
    running = True
    return screen, snake, direction, food, score, running # Retourner les valeurs initiales

def generate_food(snake): # Fonction pour générer la nourriture
    while True: # Boucle infinie
        food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) # Générer une position aléatoire pour la nourriture
        if food not in snake: # Vérifier si la nourriture n'est pas sur le serpent
            return food # Retourner la position de la nourriture

def update(snake, direction, food, score, running): # Fonction pour mettre à jour le jeu
    if not running: # Si le jeu est terminé
        return snake, food, score, running # Retourne les valeurs actuelles

    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1]) # Calcul de la nouvelle position de la tête

    if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or 
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or
        new_head in snake): # Si la tête du serpent sort de l'écran ou se mord la queue
        running = False # Arrêter le jeu
        return snake, food, score, running # Retourne les valeurs actuelles

    snake.insert(0, new_head) # Ajouter la nouvelle tête

    if new_head == food: # Si la tête du serpent atteint la nourriture
        food = generate_food(snake) # Générer une nouvelle nourriture
        score += 100 # Augmenter le score
    else: # Si la tête du serpent ne touche pas la nourriture
        snake.pop() # Supprimer la dernière partie du serpent

    return snake, food, score, running  # Retourne les nouvelles valeurs

def draw(screen, snake, food, score, message): # Fonction pour dessiner le jeu 
    screen.fill(BLACK) # Remplir l'écran en noir

    # Dessiner le serpent
    for i, (x, y) in enumerate(snake):
        # Changer la couleur de dessin de la tête
        if i == 0: # La tête est le premier élément de la liste
            pygame.draw.rect(screen, WHITE, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) # Dessiner la tête en blanc
        else:
            pygame.draw.rect(screen, GREEN, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) # Dessiner le reste du serpent en vert

    # Dessiner la nourriture
    fx, fy = food
    pygame.draw.rect(screen, RED, pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)) # Dessiner la nourriture en rouge

    # Afficher le score
    score_text = font.render(f"Score: {score}", True, WHITE) # Créer un objet texte
    screen.blit(score_text, (10, 10)) # Afficher le texte en haut à gauche

    # Afficher le message
    if message: # Si le message n'est pas vide
        message_text = font.render(message, True, WHITE) # Créer un objet texte
        text_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)) # Centrer le texte
        screen.blit(message_text, text_rect) # Afficher le texte

    # Ajouter le message "Press SPACE to restart" à côté de "You Win!" et "Game Over"
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()

def get_best_move(snake, food):
    head_x, head_y = snake[0]
    fx, fy = food

    # Calcul des distances
    distances = { # Dictionnaire des distances entre la tête du serpent et la nourriture
        UP: abs(head_x - fx) + abs(head_y - 1 - fy), # Distance entre la tête du serpent et la nourriture si le serpent se déplace vers le haut
        DOWN: abs(head_x - fx) + abs(head_y + 1 - fy), # Distance entre la tête du serpent et la nourriture si le serpent se déplace vers le bas
        LEFT: abs(head_x - 1 - fx) + abs(head_y - fy), # Distance entre la tête du serpent et la nourriture si le serpent se déplace vers la gauche
        RIGHT: abs(head_x + 1 - fx) + abs(head_y - fy) # Distance entre la tête du serpent et la nourriture si le serpent se déplace vers la droite
    }

    # Initialisation du meilleur mouvement avec une grande distance
    best_move = None
    best_distance = float('inf')

    # Vérifie les mouvements possibles et évite de se mordre la queue
    for direction in [UP, DOWN, LEFT, RIGHT]: # Pour chaque direction possible
        new_head = (head_x + direction[0], head_y + direction[1]) # Calcul de la nouvelle position de la tête
        if (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE and new_head not in snake): # Vérifie si la nouvelle position est valide
            distance = distances[direction] # Récupère la distance pour cette direction
            if distance < best_distance: # Si la distance est meilleure que la meilleure distance actuelle
                best_move = direction # Met à jour le meilleur mouvement
                best_distance = distance # Met à jour la meilleure distance

    return best_move

def ai_move(snake, direction, food, score, running): # Fonction pour déplacer le serpent automatiquement
    if running: # Si le jeu est en cours
        new_direction = get_best_move(snake, food) # Trouver le meilleur mouvement
        if new_direction:  # Vérifie si un mouvement sûr a été trouvé
            direction = new_direction # Met à jour la direction
        snake, food, score, running = update(snake, direction, food, score, running) # Mettre à jour le jeu
    return snake, direction, food, score, running # Retourne les nouvelles valeurs

def run(): # Fonction principale
    screen, snake, direction, food, score, running = init_game() # Initialisation du jeu
    clock = pygame.time.Clock() # Création d'une horloge pour contrôler la vitesse du jeu
    message = "" 

    while True: # Boucle principale
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not running: # Si la touche ESPACE est enfoncée et que le jeu est terminé
                screen, snake, direction, food, score, running = init_game() # Réinitialiser le jeu
                message = ""

        if running: # Si le jeu est en cours
            snake, direction, food, score, running = ai_move(snake, direction, food, score, running) # Mettre à jour le jeu
            if score >= 2500: # Si le score est supérieur ou égal à 2500
                message = "You Win!"
                running = False
            elif not running: # Si le jeu est terminé
                message = "Game Over"

        draw(screen, snake, food, score, message) 
        clock.tick(10)  # 10 FPS

if __name__ == "__main__":
    run() 
