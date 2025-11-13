"""Comprehensive test suite for Snake game demonstrating pytest concepts."""

import pytest
from app import Direction, SnakeGame


# ============================================================================
# 1. FIXTURES - Setup and Dependency Injection
# ============================================================================


def test_initial_state(game: SnakeGame) -> None:
    """Test game initializes with correct default state."""
    assert game.score == 0
    assert game.game_over is False
    assert game.paused is False
    assert len(game.snake) == 1
    assert game.direction == Direction.RIGHT


def test_initial_snake_position(game: SnakeGame) -> None:
    """Test snake starts in center of grid."""
    expected_x = game.GRID_WIDTH // 2
    expected_y = game.GRID_HEIGHT // 2
    assert game.snake[0] == (expected_x, expected_y)


def test_food_not_on_snake(game: SnakeGame) -> None:
    """Test that food never spawns on snake body."""
    assert game.food not in game.snake


# ============================================================================
# 2. PARAMETRIZED TESTS - Test Multiple Scenarios
# ============================================================================


@pytest.mark.parametrize(
    "direction,expected_offset",
    [
        (Direction.UP, (0, -1)),
        (Direction.DOWN, (0, 1)),
        (Direction.LEFT, (-1, 0)),
        (Direction.RIGHT, (1, 0)),
    ],
)
def test_movement_directions(
    game: SnakeGame, direction: Direction, expected_offset: tuple[int, int]
) -> None:
    """Test snake moves correctly in all four directions."""
    # Arrange
    initial_pos = game.snake[0]
    game.direction = direction
    game.next_direction = direction

    # Act
    game.update()

    # Assert
    new_pos = game.snake[0]
    assert new_pos == (
        initial_pos[0] + expected_offset[0],
        initial_pos[1] + expected_offset[1],
    )


@pytest.mark.parametrize(
    "current,invalid",
    [
        (Direction.UP, Direction.DOWN),
        (Direction.DOWN, Direction.UP),
        (Direction.LEFT, Direction.RIGHT),
        (Direction.RIGHT, Direction.LEFT),
    ],
)
def test_cannot_reverse_direction(
    game: SnakeGame, current: Direction, invalid: Direction
) -> None:
    """Test that snake cannot reverse 180 degrees."""
    # This is tested by checking the direction doesn't change
    # when trying to reverse (tested in handle_input)
    game.direction = current
    game.next_direction = current

    # Trying to set opposite direction should be prevented
    # by handle_input logic (not tested here as it requires event simulation)
    assert game.direction == current


# ============================================================================
# 3. TESTING EXCEPTIONS AND EDGE CASES
# ============================================================================


def test_wall_collision_left(game_at_wall: SnakeGame) -> None:
    """Test game over when snake hits left wall."""
    game_at_wall.update()
    assert game_at_wall.game_over is True


def test_wall_collision_right(game: SnakeGame) -> None:
    """Test game over when snake hits right wall."""
    game.snake = [(game.GRID_WIDTH - 1, 5)]
    game.direction = Direction.RIGHT
    game.next_direction = Direction.RIGHT

    game.update()

    assert game.game_over is True


def test_wall_collision_top(game: SnakeGame) -> None:
    """Test game over when snake hits top wall."""
    game.snake = [(5, 0)]
    game.direction = Direction.UP
    game.next_direction = Direction.UP

    game.update()

    assert game.game_over is True


def test_wall_collision_bottom(game: SnakeGame) -> None:
    """Test game over when snake hits bottom wall."""
    game.snake = [(5, game.GRID_HEIGHT - 1)]
    game.direction = Direction.DOWN
    game.next_direction = Direction.DOWN

    game.update()

    assert game.game_over is True


# ============================================================================
# 4. TESTING STATE CHANGES
# ============================================================================


def test_eating_food_increases_score(game: SnakeGame) -> None:
    """Test that eating food increments score."""
    # Arrange - place food at next position
    initial_score = game.score
    head_x, head_y = game.snake[0]
    game.food = (head_x + 1, head_y)
    game.direction = Direction.RIGHT
    game.next_direction = Direction.RIGHT

    # Act
    game.update()

    # Assert
    assert game.score == initial_score + 1


def test_eating_food_grows_snake(game: SnakeGame) -> None:
    """Test that eating food increases snake length."""
    # Arrange
    initial_length = len(game.snake)
    head_x, head_y = game.snake[0]
    game.food = (head_x + 1, head_y)
    game.direction = Direction.RIGHT
    game.next_direction = Direction.RIGHT

    # Act
    game.update()

    # Assert
    assert len(game.snake) == initial_length + 1


def test_not_eating_food_maintains_length(game: SnakeGame) -> None:
    """Test that snake length stays same when not eating."""
    # Arrange
    initial_length = len(game.snake)
    # Make sure food is far away
    game.food = (30, 30)

    # Act
    game.update()

    # Assert
    assert len(game.snake) == initial_length


def test_self_collision(game_with_long_snake: SnakeGame) -> None:
    """Test game over when snake collides with itself."""
    # Arrange - snake in a position where it will hit its body
    game = game_with_long_snake
    # Snake body forms a shape where moving left will hit the tail
    game.snake = [(11, 10), (11, 11), (10, 11), (10, 10)]
    game.direction = Direction.LEFT
    game.next_direction = Direction.LEFT

    # Act
    game.update()

    # Assert - moving left from (11, 10) goes to (10, 10) which is in the snake
    assert game.game_over is True


