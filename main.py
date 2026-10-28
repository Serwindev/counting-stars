import pygame
import time
import random
import math
from upgrades import *


pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 500
GROUND_TOP = 350
TEXT_LIFE = 0.8

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Star Counter")
clock = pygame.time.Clock()


default()
init()

count = getCount()
total_count = getCount(1)
earned = getEarned()
click = False
hold = False

CLICK_RATE = getMouse()["time"]
click_count = getMouse()["count"]

text_list = []
ripples = []

sample_font = pygame.font.SysFont('Comic Sans MS', 30)
big_font = pygame.font.SysFont('Comic Sans MS', 46, bold=True)
font_small = pygame.font.SysFont('Comic Sans MS', 13)
font_small2 = pygame.font.SysFont('Comic Sans MS', 18)


TEXT_LIGHT = (240, 236, 255)
TEXT_SOFT = (170, 165, 210)
GOLD = (255, 232, 150)
FRIEND_BLUE = (150, 200, 255)

MOON_POS = (690, 78)
MOON_R = 30


sky_stars = []
for i in range(170):
    sky_stars.append([
        random.randint(0, WIDTH),
        random.randint(0, GROUND_TOP - 30),
        random.choice([1, 1, 1, 2]),
        random.uniform(0, math.pi * 2),
        random.uniform(1, 3.5)
    ])


