import pygame
import random
import math
import pyautogui

print("PLAYER 1, ENTER YOUR NAME")
player1 = str(raw_input())
print("PLAYER 2, ENTER YOUR NAME")
player2 = str(raw_input())
print("NOW THE BATTLE SHALL BEGIN")
pygame.time.delay(2000)

pygame.init()

wscreen, hscreen = pyautogui.size()
wscreen *= 0.95
hscreen *= 0.95
wscreen = int(wscreen)
hscreen = int(hscreen)

win = pygame.display.set_mode((wscreen, hscreen))
pygame.display.set_caption("CORONA SZN")

walkRight = []
walkLeft = []
for i in range(1, 10):
    right = pygame.image.load("R" + str(i) + ".png")
    left = pygame.image.load("L" + str(i) + ".png")
    right = pygame.transform.scale(right, (int(round(hscreen * 0.128)), int(round(hscreen * 0.128))))
    left = pygame.transform.scale(left, (int(round(hscreen * 0.128)), int(round(hscreen * 0.128))))
    walkRight.append(right)
    walkLeft.append(left)
bg = pygame.image.load("bg.jpg")
bg = pygame.transform.scale(bg, (wscreen, hscreen))
char = pygame.image.load("standing.png")
char = pygame.transform.scale(char, (int(round(hscreen * 0.128)), int(round(hscreen * 0.128))))

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound("pewpew.wav")
#hitSound = pygame.mixer.Sound("hit.mp3")

music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

p1score = 0
p2score = 0

class Player(object):
    def __init__(self, name, x, y, right, left):
        self.name = name
        self.x = x
        self.y = y
        self.width = round(hscreen * 0.064)
        self.height = round(hscreen * 0.064)
        self.vel = round(hscreen / 50)
        self.isJump = False
        self.firstJump = math.ceil(hscreen * 0.014)
        self.jumpCount = self.firstJump
        self.left = left
        self.right = right
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + round(hscreen * 0.034), self.y + round(hscreen * 0.022), round(hscreen * 0.058), round(hscreen * 0.104))
        self.visible = True
        self.health = 100

    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 > 27:
                self.walkCount = 0

            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0] - 20, self.hitbox[1] - 20, 100, 20))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0] - 20, self.hitbox[1] - 20, self.health, 20))
            self.hitbox = (self.x + round(hscreen * 0.034), self.y + round(hscreen * 0.022), round(hscreen * 0.058), round(hscreen * 0.104))
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
       # hitSound.play()
        if self.health > 5:
            self.health -= 10
        else:
            self.visible = False
        print(self.name + " hit!")

class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = int(round(hscreen * 0.08)) * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    '''
    walkRight = []
    walkLeft = []
    for i in range(1, 12):
        right = pygame.image.load("R" + str(i) + "E.png")
        left = pygame.image.load("L" + str(i) + "E.png")
        right = pygame.transform.scale(right, (128, 128))
        left = pygame.transform.scale(left, (128, 128))
        walkRight.append(right)
        walkLeft.append(left)
    '''

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 10
        self.hitbox = (self.x + round(hscreen * 0.034), self.y + round(hscreen * 0.002), round(hscreen * 0.062), round(hscreen * 0.114))

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x + round(hscreen * 0.034), self.y + round(hscreen * 0.002), round(hscreen * 0.062), round(hscreen * 0.114))
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        print("Hit")

def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render(player1 + "'s Score:  " + str(p1score), 1, (255, 0, 0))
    win.blit(text, (10, 10))
    text = font.render(player2 + "'s Score:  " + str(p2score), 1, (255, 0, 0))
    win.blit(text, (round(wscreen * 0.8), 10))
    p1.draw(win)
    p2.draw(win)
    pygame.draw.circle(win, (120, 0, 120), inportal, int(round(hscreen * 0.080)))
    for bullet in p1bullets:
        bullet.draw(win)
    for bullet in p2bullets:
        bullet.draw(win)
    pygame.display.update()

#gongSound = pygame.mixer.Sound("chinese_gong.wav")
#gongSound.play()

p1startx = wscreen / 4
p2startx = (3 * wscreen) / 4
starty = round(hscreen * 0.8)
tolerance = round(hscreen * 0.1)

