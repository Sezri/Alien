##AnimClass.py
##Nate Miller
##Fall 2015

import pygame

class animate(object):
    
    def __init__(self, spr_list, anim_spd, image_index = 0, doreverse = False):

        self.sprite_index = []
        self.spr_index = spr_list
        for i in spr_list:
            self.sprite_index.append(pygame.image.load(i))
        
        self.speed = anim_spd
        self.image_speed = 1
        self.spdnum = 0
        self.image_index = image_index

        
        if(doreverse):
            templist = self.sprite_index.copy()
            templist.reverse()
            for j in range(len(templist)):
                self.sprite_index.append(templist[j])

        self.images = len(self.sprite_index)

    def get_sprite(self):
        self.spdnum += self.image_speed
        if(self.spdnum >= self.speed):
            self.image_index += 1
            self.spdnum = 0
            if(self.image_index >= self.images):
                self.image_index = 0
            
        spr = self.sprite_index[self.image_index]
        return spr
