# BlobGame.py
# Nate Miller
# Fall 2015

import pygame, sys, random, math, blobClass
from pygame.locals import *
from blobClass import blob

BGimageFileName = 'dungeon_wall.jpg'
FloorFileName = 'Blob_BG.png'
SPRITE01fileName = 'spr_baby_0.png'

pygame.init()
FPSCLOCK = pygame.time.Clock()
GAMETIME = pygame.time.set_timer(25, 60000)

FPS = 60
DWIDTH = 900
DHEIGHT = 600

DISPLAYSURF= pygame.display.set_mode((DWIDTH, DHEIGHT), HWSURFACE | DOUBLEBUF)
TIMEFONT = pygame.font.SysFont("Broadway", 60)
BGimage = pygame.image.load(BGimageFileName).convert()
BG2image = pygame.image.load(FloorFileName).convert()
bgsize = BGimage.get_size()
bg2size = BG2image.get_size()
bgxnum = DWIDTH//bgsize[0] + 1
bgynum = DHEIGHT//bgsize[1] + 1

SPHpos = (DWIDTH//2, 7*DHEIGHT//8)
SPHrot = 0

enemypos = []
badpos = []
shotpos = []

for i in range(10):
    enemypos.append([random.randrange(0, DWIDTH), random.randrange(0, 7*DHEIGHT//8)])
    badpos.append([random.randrange(0, DWIDTH), random.randrange(0, 7*DHEIGHT//8)])
                                         
def main():

    spr_x, spr_y = (DWIDTH//2, 7*DHEIGHT//8)
    BASESIZE = 75
    SpHeart = pygame.image.load(SPRITE01fileName).convert_alpha()
    SpHeart = pygame.transform.scale(SpHeart, (BASESIZE, BASESIZE))
    Alien = blob((spr_x, spr_y), DISPLAYSURF, BASESIZE)

    DOTNUMS = [3, -3]
    bgxmove = 0
    bg2xmove = 0
    TIMER = 0
    gameover = False
    SCORE = 9999

    while True:

        #Pygame Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == 25:
                gameover = True
                if(SCORE == 9999):
                    SCORE = Alien.MASS

            shot = Alien.control(event)
            if(shot is not None):
                shotpos.append(shot)
                        
        #Background and Floor tiling
        for i in range(bgxnum):
            for j in range(bgynum):
                DISPLAYSURF.blit(BGimage, (i*bgsize[0] - bgxmove, j*bgsize[1]))
        for i in range(4):
            DISPLAYSURF.blit(BG2image, (i*bg2size[0] - bg2xmove, SPHpos[1]))

        if Alien.x >= 3*DWIDTH//4:
            Alien.x = 3*DWIDTH//4
            bgspd = Alien.xspd
        elif Alien.x <= 0 + Alien.SIZE//2:
            Alien.x = 0 + Alien.SIZE//2
            bgspd = 0
        else:
            bgspd = max(Alien.xspd//3, 0)  

        #Move the background and floor -- tacky-ly written, needs rewriting
        bgxmove += bgspd
        bg2xmove += bgspd
        if bgxmove >= bgsize[0]: bgxmove = 0
        if bg2xmove >= bg2size[0]: bg2xmove = 0;

        #Move the shots (green circles)
        for tup in shotpos:
            pygame.draw.circle(DISPLAYSURF, (30, 255, 100), (tup[0], tup[1]), 10)
            #Delete when offscreen
            if tup[0] < 0:
                shotpos.remove(tup)
            elif tup[0] > DWIDTH:
                shotpos.remove(tup)
            if tup[1] < 0:
                shotpos.remove(tup)
            elif tup[1] > DHEIGHT:
                shotpos.remove(tup)
            tup[0] += tup[2]
            tup[1] += tup[3]
            
        #Move the yummy enemies (blue)
        for tup in enemypos:
            pygame.draw.circle(DISPLAYSURF, (30, 90, 190), (int(tup[0]), int(tup[1])), 10)
            tup[0] += random.choice(DOTNUMS) - bgspd
            tup[1] += random.choice(DOTNUMS)
            #Change Position when offscreen
            if tup[0] < 0:
                tup[0] = DWIDTH
            elif tup[0] > DWIDTH:
                tup[0] = DWIDTH
            if tup[1] < 0:
                tup[1] = 0
            elif tup[1] > SPHpos[1]:
                tup[1] = SPHpos[1]
            #Check for "collisions" with player -- tacky but less processing overhead than bounding box collision checking
            if(math.sqrt(((tup[0] - Alien.x)**2) + ((tup[1] - Alien.y)**2)) <= Alien.SIZE//2):
                enemypos.remove(tup)
                enemypos.append([random.randrange(0, DWIDTH), random.randrange(0, 7*DHEIGHT//8)])
                Alien.MASS += 5

        #Move the bad enemies (red)
        for tup in badpos:
            pygame.draw.circle(DISPLAYSURF, (255, 90, 90), (int(tup[0]), int(tup[1])), 8)
            tup[0] += random.choice(DOTNUMS) - bgspd
            tup[1] += random.choice(DOTNUMS)
            #Change Position when offscreen
            if tup[0] < 0:
                tup[0] = DWIDTH
            elif tup[0] > DWIDTH:
                tup[0] = DWIDTH
            if tup[1] < 0:
                tup[1] = 0
            elif tup[1] > SPHpos[1]:
                tup[1] = SPHpos[1]
            #Check for "collisions" with player -- tacky but less processing overhead than bounding box collision checking
            if(math.sqrt(((Alien.x - tup[0])**2) + ((Alien.y - tup[1])**2)) <= Alien.SIZE//2):
                badpos.remove(tup)
                badpos.append([random.randrange(0, DWIDTH), random.randrange(0, 7*DHEIGHT//8)])
                Alien.MASS -= 10

        Alien.displaySelf()

        #Timing crap
        if(not gameover):
            TXTSURF = TIMEFONT.render(str(60 - TIMER//1000), True, (255, 180, 30), None)
        else:
            TXTSURF = TIMEFONT.render("Your Score: "+str(SCORE), True, (255, 180, 30), None)
        w, h = TXTSURF.get_size()
        DISPLAYSURF.blit(TXTSURF, (DWIDTH//2 - w//2, int(DHEIGHT * .05)))
        FPSCLOCK.tick(FPS)
        
        TIMER = pygame.time.get_ticks()

        pygame.display.update()

if __name__ == '__main__': main()
    

