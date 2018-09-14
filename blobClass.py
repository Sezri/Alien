## blobClass.py
## Nate Miller
## Fall 15

import pygame, sys, AnimClass
from pygame.locals import *
from math import *


class blob(object):


    def __init__(self, pos, surf, size):

        self.x = pos[0]
        self.y = pos[1]
        self.xspd = 0
        self.yspd = 0
        self.xacc = 0
        self.yacc = 0
        self.SURF = surf
        self.BASESIZE = size
        self.SIZE = size
        self.MASS = 0
        self.POS = pos
        self.CANSHOOT = True
        self.ONGROUND = True
        self.xscale = True
        
        self.babyspr = {'walk':['spr_baby_0.png', 'spr_baby_1.png', 'spr_baby_2.png', 'spr_baby_3.png'],
                        'roll':['spr_baby_roll_0.png', 'spr_baby_roll_1.png', 'spr_baby_roll_2.png'],
                        'jump':['spr_baby_jump_0.png', 'spr_baby_jump_1.png', 'spr_baby_jump_2.png']}
        self.smspr = {'walk':['spr_small_0.png', 'spr_small_1.png', 'spr_small_2.png', 'spr_small_3.png'],
                      'roll':['spr_small_roll_0.png', 'spr_small_roll_1.png', 'spr_small_roll_2.png'],
                      'jump':['spr_small_jump_0.png', 'spr_small_jump_1.png', 'spr_small_jump_2.png']}
        self.medspr = {'walk':['spr_med_0.png', 'spr_med_1.png', 'spr_med_2.png', 'spr_med_3.png'],
                       'roll':['spr_med_roll_0.png', 'spr_med_roll_1.png', 'spr_med_roll_2.png', 'spr_med_roll_3.png', 'spr_med_roll_4.png', 'spr_med_roll_5.png'],
                       'jump':['spr_med_jump_0.png', 'spr_med_jump_1.png', 'spr_med_jump_2.png']}
        self.bigspr = {'walk':['spr_big_0.png', 'spr_big_1.png', 'spr_big_2.png', 'spr_big_3.png'],
                       'roll':['spr_big_roll_0.png', 'spr_big_roll_1.png', 'spr_big_roll_2.png', 'spr_big_roll_3.png', 'spr_big_roll_4.png', 'spr_big_roll_5.png'],
                       'jump':['spr_big_jump_0.png', 'spr_big_jump_1.png', 'spr_big_jump_2.png']}
        self.action = 'walk'
        self.spr = AnimClass.animate(self.babyspr[self.action], 4, 0, True)

    def __animEnd(self, SPR):
        if(SPR == 'jump'):
            self.spr.image_speed = 0
            self.spr.image_index = len(self.spr.spr_index) - 1

    def __findSpr(self):
            
        if(self.MASS <= 15):
            SPR = self.babyspr[self.action]
        elif(self.MASS > 15 and self.MASS <= 40):
            SPR = self.smspr[self.action]
        elif(self.MASS > 40 and self.MASS <= 65):
            SPR = self.medspr[self.action]
        elif(self.MASS > 65):
            SPR = self.bigspr[self.action]

        if(self.spr.spr_index is not SPR):
            print(self.action)
            self.spr = AnimClass.animate(SPR, 4, 0, True)
            

    def __drawSelf(self):

        self.__findSpr()
        if(self.action == 'walk'):
            if(self.xspd == 0):
                self.spr.image_speed = 0
            else:
                self.spr.image_speed = 1
        sprite = self.spr.get_sprite()
        self.SIZE = self.BASESIZE + self.MASS
        sprite = pygame.transform.scale(sprite, (self.SIZE, self.SIZE))
        sprite = pygame.transform.flip(sprite, self.xscale, False)
        return sprite
        

    def __changePOS(self, XSPD, YSPD, XACC, YACC):

        YSPD += YACC
        if YSPD >= 0 and YACC > 0:
            YACC = 0
        elif YSPD <= 0 and YACC < 0:
            YACC = 0
            
        XSPD += XACC
        if(XSPD >= 0 and XACC > 0):
            XACC = 0
            XSPD = 0
        elif XSPD <= 0 and XACC < 0:
            XACC = 0
            XSPD = 0
            
        self.x += XSPD
        self.y += YSPD
        BOTTOMPOS = self.POS[1] - self.MASS//2 - self.BASESIZE//2

        if self.y >= BOTTOMPOS:
            self.ONGROUND = True
            self.y = BOTTOMPOS
            YSPD = 0
            YACC = 0
            self.action = 'walk'
        else:
            self.ONGROUND = False
            YACC = .15
            self.action = 'jump'
        
        self.xspd = XSPD
        self.yspd = YSPD
        self.xacc = XACC
        self.yacc = YACC

    def control(self, event):

        shot = None
        
        if event.type == KEYDOWN:

            if self.ONGROUND:
                if event.key == K_LEFT:
                    self.xspd = -7
                    self.xscale = True
                elif event.key == K_RIGHT:
                    self.xspd = +7
                    self.xscale = False
                elif event.key == K_UP:
                    self.yspd = -13
                    
            if self.CANSHOOT and self.MASS >= -50:
                curx = int(self.x)
                cury = int(self.y)
                if event.key == K_d:
                    self.xspd = -10
                    self.xacc = .2
                    self.CANSHOOT = False
                    self.MASS -= 2
                    shot = [curx, cury, 15, 0]
                    self.xscale = False
                elif(event.key == K_a):
                    self.xspd = +10
                    self.xacc = -.2
                    self.CANSHOOT = False
                    self.MASS -= 2
                    self.xscale = True
                    shot = [curx, cury, -15, 0]
                elif event.key == K_s:
                    self.yspd = -7
                    self.CANSHOOT = False
                    self.MASS -= 2
                    shot = [curx, cury, 0, 15]
                elif event.key == K_w:
                    self.yspd = 7
                    self.CANSHOOT = False
                    self.MASS -= 2
                    shot = [curx, cury, 0, -15]
                    
                return shot
                        
        elif event.type == KEYUP:

            if event.key == K_q:
                rotationDIR = 0
            elif event.key == K_e:
                rotationDIR = 0
                
            if self.ONGROUND or self.xspd > 0:
                if event.key == K_LEFT:
                    self.xacc = 1
                elif event.key == K_RIGHT:
                    self.xacc = -1
                    
            if not self.CANSHOOT:
                if event.key == K_d:
                    self.CANSHOOT = True
                elif event.key == K_a:
                    self.CANSHOOT = True
                elif event.key == K_s:
                    self.CANSHOOT = True
                elif event.key == K_w:
                    self.CANSHOOT = True


    def displaySelf(self):
        
        self.__changePOS(self.xspd, self.yspd, self.xacc, self.yacc)
        spr = self.__drawSelf()
        self.SURF.blit(spr, (self.x - self.SIZE//2, self.y - self.SIZE//2))
