from src.ecs.components.c_surface import CSurface
import esper
import pygame

def system_pause_text_blinker(world:esper.World, text_surface:pygame.Surface, paused:bool, paused_time:float, delta_time:float):
    
    if paused:
        paused_time += delta_time*2
        if int(paused_time)%2==0:
            text_surface.visible=True
        else:
            text_surface.visible=False
        
        return paused_time
