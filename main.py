import pygame
import random
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class SnakeGame:
    def __init__(self) -> None:
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
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Game state
        self.reset_game()

    def reset_game(self) -> None:
        self.snake: list[tuple[int, int]] = [
            (self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2)
        ]
        self.direction: Direction = Direction.RIGHT
        self.next_direction: Direction = Direction.RIGHT
        self.food: tuple[int, int] = self.spawn_food()
        self.score: int = 0
        self.game_over: bool = False
        self.paused: bool = False

    def spawn_food(self) -> tuple[int, int]:
        while True:
            food: tuple[int, int] = (
                random.randint(0, self.GRID_WIDTH - 1),
                random.randint(0, self.GRID_HEIGHT - 1),
            )
            if food not in self.snake:
                return food

    def handle_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                else:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif not self.paused:
                        if (
                            event.key == pygame.K_UP
                            and self.direction != Direction.DOWN
                        ):
                            self.next_direction = Direction.UP
                        elif (
                            event.key == pygame.K_DOWN
                            and self.direction != Direction.UP
                        ):
                            self.next_direction = Direction.DOWN
                        elif (
                            event.key == pygame.K_LEFT
                            and self.direction != Direction.RIGHT
                        ):
                            self.next_direction = Direction.LEFT
                        elif (
                            event.key == pygame.K_RIGHT
                            and self.direction != Direction.LEFT
                        ):
                            self.next_direction = Direction.RIGHT

        return True

    def update(self) -> None:
        if self.game_over or self.paused:
            return

        self.direction = self.next_direction

        # Calculate new head position
        head_x: int
        head_y: int
        head_x, head_y = self.snake[0]

        if self.direction == Direction.UP:
            head_y -= 1
        elif self.direction == Direction.DOWN:
            head_y += 1
        elif self.direction == Direction.LEFT:
            head_x -= 1
        elif self.direction == Direction.RIGHT:
            head_x += 1

        new_head: tuple[int, int] = (head_x, head_y)

        # Check wall collision
        if (
            head_x < 0
            or head_x >= self.GRID_WIDTH
            or head_y < 0
            or head_y >= self.GRID_HEIGHT
        ):
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

    def draw(self) -> None:
        self.screen.fill(self.BLACK)

        # Draw snake
        for i, segment in enumerate(self.snake):
            x: int
            y: int
            x, y = segment
            color = self.GREEN if i == 0 else self.DARK_GREEN
            pygame.draw.rect(
                self.screen,
                color,
                (
                    x * self.GRID_SIZE,
                    y * self.GRID_SIZE,
                    self.GRID_SIZE - 2,
                    self.GRID_SIZE - 2,
                ),
            )

        # Draw food
        fx: int
        fy: int
        fx, fy = self.food
        pygame.draw.rect(
            self.screen,
            self.RED,
            (
                fx * self.GRID_SIZE,
                fy * self.GRID_SIZE,
                self.GRID_SIZE - 2,
                self.GRID_SIZE - 2,
            ),
        )

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw pause screen
        if self.paused:
            pause_text = self.font.render("PAUSED", True, self.WHITE)
            continue_text = self.font.render(
                "Press SPACE to continue", True, self.WHITE
            )

            text_rect = pause_text.get_rect(
                center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 20)
            )
            continue_rect = continue_text.get_rect(
                center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 20)
            )

            self.screen.blit(pause_text, text_rect)
            self.screen.blit(continue_text, continue_rect)

        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, self.RED)
            restart_text = self.font.render("Press SPACE to restart", True, self.WHITE)

            text_rect = game_over_text.get_rect(
                center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 20)
            )
            restart_rect = restart_text.get_rect(
                center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 20)
            )

            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self) -> None:
        running: bool = True

        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(10)

        pygame.quit()


def main() -> None:
    game: SnakeGame = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
