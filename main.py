import pygame
import time
import random
from upgrades import *


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([800,500])
clock = pygame.time.Clock()


default()
init()

count = getCount()
total_count = getCount(1)
click = False
hold = False

CLICK_RATE = getMouse()["time"]
click_count = getMouse()["count"]

text_list = []

sample_font = pygame.font.SysFont('Comic Sans MS', 30)
font_small = pygame.font.SysFont('Comic Sans MS', 13)
font_small2 = pygame.font.SysFont('Comic Sans MS', 18)

def createText(text, mouse_pos, rand=False):
    text_ = sample_font.render(text, False, "black")
    if rand == False:
        text_rect = text_.get_rect(center=mouse_pos)
    else:
        text_rect = text_.get_rect(center=(random.randint(100,700), random.randint(100,400)))

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

clickable = True
respawn = True
lastSpawn = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            saveData(count, total_count)
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[1] >= 350:
                if pygame.mouse.get_pos()[0] <= 250 and pygame.mouse.get_pos()[1] <= 450:
                    clickable = False
                    if getMouse()["level"] < 9:
                        count -= getMouse()["cost"]
                        upgradeMouse("time")
                        CLICK_RATE = getMouse()["time"]
            if pygame.mouse.get_pos()[0] >= 350 and pygame.mouse.get_pos()[1] >= 350:
                if pygame.mouse.get_pos()[0] <= 450 and pygame.mouse.get_pos()[1] <= 450:
                    clickable = False
                    count -= getIntern()["cost"]
                    upgradeIntern("time")
                    SPAWN_RATE = getIntern()["time"]
            else:
                clickable = True

            if event.button == 1 and not click and clickable:
                click = True
                mouse_pos = pygame.mouse.get_pos()
                createText(f"+{click_count}", mouse_pos)
                lastclick = time.time()
                count += getMouse()["count"]

            
    if getIntern()["active"] == True and respawn:
        count_ = getIntern()["count"]
        total_count = getMouse()["count"] + count_
        createText(f"+{count_}", 0, rand=True)
        respawn = False
        lastSpawn = time.time()
        count += count_
        
    if (time.time() - lastSpawn) >= getIntern()["time"]:
        respawn = True

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

    counter = sample_font.render(f"+{count}", False, (0,0,0))

    mouse_button = pygame.draw.rect(screen, (255,255,255), (150,350,110,100),0, 10)
    upgradeName1 = font_small.render(f"Click Rate: {round(CLICK_RATE,2)}", False, (0,0,0))
    nextLevel1 = font_small2.render(f"{round(CLICK_RATE,2)} -> {round(CLICK_RATE - 0.05,2)}", False, (0,0,0))
    screen.blit(upgradeName1, (155,370))
    screen.blit(nextLevel1, (160,390))

    intern_button = pygame.draw.rect(screen, (255,255,255), (350,350,100,100),0, 10)

    
    
    if click:
        elapsed = time.time() - lastclick
        if elapsed >= CLICK_RATE:
            click = False
        

    pygame.display.flip()

    clock.tick(60)

pygame.quit()