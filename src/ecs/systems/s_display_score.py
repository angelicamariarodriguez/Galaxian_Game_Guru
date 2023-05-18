import esper
import pygame
from src.create.prefab_creator import TextAlignment, create_text

def system_display_score(world:esper.World, text_entity:int, score:int):

    world.delete_entity(text_entity)

    text_entity = create_text(world, str(score), 8, 
                    pygame.Color(255, 255, 255), pygame.Vector2(40, 15), 
                    TextAlignment.CENTER)
    return text_entity
    