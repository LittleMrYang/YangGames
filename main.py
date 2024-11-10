from typing import Tuple
import pygame as pyg
from pygame import *
import math as mth

pyg.init()
pyg.font.init()
screen = pyg.display.set_mode(size=(1000*1.5, 500*1.5))
WIDTH, HEIGHT = display.get_window_size()
clockc = pyg.time.Clock()
FPS = 60
running: bool

# configs
xyd = pyg.image.load("sprites/xyd_ICO.png")
display.set_icon(xyd)
display.set_caption("turingstar")
xyd = transform.scale(xyd, (100, 100))


class Button:

    def __init__(self, size: int, _text: str, _font: str) -> None:
        self.fnt = font.Font(_font, size)
        self.image: Surface = self.fnt.render(_text, True, "white", "black")
        self.rect = self.image.get_rect()


class Monster(pyg.sprite.Sprite):
    MaxHealth: int
    Health: int
    hlthRct = Surface((60, 3))

    def __init__(self, image: Surface):
        sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.MaxHealth = 20
        self.Health = self.MaxHealth

    def set_health_rect(self):
        self.hlthRct.fill((0, 0, 0))
        self.hlthRct.fill((255-self.Health/self.MaxHealth*255, 220, 30), rect.Rect(
            0, 0, self.Health/self.MaxHealth*self.hlthRct.get_rect().width, self.hlthRct.get_rect().height))

    def blit_hlth(self, dst: Surface):
        dst.blit(self.hlthRct, (self.rect.centerx -
                                self.hlthRct.get_rect().width*0.33, self.rect.top-self.rect.height*0.2))

    def update(self):
        self.rect.centerx += (p1.rect.centerx-self.rect.centerx)/50
        self.rect.centery += \
            (max(p1.rect.centery, HEIGHT*0.8)-self.rect.centery)/10
        self.set_health_rect()


class Player(pyg.sprite.Sprite):
    MaxHealth: int
    Health: int
    hlthRct = Surface((60, 3))
    accr = 0
    isStatic = False

    def __init__(self, size: Tuple[int, int], color: Tuple[int, int, int]):
        sprite.Sprite.__init__(self)
        self.image: Surface = Surface(size)
        self.image.fill(color)
        self.rect: Rect = self.image.get_rect()
        self.MaxHealth = 20
        self.Health = self.MaxHealth

    def isOnGround(self) -> bool:
        return self.rect.y == HEIGHT-self.rect.height

    def set_health_rect(self):
        self.hlthRct.fill((0, 0, 0))
        self.hlthRct.fill((255-self.Health/self.MaxHealth*200, min(self.Health/self.MaxHealth*255+10, 255), min(self.Health/self.MaxHealth*140, 100)), rect.Rect(
            0, 0, self.Health/self.MaxHealth*self.hlthRct.get_rect().width, self.hlthRct.get_rect().height))

    def blit_hlth(self, dst: Surface):
        dst.blit(self.hlthRct, (self.rect.centerx -
                                self.hlthRct.get_rect().width*0.33, self.rect.top-self.rect.height*0.2))

    def update(self):
        ks = pyg.key.get_pressed()
        if ks[K_a]:
            p1.rect.x -= 10
        if ks[K_d]:
            p1.rect.x += 10
        if ks[K_w]:
            if p1.isOnGround():
                p1.accr = 12
        if ks[K_s]:
            p1.isStatic = True
            p1.image.fill((0, 200, 37))
        else:
            p1.isStatic = False
            p1.image.fill((255, 255, 255))

        if self.rect.collideobjects(mosts.sprites()):
            self.Health -= 1
        # test
        if ks[K_EQUALS]:
            self.Health += 1
        elif ks[K_MINUS]:
            self.Health -= 1

        if self.Health < 0:
            self.Health = 0
        elif self.Health > 20:
            self.Health = 20

        if not self.isStatic:
            self.accr -= 0.3
            self.rect.y -= self.accr
        if self.rect.y > HEIGHT-self.rect.height:
            # self.accr = -self.accr*0.8
            self.rect.y = HEIGHT-self.rect.height

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.set_health_rect()


def GoDie():
    dieTxt = font.Font("./sprites/Ubuntu-LI.ttf", 60).render(
        "Game over", True, "white", "black")
    screen.blit(dieTxt,
                ((WIDTH-dieTxt.get_rect().width) / 2, (HEIGHT-dieTxt.get_rect().height)/2))


p1 = Player((50, 50), (255, 255, 255))
Mxyd = Monster(xyd)
Exit_butt = Button(40, "Exit button", "./sprites/Ubuntu-LI.ttf")
Pause_butt = Button(40, "Pause button", "./sprites/Ubuntu-LI.ttf")
p1.rect.y = HEIGHT-p1.rect.height
p1.rect.x = WIDTH / 2
Exit_butt.rect.x = WIDTH-Exit_butt.rect.width
Exit_butt.rect.y = 0
Pause_butt.rect.x = 0
Pause_butt.rect.y = 0
plys = sprite.Group(p1)
mosts = sprite.Group(Mxyd)

running = True
Paused = False
Died = False
while running:
    for eve in pyg.event.get():
        if eve.type == pyg.QUIT:
            running = False
        if eve.type == pyg.MOUSEBUTTONDOWN:
            mousePos = mouse.get_pos()
            if Exit_butt.rect.collidepoint(mousePos):
                running = False
            if not Died and Pause_butt.rect.collidepoint(mousePos):
                Pause_butt.image = Pause_butt.fnt.render(
                    "Pause button" if Paused else "Resume button", True, "white", "black")
                Pause_butt.rect = Pause_butt.image.get_rect()
                Paused = not Paused
    for i in range(0, HEIGHT+1):
        screen.fill((max(min((i+0)/HEIGHT*255*0.2+140, 255), 0), 255 - max(min((i+20)/HEIGHT*255*0.8, 255), 0), 255 - max(min((i+-200)/HEIGHT*255, 255), 0)),
                    rect.Rect(0, i, WIDTH, 1))
    plys.draw(screen)
    mosts.draw(screen)
    p1.blit_hlth(screen)
    enmys: list[Monster] = mosts.sprites()
    for enemies in enmys:
        enemies.blit_hlth(screen)
    screen.blit(Exit_butt.image, Exit_butt.rect)
    screen.blit(Pause_butt.image, Pause_butt.rect)

    if p1.Health <= 0:
        Died = True
        GoDie()
    if not Paused and not Died:
        plys.update()
        mosts.update()
    pyg.display.flip()
    clockc.tick(FPS)

pyg.quit()
