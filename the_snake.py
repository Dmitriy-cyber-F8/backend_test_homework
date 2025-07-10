"""
Модуль the_snake.py.

Реализует классичускую игру Змейка.

Для теста, находясь в директории the_snake,
запустите модуль командой python the_snake.py.
"""

from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Абстрактный класс, на основе которого создаются конкретные классы."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=None):
        """Инициализирует атрибуты абстрактного класса."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""


class Apple(GameObject):
    """Реализует создания яблока."""

    def __init__(self, occupied_cells=None, body_color=APPLE_COLOR):
        """Инициализация яблока."""
        super().__init__()
        self.body_color = body_color
        self.occupied_cells = occupied_cells
        # По умолчанию occupied_cells (множество занятых позиций) равен None
        if occupied_cells is None:
            self.occupied_cells = set()
        self.randomize_position()

    def randomize_position(self):
        """Установка случайного положения яблока, избегая занятые клетки."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE
                             )
            if self.position not in self.occupied_cells:
                break

    def draw(self):
        """Отрисовка яблока на поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Реализует создания змейки и все ее действия."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация начального состояния."""
        super().__init__()
        self.body_color = body_color
        self.reset()

    def get_head_position(self):
        """
        Возвращает позицию головы как первый по счету элемент
        в коллекции.
        """
        return self.positions[0]

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self, next_direction=None):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки.
        Добавляет новую голову и убирает последний элемент.
        """
        self.last = self.positions[-1] if self.positions else None
        head_pos_x, head_pos_y = self.get_head_position()
        change_x, change_y = self.direction
        new_pos_x = (head_pos_x + change_x * GRID_SIZE) % SCREEN_WIDTH
        new_pos_y = (head_pos_y + change_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_pos_x, new_pos_y)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            del self.positions[-1]
        else:
            self.last = None


def handle_keys(game_object):
    """Обработка клавиш для движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit('Ошибка операции')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Выполнение цикла игры."""
    pygame.init()
    snake = Snake()
    apple = Apple(occupied_cells=set(snake.positions))

    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Обновляем занятые клетки в яблоке
        apple.occupied_cells = set(snake.positions)
        head_position = snake.get_head_position()
        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position()
        if head_position in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            pygame.display.update()
            snake.reset()

            apple.occupied_cells = set(snake.positions)
            apple.randomize_position()

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
