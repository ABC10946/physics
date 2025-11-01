import pygame
import random

def isCollistionWall(position: pygame.Vector2, screen: pygame.Surface) -> tuple[int, int]:
    if position.x > screen.get_width():
        return (-1, 0)
    if position.y > screen.get_height():
        return (0, -1)
    if position.x < 0:
        return (1, 0)
    if position.y < 0:
        return (0, 1)
    
    # if position.x > screen.get_width() and position.y > screen.get_height():
    #     return (1, 1)
    # if position.x < 0 and position.y < 0:
    #     return (-1, -1)
    # if position.x > screen.get_width() and position.y < 0:
    #     return (-1, 1)
    # if position.x > 0 and position.y > screen.get_height():
    #     return (1, -1)

    return (0, 0)


def physics(screen: pygame.Surface, position: pygame.Vector2, velocity: pygame.Vector2, mass: float=1.0, gravity: float=1.0) -> tuple[pygame.Vector2, pygame.Vector2]:
    bounceE = 0.9
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
        

    position.x = position.x + velocity.x
    position.y = position.y + velocity.y * 1/2
    return (position, velocity)



def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    positions = []
    velocities = []
    colors = []
    num = 1000

    for _ in range(num):
        position = pygame.Vector2(screen.get_width() * random.random() , screen.get_height() * random.random())
        velocity = pygame.Vector2(random.random() * 50, random.random() * 50)
        color = (random.random() * 255, random.random() * 255, random.random() * 255)
        positions.append(position)
        velocities.append(velocity)
        colors.append(color)




    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill("black")

        for i in range(num):
            pygame.draw.circle(screen, colors[i], positions[i], 10)
            position, velocity = physics(screen, positions[i], velocities[i])
            velocities[i] = velocity
            positions[i] = position

        pygame.display.flip()

        clock.tick()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()