endfont = pygame.font.SysFont('comicsans', int(round(hscreen * 0.150)), True, True)
font = pygame.font.SysFont('comicsans', int(round(hscreen * 0.060)), True, True)
p1 = Player(player1, p1startx, starty, True, False)
p2 = Player(player2, p2startx, starty, False, True)
p1bullets = []
p2bullets = []
teleCount = 50
run = True
while run:
    if teleCount >= 50:
        inportal = (random.randint(tolerance, wscreen - tolerance), random.randint(tolerance, hscreen - tolerance))
        outportal = (random.randint(tolerance, wscreen - tolerance), random.randint(tolerance, hscreen - tolerance))
        teleCount = 0
    else:
        teleCount += 1

    if inportal[1] - 60 < p2.hitbox[1] + p2.hitbox[3] and inportal[1] + 60 > p2.hitbox[1]:
        if inportal[0] + 60 > p2.hitbox[0] and inportal[0] - 60 < p2.hitbox[0] + p2.hitbox[2]:
            p2.x = outportal[0]
            p2.y = outportal[1]

    if inportal[1] - 60 < p1.hitbox[1] + p1.hitbox[3] and inportal[1] + 60 > p1.hitbox[1]:
        if inportal[0] + 60 > p1.hitbox[0] and inportal[0] - 60 < p1.hitbox[0] + p1.hitbox[2]:
            p1.x = outportal[0]
            p1.y = outportal[1]
    
    if not(p1.isJump) and p1.y < starty + 10 - p1.vel * 3:
        if p1.y > starty - p1.vel * 3:
            p1.y = starty
        else:
            p1.y += p1.vel * 3

    if not(p2.isJump) and p2.y < starty + 10 - p2.vel * 3:
        if p2.y > starty - p2.vel * 3:
            p2.y = starty
        else:
            p2.y += p2.vel * 3

    if p1.y > starty:
        p1.y = starty
    if p2.y > starty:
        p2.y = starty

    if p1score > 4:
        winner = endfont.render("WINNER: " + player1, 1, (0, 150, 0))
        end = endfont.render("GAME OVER", 1, (255, 0, 0))
        win.blit(winner, ((wscreen / 2) - winner.get_width()/2,500))
        win.blit(end, ((wscreen / 2) - end.get_width()/2, 400))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
    if p2score > 4:
        winner = endfont.render("WINNER: " + player2, 1, (0, 150, 0))
        end = endfont.render("GAME OVER", 1, (255, 0, 0))
        win.blit(winner, ((wscreen / 2) - winner.get_width()/2,500))
        win.blit(end, ((wscreen / 2) - end.get_width()/2, 400))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()

    if p1.visible == False:
        p1bullets = []
        p2bullets = []
        p2score += 1
        pygame.time.delay(1000)
        p1 = Player(player1, p1startx, starty, True, False)
    if p2.visible == False:
        p1bullets = []
        p2bullets = []
        p1score += 1
        pygame.time.delay(1000)
        p2 = Player(player2, p2startx, starty, False, True)

    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in p1bullets:
        if bullet.y - bullet.radius < p2.hitbox[1] + p2.hitbox[3] and bullet.y + bullet.radius > p2.hitbox[1]:
            if bullet.x + bullet.radius > p2.hitbox[0] and bullet.x - bullet.radius < p2.hitbox[0] + p2.hitbox[2]:
                p2.hit()
                p1bullets.pop(p1bullets.index(bullet))

        if bullet.x < wscreen and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            p1bullets.pop(p1bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_1]:
        if len(p1bullets) < 10:
            bulletSound.play()
            if p1.left:
                facing = -1
            else:
                facing = 1
            p1bullets.append(Projectile(round(p1.x + p1.width//2), round(p1.y + p1.height//2), 9, (226, 88, 34), facing))

    if keys[pygame.K_f] and p1.x > p1.vel:
        p1.x -= p1.vel
        p1.left = True
        p1.right = False
        p1.standing = False
    elif keys[pygame.K_h] and p1.x < wscreen - p1.vel - p1.width:
        p1.x += p1.vel
        p1.left = False
        p1.right = True
        p1.standing = False
    else:
        p1.standing = True
        p1.walkCount = 0

    if not(p1.isJump):
        if keys[pygame.K_t]:
            p1.isJump = True
            p1.walkCount = 0
    else:
        if p1.jumpCount >= -1 * p1.firstJump:
            neg = 1
            if p1.jumpCount < 0:
                neg = -1
            if p1.jumpCount == 4:
                p1.jumpCount -= 7
            p1.y -= (p1.jumpCount ** 2) * neg * 0.5
            p1.jumpCount -= 1
        else:
            p1.isJump = False
            p1.jumpCount = p1.firstJump



    for bullet in p2bullets:
        if bullet.y - bullet.radius < p1.hitbox[1] + p1.hitbox[3] and bullet.y + bullet.radius > p1.hitbox[1]:
            if bullet.x + bullet.radius > p1.hitbox[0] and bullet.x - bullet.radius < p1.hitbox[0] + p1.hitbox[2]:
                p1.hit()
                p2bullets.pop(p2bullets.index(bullet))

        if bullet.x < wscreen and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            p2bullets.pop(p2bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RETURN]:
        if len(p2bullets) < 10:
            bulletSound.play()
            if p2.left:
                facing = -1
            else:
                facing = 1
            p2bullets.append(Projectile(int(round(p2.x + p2.width//2)), int(round(p2.y + p2.height//2)), 9, (226, 88, 34), facing))

    if keys[pygame.K_LEFT] and p2.x > p2.vel:
        p2.x -= p2.vel
        p2.left = True
        p2.right = False
        p2.standing = False
    elif keys[pygame.K_RIGHT] and p2.x < wscreen - p2.vel - p2.width:
        p2.x += p2.vel
        p2.left = False
        p2.right = True
        p2.standing = False
    else:
        p2.standing = True
        p2.walkCount = 0

    if not(p2.isJump):
        if keys[pygame.K_UP]:
            p2.isJump = True
            p2.walkCount = 0
    else:
        if p2.jumpCount >= -1 * p2.firstJump:
            neg = 1
            if p2.jumpCount < 0:
                neg = -1
            if p2.jumpCount == 4:
                p2.jumpCount -= 7
            p2.y -= (p2.jumpCount ** 2) * neg * 0.5
            p2.jumpCount -= 1
        else:
            p2.isJump = False
            p2.jumpCount = p2.firstJump

    redrawGameWindow()

pygame.quit()
