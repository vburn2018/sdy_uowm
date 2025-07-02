import pygame
import sys
import random

pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Game constants
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = SCREEN_WIDTH // (BRICK_COLS + 2)
BRICK_HEIGHT = 30
BRICK_GAP = 5
PADDLE_WIDTH = SCREEN_WIDTH // 8
PADDLE_HEIGHT = 20
BALL_RADIUS = 12
BALL_SPEED = max(5, SCREEN_WIDTH // 460)
PADDLE_SPEED = max(8, SCREEN_WIDTH // 100)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Arkanoid')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 32)

def create_bricks():
    bricks = []
    x_offset = (SCREEN_WIDTH - (BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP)) // 2
    y_offset = 60
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = x_offset + col * (BRICK_WIDTH + BRICK_GAP)
            y = y_offset + row * (BRICK_HEIGHT + BRICK_GAP)
            bricks.append(pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT))
    return bricks

def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)
        pygame.draw.rect(screen, WHITE, brick, 2)

def main():
    paddle = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - 60, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect((SCREEN_WIDTH - BALL_RADIUS) // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_dx = BALL_SPEED * random.choice([-1, 1])
    ball_dy = -BALL_SPEED
    bricks = create_bricks()
    score = 0
    running = True
    game_over = False
    win = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.x += PADDLE_SPEED

        if not game_over:
            # Move ball
            ball.x += int(ball_dx)
            ball.y += int(ball_dy)

            # Ball collision with walls
            if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
                ball_dx = -ball_dx
            if ball.top <= 0:
                ball_dy = -ball_dy

            # Ball collision with paddle
            if ball.colliderect(paddle):
                ball_dy = -abs(BALL_SPEED)
                offset = (ball.centerx - paddle.centerx) / (PADDLE_WIDTH // 2)
                ball_dx = BALL_SPEED * offset

            # Ball collision with bricks
            hit_index = ball.collidelist(bricks)
            if hit_index != -1:
                hit_brick = bricks.pop(hit_index)
                score += 10
                if abs(ball.bottom - hit_brick.top) < 15 and ball_dy > 0:
                    ball_dy = -ball_dy
                elif abs(ball.top - hit_brick.bottom) < 15 and ball_dy < 0:
                    ball_dy = -ball_dy
                else:
                    ball_dx = -ball_dx

            # Ball out of bounds
            if ball.top > SCREEN_HEIGHT:
                game_over = True
                win = False

            # Win condition
            if not bricks:
                game_over = True
                win = True

        # Drawing
        screen.fill(BLACK)
        draw_bricks(bricks)
        pygame.draw.rect(screen, GREEN, paddle)
        pygame.draw.ellipse(screen, RED, ball)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (20, 20))

        if game_over:
            msg = 'You Win!' if win else 'Game Over!'
            msg_text = font.render(msg + ' Press R to Restart or Q to Quit.', True, WHITE)
            screen.blit(msg_text, (SCREEN_WIDTH // 2 - msg_text.get_width() // 2, SCREEN_HEIGHT // 2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()
                return
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main() 