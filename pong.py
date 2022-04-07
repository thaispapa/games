import pygame
import sys


# CLASSES
class Ball:
    def __init__(self, screen, color, posX, posY, radius):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.show()

    def show(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    def start_moving(self):
        self.dx = 15
        self.dy = 5

    def move(self):
        self.posX += self.dx
        self.posY += self.dy

    def paddle_collision(self):
        self.dx = -self.dx

    def wall_collision(self):
        self.dy = -self.dy

    def restart_position(self):
        self.posX = WIDTH//2
        self.posY = HEIGHT//2
        self.dx = 0
        self.dy = 0
        self.show()


class Paddle:
    def __init__(self, screen, color, posX, posY, width, height):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.state = 'stopped'
        self.show()

    def show(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width, self.height))

    def move(self):
        if self.state == 'up':
            self.posY -= 10
        elif self.state == 'down':
            self.posY += 10

    def clamp(self):
        if self.posY <= 0:
            self.posY = 0

        if self.posY + self.height >= HEIGHT:
            self.posY = HEIGHT - self.height

    def restart_position(self):
        self.posY = HEIGHT//2 - self.height//2
        self.state = 'stopped'
        self.show()


class Score:
    def __init__(self, screen, points, posX, posY):
        self.screen = screen
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("monospace", 80, bold=True)
        self.label = self.font.render(self.points, 0, WHITE)
        self.show()

    def show(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

    def increase_score(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, WHITE)

    def restart(self):
        self.points = '0'
        self.label = self.font.render(self.points, 0, WHITE)


class CollisionManager:
    def between_ball_and_paddle1(self, ball, paddle1):
        if ball.posY + ball.radius > paddle1.posY and ball.posY - ball.radius < paddle1.posY + paddle1.height:
            if ball.posX - ball.radius <= paddle1.posX + paddle1.width:
                return True

        return False

    def between_ball_and_paddle2(self, ball, paddle2):
        if ball.posY + ball.radius > paddle2.posY and ball.posY - ball.radius < paddle2.posY + paddle2.height:
            if ball.posX + ball.radius >= paddle2.posX:
                return True

        return False

    def between_ball_and_walls(self, ball):
        # top collision
        if ball.posY - ball.radius <= 0:
            return True

        # bottom collision
        if ball.posY + ball.radius >= HEIGHT:
            return True

        return False

    def check_goal_player1(self, ball):
        return ball.posX - ball.radius >= WIDTH

    def check_goal_player2(self, ball):
        return ball.posX - ball.radius <= 0


# CONSTANTS
WIDTH, HEIGHT = 900, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# SCREEN
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PONG')


# FUNCTIONS
def draw_board():
    screen.fill(BLACK)


def paint_background():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)


def restart():
    paint_background()
    score1.restart()
    score2.restart()
    ball.restart_position()
    paddle1.restart_position()
    paddle2.restart_position()


paint_background()

# OBJECTS
ball = Ball(screen, WHITE, WIDTH // 2, HEIGHT // 2, 15)
paddle1 = Paddle(screen, WHITE, 15, HEIGHT // 2 - 60, 20, 120)
paddle2 = Paddle(screen, WHITE, WIDTH - 20 - 15, HEIGHT // 2 - 60, 20, 120)
collision = CollisionManager()
score1 = Score(screen, '0', WIDTH//4, 15)
score2 = Score(screen, '0', WIDTH - WIDTH//4, 15)

# VARIABLES
playing = False

# mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                ball.start_moving()
                playing = True

            if event.key == pygame.K_r:
                restart()
                playing = False

            if event.key == pygame.K_w:
                paddle1.state = 'up'

            if event.key == pygame.K_s:
                paddle1.state = 'down'

            if event.key == pygame.K_UP:
                paddle2.state = 'up'

            if event.key == pygame.K_DOWN:
                paddle2.state = 'down'

        if event.type == pygame.KEYUP:
            paddle1.state = 'stopped'
            paddle2.state = 'stopped'

    if playing:
        paint_background()

        # ball movement
        ball.move()
        pygame.time.delay(40)
        ball.show()

        # paddle 1
        paddle1.move()
        paddle1.clamp()
        paddle1.show()

        # paddle 2
        paddle2.move()
        paddle2.clamp()
        paddle2.show()

        # check for collisions
        if collision.between_ball_and_paddle1(ball, paddle1):
            ball.paddle_collision()

        if collision.between_ball_and_paddle2(ball, paddle2):
            ball.paddle_collision()

        if collision.between_ball_and_walls(ball):
            ball.wall_collision()

        if collision.check_goal_player1(ball):
            paint_background()
            score1.increase_score()
            ball.restart_position()
            paddle1.restart_position()
            paddle2.restart_position()
            playing = False

        if collision.check_goal_player2(ball):
            paint_background()
            score2.increase_score()
            ball.restart_position()
            paddle1.restart_position()
            paddle2.restart_position()
            playing = False

    score1.show()
    score2.show()

    pygame.display.update()
