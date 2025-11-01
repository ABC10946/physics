import pygame
import random
import uuid

class Ball:
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, color: tuple[float, float, float], radius: float):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.uuid = uuid.uuid4()


def isCollistionWall(position: pygame.Vector2, screen: pygame.Surface) -> tuple[int, int]:
    if position.x > screen.get_width():
        return (-1, 0)
    if position.y > screen.get_height():
        return (0, -1)
    if position.x < 0:
        return (1, 0)
    if position.y < 0:
        return (0, 1)

    return (0, 0)

def isCollisionBall(position: pygame.Vector2, positions: list[pygame.Vector2], radius: float=10) -> bool:
    for i in positions:
        dist = (i.x - position.x) * (i.x - position.x) + (i.y - position.y) * (i.y - position.y)
        if 25 < dist and dist < radius * radius:
            print("ball collision", dist, i, position)
            return True

    return False



def physics(screen: pygame.Surface, position: pygame.Vector2, velocity: pygame.Vector2, positions: list[pygame.Vector2], mass: float=1.0, gravity: float=1.0, radius: float=10.0) -> tuple[pygame.Vector2, pygame.Vector2]:
    bounceE = 0.999999
    velocity.y = velocity.y + gravity * mass * 1/2
    isCollision = isCollistionWall(position, screen)

    if isCollision == (1, 0) or isCollision == (-1, 0):
        if isCollision == (1, 0):
            position.x = 0 + 1
        elif isCollision == (-1, 0):
            position.x = screen.get_width() - 1
        velocity.x = -1 * bounceE * velocity.x
    elif isCollistionWall(position, screen) == (0, 1) or isCollistionWall(position, screen) == (0, -1):
        if isCollision == (1, 0):
            position.y = 0 + 1
        elif isCollision == (-1, 0):
            position.y = screen.get_height() - 1
        velocity.y = -1 * bounceE * velocity.y
    
    if isCollisionBall(position, positions, radius):
        velocity.x *= -1
        velocity.y *= -1

    position.x = position.x + velocity.x
    position.y = position.y + velocity.y * 1/2
    return (position, velocity)


def killBall(velocity: pygame.Vector2):
    return velocity.x * velocity.x + velocity.y + velocity.y < 0.01


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    balls: list[Ball] = []
    num = 100
    radius = 50

    for _ in range(num):
        position = pygame.Vector2(screen.get_width() * random.random() , screen.get_height() * random.random())
        velocity = pygame.Vector2(random.random() * 10, random.random() * 10)
        color = (random.random() * 255, random.random() * 255, random.random() * 255)
        balls.append(Ball(position, velocity, color, radius))




    running = True
    pause = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause= not pause

        screen.fill("black")


        for i in range(num):
            pygame.draw.circle(screen, balls[i].color, balls[i].position, balls[i].radius)
            if not pause:
                position, velocity = physics(screen, balls[i].position, balls[i].velocity,[x.position for x in balls], radius=radius + 50)
                balls[i].velocity = velocity
                balls[i].position = position

        pygame.display.flip()

        clock.tick()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()