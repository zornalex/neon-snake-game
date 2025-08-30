import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock for controlling game speed
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        self.body.insert(0, new_head)

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def check_collision(self):
        head = self.body[0]
        
        # Wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        
        # Self collision
        if head in self.body[1:]:
            return True
        
        return False

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)

    def generate_position(self, snake_body):
        while True:
            position = (random.randint(0, GRID_WIDTH-1), 
                        random.randint(0, GRID_HEIGHT-1))
            if position not in snake_body:
                return position

def main():
    print("Starting Snake Game...")
    try:
        snake = Snake()
        food = Food(snake.body)
        score = 0
        game_over = False

        print("Initializing game loop...")
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))

            snake.move()

            # Check for food collision
            if snake.body[0] == food.position:
                snake.grow = True
                score += 1
                food = Food(snake.body)
                print(f"Food eaten! Score: {score}")

            # Check for game over conditions
            if snake.check_collision():
                print("Game Over - Collision detected")
                game_over = True

            # Drawing
            screen.fill(BLACK)
            
            # Draw Snake
            for segment in snake.body:
                pygame.draw.rect(screen, GREEN, 
                                 (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, 
                                  GRID_SIZE-1, GRID_SIZE-1))
            
            # Draw Food
            pygame.draw.rect(screen, RED, 
                             (food.position[0]*GRID_SIZE, food.position[1]*GRID_SIZE, 
                              GRID_SIZE-1, GRID_SIZE-1))

            # Display Score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {score}', True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(10)  # Control game speed

        # Game Over Screen
        print(f"Final Score: {score}")
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        game_over_text = font.render('Game Over', True, WHITE)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 50))
        pygame.display.flip()

        # Wait before closing
        pygame.time.wait(2000)
        pygame.quit()
        print("Game closed successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
