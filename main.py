import pygame
import random

class Star(pygame.sprite.Sprite):
    def __init__(self, col, x, y):
        super().__init__()
        self.image = pygame.Surface([x,y])
        self.image.fill(col)
        pygame.draw.rect(self.image, col, pygame.Rect(0,0,x,y))
        self.rect = self.image.get_rect()

pygame.init()
screen = pygame.display.set_mode([800,500])
clock = pygame.time.Clock()

rect = pygame.Rect(100,200,10,10)

stars_list = pygame.sprite.Group()

for i in range(10):
    star_obj = Star("blue", 10, 10)
    star_obj.rect.x = 100 + (random.randint(10,150))
    star_obj.rect.y = 100 + (random.randint(10,200))
    stars_list.add(star_obj)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for star in stars_list.sprites():
                pass
    
    screen.fill("cyan")

    pygame.draw.rect(screen, "black", rect)
    stars_list.update()
    stars_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()