import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GOAL_WIDTH = 100
GOAL_HEIGHT = 200
PLAYER_SIZE = 30
BALL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Premier League Football Game")

# Load images or create basic shapes for players and ball
ball = pygame.Surface((BALL_SIZE, BALL_SIZE))
ball.fill(BLACK)
player1 = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player1.fill(RED)
player2 = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player2.fill(BLUE)

# Premier League teams
teams = ["Arsenal", "Chelsea", "Manchester United", "Liverpool"]

# Game objects
class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.color = color
        self.controls = controls
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls['up']] and self.rect.top > 0:
            self.rect.move_ip(0, -self.speed)
        if keys[self.controls['down']] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, self.speed)
        if keys[self.controls['left']] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[self.controls['right']] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(self.speed, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def move(self):
        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, BLACK, self.rect)

    def reset_position(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

# Main game loop
def main():
    clock = pygame.time.Clock()
    player1 = Player(50, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, RED, 
                     {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
    player2 = Player(SCREEN_WIDTH - 50 - PLAYER_SIZE, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, BLUE, 
                     {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    score1 = 0
    score2 = 0

    running = True

    while running:
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move players and ball
        player1.move()
        player2.move()
        ball.move()

        # Collision detection
        if player1.rect.colliderect(ball.rect):
            ball.speed_x = -ball.speed_x
        if player2.rect.colliderect(ball.rect):
            ball.speed_x = -ball.speed_x

        # Check for goals
        if ball.rect.left <= 0:
            score2 += 1
            ball.reset_position()
        if ball.rect.right >= SCREEN_WIDTH:
            score1 += 1
            ball.reset_position()

        # Draw everything
        player1.draw(screen)
        player2.draw(screen)
        ball.draw(screen)

        # Display score
        font = pygame.font.SysFont(None, 55)
        text = font.render(f"{teams[0]} {score1} - {score2} {teams[1]}", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
