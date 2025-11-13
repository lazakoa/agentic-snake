import pygame
import random
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class SnakeGame:
    def __init__(self):
        pygame.init()

        # Game constants
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.GRID_SIZE = 20
        self.GRID_WIDTH = self.WINDOW_WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.WINDOW_HEIGHT // self.GRID_SIZE

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.DARK_GREEN = (0, 200, 0)

        # Setup display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Game state
        self.reset_game()

    def reset_game(self):
        self.snake = [(self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, self.GRID_WIDTH - 1),
                   random.randint(0, self.GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                else:
                    if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.next_direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.next_direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.next_direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.next_direction = Direction.RIGHT

        return True

    def update(self):
        if self.game_over:
            return

        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.snake[0]

        if self.direction == Direction.UP:
            head_y -= 1
        elif self.direction == Direction.DOWN:
            head_y += 1
        elif self.direction == Direction.LEFT:
            head_x -= 1
        elif self.direction == Direction.RIGHT:
            head_x += 1

        new_head = (head_x, head_y)

        # Check wall collision
        if (head_x < 0 or head_x >= self.GRID_WIDTH or
            head_y < 0 or head_y >= self.GRID_HEIGHT):
            self.game_over = True
            return

        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()

    def draw(self):
        self.screen.fill(self.BLACK)

        # Draw snake
        for i, segment in enumerate(self.snake):
            x, y = segment
            color = self.GREEN if i == 0 else self.DARK_GREEN
            pygame.draw.rect(self.screen,
                           color,
                           (x * self.GRID_SIZE, y * self.GRID_SIZE,
                            self.GRID_SIZE - 2, self.GRID_SIZE - 2))

        # Draw food
        fx, fy = self.food
        pygame.draw.rect(self.screen,
                        self.RED,
                        (fx * self.GRID_SIZE, fy * self.GRID_SIZE,
                         self.GRID_SIZE - 2, self.GRID_SIZE - 2))

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, self.WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render('GAME OVER!', True, self.RED)
            restart_text = self.font.render('Press SPACE to restart', True, self.WHITE)

            text_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 20))

            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(10)

        pygame.quit()

def main():
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()
