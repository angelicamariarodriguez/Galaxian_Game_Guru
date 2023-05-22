import esper
import pygame
from src.create.prefab_creator import TextAlignment, create_text

def system_display_player(world:esper.World, pl_s, display_time:float, delta_time:float):
    display_time+=delta_time
    
    
    if display_time>2:
        pl_s.visible = True
        return 0, True
    
    return display_time, False
