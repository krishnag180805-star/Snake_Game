import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
WHITE = (255, 255, 255)

# Clock controls game speed
clock = pygame.time.Clock()
FPS = 10

# Font
font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 50)


def create_food():
    """Generate food at a random grid position."""
    x = random.randrange(0, WIDTH, CELL_SIZE)
    y = random.randrange(0, HEIGHT, CELL_SIZE)
    return [x, y]


def draw_snake(snake):
    """Draw every part of the snake."""
    for i, segment in enumerate(snake):
        color = DARK_GREEN if i == 0 else GREEN

        pygame.draw.rect(
            screen,
            color,
            (segment[0], segment[1], CELL_SIZE, CELL_SIZE)
        )


def draw_food(food):
    """Draw the food."""
    pygame.draw.rect(
        screen,
        RED,
        (food[0], food[1], CELL_SIZE, CELL_SIZE)
    )


def show_score(score):
    """Display the score."""
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def game_over(score):
    """Display game-over screen."""
    screen.fill(BLACK)

    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render(
        "Press R to restart or Q to quit",
        True,
        WHITE
    )

    screen.blit(
        game_over_text,
        (
            WIDTH // 2 - game_over_text.get_width() // 2,
            HEIGHT // 2 - 80
        )
    )

    screen.blit(
        score_text,
        (
            WIDTH // 2 - score_text.get_width() // 2,
            HEIGHT // 2
        )
    )

    screen.blit(
        restart_text,
        (
            WIDTH // 2 - restart_text.get_width() // 2,
            HEIGHT // 2 + 50
        )
    )

    pygame.display.update()


def run_game():

    # Starting position of snake
    snake = [
        [300, 200],
        [280, 200],
        [260, 200]
    ]

    # Starting direction
    direction = "RIGHT"

    # Food
    food = create_food()

    score = 0

    running = True
    game_ended = False

    while running:

        # -----------------------------
        # Handle keyboard events
        # -----------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"

                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"

                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"

                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # -----------------------------
        # Move snake
        # -----------------------------

        head_x = snake[0][0]
        head_y = snake[0][1]

        if direction == "UP":
            head_y -= CELL_SIZE

        elif direction == "DOWN":
            head_y += CELL_SIZE

        elif direction == "LEFT":
            head_x -= CELL_SIZE

        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = [head_x, head_y]

        # Add new head
        snake.insert(0, new_head)

        # -----------------------------
        # Check food collision
        # -----------------------------

        if new_head == food:

            score += 1

            # Create new food
            food = create_food()

        else:
            # Remove tail
            snake.pop()

        # -----------------------------
        # Check wall collision
        # -----------------------------

        if (
            head_x < 0
            or head_x >= WIDTH
            or head_y < 0
            or head_y >= HEIGHT
        ):
            game_ended = True

        # -----------------------------
        # Check snake body collision
        # -----------------------------

        if new_head in snake[1:]:
            game_ended = True

        # -----------------------------
        # Game over
        # -----------------------------

        if game_ended:

            game_over(score)

            waiting = True

            while waiting:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_r:
                            return run_game()

                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

        # -----------------------------
        # Draw everything
        # -----------------------------

        screen.fill(BLACK)

        draw_snake(snake)
        draw_food(food)
        show_score(score)

        pygame.display.update()

        # Control speed
        clock.tick(FPS)


# Start game
run_game()