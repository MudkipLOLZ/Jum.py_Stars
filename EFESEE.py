from pygame import *
from random import *
from math import *
from ctypes import *

user32 = windll.user32
size = width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen = display.set_mode(size,FULLSCREEN)
display.set_icon(image.load("backs/4star.png"))
mouse.set_visible(False)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
magenta = (255, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (69, 69, 69)
stock1 = stock2 = 3
init()
# Font Loading
arial = font.SysFont("Arial Bold", 23)
broadway = font.SysFont("Broadway", 50)
smolBroad = font.SysFont("Broadway", 20)
# Player positions
p1Rect = Rect(500, 100, -20, -45)
p2Rect = Rect(800, 100, -20, -45)
camRect = Rect(20, 20, 1000, 800)
p1 = ["", 0, "undecided", 0, "right", 0, 0, False, False, 0, False, 0, 0, False, 0]
p2 = ["", 0, "undecided", 0, "left", 0, 0, False, False, 0, False, 0, 0, False, 0]
# Player Indexes
direction = 0
frame = 1
leftOrRight = 2
fighter = 3
facing = 4
vx = 5
vy = 6
grounded = 7
lastJump = 8
jumpNum = 9
attack = 10
cooldown = 11
stunUntil = 12
hit = 13
damage = 14
# Animation Index
idle = 0
walk = 1
jump = 2
nLight = 3
sLight = 4
dLight = 5
nSpecial = 6
sSpecial = 7
dSpecial = 8
nAir = 9
sAir = 10
dAir = 11
recovery = 12
hurt = 13
knocked = 14
icon = 15


def addPics(filePath):
    picList = []
    for i in range(100):
        try:
            picList.append(image.load(filePath + str(i) + ".png"))  # Keeps adding pictures from the directory to the list
        except:
            return picList  # Ends the loop when the error (filename not found) occurs

        # spr,                 hitSpr,  dmg,hitStun,xMo,yMo, increment, attackCool, xForce, yForce


killua = [[addPics("killua/idle/"), [], 0, 0, 0, 0, 0.15, 1, 2, 11],
          [addPics("killua/walk/"), [], 0, 0, 0, 0, 0.2, 1, 2, 11],
          [addPics("killua/jump/"), [], 0, 0, 0, 0, 0.2, 1, 2, 11],
          [addPics("killua/nLight/spr/"),
           addPics("killua/nLight/hitSpr/"), 0.5, 0.5, 0, 0, 0.2, 1, 2, 11],
          [addPics("killua/sLight/spr/"),
           addPics("killua/sLight/hitSpr/"), 0.5, 0.5, 0, 0, 0.18, 1, 1, 3],
          [addPics("killua/dLight/spr/"),
           addPics("killua/dLight/hitSpr/"), 1, 0.5, 0, 0, 0.2, 1, 15, 5],
          [addPics("killua/nSpecial/spr/"),
           addPics("killua/nSpecial/hitSpr/"), 1, 0.5, 0, 0, 0.2, 1, 10, 8],
          [addPics("killua/sSpecial/spr/"),
           addPics("killua/sSpecial/hitSpr/"), 1, 0.5, 0, 0, 0.4, 1, 10, 5],
          [addPics("killua/dSpecial/spr/"),
           addPics("killua/dSpecial/hitSpr/"), 1, 0.5, 0, 0, 0.2, 1, 10, 2],
          [addPics("killua/nAir/spr/"),
           addPics("killua/nAir/hitSpr/"), 1, 0.5, 0, 0, 0.2, 1, 1, 10],
          [addPics("killua/sAir/spr/"),
           addPics("killua/sAir/hitSpr/"), 1, 0.5, 8, 2, 0.2, 1, 10, 5],
          [addPics("killua/dAir/spr/"),
           addPics("killua/dAir/hitSpr/"), 1, 0.5, 0, 0, 0.28, 1, 1, -5],
          [addPics("killua/recovery/spr/"),
           addPics("killua/recovery/hitSpr/"), 1, 0.5, 5, 10, 0.3, 1, 15, 10],
          [addPics("killua/hurt/"), [], 0, 0.5, 0, 0, 0.5, 1, 10, 10],
          [addPics("killua/knocked/"), [], 0, 0.5, 0, 0, 0.15, 1, 10, 10],
          image.load("killua/icon.png")]

midoriya = [[addPics("midoriya/idle/"), [], 0, 0, 0, 0, 0.15, 1, 2, 11],
            [addPics("midoriya/walk/"), [], 0, 0, 0, 0, 0.2, 1, 2, 11],
            [addPics("midoriya/jump/"), [], 0, 0, 0, 0, 0.2, 1, 2, 11],
            [addPics("midoriya/nLight/spr/"),
             addPics("midoriya/nLight/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 15, 10],
            [addPics("midoriya/sLight/spr/"),
             addPics("midoriya/sLight/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 15, 10],
            [addPics("midoriya/dLight/spr/"),
             addPics("midoriya/dLight/hitSpr/"), 0, 0.5, 0, 0, 0.14, 1, 15, 10],
            [addPics("midoriya/nSpecial/spr/"),
             addPics("midoriya/nSpecial/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 30, 10],
            [addPics("midoriya/sSpecial/spr/"),
             addPics("midoriya/sSpecial/hitSpr/"), 0, 0.5, 8, 5, 0.3, 1, 30, 10],
            [addPics("midoriya/dSpecial/spr/"),
             addPics("midoriya/dSpecial/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 30, 5],
            [addPics("midoriya/nAir/spr/"),
             addPics("midoriya/nAir/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 10, 10],
            [addPics("midoriya/sAir/spr/"),
             addPics("midoriya/sAir/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 10, 10],
            [addPics("midoriya/dAir/spr/"),
             addPics("midoriya/dAir/hitSpr/"), 0, 0.5, 0, 0, 0.18, 1, 10, 10],
            [addPics("midoriya/recovery/spr/"),
             addPics("midoriya/recovery/hitSpr/"), 1, 0.5, 5, 10, 0.3, 1, 15, 10],
            [addPics("midoriya/hurt/"), [], 0, 0.5, 0, 0, 0.3, 1, 10, 10],
            [addPics("midoriya/knocked/"), [], 0, 1, 0, 0, 0.15, 1, 10, 10],
            image.load("midoriya/icon.png")]

goku = [[addPics("goku/idle/"), [], 0, 0, 0, 0, 0.15, 1, 2, 11],
        [addPics("goku/walk/"), [], 0, 0, 0, 0, 0.2, 1, 2, 11],
        [addPics("goku/jump/"), [], 0, 0, 0, 0, 0.16, 1, 2, 11],
        [addPics("goku/nLight/spr/"),
         addPics("goku/nLight/hitSpr/"), 0, 0.5, 0, 0, 0.2, 0.5, 15, 10],
        [addPics("goku/sLight/spr/"),
         addPics("goku/sLight/hitSpr/"), 0, 0.5, 0, 0, 0.22, 1, 15, 10],
        [addPics("goku/dLight/spr/"),
         addPics("goku/dLight/hitSpr/"), 0, 0.5, 0, 0, 0.3, 1, 15, 10],
        [addPics("goku/nSpecial/spr/"),
         addPics("goku/nSpecial/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 30, 10],
        [addPics("goku/sSpecial/spr/"),
         addPics("goku/sSpecial/hitSpr/"), 0, 0.5, 0, 0, 0.3, 1, 30, 10],
        [addPics("goku/dSpecial/spr/"),
         addPics("goku/dSpecial/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 30, 5],
        [addPics("goku/nAir/spr/"),
         addPics("goku/nAir/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 15, 10],
        [addPics("goku/sAir/spr/"),
         addPics("goku/sAir/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 15, 10],
        [addPics("goku/dAir/spr/"),
         addPics("goku/dAir/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 15, 10],
        [addPics("goku/recovery/spr/"),
         addPics("goku/recovery/hitSpr/"), 0, 0.5, 5, 10, 0.1, 1, 15, 10],
        [addPics("goku/hurt/"), [], 0, 0.5, 0, 0, 0.2, 1, 15, 10],
        [addPics("goku/knocked/"), [], 0, 0.5, 0, 0, 0.2, 1, 15, 10],
        image.load("goku/icon.png")]

naruto = [[addPics("naruto/idle/"), [], 0, 0, 0, 0, 0.15, 2, 2, 11],
          [addPics("naruto/walk/"), [], 0, 0, 0, 0, 0.2, 2, 2, 11],
          [addPics("naruto/jump/"), [], 0, 0, 0, 0, 0.16, 2, 2, 11],
          [addPics("naruto/nLight/spr/"),
           addPics("naruto/nLight/hitSpr/"), 0, 0.5, 0, 0, 0.2, 1, 15, 10],
          [addPics("naruto/sLight/spr/"),
           addPics("naruto/sLight/hitSpr/"), 0, 0.5, 0, 0, 0.25, 2, 15, 10],
          [addPics("naruto/dLight/spr/"),
           addPics("naruto/dLight/hitSpr/"), 0, 0.5, 0, 0, 0.18, 2, 15, 10],
          [addPics("naruto/nSpecial/spr/"),
           addPics("naruto/nSpecial/hitSpr/"), 0, 0.5, 0, 0, 0.25, 2, 30, 10],
          [addPics("naruto/sSpecial/spr/"),
           addPics("naruto/sSpecial/hitSpr/"), 0, 0.5, 0, 0, 0.18, 2, 30, 10],
          [addPics("naruto/dSpecial/spr/"),
           addPics("naruto/dSpecial/hitSpr/"), 0, 0.5, 0, 0, 0.2, 2, 30, 5],
          [addPics("naruto/nAir/spr/"),
           addPics("naruto/nAir/hitSpr/"), 0, 0.5, 0, 0, 0.2, 2, 10, 10],
          [addPics("naruto/sAir/spr/"),
           addPics("naruto/sAir/hitSpr/"), 0, 0.5, 0, 0, 0.2, 2, 10, 10],
          [addPics("naruto/dAir/spr/"),
           addPics("naruto/dAir/hitSpr/"), 0, 0.5, -7, -7, 0.18, 2, 10, 10],
          [addPics("naruto/recovery/spr/"),
           addPics("naruto/recovery/hitSpr/"), 1, 0.5, 5, 10, 0.3, 1, 15, 10],
          [addPics("naruto/hurt/"), [], 0, 0.5, 0, 0, 0.2, 1, 15, 10],
          [addPics("naruto/knocked/"), [], 0, 0.5, 0, 0, 0.2, 1, 15, 10],
          image.load("naruto/icon.png")]

charList = [goku, killua, midoriya, naruto]
# Individual sprite list indexes
spr = 0
hitSpr = 1
dmg = 2
hitStun = 3
xMo = 4
yMo = 5
increment = 6
attackCool = 7
xForce = 8
yForce = 9
myClock = time.Clock()
frames = 0
seconds = 0
fps = 60
blastFrame = 10
blastPos = (0, 0)
# Map
map = [
    Rect(400, 250, 100, 200),
    Rect(400, 550, 650, 100),
    Rect(950, 250, 100, 200)
]
# Misc Loads
stages = transform.scale(image.load("maps/battlefield.png"), (1200, 800))
back = image.load("backs/background.png")
back = transform.scale(back, (int(back.get_width() / back.get_height() * height), height))
charSelBack = image.load("backs/charSel.jpg")
charSelBack = transform.scale(charSelBack, (int(charSelBack.get_width() / charSelBack.get_height() * height), height))
blastAnim = [image.load("misc/death/" + str(i) + ".png") for i in range(10)]
title = image.load("backs/title.png")
opening = mixer.Sound("sounds/OP.ogg")
ping = mixer.Sound("sounds/ping.ogg")
enter = mixer.Sound("sounds/enter.ogg")
yay = mixer.Sound("sounds/yay.ogg")
woof = mixer.Sound("sounds/woof.ogg")
goBack = mixer.Sound("sounds/back.ogg")
punches = [mixer.Sound("sounds/pun1.wav"), mixer.Sound("sounds/pun2.wav")]
blast = mixer.Sound("sounds/blast.ogg")


# Different things like the walls and the surface

def timer():
    global fps
    global frames
    global seconds
    seconds += 1 / 60


def fadeScreen(transInt):  # Fades into black
    # Help from Aarmaan Rhandawa
    alphaSurface = Surface((width, height), SRCALPHA)  # Making an alpha surface
    alphaSurface.fill((0, 0, 0, transInt))  # Fill the surface with a black background
    screen.blit(alphaSurface, (0, 0))  # Blit it into the actual screen


def nextSprite(p1, p2, light1, heavy1, light2, heavy2):
    # Checking player stun
    if p1[stunUntil] > 0:
        p1Stun = True
    else:
        p1Stun = False
    if p2[stunUntil] > 0:
        p2Stun = True
    else:
        p2Stun = False
    keys = key.get_pressed()
    # The next picture to be blitted to P1's position
    # Detemining attack (if any)
    if light1 and p1[cooldown] <= 0:
        if p1[grounded]:  # Light attack
            if keys[K_s] and (not p1[attack] or p1[attack] == dLight):
                p1[attack] = dLight
                p1[frame] = 0
            elif p1[direction] != "none" and (not p1[attack] or p1[attack] == sLight):
                p1[attack] = sLight
                p1[frame] = 0
            elif p1[direction] == "none" and (not p1[attack] or p1[attack] == nLight):
                p1[attack] = nLight
                p1[frame] = 0
            p1[cooldown] = p1[fighter][p1[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        else:  # Air attack
            if keys[K_s] and (not p1[attack] or p1[attack] == dAir):
                p1[attack] = dAir
                p1[frame] = 0
            elif p1[direction] != "none" and (not p1[attack] or p1[attack] == sAir):
                p1[attack] = sAir
                p1[frame] = 0
            elif p1[direction] == "none" and (not p1[attack] or p1[attack] == nAir):
                p1[attack] = nAir
                p1[frame] = 0
            p1[cooldown] = p1[fighter][p1[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        # Momentum
        p1[vx] += p1[fighter][p1[attack]][xMo] - 2 * p1[fighter][p1[attack]][xMo] * (p1[facing] == "left")
        p1[vy] += -p1[fighter][p1[attack]][yMo]
    if heavy1 and p1[cooldown] <= 0:
        if p1[grounded]:
            if keys[K_s] and (not p1[attack] or p1[attack] == dSpecial):
                p1[attack] = dSpecial
                p1[frame] = 0
            elif p1[direction] != "none" and (not p1[attack] or p1[attack] == sSpecial):
                p1[attack] = sSpecial
                p1[frame] = 0
            elif p1[direction] == "none" and (not p1[attack] or p1[attack] == nSpecial):
                p1[attack] = nSpecial
                p1[frame] = 0
            p1[cooldown] = p1[fighter][p1[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        elif p1[jumpNum] > -1:
            p1[attack] = recovery
            p1[jumpNum] -= 1
            p1[cooldown] = p1[fighter][p1[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        # Momentum
        p1[vx] = p1[fighter][p1[attack]][xMo] - 2 * p1[fighter][p1[attack]][xMo] * (p1[facing] == "left")
        p1[vy] = -p1[fighter][p1[attack]][yMo]
    # Choosing next sprite
    if p1Stun:  # Knocked animation
        if sqrt(p1[vy] ** 2 + p1[vx] ** 2) > 8:
            p1[frame] += p1[fighter][knocked][increment]
            p1[frame] %= len(p1[fighter][knocked][spr])
            try:
                p1Pic = transform.rotate(p1[fighter][knocked][spr][int(p1[frame])], -abs(degrees(atan(p1[vy] / p1[vx]))))  # Rotates the character based on the vector
            except:
                p1Pic = p1[fighter][knocked][spr][int(p1[frame])]
            p1Hit = p1Pic
        else:  # Hurt animation for slower knockback
            if int(p1[frame]) > len(p1[fighter][hurt][spr]) - 1:
                p1[frame] = 0
            if int(p1[frame]) < len(p1[fighter][hurt][spr]) - 1:
                p1[frame] += p1[fighter][hurt][increment]
            p1Pic = p1[fighter][hurt][spr][int(p1[frame])]
            p1Hit = p1Pic
    else:
        if p1[attack] != False:  # Attack Sprite Frame Finder
            if int(p1[frame]) > len(p1[fighter][p1[attack]][spr]):
                p1[frame] = 0
            elif int(p1[frame]) < len(p1[fighter][p1[attack]][spr]) - 1:
                p1[frame] += p1[fighter][p1[attack]][increment]
                p1Pic = p1[fighter][p1[attack]][spr][int(p1[frame])]
                p1Hit = p1[fighter][p1[attack]][hitSpr][int(p1[frame])]
            else:
                p1[attack] = False
        if not p1[attack]:  # Walking animation
            if p1[direction] != "none" and p1[grounded]:
                p1[frame] += p1[fighter][walk][increment]
                p1[frame] %= len(p1[fighter][walk][spr])
                p1Pic = p1[fighter][walk][spr][int(p1[frame])]
            elif not p1[grounded]:  # Jump animation
                if int(p1[frame]) > len(p1[fighter][jump][spr]) - 1:
                    p1[frame] = 0
                if int(p1[frame]) < len(p1[fighter][jump][spr]) - 1:
                    p1[frame] += p1[fighter][jump][increment]
                p1Pic = p1[fighter][jump][spr][int(p1[frame])]
            elif p1[grounded]:  # Idle animation
                p1[frame] += p1[fighter][idle][increment]
                p1[frame] %= len(p1[fighter][idle][spr])
                p1Pic = p1[fighter][idle][spr][int(p1[frame])]
            p1Hit = p1Pic
    # The next picture to be blitted to P2's position
    # Determining attack (if any)
    if light2 and p2[cooldown] <= 0:
        if p2[grounded]:
            if keys[K_DOWN]:
                p2[attack] = dLight
                p2[frame] = 0
            elif p2[direction] != "none":
                p2[attack] = sLight
                p2[frame] = 0
            elif p2[direction] == "none":
                p2[attack] = nLight
                p2[frame] = 0
            p2[cooldown] = p2[fighter][p2[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        else:
            if keys[K_DOWN]:
                p2[attack] = dAir
                p2[frame] = 0
            elif p2[direction] != "none":
                p2[attack] = sAir
                p2[frame] = 0
            elif p2[direction] == "none":
                p2[attack] = nAir
                p2[frame] = 0
            p2[cooldown] = p2[fighter][p2[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        # Momentum
        p2[vx] += p2[fighter][p2[attack]][xMo] - 2 * p2[fighter][p2[attack]][xMo] * (p2[facing] == "left")
        p2[vy] += -p2[fighter][p2[attack]][yMo]
    if heavy2 and p2[cooldown] <= 0:
        if p2[grounded]:
            if keys[K_DOWN]:
                p2[attack] = dSpecial
                p2[frame] = 0
            elif p2[direction] != "none":
                p2[attack] = sSpecial
                p2[frame] = 0
            elif p2[direction] == "none":
                p2[attack] = nSpecial
                p2[frame] = 0
            p2[cooldown] = p2[fighter][p2[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        elif p2[jumpNum] > -1:
            p2[attack] = recovery
            p2[jumpNum] -= 1
            p2[cooldown] = p2[fighter][p2[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        p2[vx] += p2[fighter][p2[attack]][xMo] - 2 * p2[fighter][p2[attack]][xMo] * (p2[facing] == "left")
        p2[vy] += -p2[fighter][p2[attack]][yMo]
    # Choosing next sprite
    if p2Stun:  # Knocked animation
        if sqrt(p2[vy] ** 2 + p2[vx] ** 2) > 6:
            p2[frame] += p2[fighter][knocked][increment]
            p2[frame] %= len(p2[fighter][knocked][spr])
            try:
                p2Pic = transform.rotate(p2[fighter][knocked][spr][int(p2[frame])], -abs(degrees(atan(p2[vy] / p2[vx]))))  # Rotates the character based on the vector
            except:
                p2Pic = transform.rotate(p2[fighter][knocked][spr][int(p2[frame])], -abs(degrees(atan(p2[vy] / 1))))
            p2Hit = p2Pic
        else:
            p2[frame] += p2[fighter][hurt][increment]
            p2[frame] %= len(p2[fighter][hurt][spr])
            p2Pic = p2[fighter][hurt][spr][int(p2[frame])]
            p2Hit = p2Pic
    else:
        if p2[attack] != False:  # Attack animation
            if int(p2[frame]) > len(p2[fighter][p2[attack]][spr]):
                p2[frame] = 0
            elif int(p2[frame]) < len(p2[fighter][p2[attack]][spr]) - 1:
                p2[frame] += p2[fighter][p2[attack]][increment]
                p2Pic = p2[fighter][p2[attack]][spr][int(p2[frame])]
                p2Hit = p2[fighter][p2[attack]][hitSpr][int(p2[frame])]
            else:
                p2[attack] = False
        if not p2[attack]:  # Walk animation
            if p2[direction] != "none" and p2[grounded]:
                p2[frame] += p2[fighter][walk][increment]
                p2[frame] %= len(p2[fighter][walk][spr])
                p2Pic = p2[fighter][walk][spr][int(p2[frame])]
            elif not p2[grounded]:  # Jump animation
                if int(p2[frame]) > len(p2[fighter][jump][spr]) - 1:
                    p2[frame] = 0
                if int(p2[frame]) < len(p2[fighter][jump][spr]) - 1:
                    p2[frame] += p2[fighter][jump][increment]
                p2Pic = p2[fighter][jump][spr][int(p2[frame])]
            elif p2[grounded]:  # Idle animation
                p2[frame] += p2[fighter][idle][increment]
                p2[frame] %= len(p2[fighter][idle][spr])
                p2Pic = p2[fighter][idle][spr][int(p2[frame])]
            p2Hit = p2Pic
    # Flips if Nesessary
    if p1[facing] == "left":
        p1Pic = transform.flip(p1Pic, True, False)
        p1Hit = transform.flip(p1Hit, True, False)
    if p2[facing] == "left":
        p2Pic = transform.flip(p2Pic, True, False)
        p2Hit = transform.flip(p2Hit, True, False)
    return p1Pic, p2Pic, p1Hit, p2Hit


def singleSprite(p1, p2, light1, heavy1, light2, heavy2):
    # Checking player stun
    if p1[stunUntil] > 0:
        p1Stun = True
    else:
        p1Stun = False
    if p2[stunUntil] > 0:
        p2Stun = True
    else:
        p2Stun = False
    keys = key.get_pressed()
    cpuLeft, cpuRight, cpuJump, cpuFall, cpuHeavy, cpuLight = cpuInput(p1, p2, p1Rect, p2Rect)
    # The next picture to be blitted to P1's position
    # Detemining attack (if any)
    if light1 and p1[cooldown] <= 0:
        if p1[grounded]:  # Light attack
            if keys[K_s] and (not p1[attack] or p1[attack] == dLight):
                p1[attack] = dLight
                p1[frame] = 0
            elif p1[direction] != "none" and (not p1[attack] or p1[attack] == sLight):
                p1[attack] = sLight
                p1[frame] = 0
            elif p1[direction] == "none" and (not p1[attack] or p1[attack] == nLight):
                p1[attack] = nLight
                p1[frame] = 0
            p1[cooldown] = p1[fighter][p1[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        else:  # Air attack
            if keys[K_s] and (not p1[attack] or p1[attack] == dAir):
                p1[attack] = dAir
                p1[frame] = 0
            elif p1[direction] != "none" and (not p1[attack] or p1[attack] == sAir):
                p1[attack] = sAir
                p1[frame] = 0
            elif p1[direction] == "none" and (not p1[attack] or p1[attack] == nAir):
                p1[attack] = nAir
                p1[frame] = 0
            p1[cooldown] = p1[fighter][p1[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        # Momentum
        p1[vx] += p1[fighter][p1[attack]][xMo] - 2 * p1[fighter][p1[attack]][xMo] * (p1[facing] == "left")
        p1[vy] += -p1[fighter][p1[attack]][yMo]
    if heavy1 and p1[cooldown] <= 0:
        if p1[grounded]:
            if keys[K_s] and (not p1[attack] or p1[attack] == dSpecial):
                p1[attack] = dSpecial
                p1[frame] = 0
            elif p1[direction] != "none" and (not p1[attack] or p1[attack] == sSpecial):
                p1[attack] = sSpecial
                p1[frame] = 0
            elif p1[direction] == "none" and (not p1[attack] or p1[attack] == nSpecial):
                p1[attack] = nSpecial
                p1[frame] = 0
            p1[cooldown] = p1[fighter][p1[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        elif p1[jumpNum] > -1:
            p1[attack] = recovery
            p1[jumpNum] -= 1
            p1[cooldown] = p1[fighter][p1[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        # Momentum
        p1[vx] = p1[fighter][p1[attack]][xMo] - 2 * p1[fighter][p1[attack]][xMo] * (p1[facing] == "left")
        p1[vy] = -p1[fighter][p1[attack]][yMo]
    # Choosing next sprite
    if p1Stun:  # Knocked animation
        if sqrt(p1[vy] ** 2 + p1[vx] ** 2) > 8:
            p1[frame] += p1[fighter][knocked][increment]
            p1[frame] %= len(p1[fighter][knocked][spr])
            try:
                p1Pic = transform.rotate(p1[fighter][knocked][spr][int(p1[frame])], -abs(degrees(atan(p1[vy] / p1[vx]))))  # Rotates the character based on the vector
            except:
                p1Pic = p1[fighter][knocked][spr][int(p1[frame])]
            p1Hit = p1Pic
        else:  # Hurt animation for slower knockback
            if int(p1[frame]) > len(p1[fighter][hurt][spr]) - 1:
                p1[frame] = 0
            if int(p1[frame]) < len(p1[fighter][hurt][spr]) - 1:
                p1[frame] += p1[fighter][hurt][increment]
            p1Pic = p1[fighter][hurt][spr][int(p1[frame])]
            p1Hit = p1Pic
    else:
        if p1[attack] != False:  # Attack Sprite Frame Finder
            if int(p1[frame]) > len(p1[fighter][p1[attack]][spr]):
                p1[frame] = 0
            elif int(p1[frame]) < len(p1[fighter][p1[attack]][spr]) - 1:
                p1[frame] += p1[fighter][p1[attack]][increment]
                p1Pic = p1[fighter][p1[attack]][spr][int(p1[frame])]
                p1Hit = p1[fighter][p1[attack]][hitSpr][int(p1[frame])]
            else:
                p1[attack] = False
        if not p1[attack]:  # Walking animation
            if p1[direction] != "none" and p1[grounded]:
                p1[frame] += p1[fighter][walk][increment]
                p1[frame] %= len(p1[fighter][walk][spr])
                p1Pic = p1[fighter][walk][spr][int(p1[frame])]
            elif not p1[grounded]:  # Jump animation
                if int(p1[frame]) > len(p1[fighter][jump][spr]) - 1:
                    p1[frame] = 0
                if int(p1[frame]) < len(p1[fighter][jump][spr]) - 1:
                    p1[frame] += p1[fighter][jump][increment]
                p1Pic = p1[fighter][jump][spr][int(p1[frame])]
            elif p1[grounded]:  # Idle animation
                p1[frame] += p1[fighter][idle][increment]
                p1[frame] %= len(p1[fighter][idle][spr])
                p1Pic = p1[fighter][idle][spr][int(p1[frame])]
            p1Hit = p1Pic
    # The next picture to be blitted to P2's position
    # Determining attack (if any)
    if cpuLight and p2[cooldown] <= 0:
        if p2[grounded]:
            if cpuFall:
                p2[attack] = dLight
                p2[frame] = 0
            elif p2[direction] != "none":
                p2[attack] = sLight
                p2[frame] = 0
            elif p2[direction] == "none":
                p2[attack] = nLight
                p2[frame] = 0
            p2[cooldown] = p2[fighter][p2[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        else:
            if cpuFall:
                p2[attack] = dAir
                p2[frame] = 0
            elif p2[direction] != "none":
                p2[attack] = sAir
                p2[frame] = 0
            elif p2[direction] == "none":
                p2[attack] = nAir
                p2[frame] = 0
            p2[cooldown] = p2[fighter][p2[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        # Momentum
        p2[vx] += p2[fighter][p2[attack]][xMo] - 2 * p2[fighter][p2[attack]][xMo] * (p2[facing] == "left")
        p2[vy] += -p2[fighter][p2[attack]][yMo]
    if cpuHeavy and p2[cooldown] <= 0:
        if p2[grounded]:
            if cpuFall:
                p2[attack] = dSpecial
                p2[frame] = 0
            elif p2[direction] != "none":
                p2[attack] = sSpecial
                p2[frame] = 0
            elif p2[direction] == "none":
                p2[attack] = nSpecial
                p2[frame] = 0
            p2[cooldown] = p2[fighter][p2[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        elif p2[jumpNum] > -1:
            p2[attack] = recovery
            p2[jumpNum] -= 1
            p2[cooldown] = p2[fighter][p2[attack]][attackCool]  # Applys cooldown at the beggining of the attack
        p2[vx] += p2[fighter][p2[attack]][xMo] - 2 * p2[fighter][p2[attack]][xMo] * (p2[facing] == "left")
        p2[vy] += -p2[fighter][p2[attack]][yMo]
    # Choosing next sprite
    if p2Stun:  # Knocked animation
        if sqrt(p2[vy] ** 2 + p2[vx] ** 2) > 6:
            p2[frame] += p2[fighter][knocked][increment]
            p2[frame] %= len(p2[fighter][knocked][spr])
            try:
                p2Pic = transform.rotate(p2[fighter][knocked][spr][int(p2[frame])], -abs(degrees(atan(p2[vy] / p2[vx]))))  # Rotates the character based on the vector
            except:
                p2Pic = p2[fighter][knocked][spr][int(p2[frame])]
            p2Hit = p2Pic
        else:
            p2[frame] += p2[fighter][hurt][increment]
            p2[frame] %= len(p2[fighter][hurt][spr])
            p2Pic = p2[fighter][hurt][spr][int(p2[frame])]
            p2Hit = p2Pic
    else:
        if p2[attack] != False:  # Attack animation
            if int(p2[frame]) > len(p2[fighter][p2[attack]][spr]):
                p2[frame] = 0
            elif int(p2[frame]) < len(p2[fighter][p2[attack]][spr]) - 1:
                p2[frame] += p2[fighter][p2[attack]][increment]
                p2Pic = p2[fighter][p2[attack]][spr][int(p2[frame])]
                p2Hit = p2[fighter][p2[attack]][hitSpr][int(p2[frame])]
            else:
                p2[attack] = False
        if not p2[attack]:  # Walk animation
            if p2[direction] != "none" and p2[grounded]:
                p2[frame] += p2[fighter][walk][increment]
                p2[frame] %= len(p2[fighter][walk][spr])
                p2Pic = p2[fighter][walk][spr][int(p2[frame])]
            elif not p2[grounded]:  # Jump animation
                if int(p2[frame]) > len(p2[fighter][jump][spr]) - 1:
                    p2[frame] = 0
                if int(p2[frame]) < len(p2[fighter][jump][spr]) - 1:
                    p2[frame] += p2[fighter][jump][increment]
                p2Pic = p2[fighter][jump][spr][int(p2[frame])]
            elif p2[grounded]:  # Idle animation
                p2[frame] += p2[fighter][idle][increment]
                p2[frame] %= len(p2[fighter][idle][spr])
                p2Pic = p2[fighter][idle][spr][int(p2[frame])]
            p2Hit = p2Pic
    # Flips if Nesessary
    if p1[facing] == "left":
        p1Pic = transform.flip(p1Pic, True, False)
        p1Hit = transform.flip(p1Hit, True, False)
    if p2[facing] == "left":
        p2Pic = transform.flip(p2Pic, True, False)
        p2Hit = transform.flip(p2Hit, True, False)
    return p1Pic, p2Pic, p1Hit, p2Hit


def checkHit(p1, p2, p1Rect, p2Rect):
    points = [(0, 20), (0, -20), (10, 0), (-10, 0), (8, 9), (-8, 9), (-8, -9), (8, -9)]  # Multiple points to check for the colour collision
    global stock1, stock2
    # Drawing Hitboxes
    if not p1[grounded] and p1[attack] != False:
        screen.blit(p1Hit, (p1Rect[0] - p1Pic.get_width() // 2, p1Rect[1] - p1Pic.get_height() // 2))
    else:
        screen.blit(p1Hit, (p1Rect[0] - p1Pic.get_width() // 2, p1Rect[1] - p1Pic.get_height()))
    if not p2[grounded] and p2[attack] != False:
        screen.blit(p2Hit, (p2Rect[0] - p2Pic.get_width() // 2, p2Rect[1] - p2Pic.get_height() // 2))
    else:
        screen.blit(p2Hit, (p2Rect[0] - p2Pic.get_width() // 2, p2Rect[1] - p2Pic.get_height()))
    global blastPos, blastFrame
    # Goes through every frame to check for the hitbox color
    for i in points:
        try:
            # For some reason, the hitbox changes when the player is not grounded, so this is to comphensate
            if p1[grounded] and not p1[attack]:
                if screen.get_at((p1Rect[0] - i[0], p1Rect[1] - 25 - i[1])) == (69, 255, 69):
                    p1[stunUntil] = p2[fighter][p2[attack]][hitStun]
                    p1[hit] = True
                    p1[frame] = 0
                    p1[damage] += p2[fighter][p2[attack]][dmg]
                    playSound(choice(punches), "effect")
                    break
                else:
                    p1[hit] = False
            else:
                if screen.get_at((p1Rect[0] - i[0], p1Rect[1] - 25 - i[1] + 20)) == (69, 255, 69):
                    p1[stunUntil] = p2[fighter][p2[attack]][hitStun]
                    p1[hit] = True
                    p1[frame] = 0
                    p1[damage] += p2[fighter][p2[attack]][dmg]
                    playSound(choice(punches), "effect")
                    break
                else:
                    p1[hit] = False
        except:  # Error occurs when screen.get_at() is called on a pixel outside of the screen, so If this occurs the player "dies"
            playSound(blast, "effect")
            blastFrame = p1[vy] = p1[vx] = 0
            blastPos = (p1Rect[0], p1Rect[1])
            p1Rect[0], p1Rect[1] = width // 2 - 100, height // 2 - 100
            p1[damage] = 0
            stock1 -= 1
    # Goes through every frame to check for the hitbox color
    for i in points:
        try:
            # For some reason, the hitbox changes when the player is not grounded, so this is to comphensate
            if p2[grounded] and not p2[attack]:
                if screen.get_at((p2Rect[0] - i[0], p2Rect[1] - 25 - i[1])) == (69, 255, 69):
                    p2[stunUntil] = p1[fighter][p1[attack]][hitStun]
                    p2[hit] = True
                    p2[frame] = 0
                    p2[damage] += p1[fighter][p1[attack]][dmg]
                    playSound(choice(punches), "effect")
                    break
                else:
                    p2[hit] = False
            else:
                if screen.get_at((p2Rect[0] - i[0], p2Rect[1] - 25 - i[1] + 20)) == (69, 255, 69):
                    p2[stunUntil] = p1[fighter][p1[attack]][hitStun]
                    p2[hit] = True
                    print(int(p2[frame]))
                    p2[frame] = 0
                    p2[damage] += p1[fighter][p1[attack]][dmg]
                    playSound(choice(punches), "effect")
                    break
                else:
                    p2[hit] = False
        except:  # Error occurs when screen.get_at() is called on a pixel outside of the screen, so If this occurs the player "dies"
            playSound(blast, "effect")
            blastFrame = p2[vy] = p2[vx] = 0
            blastPos = (p2Rect[0], p2Rect[1])
            p2Rect[0], p2Rect[1] = width // 2 + 100, height // 2 - 100
            p1[damage] = 0
            stock2 -= 1


def movePs(p1, p2, p1Rect, p2Rect):
    global stock1, stock2
    keys = key.get_pressed()
    # Determines stun
    if p1[stunUntil] > 0:
        p1Stun = True
    else:
        p1Stun = False
        p1[stunUntil] = 0
    if p2[stunUntil] > 0:
        p2Stun = True
    else:
        p2Stun = False
        p2[stunUntil] = 0
    # Deacreases the stun and cooldown time
    p1[stunUntil] -= 1 / 60
    p2[stunUntil] -= 1 / 60
    p1[cooldown] -= 1 / 60
    p2[cooldown] -= 1 / 60
    checkHit(p1, p2, p1Rect, p2Rect)
    # Checks if Player 1 is on the ground
    for i in map:
        if i.collidepoint((p1Rect[0], p1Rect[1])):
            if p1Rect[0] >= i[0] + i[2] - 10:
                p1Rect[0] = i[0] + i[2]
                if p1Stun:  # Bounces off the map if the player is attacked
                    p1[vx] *= -1
                if p1[vx] < 0:
                    p1[vx] = 0
                break
            elif p1Rect[0] <= i[0] + 10:
                p1Rect[0] = i[0] - 1
                if p1Stun:  # Bounces off the map if the player is attacked
                    p1[vx] *= -1
                if p1[vx] > 0:
                    p1[vx] = 0
                break
            elif p1Rect[1] <= i[1] + 10 and p1[attack] != nAir and p1[attack] != sAir and p1[attack] != dAir and p1[attack] != recovery:
                p1[grounded] = True
                p1[vy] = 0
                p1Rect[1] = i[1] + 1
                p1[jumpNum] = 3
            elif p1[attack] != nAir or p1[attack] != sAir or p1[attack] != dAir or p1[attack] != recovery:  # prevents falling through the map when attacking
                p1[vy] = 0
                p1Rect[1] = i[1] + 1
            break
        # If he's not, apply gravity
        elif p1[vy] <= 5 and map.index(i) == 2:
            p1[grounded] = False
            p1[vy] += 0.35
            if p1[jumpNum] == 3:
                p1[jumpNum] = 2
        # If they collide with the bottom of the map
        if i.collidepoint((p1Rect[0], p1Rect[1] + p1Rect[3])):
            if p1Stun:  # Bounces off the map if the player is attacked
                p1[vy] *= -1
            else:
                p1[vy] = 0
                p1Rect[1] = i[1] + i[3] - p1Rect[3]
    # Checks if Player 2 is on the ground (negates gravity if True)
    for i in map:
        if i.collidepoint((p2Rect[0], p2Rect[1])):
            if p2Rect[0] >= i[0] + i[2] - 10:
                p2Rect[0] = i[0] + i[2]
                if p2Stun:  # Bounces off the map if the player is attacked
                    p2[vx] *= -1
                if p2[vx] < 0:
                    p2[vx] = 0
                break
            elif p2Rect[0] <= i[0] + 10:
                p2Rect[0] = i[0] - 1
                if p2Stun:  # Bounces off the map if the player is attacked
                    p2[vx] *= -1
                if p2[vx] > 0:
                    p2[vx] = 0
                break
            elif p2Rect[1] <= i[1] + 10 and p2[attack] != nAir and p2[attack] != sAir and p2[attack] != dAir and p2[attack] != recovery:
                p2[grounded] = True
                p2[vy] = 0
                p2Rect[1] = i[1] + 1
                p2[jumpNum] = 3
            elif p2[attack] != nAir or p2[attack] != sAir or p2[attack] != dAir or p2[attack] != recovery:
                p2[vy] = 0
                p2Rect[1] = i[1]
            break
        # If he's not, apply gravity
        elif p2[vy] <= 5 and map.index(i) == 2:
            p2[grounded] = False
            p2[vy] += 0.35
            if p2[jumpNum] == 3:
                p2[jumpNum] = 2
        # If they collide with the bottom of the map
        if i.collidepoint((p2Rect[0], p2Rect[1] + p2Rect[3])):
            if p2Stun:  # Bounces off the map if the player is attacked
                p2[vy] *= -1
            else:
                p2[vy] = 0
                p2Rect[1] = i[1] + i[3] - p1Rect[3]
    # P1 Movement Calculations
    # Reflex Click Bug (if they click one way and then the other at the same time)
    if not p1[attack] and not p1Stun:
        if keys[K_d] and keys[K_a]:
            if p1[leftOrRight] == "undecided":
                if p1[direction] == "left":
                    p1[direction] = "right"
                    p1[facing] = "right"
                    p1[leftOrRight] = "decided"
                elif p1[direction] == "right":
                    p1[direction] = "left"
                    p1[facing] = "left"
                    p1[leftOrRight] = "decided"
        else:
            p1[leftOrRight] = "undecided"
    if keys[K_a] and not keys[K_d] and not p1[attack]:
        p1[direction] = "left"
        p1[facing] = "left"
    elif keys[K_d] and not keys[K_a] and not p1[attack]:
        p1[direction] = "right"
        p1[facing] = "right"
    elif not keys[K_a] and not keys[K_d]:
        p1[direction] = "none"
    # Movement
    if p1[direction] == "right" and p1[vx] < 4 and not p1[attack]:
        p1[vx] += 0.5
    elif p1[direction] == "left" and p1[vx] > -4 and not p1[attack]:
        p1[vx] -= 0.5
    # Fastfall
    if keys[K_s] and not p1[grounded] and p1[vy] < 8:
        p1[vy] += 0.5
    # Drag
    if p1[direction] == "none" or p1[attack] != False or p1[vx] > 4 or p1[vx] < -4:
        p1[vx] /= 1.1
    # Only jumps once on click
    if keys[K_w] and not p1[lastJump] and p1[jumpNum] > 0 and not p1[attack] and not p1Stun:  # Knocked animation
        p1[vy] = -10
        p1[frame] = 0
        p1[jumpNum] -= 1
    # Knockback Calcutlation
    if p1[hit] == True:
        p1[vx] = (p2[fighter][p2[attack]][xForce] + p1[damage]) - 2 * (p2[fighter][p2[attack]][xForce] + p1[damage]) * (p2[facing] == "left")
        p1[vy] = -p2[fighter][p2[attack]][yForce] - p1[damage]

    # P2 Movement Calculations
    # Reflex Click Bug (if they click one way and then the other at the same time)
    if not p2[attack] and not p2Stun:
        if keys[K_RIGHT] and keys[K_LEFT]:
            if p2[leftOrRight] == "undecided":
                if p2[direction] == "left":
                    p2[direction] = "right"
                    p2[facing] = "right"
                    p2[leftOrRight] = "decided"
                elif p2[direction] == "right":
                    p2[direction] = "left"
                    p2[facing] = "left"
                    p2[leftOrRight] = "decided"
        else:
            p2[leftOrRight] = "undecided"
    if keys[K_LEFT] and not keys[K_RIGHT] and not p2[attack]:
        p2[direction] = "left"
        p2[facing] = "left"
    if keys[K_RIGHT] and not keys[K_LEFT] and not p2[attack]:
        p2[direction] = "right"
        p2[facing] = "right"
    if not keys[K_LEFT] and not keys[K_RIGHT]:
        p2[direction] = "none"
    # Movement
    if p2[direction] == "right" and p2[vx] < 4 and not p2[attack]:
        p2[vx] += 0.5
    elif p2[direction] == "left" and p2[vx] > -4 and not p2[attack]:
        p2[vx] -= 0.5
    # Fastfall
    if keys[K_DOWN] and not p2[grounded] and p2[vy] < 8:
        p2[vy] += 0.5
    # Drag
    if p2[direction] == "none" or p2[attack] != False or p2[vx] > 4 or p2[vx] < -4:
        p2[vx] /= 1.1
    # Only jumps once on click
    if keys[K_UP] and not p2[lastJump] and p2[jumpNum] > 0 and not p2[attack] and not p2Stun:  # Knocked animation
        p2[vy] = -10
        p2[frame] = 0
        p2[jumpNum] -= 1
    # Knockback Calculation
    if p2[hit] == True:
        p2[vx] = (p1[fighter][p1[attack]][xForce] + p2[damage]) - 2 * (p1[fighter][p1[attack]][xForce] + p2[damage]) * (p1[facing] == "left")
        p2[vy] = -p1[fighter][p1[attack]][yForce] - p2[damage]
    # Applying forces
    p1Rect[1] += int(p1[vy])
    p1Rect[0] += int(p1[vx])
    p2Rect[1] += int(p2[vy])
    p2Rect[0] += int(p2[vx])
    p1[lastJump] = keys[K_w]
    p2[lastJump] = keys[K_UP]


def cpuInput(p1, p2, p1Rect, p2Rect):  # For getting cpu input for thinkgs like movement and attacks
    cpuLeft = cpuRight = cpuJump = cpuFall = cpuHeavy = cpuLight = False
    if p1Rect[0] + 100 < p2Rect[0]:
        cpuLeft = True
    if p1Rect[0] - 100 > p2Rect[0]:
        cpuRight = True
    if p1Rect[1] + 100 < p2Rect[1]:
        cpuJump = True
    if p1Rect[1] - 100 > p2Rect[1]:
        cpuFall = True
    if (p2Rect[0] - p1Rect[0]) ** 2 + (p2Rect[1] - p1Rect[1]) ** 2 <= 70 ** 2 and p2[cooldown] != 0:  # If the player is within a certain range
        choice = randint(0, 1)
        if choice == 0:
            cpuHeavy = True
        else:
            cpuLight = True
        direction = randint(0, 2)
        if direction == 0:
            cpuLeft = True
        elif direction == 1:
            cpuRight = True
        else:
            cpuLeft = cpuRight = False
            cpuFall = True
    return cpuLeft, cpuRight, cpuJump, cpuFall, cpuHeavy, cpuLight


def singlePMove(p1, p2, p1Rect, p2Rect):
    global stock1, stock2
    keys = key.get_pressed()
    cpuLeft, cpuRight, cpuJump, cpuFall, cpuHeavy, cpuLight = cpuInput(p1, p2, p1Rect, p2Rect)
    # Determines stun
    if p1[stunUntil] > 0:
        p1Stun = True
    else:
        p1Stun = False
        p1[stunUntil] = 0
    if p2[stunUntil] > 0:
        p2Stun = True
    else:
        p2Stun = False
        p2[stunUntil] = 0
    # Deacreases the stun and cooldown time
    p1[stunUntil] -= 1 / 60
    p2[stunUntil] -= 1 / 60
    p1[cooldown] -= 1 / 60
    p2[cooldown] -= 1 / 60
    checkHit(p1, p2, p1Rect, p2Rect)
    # Checks if Player 1 is on the ground
    for i in map:
        if i.collidepoint((p1Rect[0], p1Rect[1])):
            if p1Rect[0] >= i[0] + i[2] - 10:
                p1Rect[0] = i[0] + i[2]
                if p1Stun:  # Bounces off the map if the player is attacked
                    p1[vx] *= -1
                if p1[vx] < 0:
                    p1[vx] = 0
                break
            elif p1Rect[0] <= i[0] + 10:
                p1Rect[0] = i[0] - 1
                if p1Stun:  # Bounces off the map if the player is attacked
                    p1[vx] *= -1
                if p1[vx] > 0:
                    p1[vx] = 0
                break
            elif p1Rect[1] <= i[1] + 10 and p1[attack] != nAir and p1[attack] != sAir and p1[attack] != dAir and p1[attack] != recovery:
                p1[grounded] = True
                p1[vy] = 0
                p1Rect[1] = i[1] + 1
                p1[jumpNum] = 3
            elif p1[attack] != nAir or p1[attack] != sAir or p1[attack] != dAir or p1[attack] != recovery:  # prevents falling through the map when attacking
                p1[vy] = 0
                p1Rect[1] = i[1] + 1
            break
        # If he's not, apply gravity
        elif p1[vy] <= 5 and map.index(i) == 2:
            p1[grounded] = False
            p1[vy] += 0.35
            if p1[jumpNum] == 3:
                p1[jumpNum] = 2
        # If they collide with the bottom of the map
        if i.collidepoint((p1Rect[0], p1Rect[1] + p1Rect[3])):
            if p1Stun:  # Bounces off the map if the player is attacked
                p1[vy] *= -1
            else:
                p1[vy] = 0
                p1Rect[1] = i[1] + i[3] - p1Rect[3]
    # Checks if Player 2 is on the ground (negates gravity if True)
    for i in map:
        if i.collidepoint((p2Rect[0], p2Rect[1])):
            if p2Rect[0] >= i[0] + i[2] - 10:
                p2Rect[0] = i[0] + i[2]
                if p2Stun:  # Bounces off the map if the player is attacked
                    p2[vx] *= -1
                if p2[vx] < 0:
                    p2[vx] = 0
                break
            elif p2Rect[0] <= i[0] + 10:
                p2Rect[0] = i[0] - 1
                if p2Stun:  # Bounces off the map if the player is attacked
                    p2[vx] *= -1
                if p2[vx] > 0:
                    p2[vx] = 0
                break
            elif p2Rect[1] <= i[1] + 10 and p2[attack] != nAir and p2[attack] != sAir and p2[attack] != dAir and p2[attack] != recovery:
                p2[grounded] = True
                p2[vy] = 0
                p2Rect[1] = i[1] + 1
                p2[jumpNum] = 3
            elif p2[attack] != nAir or p2[attack] != sAir or p2[attack] != dAir or p2[attack] != recovery:
                p2[vy] = 0
                p2Rect[1] = i[1]
            break
        # If he's not, apply gravity
        elif p2[vy] <= 5 and map.index(i) == 2:
            p2[grounded] = False
            p2[vy] += 0.35
            if p2[jumpNum] == 3:
                p2[jumpNum] = 2
        # If they collide with the bottom of the map
        if i.collidepoint((p2Rect[0], p2Rect[1] + p2Rect[3])):
            if p2Stun:  # Bounces off the map if the player is attacked
                p2[vy] *= -1
            else:
                p2[vy] = 0
                p2Rect[1] = i[1] + i[3] - p1Rect[3]
    # P1 Movement Calculations
    # Reflex Click Bug (if they click one way and then the other at the same time)
    if not p1[attack] and not p1Stun:
        if keys[K_d] and keys[K_a]:
            if p1[leftOrRight] == "undecided":
                if p1[direction] == "left":
                    p1[direction] = "right"
                    p1[facing] = "right"
                    p1[leftOrRight] = "decided"
                elif p1[direction] == "right":
                    p1[direction] = "left"
                    p1[facing] = "left"
                    p1[leftOrRight] = "decided"
        else:
            p1[leftOrRight] = "undecided"
    if keys[K_a] and not keys[K_d] and not p1[attack]:
        p1[direction] = "left"
        p1[facing] = "left"
    elif keys[K_d] and not keys[K_a] and not p1[attack]:
        p1[direction] = "right"
        p1[facing] = "right"
    elif not keys[K_a] and not keys[K_d]:
        p1[direction] = "none"
    # Movement
    if p1[direction] == "right" and p1[vx] < 4 and not p1[attack]:
        p1[vx] += 0.5
    elif p1[direction] == "left" and p1[vx] > -4 and not p1[attack]:
        p1[vx] -= 0.5
    # Fastfall
    if keys[K_s] and not p1[grounded] and p1[vy] < 8:
        p1[vy] += 0.5
    # Drag
    if p1[direction] == "none" or p1[attack] != False or p1[vx] > 4 or p1[vx] < -4:
        p1[vx] /= 1.1
    # Only jumps once on click
    if keys[K_w] and not p1[lastJump] and p1[jumpNum] > 0 and not p1[attack] and not p1Stun:  # Knocked animation
        p1[vy] = -10
        p1[frame] = 0
        p1[jumpNum] -= 1
    # Knockback Calcutlation
    if p1[hit] == True:
        p1[vx] = (p2[fighter][p2[attack]][xForce] + p1[damage]) - 2 * (p2[fighter][p2[attack]][xForce] + p1[damage]) * (p2[facing] == "left")
        p1[vy] = -p2[fighter][p2[attack]][yForce] - p1[damage]

    # P2 Movement Calculations
    # Reflex Click Bug (if they click one way and then the other at the same time)
    if not p2[attack] and not p2Stun:
        if cpuLeft and cpuRight:
            if p2[leftOrRight] == "undecided":
                if p2[direction] == "left":
                    p2[direction] = "right"
                    p2[facing] = "right"
                    p2[leftOrRight] = "decided"
                elif p2[direction] == "right":
                    p2[direction] = "left"
                    p2[facing] = "left"
                    p2[leftOrRight] = "decided"
        else:
            p2[leftOrRight] = "undecided"
    if cpuLeft and not cpuRight and not p2[attack]:
        p2[direction] = "left"
        p2[facing] = "left"
    if cpuRight and not cpuLeft and not p2[attack]:
        p2[direction] = "right"
        p2[facing] = "right"
    if not cpuLeft and not cpuRight:
        p2[direction] = "none"
    # Movement
    if p2[direction] == "right" and p2[vx] < 4 and not p2[attack]:
        p2[vx] += 0.5
    elif p2[direction] == "left" and p2[vx] > -4 and not p2[attack]:
        p2[vx] -= 0.5
    # Fastfall
    if cpuFall and not p2[grounded] and p2[vy] < 8:
        p2[vy] += 0.5
    # Drag
    if p2[direction] == "none" or p2[attack] != False or p2[vx] > 4 or p2[vx] < -4:
        p2[vx] /= 1.1
    # Only jumps once on click
    if cpuJump and not p2[lastJump] and p2[jumpNum] > 0 and not p2[attack] and not p2Stun:  # Knocked animation
        p2[vy] = -10
        p2[frame] = 0
        p2[jumpNum] -= 1
    # Knockback Calculation
    if p2[hit] == True:
        p2[vx] = (p1[fighter][p1[attack]][xForce] + p2[damage]) - 2 * (p1[fighter][p1[attack]][xForce] + p2[damage]) * (p1[facing] == "left")
        p2[vy] = -p1[fighter][p1[attack]][yForce] - p2[damage]
    # Applying forces
    p1Rect[1] += int(p1[vy])
    p1Rect[0] += int(p1[vx])
    p2Rect[1] += int(p2[vy])
    p2Rect[0] += int(p2[vx])
    p1[lastJump] = keys[K_w]
    p2[lastJump] = cpuJump


def drawPs(screen, p1, p2, rainbowVal):
    screen.fill(grey)
    for i in map:
        draw.rect(screen, rainbowVal, i)
    global blastPos
    # If the player is grounded, they are drawn offsetted by thier height (for bobbing characters, idle animations, vertical attacks, etc.),
    # otherwise they are drawn offsetted by half their height
    if not p1[grounded] and p1[attack] != False:
        screen.blit(p1Pic, (p1Rect[0] - p1Pic.get_width() // 2, p1Rect[1] - p1Pic.get_height() // 2))
    else:
        screen.blit(p1Pic, (p1Rect[0] - p1Pic.get_width() // 2, p1Rect[1] - p1Pic.get_height()))
    if not p2[grounded] and p2[attack] != False:
        screen.blit(p2Pic, (p2Rect[0] - p2Pic.get_width() // 2, p2Rect[1] - p2Pic.get_height() // 2))
    else:
        screen.blit(p2Pic, (p2Rect[0] - p2Pic.get_width() // 2, p2Rect[1] - p2Pic.get_height()))
    deathAnim(blastAnim, blastPos)


def camera(camRect, rect1, rect2):
    x1 = rect1[0]
    y1 = rect1[1]
    x2 = rect2[0]
    y2 = rect2[1]
    smolX, smolY, bigX, bigY = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)  # Finds the maximum and minimum heights and distances
    xOffset = 200  # Space to be left between the edges and the characters
    yOffset = 100
    midpoint = (x1 + x2) // 2, (y1 + y2) // 2
    camRect[2] += ((bigX - smolX + xOffset * 2) - camRect[2]) // 7  # Resizes the rect - which is copied - by increments for a smoother pan
    if ((camRect[2] // (width / height) + bigY - smolY) - camRect[3]) < 0:  # The camera zooms out faster than it zooms in without this statement
        camRect[3] += ((camRect[2] // (width / height) + bigY - smolY) - camRect[3]) // 10  # Zooms in faster
    else:
        camRect[3] += ((camRect[2] // (width / height) + bigY - smolY) - camRect[3]) // 50  # Zooms out slower

    camRect[2] = (camRect[3] * (width / height))  # Scales the width based on aspect ratio of the screen
    camRect[0], camRect[1] = midpoint[0] - camRect[2] // 2, midpoint[1] - camRect[3] // 2 - yOffset  # Offsets the camera so that the midpoint is in the center of the rect
    try:
        if blastFrame < 9:  # Keeps the camera zoomed out a little while after a player dies
            footage = screen
        else:
            footage = transform.scale(screen.subsurface(camRect).copy(), (width, height))  # Footage becomes a copy of the screen in the rect
    except:  # Error occurs if the Camera rect is outside of the surface
        try:
            if camRect[0] < 0:  # If the camera is all the way to the left
                camRect[0] = 0
            if camRect[1] < 0:  # if the camera is app the way t the top
                camRect[1] = 0
            if camRect[0] + camRect[2] >= width:  # If the camera is all the way t the right
                camRect[0] = width - camRect[2]
            if camRect[1] + camRect[3] >= height:  # If the camera is past the bottom of the screen
                camRect[1] = height - camRect[3]
            footage = transform.scale(screen.subsurface(camRect).copy(), (width, height))  # Retakes footage
        except:
            footage = screen  # If the camera is zoomed all the way out (or more)
    screen.blit(footage, (0, 0))
    display.flip()


def arena(p1, p2, p1Rect, p2Rect):
    global p1Pic, p2Pic, p1Hit, p2Hit, stock1, stock2
    stock1 = stock2 = 3
    points = [(0, 20), (0, -20), (10, 0), (-10, 0), (8, 9), (-8, 9), (-8, -9), (8, -9)]
    rainbowVal = (255, 0, 0)
    running = True
    paused = False
    while running:
        light1 = heavy1 = light2 = heavy2 = False
        for evt in event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_f:
                    light1 = True
                if evt.key == K_g:
                    heavy1 = True
                if evt.key == K_PERIOD:
                    light2 = True
                if evt.key == K_COMMA:
                    heavy2 = True
                if evt.key == K_ESCAPE:
                    if paused:
                        paused = False
                    else:
                        paused = True
                if evt.key == K_RETURN and paused:
                    return "menu"
            if evt.type == QUIT:
                running = False
        timer()
        keys = key.get_pressed()
        mx, my = mouse.get_pos()
        if rainbowVal[0] == 255 and rainbowVal[1] < 255 and rainbowVal[2] == 0:
            rainbowVal = (rainbowVal[0], rainbowVal[1] + 5, rainbowVal[2])
        elif rainbowVal[0] > 0 and rainbowVal[1] == 255:
            rainbowVal = (rainbowVal[0] - 5, rainbowVal[1], rainbowVal[2])
        elif rainbowVal[1] == 255 and rainbowVal[2] < 255:
            rainbowVal = (rainbowVal[0], rainbowVal[1], rainbowVal[2] + 5)
        elif rainbowVal[1] > 0 and rainbowVal[2] == 255:
            rainbowVal = (rainbowVal[0], rainbowVal[1] - 5, rainbowVal[2])
        elif rainbowVal[2] == 255 and rainbowVal[0] < 255:
            rainbowVal = (rainbowVal[0] + 5, rainbowVal[1], rainbowVal[2])
        elif rainbowVal[2] > 0 and rainbowVal[0] == 255:
            rainbowVal = (rainbowVal[0], rainbowVal[1], rainbowVal[2] - 5)
        p1Pic, p2Pic, p1Hit, p2Hit = nextSprite(p1, p2, light1, heavy1, light2, heavy2)
        movePs(p1, p2, p1Rect, p2Rect)
        drawPs(screen, p1, p2, rainbowVal)
        camera(camRect, p1Rect, p2Rect)
        if stock1 == 0:
            screen.fill(black)
            screen.blit(broadway.render("Player 2 Wins!", True, ((0, 0, 255))), (width // 2 - 200, height // 2))
            display.flip()
            playSound(yay, "effect")
            time.wait(2500)
            return "menu"
        if stock2 == 0:
            screen
            screen.fill(black)
            screen.blit(broadway.render("Player 1 Wins!", True, ((255, 0, 0))), (width // 2 - 200, height // 2))
            display.flip()
            playSound(yay, "effect")
            time.wait(2500)
            return "menu"
        myClock.tick(fps)
    quit()


def single(p1, p2, p1Rect, p2Rect):
    global p1Pic, p2Pic, p1Hit, p2Hit, stock1, stock2
    stock1 = stock2 = 3
    points = [(0, 20), (0, -20), (10, 0), (-10, 0), (8, 9), (-8, 9), (-8, -9), (8, -9)]
    rainbowVal = (255, 0, 0)
    running = True
    paused = False
    while running:
        light1 = heavy1 = light2 = heavy2 = False
        for evt in event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_f:
                    light1 = True
                if evt.key == K_g:
                    heavy1 = True
                if evt.key == K_PERIOD:
                    light2 = True
                if evt.key == K_COMMA:
                    heavy2 = True
                if evt.key == K_ESCAPE:
                    if paused:
                        paused = False
                    else:
                        paused = True
                if evt.key == K_RETURN and paused:
                    return "menu"
            if evt.type == QUIT:
                running = False
        timer()
        keys = key.get_pressed()
        mx, my = mouse.get_pos()
        if rainbowVal[0] == 255 and rainbowVal[1] < 255 and rainbowVal[2] == 0:
            rainbowVal = (rainbowVal[0], rainbowVal[1] + 5, rainbowVal[2])
        elif rainbowVal[0] > 0 and rainbowVal[1] == 255:
            rainbowVal = (rainbowVal[0] - 5, rainbowVal[1], rainbowVal[2])
        elif rainbowVal[1] == 255 and rainbowVal[2] < 255:
            rainbowVal = (rainbowVal[0], rainbowVal[1], rainbowVal[2] + 5)
        elif rainbowVal[1] > 0 and rainbowVal[2] == 255:
            rainbowVal = (rainbowVal[0], rainbowVal[1] - 5, rainbowVal[2])
        elif rainbowVal[2] == 255 and rainbowVal[0] < 255:
            rainbowVal = (rainbowVal[0] + 5, rainbowVal[1], rainbowVal[2])
        elif rainbowVal[2] > 0 and rainbowVal[0] == 255:
            rainbowVal = (rainbowVal[0], rainbowVal[1], rainbowVal[2] - 5)
        p1Pic, p2Pic, p1Hit, p2Hit = singleSprite(p1, p2, light1, heavy1, light2, heavy2)
        singlePMove(p1, p2, p1Rect, p2Rect)
        drawPs(screen, p1, p2, rainbowVal)
        camera(camRect, p1Rect, p2Rect)
        if stock1 == 0:
            screen.fill(black)
            screen.blit(broadway.render("Player 2 Wins!", True, ((0, 0, 255))), (width // 2 - 200, height // 2))
            display.flip()
            playSound(yay, "effect")
            time.wait(2500)
            return "menu"
        if stock2 == 0:
            screen.fill(black)
            screen.blit(broadway.render("Player 1 Wins!", True, ((255, 0, 0))), (width // 2 - 200, height // 2))
            display.flip()
            playSound(yay, "effect")
            time.wait(2500)
            return "menu"
        myClock.tick(fps)
    quit()


def deathAnim(pics, pos):
    global blastFrame
    if blastFrame <= 9:
        opp = (width / 2 - pos[0])
        adj = (height / 2 - pos[1])
        rotAngle = 45 * round(-(180 - 180 * (adj < 0) - degrees(atan(opp / adj))) / 45)
        pic = transform.rotate(pics[int(blastFrame)], rotAngle)
        screen.blit(pic, (pos[0] - pic.get_width() // 2, pos[1] - 200))
        blastFrame += 0.3


def playSound(soundFile, soundChannel):
    """ Function to load in sounds and play them on a channel """
    channelList = [["backMus", 0], ["effect", 1], ["p1", 2], ["p2", 3]]  # List to keep track of mixer channels
    for subList in channelList:  # For loop to identify the input
        if subList[0] == soundChannel:
            channelNumber = subList[1]
    mixer.Channel(channelNumber).stop()  # Stopping any previous sound
    mixer.Channel(channelNumber).play(soundFile)  # Playing new sound


def globalSound(command):
    """ Function to apply commands to all mixer channels """
    # Help from Armaan
    for id in range(mixer.get_num_channels()):
        if command == "stop":
            mixer.Channel(id).stop()
        elif command == "pause":
            mixer.Channel(id).pause()
        elif command == "unpause":
            mixer.Channel(id).unpause()


def menu():
    running = True
    playSound(opening, "backMus")
    singleP = arial.render("Single Player", True, ((255, 0, 0)))
    twoP = arial.render("Two Player", True, ((255, 0, 0)))
    cred = arial.render("Credits", True, ((255, 0, 0)))
    inst = arial.render("Instructions", True, ((255, 0, 0)))
    buttons = [Rect(280, 340, 135, 80), Rect(450, 340, 138, 80), Rect(610, 340, 135, 80), Rect(770, 340, 135, 80)]
    aspectRatio = width / height
    startBack = back.subsurface((0, 0), (width, height))
    scrollX = 0
    startBackX = int(width * aspectRatio)
    selected = 0
    while running:
        for evt in event.get():
            if evt.type == KEYDOWN:
                if (evt.key == K_LEFT or evt.key == K_a):
                    playSound(ping, "effect")
                    if selected > 0:
                        selected -= 1
                    else:
                        selected = len(buttons) - 1
                if (evt.key == K_RIGHT or evt.key == K_d):
                    playSound(ping, "effect")
                    if selected < len(buttons) - 1:
                        selected += 1
                    else:
                        selected = 0
                if evt.key == K_RETURN:
                    playSound(enter, "effect")
                    if selected == 0:
                        return "charSel2"
                    if selected == 1:
                        return "charSel"
                    if selected == 2:
                        return "credits"
            if evt.type == QUIT:
                return "exit"
        screen.fill(black)
        try:
            scrollSurface = back.subsurface((scrollX, 0), (width, height))
            screen.blit(scrollSurface, (0, 0))
        except:
            screen.blit(startBack, (startBackX, 0))
            startBackX -= 10
        scrollX += 6
        if scrollX + width >= back.get_width():
            scrollX = 0
        if scrollX + width * aspectRatio >= back.get_width() and startBackX <= 0:
            scrollX = 0
            startBackX = int(width * aspectRatio)
        for i in buttons:
            draw.rect(screen, (10, 10, 10, 255), i)
        draw.rect(screen, green, buttons[selected], 2)
        screen.blit(singleP, (300, 375))
        screen.blit(twoP, (480, 375))
        screen.blit(cred, (640, 375))
        screen.blit(inst, (800, 375))
        screen.blit(title, (width // 2 - title.get_width() // 2, 100))
        display.flip()


def characterSel(p1, p2):
    running = True
    playSound(opening, "backMus")
    buttons = [Rect(280, 340, 135, 80), Rect(450, 340, 138, 80), Rect(610, 340, 135, 80), Rect(770, 340, 135, 80)]
    select1 = 0
    select2 = 1
    lock1 = False
    lock2 = False
    transInt = 255
    while running:
        for evt in event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_a and not lock1:
                    playSound(ping, "effect")
                    select1 -= 1
                if evt.key == K_d and not lock1:
                    playSound(ping, "effect")
                    select1 += 1
                if select1 > len(charList) - 1:
                    select1 = 0
                if select1 < 0:
                    select1 = len(charList) - 1

                if evt.key == K_LEFT and not lock2:
                    playSound(ping, "effect")
                    select2 -= 1
                if evt.key == K_RIGHT and not lock2:
                    playSound(ping, "effect")
                    select2 += 1
                if select2 > len(charList) - 1:
                    select2 = 0
                if select2 < 0:
                    select2 = len(charList) - 1
                if evt.key == K_f:
                    if lock1:
                        playSound(goBack, "effect")
                        lock1 = False
                    else:
                        playSound(enter, "effect")
                        lock1 = True
                if evt.key == K_PERIOD:
                    if lock2:
                        playSound(goBack, "effect")
                        lock2 = False
                    else:
                        playSound(enter, "effect")
                        lock2 = True
                if evt.key == K_RETURN:
                    if lock1 and lock2:
                        playSound(enter, "effect")
                        p1[fighter] = charList[select1]
                        p2[fighter] = charList[select2]
                        return "arena"
                    else:
                        playSound(goBack, "effect")
                if evt.key == K_ESCAPE:
                    return "menu"
            if evt.type == QUIT:
                return "exit"
        screen.blit(charSelBack, ((width - charSelBack.get_width()) // 2, 0))
        for c in charList:
            screen.blit(c[icon], (charList.index(c) * 60 % 360 + width // 2 - 180, charList.index(c) * 60 // 360 + height // 2 - 180))
            if charList.index(c) == select1:
                if lock1:
                    draw.rect(screen, green, (charList.index(c) * 60 % 360 + width // 2 - 180, charList.index(c) * 60 // 360 + height // 2 - 180, 42, 42), 2)
                else:
                    draw.rect(screen, red, (charList.index(c) * 60 % 360 + width // 2 - 180, charList.index(c) * 60 // 360 + height // 2 - 180, 42, 42), 2)
            if charList.index(c) == select2:
                if lock2:
                    draw.rect(screen, green, (charList.index(c) * 60 % 360 + width // 2 - 180 + 1, charList.index(c) * 60 // 360 + height // 2 - 180 + 1, 42, 42), 2)
                else:
                    draw.rect(screen, blue, (charList.index(c) * 60 % 360 + width // 2 - 180 + 1, charList.index(c) * 60 // 360 + height // 2 - 180 + 1, 42, 42), 2)

        if transInt > 0:
            fadeScreen(transInt)
            transInt -= 20
        display.flip()


def characterSel2(p1, p2):
    running = True
    playSound(opening, "backMus")
    buttons = [Rect(280, 340, 135, 80), Rect(450, 340, 138, 80), Rect(610, 340, 135, 80), Rect(770, 340, 135, 80)]
    select1 = 0
    select2 = 1
    lock1 = False
    lock2 = False
    transInt = 255
    while running:
        for evt in event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_a and not lock1:
                    playSound(ping, "effect")
                    select1 -= 1
                if evt.key == K_d and not lock1:
                    playSound(ping, "effect")
                    select1 += 1
                if select1 > len(charList) - 1:
                    select1 = 0
                if select1 < 0:
                    select1 = len(charList) - 1
                if evt.key == K_f:
                    if lock1:
                        playSound(goBack, "effect")
                        lock1 = False
                    else:
                        playSound(enter, "effect")
                        lock1 = True
                if evt.key == K_RETURN:
                    playSound(enter, "effect")
                    if lock1:
                        p1[fighter] = charList[select1]
                        p2[fighter] = choice(charList)
                        return "single"
                    else:
                        playSound(goBack, "effect")
                if evt.key == K_ESCAPE:
                    return "menu"
            if evt.type == QUIT:
                return "exit"
        screen.blit(charSelBack, ((width - charSelBack.get_width()) // 2, 0))
        for c in charList:
            screen.blit(c[icon], (charList.index(c) * 60 % 360 + width // 2 - 180, charList.index(c) * 60 // 360 + height // 2 - 180))
            if charList.index(c) == select1:
                if lock1:
                    draw.rect(screen, green, (charList.index(c) * 60 % 360 + width // 2 - 180, charList.index(c) * 60 // 360 + height // 2 - 180, 42, 42), 2)
                else:
                    draw.rect(screen, red, (charList.index(c) * 60 % 360 + width // 2 - 180, charList.index(c) * 60 // 360 + height // 2 - 180, 42, 42), 2)

        if transInt > 0:
            fadeScreen(transInt)
            transInt -= 20
        display.flip()


def credits():
    me = broadway.render("ME!", True, white)
    msg1 = broadway.render("This project was created with the", True, white)
    msg4 = broadway.render("efforts of Samir Bhuiyan alone.", True, white)
    msg2 = smolBroad.render("(Special thanks to Armaan Rhandawa, Arsalaan Ali,", True, white)
    msg3 = smolBroad.render(" and Tanveer Mahngar for tidbits of code.)", True, white)
    msg5 = smolBroad.render("< Press enter to go back", True, white)
    screen.fill(black)
    for w in range(width // 100):
        for h in range(height // 50):
            screen.blit(me, (w * 100, h * 50))
            time.wait(10)
            display.flip()
    time.wait(1000)
    screen.fill(black)
    screen.blit(msg1, (width // 2 - msg1.get_width() // 2, height // 2 - 50))
    screen.blit(msg4, (width // 2 - msg4.get_width() // 2, height // 2))
    display.flip()
    playSound(yay, "effect")
    time.wait(5000)
    screen.blit(msg2, (width // 2 - msg2.get_width() // 2, height - 100))
    screen.blit(msg3, (width // 2 - msg3.get_width() // 2, height - 50))
    display.flip()
    time.wait(1000)
    screen.blit(msg5, (20, 20))
    display.flip()
    while True:
        for evt in event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_RETURN:
                    return "menu"
            if evt.type == QUIT:
                return "menu"


running = True
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
        mixer.Sound.stop(opening)
        for i in range(80):
            fadeScreen(i)
            display.flip()
    if page == "charSel2":
        page = characterSel2(p1, p2)
        mixer.Sound.stop(opening)
        for i in range(80):
            fadeScreen(i)
            display.flip()
    if page == "charSel":
        page = characterSel(p1, p2)
        mixer.Sound.stop(opening)
        for i in range(80):
            fadeScreen(i)
            display.flip()
    if page == "arena":
        page = arena(p1, p2, p1Rect, p2Rect)
        for i in range(80):
            fadeScreen(i)
            display.flip()
    if page == "single":
        page = single(p1, p2, p1Rect, p2Rect)
    if page == "instructions":
        page = instructions()
    if page == "story":
        page = story()
    if page == "credits":
        page = credits()
quit()
