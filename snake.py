import random
from dataclasses import dataclass
from enum import Enum, auto

import pygame

WIDTH_IN_BLOCKS = 600 // 20
HEIGHT_IN_BLOCKS = 400 // 20
BLOCK_SIZE = 20


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()
    UP = auto()


@dataclass()
class IntVector2D:
    x: int
    y: int

    def __add__(self, other: "IntVector2D"):
        return IntVector2D(self.x + other.x, self.y + other.y)


class Snake:
    def __init__(self, body: list[IntVector2D], direction: Direction) -> None:
        self.body = body
        self.direction = direction

    def move(self, delta: IntVector2D, grow: bool):
        """Moves snake by moving the head using delta, it also moves the body accordingly"""
        if grow:
            self.body.append(IntVector2D(0, 0))

        for part, next_part in zip(self.body[::-1], self.body[::-1][1:]):
            part.x = next_part.x
            part.y = next_part.y

        self.body[0] += delta

    def head(self):
        return self.body[0]


@dataclass
class Game:
    food_position: IntVector2D
    snake: Snake
    is_running: bool = True


def handle_input(game: Game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.is_running = False
            return

        elif event.type == pygame.KEYDOWN:
            # Change direction based on key
            match event.key:
                case pygame.K_RIGHT:
                    game.snake.direction = Direction.RIGHT
                case pygame.K_LEFT:
                    game.snake.direction = Direction.LEFT
                case pygame.K_DOWN:
                    game.snake.direction = Direction.DOWN
                case pygame.K_UP:
                    game.snake.direction = Direction.UP


def handle_logic(game: Game):
    # Calculate head movement
    head_delta = IntVector2D(0, 0)
    match game.snake.direction:
        case Direction.RIGHT:
            head_delta.x += BLOCK_SIZE
        case Direction.LEFT:
            head_delta.x -= BLOCK_SIZE
        case Direction.UP:
            head_delta.y -= BLOCK_SIZE
        case Direction.DOWN:
            head_delta.y += BLOCK_SIZE

    # Collision detection
    did_hit_food = game.snake.head() == game.food_position

    if did_hit_food:
        game.food_position.x = random.randrange(0, WIDTH_IN_BLOCKS) * BLOCK_SIZE
        game.food_position.y = random.randrange(0, HEIGHT_IN_BLOCKS) * BLOCK_SIZE

    game.snake.move(head_delta, grow=did_hit_food)


def render(game: Game, surface: pygame.Surface):
    # Clear screen
    surface.fill((0, 0, 0))

    # Draw food
    surface.fill(
        (255, 0, 0),
        (game.food_position.x, game.food_position.y, BLOCK_SIZE, BLOCK_SIZE),
    )

    # Draw snake
    for snake_part in game.snake.body:
        surface.fill(
            (255, 255, 0), (snake_part.x, snake_part.y, BLOCK_SIZE, BLOCK_SIZE)
        )

    pygame.display.flip()


def main():
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode(
        (WIDTH_IN_BLOCKS * BLOCK_SIZE, HEIGHT_IN_BLOCKS * BLOCK_SIZE)
    )

    # Init game state
    food_position = IntVector2D(
        WIDTH_IN_BLOCKS * BLOCK_SIZE // 2,
        HEIGHT_IN_BLOCKS * BLOCK_SIZE // 2,
    )
    snake = Snake([IntVector2D(0, 0)], Direction.RIGHT)
    game = Game(food_position, snake)

    while game.is_running:
        handle_input(game)
        handle_logic(game)
        render(game, window)
        clock.tick(5)


if __name__ == "__main__":
    main()
