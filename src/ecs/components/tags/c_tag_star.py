import pygame
class CTagStar:
    def __init__(self, blink_rate:float, orig_color:pygame.Color):
        self.blink_rate = blink_rate    
        self.orig_color = orig_color
        self.blink_time = 0.0
        self.show = True
