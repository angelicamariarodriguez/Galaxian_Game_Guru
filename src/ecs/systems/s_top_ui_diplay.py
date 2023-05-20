from src.create.prefab_creator import create_sprite
import esper
import pygame
from src.create.prefab_creator import TextAlignment, create_text
from src.engine.service_locator import ServiceLocator

def system_top_ui_display(ecs_world:esper.World, window_cfg:dict):

    level_flag_surface = ServiceLocator.images_services.get("assets/img/invaders_level_flag.png")

    create_text(ecs_world, "1UP", 8, 
                    pygame.Color(255, 50, 50), pygame.Vector2(25, 5), 
                    TextAlignment.CENTER)
    score_text_entity= create_text(ecs_world, "00", 8, 
                    pygame.Color(255, 255, 255), pygame.Vector2(40, 15), 
                    TextAlignment.CENTER)
        
        
    paused_text_ent = create_text(ecs_world, "PAUSE", 8, 
                    pygame.Color(255, 50, 50), pygame.Vector2(window_cfg["size"]["w"]/2, window_cfg["size"]["h"]/2), 
                    TextAlignment.CENTER)
    

    create_sprite(ecs_world, pygame.Vector2(window_cfg["size"]["w"]-50,8), pygame.Vector2(0,0),level_flag_surface)
    level_text_entity = create_text(ecs_world, "01", 8, 
                    pygame.Color(255, 255, 255), pygame.Vector2(window_cfg["size"]["w"]-30, 15), 
                    TextAlignment.CENTER)

    return score_text_entity, paused_text_ent, level_text_entity