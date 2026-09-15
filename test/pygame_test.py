import pygame

pygame.init()

WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("дом")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (150, 220, 200, 150))
    pygame.draw.polygon(screen, RED, [(130, 220), (370, 220), (250, 100)])
    text = font.render("Дом", True, GREEN)
    screen.blit(text, (220, 400))
    pygame.display.flip()

pygame.quit()