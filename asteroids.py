import pygame
import random

WIDTH = 640
HEIGHT = 480

pygame.init()


class State:
    def __init__(self):
        self.__state = 0

    @property
    def endgame(self):
        return self.__state

    def switch(self):
        self.__state = 0 if self.__state else 1


class AsteroidsCollection:
    def __init__(self):
        self.asteroids = []

    def add(self, asteroid):
        self.asteroids.append(asteroid)

    def update(self):
        if random.random() < 0.008:
            self.add(Asteroid(random.randint(
                0, WIDTH-100), -35, random.randint(50, 300)/100))
        new_asteroids = []
        for asteroid in self.asteroids:
            asteroid.update()
            if asteroid.height + asteroid.y < HEIGHT:
                if not robot.collides(asteroid):
                    new_asteroids.append(asteroid)
                else:
                    pygame.mixer.Sound.play(hit_sound)
                    score.update()
            else:
                pygame.mixer.Sound.play(gameover_sound)
                state.switch()
                break
        self.asteroids = new_asteroids

    def render(self):
        for asteroid in self.asteroids:
            asteroid.render()


class Asteroid:
    image = pygame.transform.scale(pygame.image.load("asteroid.png"), (75, 75))

    def __init__(self, x, y, velocity):
        self.width = Asteroid.image.get_width()
        self.height = Asteroid.image.get_height()
        self.x = x
        self.y = y
        self.velocity = velocity

    def update(self):
        self.y += self.velocity

    def render(self):
        window.blit(Asteroid.image, (self.x, self.y))


class Robot:
    image = pygame.image.load("robot.png")

    def __init__(self):
        self.width = Robot.image.get_width()
        self.height = Robot.image.get_height()
        self.x = 0
        self.y = HEIGHT - self.height
        self.velocity = 3

    def update(self):
        if to_right:
            self.x = min(self.x + self.velocity, WIDTH - self.width)
        if to_left:
            self.x = max(self.x - self.velocity, 0)

    def render(self):
        window.blit(Robot.image, (self.x, self.y))

    def collides(self, other):
        if self.x > other.x + other.width or other.x > self.x + self.width:
            return False

        if self.y > other.y + other.height or other.y > self.y + self.height:
            return False

        return True


class Score:
    font = pygame.font.SysFont("Arial", 24)

    def __init__(self):
        self.score = 0

    def update(self):
        self.score += 1

    def render(self):
        score_text = Score.font.render(
            f"Score: {self.score}", True, (255, 0, 0))
        window.blit(score_text, (WIDTH - 90, 5))


def update():
    robot.update()
    asteroids.update()


def render():
    window.fill((0, 0, 0))
    robot.render()
    asteroids.render()
    score.render()
    pygame.display.flip()


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot vs Asteroids")
big_font = pygame.font.SysFont("Arial", 56)
small_font = pygame.font.SysFont("Arial", 30)
text = big_font.render("GAME OVER", True, (255, 0, 0))
text2 = small_font.render("press SPACE to start over", True, (255, 0, 0))
hit_sound = pygame.mixer.Sound("hit.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")
clock = pygame.time.Clock()
to_right = False
to_left = False
state = State()
robot = Robot()
score = Score()
asteroids = AsteroidsCollection()

while True:
    if state.endgame:
        window.fill((0, 0, 0))
        score.render()
        window.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 50))
        window.blit(text2, (WIDTH//2 - 150, HEIGHT//2))
        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True
            if event.key == pygame.K_SPACE and state.endgame:
                asteroids = AsteroidsCollection()
                score = Score()
                state.switch()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False

        if event.type == pygame.QUIT:
            exit()

    if not state.endgame:
        update()
        render()
    clock.tick(60)
