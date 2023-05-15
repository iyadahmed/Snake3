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

    while True:
        # Clear screen
        window.fill((0, 0, 0))

        #####################
        ##      Input      ##
        #####################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                # Change direction based on key
                match event.key:
                    case pygame.K_RIGHT:
                        snake_direction = Direction.RIGHT
                    case pygame.K_LEFT:
                        snake_direction = Direction.LEFT
                    case pygame.K_DOWN:
                        snake_direction = Direction.DOWN
                    case pygame.K_UP:
                        snake_direction = Direction.UP

        ################################
        ##      Physics and Logic     ##
        ################################

        snake_head = snake[-1]

        # Collision detection
        if snake_head.x == food.x and snake_head.y == food.y:
            snake.append(copy.deepcopy(snake[-1]))
            snake_head = snake[-1]
            food.x = random.randrange(0, WIDTH_IN_BLOCKS) * BLOCK_SIZE
            food.y = random.randrange(0, HEIGHT_IN_BLOCKS) * BLOCK_SIZE

        # Move snake
        for snake_part, next_snake_part in zip(snake, snake[1:]):
            snake_part.x = next_snake_part.x
            snake_part.y = next_snake_part.y

        # Move head
        match snake_direction:
            case Direction.RIGHT:
                snake_head.x += BLOCK_SIZE
            case Direction.LEFT:
                snake_head.x -= BLOCK_SIZE
            case Direction.UP:
                snake_head.y -= BLOCK_SIZE
            case Direction.DOWN:
                snake_head.y += BLOCK_SIZE

        #####################
        ##      Render     ##
        #####################

        # Draw food
        window.fill((255, 0, 0), (food.x, food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Draw snake
        for snake_part in snake:
            window.fill(
                (255, 255, 0), (snake_part.x, snake_part.y, BLOCK_SIZE, BLOCK_SIZE)
            )

        pygame.display.flip()
        clock.tick(5)


if __name__ == "__main__":
    main()
