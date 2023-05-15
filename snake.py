import copy
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
class Position:
    x: int
    y: int


@dataclass
class Game:
    food: Position
    snake_direction: Direction
    snake: list[Position]
    running: bool = True


def handle_input(game: Game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            return

        elif event.type == pygame.KEYDOWN:
            # Change direction based on key
            match event.key:
                case pygame.K_RIGHT:
                    game.snake_direction = Direction.RIGHT
                case pygame.K_LEFT:
                    game.snake_direction = Direction.LEFT
                case pygame.K_DOWN:
                    game.snake_direction = Direction.DOWN
                case pygame.K_UP:
                    game.snake_direction = Direction.UP


def handle_logic(game: Game):
    snake_head = game.snake[-1]

    # Move head
    new_snake_head = copy.deepcopy(snake_head)
    match game.snake_direction:
        case Direction.RIGHT:
            new_snake_head.x += BLOCK_SIZE
        case Direction.LEFT:
            new_snake_head.x -= BLOCK_SIZE
        case Direction.UP:
            new_snake_head.y -= BLOCK_SIZE
        case Direction.DOWN:
            new_snake_head.y += BLOCK_SIZE

    game.snake.append(new_snake_head)

    # Collision detection
    if snake_head.x == game.food.x and snake_head.y == game.food.y:
        game.food.x = random.randrange(0, WIDTH_IN_BLOCKS) * BLOCK_SIZE
        game.food.y = random.randrange(0, HEIGHT_IN_BLOCKS) * BLOCK_SIZE
    else:
        # We allow snake to grow if we hit food otherwise, we pop tail
        game.snake.pop(0)


def render(game: Game, window: pygame.Surface):
    # Clear screen
    window.fill((0, 0, 0))

    # Draw food
    window.fill((255, 0, 0), (game.food.x, game.food.y, BLOCK_SIZE, BLOCK_SIZE))

    # Draw snake
    for snake_part in game.snake:
        window.fill((255, 255, 0), (snake_part.x, snake_part.y, BLOCK_SIZE, BLOCK_SIZE))

    pygame.display.flip()


def main():
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode(
        (WIDTH_IN_BLOCKS * BLOCK_SIZE, HEIGHT_IN_BLOCKS * BLOCK_SIZE)
    )

    # Init game state
    food = Position(
        WIDTH_IN_BLOCKS * BLOCK_SIZE // 2,
        HEIGHT_IN_BLOCKS * BLOCK_SIZE // 2,
    )
    snake_direction = Direction.RIGHT
    snake: list[Position] = [Position(0, 0)]
    game = Game(food, snake_direction, snake)

    while game.running:
        handle_input(game)
        handle_logic(game)
        render(game, window)
        clock.tick(5)


if __name__ == "__main__":
    main()
