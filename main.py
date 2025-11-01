import pygame
import random
import uuid
import math

class PhysicsObjectBase:
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, activate: bool=True):
        self.uuid = uuid.uuid4()
        self.position = position
        self.velocity = velocity
        self.activate = activate


class Ball(PhysicsObjectBase):
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, color: tuple[float, float, float], radius: float):
        super().__init__(position, velocity)
        self.radius = radius
        self.color = color


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

def isCollisionBall(pObject: PhysicsObjectBase, pObjects: list[PhysicsObjectBase], radius: float) -> tuple[bool, PhysicsObjectBase|None]:
    for i in pObjects:
        position = pObject.position
        if i.uuid != pObject.uuid and i.activate:
            dist = (i.position.x - position.x) * (i.position.x - position.x) + (i.position.y - position.y) * (i.position.y - position.y)
            if dist < radius * radius:
                return True, i

    return False, None



def physics(screen: pygame.Surface, pObject: PhysicsObjectBase, pObjects: list[PhysicsObjectBase], mass: float, gravity: float, radius: float) -> tuple[pygame.Vector2, pygame.Vector2]:
    bounceE = 0.9
    velocity = pObject.velocity
    position = pObject.position

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
    
    isCollision, collision = isCollisionBall(pObject, pObjects, radius)

    if isCollision:
        immersedDist = math.sqrt( (radius * radius) - ((position.x - collision.position.x) * (position.x - collision.position.x) + (position.y - collision.position.y) * (position.y - collision.position.y)) )
        vector = pygame.Vector2(position.x - collision.position.x, position.y - collision.position.y)
        immersedDistVect = immersedDist * vector.normalize()
        print(immersedDistVect)
        position.x = position.x + immersedDistVect.x
        position.y = position.y + immersedDistVect.y
        velocity.x = -1 * bounceE * velocity.x
        velocity.y = -1 * bounceE * velocity.y
            


    position.x = position.x + velocity.x
    position.y = position.y + velocity.y * 1/2
    return (position, velocity)


def isKillBall(velocity: pygame.Vector2):
    return velocity.x * velocity.x + velocity.y * velocity.y < 0.0000001


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280 * 2, 720 * 2))
    clock = pygame.time.Clock()

    balls: list[Ball] = []
    num = 25
    radius = 40

    for _ in range(num):
        position = pygame.Vector2(screen.get_width() * random.random() , screen.get_height() * random.random())
        velocity = pygame.Vector2(random.random() * 10, random.random() * 10)
        color = (random.random() * 255, random.random() * 255, random.random() * 255)
        ball = Ball(position, velocity, color, radius)
        balls.append(ball)




    running = True
    pause = False
    while running:
        step = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause= not pause
                if event.key == pygame.K_s:
                    step = True

        screen.fill("black")


        for i in range(num):
            if balls[i].activate:
                pygame.draw.circle(screen, balls[i].color, balls[i].position, balls[i].radius)
                if not pause:
                    position, velocity = physics(screen, balls[i], balls , 1.0, 9.8, radius)
                    balls[i].velocity = velocity
                    balls[i].position = position
                

        pygame.display.flip()

        clock.tick()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()