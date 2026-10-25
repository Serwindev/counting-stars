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

def cardInfo(name):
    mouse = getMouse()
    intern = getIntern()

    if name == "mouse_time":
        info = {"title": "Sharper Eyes", "level": mouse["level"], "cost": mouse["cost"], "status": None}
        if mouse["time"] <= MOUSE_MIN_TIME:
            info["line"] = f"{mouse['time']}s per look"
            info["status"] = "max"
        else:
            nxt = round(max(MOUSE_MIN_TIME, mouse["time"] - MOUSE_STEP), 2)
            info["line"] = f"{mouse['time']}s -> {nxt}s"
        return info

    if name == "mouse_count":
        info = {"title": "Wider Gaze", "level": mouse["powerLevel"], "cost": mouse["powerCost"], "status": None}
        if mouse["powerLevel"] >= MAX_POWER:
            info["line"] = f"+{mouse['count']} stars per look"
            info["status"] = "max"
        else:
            info["line"] = f"+{mouse['count']} -> +{mouse['count'] + 1}"
        return info

    if name == "intern_time":
        if intern["active"] == False:
            return {"title": "Invite a Friend", "level": None, "cost": intern["cost"], "status": None,
                    "line": f"+{intern['count']} every {intern['time']}s"}
        info = {"title": "Friend Focuses", "level": intern["level"], "cost": intern["cost"], "status": None}
        if intern["time"] <= INTERN_MIN_TIME:
            info["line"] = f"every {intern['time']}s"
            info["status"] = "max"
        else:
            nxt = round(max(INTERN_MIN_TIME, intern["time"] - INTERN_STEP), 2)
            info["line"] = f"{intern['time']}s -> {nxt}s"
        return info

    if name == "intern_count":
        info = {"title": "Binoculars", "level": intern["powerLevel"], "cost": intern["powerCost"], "status": None}
        if intern["active"] == False:
            info["line"] = "invite a friend first"
            info["status"] = "locked"
            info["level"] = None
        elif intern["powerLevel"] >= MAX_POWER:
            info["line"] = f"+{intern['count']} each time"
            info["status"] = "max"
        else:
            info["line"] = f"+{intern['count']} -> +{intern['count'] + 2}"
        return info

def buy(name):
    global count, CLICK_RATE, click_count, total_count
    info = cardInfo(name)

    if info["status"] == "max":
        showToast("That one's maxed out!")
        return
    if info["status"] == "locked":
        showToast("Invite a friend first")
        return
    if count < info["cost"]:
        showToast(f"Count {info['cost'] - count:,} more stars first")
        return

    kind = "time" if name.endswith("time") else "count"
    if name.startswith("mouse"):
        bought = upgradeMouse(kind)
    else:
        bought = upgradeIntern(kind)

    if bought:
        count -= info["cost"]
        CLICK_RATE = getMouse()["time"]
        click_count = getMouse()["count"]
        total_count = getTotalCount()
        if name == "intern_time" and info["title"] == "Invite a Friend":
            showToast("Your friend brought a blanket and sat down!")
        saveData(count, total_count, earned)

def drawCount():
    surf = big_font.render(f"{count:,}", True, (50, 35, 30))
    t = time.time() - lastGain
    if t < 0.15:
        scale = 1 + 0.12 * (1 - t / 0.15)
        surf = pygame.transform.smoothscale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
    screen.blit(surf, surf.get_rect(center=(WIDTH // 2, 58)))

    label = font_small2.render("stars counted", True, (120, 95, 80))
    screen.blit(label, label.get_rect(center=(WIDTH // 2, 95)))

    intern = getIntern()
    if intern["active"]:
        stats = f"+{click_count} per look   |   friend: +{intern['count']} every {intern['time']}s"
    else:
        stats = f"+{click_count} per look   |   counting alone"
    stats_text = font_small.render(stats, True, (110, 85, 70))
    screen.blit(stats_text, stats_text.get_rect(center=(WIDTH // 2, 122)))

    alltime = font_small.render(f"all time: {earned:,}", True, (130, 105, 90))
    screen.blit(alltime, (12, DESK_TOP - 22))

    if earned < 40:
        hint = font_small.render("click the sky to count a star (you can hold it too)", True, (130, 105, 90))
        screen.blit(hint, hint.get_rect(midright=(WIDTH - 12, DESK_TOP - 14)))

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
    if (round(CLICK_RATE, 2) == 0.1):
        nextLevel1 = font_small2.render("MAX", False, (0,0,0))
        screen.blit(nextLevel1, (180,390))
    else:
        nextLevel1 = font_small2.render(f"{round(CLICK_RATE,2)} -> {round(CLICK_RATE - 0.05,2)}", False, (0,0,0))
        screen.blit(nextLevel1, (160,390))
    screen.blit(upgradeName1, (165,370))
    

    intern_button = pygame.draw.rect(screen, (255,255,255), (350,350,110,100),0, 10)
    upgradeName2 = font_small.render(f"Click Rate: {round(CLICK_RATE,2)}", False, (0,0,0))
    if (round(CLICK_RATE, 2) == 0.1):
        nextLevel2 = font_small2.render("MAX", False, (0,0,0))
        screen.blit(nextLevel2, (380,390))
    else:
        nextLevel2 = font_small2.render(f"{round(CLICK_RATE,2)} -> {round(CLICK_RATE - 0.05,2)}", False, (0,0,0))
        screen.blit(nextLevel2, (360,390))
    screen.blit(upgradeName2, (365,370))

    
    
    if click:
        elapsed = time.time() - lastclick
        if elapsed >= CLICK_RATE:
            click = False
        

    pygame.display.flip()

    clock.tick(60)

pygame.quit()