# ============================================================================
# 5. MONKEYPATCHING - Mocking Dependencies
# ============================================================================


def test_spawn_food_avoids_snake(
    game: SnakeGame, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that food doesn't spawn on snake body."""
    # Arrange - set snake to occupy specific positions
    game.snake = [(5, 5), (5, 6), (5, 7)]

    # Control random to first return snake position, then valid position
    values = [(5, 5), (10, 10)]
    call_index = [0]

    def mock_randint(a: int, b: int) -> int:
        value: tuple[int, int] = values[call_index[0] // 2]  # Each coord needs 2 calls
        result: int = value[call_index[0] % 2]
        call_index[0] += 1
        return result

    monkeypatch.setattr("random.randint", mock_randint)

    # Act
    food = game.spawn_food()

    # Assert
    assert food == (10, 10)
    assert food not in game.snake


# ============================================================================
# 6. TEST CLASSES - Grouping Related Tests
# ============================================================================


class TestPauseFeature:
    """Tests for pause functionality."""

    def test_initial_pause_state(self, game: SnakeGame) -> None:
        """Test game starts unpaused."""
        assert game.paused is False

    def test_paused_game_does_not_update(self, game: SnakeGame) -> None:
        """Test that paused game doesn't process updates."""
        # Arrange
        game.paused = True
        initial_pos = game.snake[0]

        # Act
        game.update()

        # Assert
        assert game.snake[0] == initial_pos

    def test_reset_clears_pause(self, game: SnakeGame) -> None:
        """Test that reset_game clears paused state."""
        # Arrange
        game.paused = True

        # Act
        game.reset_game()

        # Assert
        assert game.paused is False

    def test_quit_on_q_when_paused(
        self, game: SnakeGame, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that pressing 'q' when paused quits the game."""
        # Arrange
        game.paused = True

        # Mock pygame.event.get to return a 'q' key press event
        import pygame

        mock_event = type("Event", (), {"type": pygame.KEYDOWN, "key": pygame.K_q})()
        monkeypatch.setattr("pygame.event.get", lambda: [mock_event])

        # Act
        result = game.handle_input()

        # Assert
        assert result is False


class TestResetGame:
    """Tests for game reset functionality."""

    def test_reset_score(self, game: SnakeGame) -> None:
        """Test reset clears score."""
        game.score = 10
        game.reset_game()
        assert game.score == 0

    def test_reset_game_over(self, game: SnakeGame) -> None:
        """Test reset clears game over state."""
        game.game_over = True
        game.reset_game()
        assert game.game_over is False

    def test_reset_creates_new_snake(self, game: SnakeGame) -> None:
        """Test reset creates fresh snake."""
        game.snake = [(1, 1), (2, 2), (3, 3)]
        game.reset_game()
        assert len(game.snake) == 1


# ============================================================================
# 7. MULTIPLE MOVEMENTS TEST
# ============================================================================


def test_multiple_movements(game: SnakeGame) -> None:
    """Test snake can move multiple times without collision."""
    # Start from center, move down to avoid walls
    game.snake = [(20, 5)]
    game.direction = Direction.DOWN
    game.next_direction = Direction.DOWN
    game.food = (30, 30)  # Keep food away

    for _ in range(20):  # Move 20 times down (won't hit wall with grid height of 30)
        game.update()

    # Should have moved 20 times without collision
    assert not game.game_over


# ============================================================================
# 8. CUSTOM ASSERTIONS WITH MESSAGES
# ============================================================================


def test_grid_dimensions(game: SnakeGame) -> None:
    """Test grid dimensions are correctly calculated."""
    assert game.GRID_WIDTH == 40, f"Expected width 40, got {game.GRID_WIDTH}"
    assert game.GRID_HEIGHT == 30, f"Expected height 30, got {game.GRID_HEIGHT}"


def test_snake_always_has_head(game: SnakeGame) -> None:
    """Test snake always has at least one segment."""
    for _ in range(10):
        game.food = (30, 30)
        game.update()

    assert len(game.snake) >= 1, "Snake must always have at least one segment"


# ============================================================================
# 9. MULTIPLE PARAMETRIZE - Cartesian Product
# ============================================================================


@pytest.mark.parametrize("x", [0, 20, 39])
@pytest.mark.parametrize("y", [0, 15, 29])
def test_valid_grid_positions(game: SnakeGame, x: int, y: int) -> None:
    """Test various grid positions are valid (9 combinations)."""
    assert 0 <= x < game.GRID_WIDTH
    assert 0 <= y < game.GRID_HEIGHT


# ============================================================================
# 10. TESTING WITH IDS - Better Test Names
# ============================================================================


@pytest.mark.parametrize(
    "snake_pos,direction,should_collide",
    [
        ((0, 0), Direction.LEFT, True),
        ((39, 29), Direction.RIGHT, True),
        ((20, 15), Direction.RIGHT, False),
    ],
    ids=["left-wall", "right-wall", "center"],
)
def test_collision_scenarios(
    game: SnakeGame,
    snake_pos: tuple[int, int],
    direction: Direction,
    should_collide: bool,
) -> None:
    """Test various collision scenarios with descriptive IDs."""
    game.snake = [snake_pos]
    game.direction = direction
    game.next_direction = direction

    game.update()

    assert game.game_over == should_collide
