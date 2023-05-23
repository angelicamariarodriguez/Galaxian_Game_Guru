import esper
import pygame
from src.create.prefab_creator import TextAlignment, create_text
from src.engine.service_locator import ServiceLocator

def system_display_game_start(world:esper.World, text_entity:int, display_time:float, delta_time:float, window_cfg:dict):
    
    if display_time==0:
        text_entity = create_text(world, "GAME START", 8, 
                    pygame.Color(255, 255, 255), pygame.Vector2(window_cfg["size"]["w"]/2, window_cfg["size"]["h"]/2), 
                    TextAlignment.CENTER)
        ServiceLocator.sounds_service.play('assets/snd/game_start.ogg')

    display_time+=delta_time
    
    
    if display_time>2.5:
        world.delete_entity(text_entity)
        return 0, False, text_entity
    
    return display_time, True, text_entity
