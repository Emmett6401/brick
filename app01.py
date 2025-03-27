import pygame
import sys
import random
import os  # 파일 존재 여부 확인을 위한 모듈

# Initialize pygame
pygame.init()

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sound effects (with error handling)
try:
    if os.path.exists("brick_hit.wav"):  # wav 파일 사용
        brick_hit_sound = pygame.mixer.Sound("brick_hit.wav")  # 벽돌 충돌 소리
    else:
        print("경고: 'brick_hit.wav' 파일이 없습니다. 소리가 재생되지 않습니다.")
except pygame.error as e:
    print(f"오류: 'brick_hit.wav' 파일을 로드할 수 없습니다. {e}")

try:
    if os.path.exists("paddle_hit.wav"):
        paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")  # 패들 충돌 소리
    else:
        print("경고: 'paddle_hit.wav' 파일이 없습니다. 소리가 재생되지 않습니다.")
except pygame.error as e:
    print(f"오류: 'paddle_hit.wav' 파일을 로드할 수 없습니다. {e}")

# Font for score display
font = pygame.font.Font(None, 36)

# Initialize score
score = 0

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Paddle dimensions
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10

# Ball dimensions
BALL_RADIUS = 10

# Brick dimensions
BRICK_WIDTH = 75
BRICK_HEIGHT = 20

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")
print("게임이 시작되었습니다! 게임 창이 열렸는지 확인하세요.")  # 게임 시작 메시지 추가

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Paddle setup
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball setup
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_dx = 4 * random.choice((1, -1))
ball_dy = -4

# Bricks setup
bricks = []
for row in range(5):
    for col in range(10):
        brick = pygame.Rect(col * (BRICK_WIDTH + 5) + 35, row * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Function to play brick hit sound
def play_brick_hit_sound():
    try:
        print("벽돌 충돌 소리 재생 시도 중...")  # 디버깅 메시지
        brick_hit_sound.play()  # wav 소리 재생
        print("벽돌 충돌 소리 재생 성공!")  # 디버깅 메시지
    except pygame.error as e:
        print(f"오류: 벽돌 충돌 소리를 재생할 수 없습니다. {e}")

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("게임이 종료되었습니다.")  # 게임 종료 메시지 추가
            pygame.quit()
            sys.exit()

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-6, 0)
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.move_ip(6, 0)

    # Ball movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_dx = -ball_dx
    if ball.top <= 0:
        ball_dy = -ball_dy

    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_dy = -ball_dy
        try:
            print("패들 충돌 소리 재생 시도 중...")  # 디버깅 메시지
            paddle_hit_sound.play()  # 패들 충돌 소리 재생
            print("패들 충돌 소리 재생 성공!")  # 디버깅 메시지
        except pygame.error as e:
            print(f"오류: 패들 충돌 소리를 재생할 수 없습니다. {e}")

    # Ball collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_dy = -ball_dy
            play_brick_hit_sound()  # 벽돌 충돌 소리 재생
            score += 10  # 점수 증가
            break

    # Ball falls below screen
    if ball.bottom >= SCREEN_HEIGHT:
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Clear screen
    screen.fill(BLACK)

    # Draw paddle
    pygame.draw.rect(screen, WHITE, paddle)

    # Draw ball
    pygame.draw.ellipse(screen, RED, ball)

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
