import pygame
import time
from upgrades import *


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([800,500])
clock = pygame.time.Clock()

count = 0
click = False
hold = False

CLICK_RATE = getMouse()["time"]
click_count = getMouse()["count"]

text_list = []

sample_font = pygame.font.SysFont('Comic Sans MS', 30)

def createText(text, mouse_pos):
    text_ = sample_font.render(text, False, "black")
    text_rect = text_.get_rect(center=mouse_pos)

    vel_y = -1
    createdAt = time.time()

    text_list.append({
        "surface": text_,
        "rect": text_rect,
        "vel_y": vel_y,
        "createdAt": createdAt
    })

running = True
spawn = False
lastclick = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                count -= 10
                upgrade(1, "time")
                CLICK_RATE -= 0.05
                
            elif event.key == pygame.K_a:
                count -= 500
                click_count += 1
                hold = True
                

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not click:
                click = True
                mouse_pos = pygame.mouse.get_pos()
                createText(f"+{click_count}", mouse_pos)
                lastclick = time.time()
                count += 1
        
        if pygame.mouse.get_pressed(3) == (False, False, True) and hold:
            click = True

    screen.fill("cyan")

    for text in text_list[:]:
            current = time.time()
            elapsed = current - text["createdAt"]
            if elapsed >= 0.4:
                text_list.remove(text)
                continue
                
            text["vel_y"] -= 0.3

            text["rect"].y += text["vel_y"]
            
            if elapsed >= 0.2:
                text["surface"].set_alpha(25)
            elif elapsed >= 0.3:
                text["surface"].set_alpha(50)

            screen.blit(text["surface"], text["rect"])

    count_text = sample_font.render(f"Count: {count}", False, (0,0,0))
    screen.blit(count_text, (350,50))

    counter = sample_font.render("+1", False, (0,0,0))
    
    if click:
        elapsed = time.time() - lastclick
        if elapsed >= CLICK_RATE:
            click = False
        

    pygame.display.flip()

    clock.tick(60)

pygame.quit()