clouds = []
for i in range(3):
    w = random.randint(120, 200)
    cloud = pygame.Surface((w, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(cloud, (90, 90, 140, 70), (0, 12, w, 20))
    pygame.draw.ellipse(cloud, (90, 90, 140, 60), (w * 0.2, 2, w * 0.5, 26))
    clouds.append({
        "surface": cloud,
        "x": random.uniform(-200, WIDTH),
        "y": random.randint(40, 200),
        "speed": random.uniform(5, 12)
    })

cards = [
    {"name": "mouse_time", "rect": pygame.Rect(30, 375, 170, 105)},
    {"name": "mouse_count", "rect": pygame.Rect(220, 375, 170, 105)},
    {"name": "intern_time", "rect": pygame.Rect(410, 375, 170, 105)},
    {"name": "intern_count", "rect": pygame.Rect(600, 375, 170, 105)},
]

toast = {"text": "", "until": 0}


spotted = []
MAX_SPOTTED = 60


shooting = None
nextShooting = time.time() + random.uniform(8, 15)
caught = data["overall"].get("caught", 0)


def hillY(x, base, height, waves):
    return base - height * (0.5 + 0.5 * math.sin(x / waves))


def makeBackground():
    bg = pygame.Surface((WIDTH, HEIGHT))


    top = (8, 10, 32)
    bottom = (58, 38, 88)
    for y in range(GROUND_TOP):
        t = y / GROUND_TOP
        color = [int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)]
        pygame.draw.line(bg, color, (0, y), (WIDTH, y))


    rng = random.Random(7)
    milky = pygame.Surface((WIDTH, GROUND_TOP), pygame.SRCALPHA)
    for i in range(900):
        x = rng.uniform(0, WIDTH)
        y = 260 - x * 0.28 + rng.gauss(0, 28)
        pygame.draw.circle(milky, (210, 200, 255, rng.randint(15, 45)), (int(x), int(y)), rng.choice([1, 1, 2]))
    for i in range(12):
        x = i * 75
        pygame.draw.ellipse(milky, (150, 130, 220, 10), (x - 60, 260 - x * 0.28 - 40, 160, 80))
    bg.blit(milky, (0, 0))


    glow = pygame.Surface((200, 200), pygame.SRCALPHA)
    for r in range(90, MOON_R, -6):
        pygame.draw.circle(glow, (255, 245, 210, 6), (100, 100), r)
    bg.blit(glow, (MOON_POS[0] - 100, MOON_POS[1] - 100))
    pygame.draw.circle(bg, (246, 240, 220), MOON_POS, MOON_R)
    for dx, dy, r in [(-9, -6, 6), (8, 7, 4), (5, -12, 3), (-4, 12, 3)]:
        pygame.draw.circle(bg, (225, 218, 196), (MOON_POS[0] + dx, MOON_POS[1] + dy), r)


    far = [(0, HEIGHT)]
    for x in range(0, WIDTH + 10, 10):
        far.append((x, hillY(x + 40, GROUND_TOP + 5, 45, 90)))
    far.append((WIDTH, HEIGHT))
    pygame.draw.polygon(bg, (34, 30, 66), far)


    for x in range(470, 800, 22):
        h = rng.randint(22, 40)
        base = hillY(x + 40, GROUND_TOP + 5, 45, 90) + 4
        pygame.draw.polygon(bg, (24, 22, 50), [(x, base - h), (x - 9, base), (x + 9, base)])


    near = [(0, HEIGHT)]
    for x in range(0, WIDTH + 10, 10):
        near.append((x, hillY(x, GROUND_TOP + 18, 18, 140)))
    near.append((WIDTH, HEIGHT))
    pygame.draw.polygon(bg, (18, 18, 38), near)

    tx, ty = 52, hillY(52, GROUND_TOP + 18, 18, 140)
    pygame.draw.line(bg, (12, 12, 26), (tx, ty - 22), (tx - 10, ty), 3)
    pygame.draw.line(bg, (12, 12, 26), (tx, ty - 22), (tx + 10, ty), 3)
    pygame.draw.line(bg, (12, 12, 26), (tx - 14, ty - 16), (tx + 18, ty - 36), 7)


    for i in range(70):
        x = rng.randint(0, WIDTH)
        y = rng.randint(GROUND_TOP + 25, HEIGHT)
        pygame.draw.line(bg, (28, 30, 55), (x, y), (x + rng.randint(-2, 2), y - rng.randint(3, 6)), 1)

    return bg


def drawSky(dt):
    t = time.time()
    for s in sky_stars:
        b = 150 + 105 * math.sin(t * s[4] + s[3])
        b = max(60, min(255, b))
        pygame.draw.circle(screen, (int(b), int(b), min(255, int(b) + 25)), (s[0], s[1]), s[2])

    for c in clouds:
        c["x"] += c["speed"] * dt
        if c["x"] > WIDTH:
            c["x"] = -c["surface"].get_width()
            c["y"] = random.randint(40, 200)
        screen.blit(c["surface"], (int(c["x"]), c["y"]))


def drawSparkle(pos, size, color):
    x, y = pos
    t = size * 0.3
    points = [(x, y - size), (x + t, y - t), (x + size, y), (x + t, y + t),
              (x, y + size), (x - t, y + t), (x - size, y), (x - t, y - t)]
    pygame.draw.polygon(screen, color, points)


def drawSpotted():
    t = time.time()
    for s in spotted:
        grow = min(1, (t - s["born"]) / 0.2)
        twinkle = 0.75 + 0.25 * math.sin(t * 3 + s["phase"])
        size = s["size"] * grow * twinkle
        if size >= 1:
            drawSparkle(s["pos"], size, (255, 240, 190))


def spawnShootingStar():
    global shooting
    going_right = random.random() < 0.5
    if going_right:
        x = random.randint(40, 350)
    else:
        x = random.randint(450, 760)
    speed = random.uniform(360, 460)
    angle = math.radians(random.uniform(18, 32))
    shooting = {
        "x": x,
        "y": random.randint(-10, 40),
        "vx": speed * math.cos(angle) * (1 if going_right else -1),
        "vy": speed * math.sin(angle),
        "trail": []
    }


def updateShootingStar(dt):
    global shooting, nextShooting
    now = time.time()
    if shooting is None:
        if now >= nextShooting:
            spawnShootingStar()
        return

    shooting["trail"].append((shooting["x"], shooting["y"]))
    if len(shooting["trail"]) > 18:
        shooting["trail"].pop(0)
    shooting["x"] += shooting["vx"] * dt
    shooting["y"] += shooting["vy"] * dt

    if shooting["y"] > GROUND_TOP or shooting["x"] < -20 or shooting["x"] > WIDTH + 20:
        shooting = None
        nextShooting = now + random.uniform(15, 30)


def drawShootingStar():
    if shooting is None:
        return
    trail = shooting["trail"]
    for i in range(1, len(trail)):
        fade = i / len(trail)
        c = int(255 * fade)
        pygame.draw.line(screen, (c, c, min(255, c + 30)), trail[i - 1], trail[i], max(1, int(3 * fade)))
    head = (int(shooting["x"]), int(shooting["y"]))
    pygame.draw.circle(screen, (255, 255, 255), head, 3)
    pygame.draw.circle(screen, (255, 245, 210), head, 7, 1)


def tryCatch(pos):
    global shooting, caught, nextShooting
    if shooting is None:
        return False
    if math.hypot(pos[0] - shooting["x"], pos[1] - shooting["y"]) > 30:
        return False

    bonus = max(20, getTotalCount() * 10)
    addCount(bonus)
    caught += 1
    data["overall"]["caught"] = caught
    createText(f"+{bonus}!", pos)
    showToast("You caught a shooting star! Make a wish.")

    for i in range(5):
        spot = (pos[0] + random.randint(-25, 25), pos[1] + random.randint(-20, 20))
        spotted.append({"pos": spot, "born": time.time(), "size": random.uniform(3, 6), "phase": random.uniform(0, 6)})

    shooting = None
    nextShooting = time.time() + random.uniform(15, 30)
    return True


def createText(text, mouse_pos, rand=False, color=GOLD):
    text_ = sample_font.render(text, True, color)
    if rand == False:
        text_rect = text_.get_rect(center=mouse_pos)
    else:
        text_rect = text_.get_rect(center=(random.randint(150, 600), random.randint(160, 310)))

    text_list.append({
        "surface": text_,
        "rect": text_rect,
        "y": float(text_rect.y),
        "vel_y": -3,
        "createdAt": time.time()
    })


def showToast(msg):
    toast["text"] = msg
    toast["until"] = time.time() + 1.5


def addCount(n):
    global count, earned, lastGain
    count += n
    earned += n
    lastGain = time.time()


def doClick(pos):
    global click, lastclick
    if click:
        return
    click = True
    lastclick = time.time()
    createText(f"+{click_count}", pos)
    ripples.append({"pos": pos, "createdAt": lastclick})
    addCount(click_count)

    spot = (pos[0] + random.randint(-6, 6), pos[1] + random.randint(-6, 6))
    spotted.append({"pos": spot, "born": lastclick, "size": random.uniform(3, 5), "phase": random.uniform(0, 6)})
    while len(spotted) > MAX_SPOTTED:
        spotted.pop(0)


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


def drawCard(card, mouse_pos):
    info = cardInfo(card["name"])
    rect = card["rect"]
    hovered = rect.collidepoint(mouse_pos)
    affordable = info["status"] is None and count >= info["cost"]

    if info["status"] == "max":
        bg = (32, 66, 70)
        border = (90, 180, 160)
    elif info["status"] == "locked":
        bg = (24, 24, 42)
        border = (50, 50, 75)
    elif affordable:
        bg = (52, 52, 100) if hovered else (40, 40, 82)
        border = GOLD
    else:
        bg = (30, 30, 56)
        border = (65, 65, 100)

    pygame.draw.rect(screen, (6, 6, 18), rect.move(0, 4), 0, 10)
    body = rect.move(0, -3) if hovered and info["status"] is None else rect
    pygame.draw.rect(screen, bg, body, 0, 10)
    pygame.draw.rect(screen, border, body, 1, 10)

    title = font_small2.render(info["title"], True, TEXT_LIGHT)
    screen.blit(title, title.get_rect(center=(body.centerx, body.top + 20)))

    if info["level"] is not None:
        lv = font_small.render(f"Lv {info['level']}", True, TEXT_SOFT)
        screen.blit(lv, (body.right - lv.get_width() - 8, body.top + 4))

    line = font_small.render(info["line"], True, TEXT_SOFT)
    screen.blit(line, line.get_rect(center=(body.centerx, body.top + 50)))

    if info["status"] == "max":
        bottom = font_small2.render("MAX", True, (120, 225, 190))
    elif info["status"] == "locked":
        bottom = font_small2.render("locked", True, (100, 100, 130))
    else:
        color = (130, 225, 150) if affordable else (235, 120, 120)
        bottom = font_small2.render(f"{info['cost']:,} stars", True, color)
    screen.blit(bottom, bottom.get_rect(center=(body.centerx, body.top + 80)))


    if card["name"] == "intern_time" and getIntern()["active"]:
        progress = min(1, (time.time() - lastSpawn) / getIntern()["time"])
        pygame.draw.rect(screen, (20, 20, 40), (body.left + 12, body.bottom - 9, body.width - 24, 4), 0, 2)
        pygame.draw.rect(screen, FRIEND_BLUE, (body.left + 12, body.bottom - 9, int((body.width - 24) * progress), 4), 0, 2)


def drawCount():
    surf = big_font.render(f"{count:,}", True, TEXT_LIGHT)
    t = time.time() - lastGain
    if t < 0.15:
        scale = 1 + 0.12 * (1 - t / 0.15)
        surf = pygame.transform.smoothscale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
    screen.blit(surf, surf.get_rect(center=(WIDTH // 2, 58)))

    label = font_small2.render("stars counted", True, TEXT_SOFT)
    screen.blit(label, label.get_rect(center=(WIDTH // 2, 95)))

    intern = getIntern()
    if intern["active"]:
        stats = f"+{click_count} per look   |   friend: +{intern['count']} every {intern['time']}s"
    else:
        stats = f"+{click_count} per look   |   counting alone"
    stats_text = font_small.render(stats, True, TEXT_SOFT)
    screen.blit(stats_text, stats_text.get_rect(center=(WIDTH // 2, 122)))

    alltime = font_small.render(f"all time: {earned:,}", True, TEXT_SOFT)
    screen.blit(alltime, (90, GROUND_TOP - 22))

    if caught > 0:
        caught_text = font_small.render(f"shooting stars caught: {caught}", True, GOLD)
        screen.blit(caught_text, (90 + alltime.get_width() + 20, GROUND_TOP - 22))

    if earned < 40:
        hint = font_small.render("click the sky to count a star (you can hold it too)", True, TEXT_SOFT)
        screen.blit(hint, hint.get_rect(midright=(WIDTH - 12, GROUND_TOP - 14)))


def drawToast():
    if time.time() > toast["until"]:
        return
    text = font_small2.render(toast["text"], True, (30, 28, 60))
    box = text.get_rect(center=(WIDTH // 2, GROUND_TOP - 40)).inflate(28, 12)
    pygame.draw.rect(screen, (245, 240, 225), box, 0, 14)
    screen.blit(text, text.get_rect(center=box.center))


def drawCooldown(pos):
    if not click or pos[1] >= GROUND_TOP:
        return
    progress = min(1, (time.time() - lastclick) / CLICK_RATE)
    rect = pygame.Rect(pos[0] + 10, pos[1] + 10, 18, 18)
    pygame.draw.circle(screen, (60, 60, 100), rect.center, 9, 3)
    if progress > 0.02:
        pygame.draw.arc(screen, GOLD, rect, math.pi / 2, math.pi / 2 + math.pi * 2 * progress, 3)


background = makeBackground()

running = True
lastclick = 0
lastSpawn = time.time()
lastGain = 0
lastSave = time.time()

while running:
    dt = clock.tick(60) / 1000
    now = time.time()
    mouse_pos = pygame.mouse.get_pos()

    if click and now - lastclick >= CLICK_RATE:
        click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] < GROUND_TOP:
                if not tryCatch(event.pos):
                    hold = True
                    doClick(event.pos)
            else:
                for card in cards:
                    if card["rect"].collidepoint(event.pos):
                        buy(card["name"])

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            hold = False

    if hold and not pygame.mouse.get_pressed()[0]:
        hold = False
    if hold and mouse_pos[1] < GROUND_TOP:
        doClick(mouse_pos)

    if getIntern()["active"] == True:
        if now - lastSpawn >= getIntern()["time"]:
            count_ = getIntern()["count"]
            createText(f"+{count_}", 0, rand=True, color=FRIEND_BLUE)
            lastSpawn = now
            addCount(count_)

    updateShootingStar(dt)

    if now - lastSave >= 15:
        saveData(count, total_count, earned)
        lastSave = now

    screen.blit(background, (0, 0))
    drawSky(dt)
    drawSpotted()
    drawShootingStar()

    for r in ripples[:]:
        age = now - r["createdAt"]
        if age > 0.35:
            ripples.remove(r)
            continue
        radius = int(8 + age * 90)
        pygame.draw.circle(screen, (255, 245, 200), r["pos"], radius, 1)

    for text in text_list[:]:
        elapsed = now - text["createdAt"]
        if elapsed >= TEXT_LIFE:
            text_list.remove(text)
            continue

        text["vel_y"] *= 0.93
        text["y"] += text["vel_y"]
        text["rect"].y = int(text["y"])
        text["surface"].set_alpha(int(255 * (1 - elapsed / TEXT_LIFE)))
        screen.blit(text["surface"], text["rect"])

    drawCount()

    for card in cards:
        drawCard(card, mouse_pos)

    drawToast()
    drawCooldown(mouse_pos)

    pygame.display.flip()

saveData(count, total_count, earned)
pygame.quit()