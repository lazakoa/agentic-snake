"""Shared fixtures for all tests."""

import pytest
from unittest.mock import Mock
from app import Direction, SnakeGame


@pytest.fixture
def mock_pygame(monkeypatch: pytest.MonkeyPatch) -> dict[str, Mock]:
    """Mock pygame to avoid display initialization in tests."""
    mock_display: Mock = Mock()
    mock_font: Mock = Mock()
    mock_clock: Mock = Mock()

    monkeypatch.setattr("pygame.init", Mock())
    monkeypatch.setattr("pygame.display.set_mode", lambda x: mock_display)
    monkeypatch.setattr("pygame.display.set_caption", Mock())
    monkeypatch.setattr("pygame.font.Font", lambda x, y: mock_font)
    monkeypatch.setattr("pygame.time.Clock", lambda: mock_clock)
    monkeypatch.setattr("pygame.quit", Mock())

    return {
        "display": mock_display,
        "font": mock_font,
        "clock": mock_clock,
    }


@pytest.fixture
def game(mock_pygame: dict[str, Mock]) -> SnakeGame:
    """Create a fresh game instance for each test."""
    return SnakeGame()


@pytest.fixture
def game_with_long_snake(mock_pygame: dict[str, Mock]) -> SnakeGame:
    """Game with a longer snake for collision testing."""
    game: SnakeGame = SnakeGame()
    game.snake = [(10, 10), (11, 10), (12, 10), (13, 10)]
    return game


@pytest.fixture
def game_at_wall(mock_pygame: dict[str, Mock]) -> SnakeGame:
    """Game with snake positioned at the wall."""
    game: SnakeGame = SnakeGame()
    game.snake = [(0, 5)]
    game.direction = Direction.LEFT
    game.next_direction = Direction.LEFT
    return game
