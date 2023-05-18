import esper
import pygame
from src.create.prefab_creator import TextAlignment, create_text

def system_display_game_start(world:esper.World, text_entity:int, display_time:float, delta_time:float):
    display_time+=delta_time
    
    
    if display_time>2:
        world.delete_entity(text_entity)
        return 0, False
    
    return display_time, True
