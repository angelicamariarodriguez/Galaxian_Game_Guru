import esper
import pygame
from src.create.prefab_creator import TextAlignment, create_text

def system_display_level_restart_msg(world:esper.World, window_info:dict, restart:bool, complete_text_ent:int, get_ready_text_ent:int):
    if restart :
        
        if complete_text_ent==-1 and get_ready_text_ent==-1:
            complete_text_ent= create_text(world, "LEVEL COMPLETE", 8, 
                                pygame.Color(255, 255, 255), pygame.Vector2(window_info["size"]["w"]/2, (window_info["size"]["h"]/2)-10), 
                                TextAlignment.CENTER)

            get_ready_text_ent = create_text(world, "GET READY FOR THE NEXT LEVEL", 8, 
                                pygame.Color(255, 50, 50), pygame.Vector2(window_info["size"]["w"]/2, (window_info["size"]["h"]/2)+5), 
                                TextAlignment.CENTER)
        
        return complete_text_ent, get_ready_text_ent
    
    else: 
        return -1,-1