# WELCOME TO PONG!

import pygame

pygame.init()
pygame.display.set_caption("Pong")

WIDTH = 700 
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Paddle:
    COLOR = WHITE
    VELOCITY = 4
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(window, paddles, ball):
    window.fill(BLACK)

    for paddle in paddles:
        paddle.draw(window)

    # Dotted vertical line at the center
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
        
    ball.draw(window)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_s] and left_paddle.y - left_paddle.VELOCITY >= 0: # If your keyboard is Qwerty, replace [pygame.K_s] by [pygame.K_w] here
        left_paddle.move(up=True)
    if keys[pygame.K_w] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT: # If your keyboard is Qwerty, replace [pygame.K_w] by [pygame.K_s] here
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    
    while run:
        clock.tick(FPS)
        draw(WINDOW, [left_paddle, right_paddle], ball)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

    pygame.quit()

if __name__ == "__main__":
    main()