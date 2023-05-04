from src.create.prefab_creator import create_star
import esper
import pygame
import random

def system_star_spawner(world:esper.World, star_info:dict, window_info:dict):
    
    color_list=[pygame.Color(star_info["star_colors"][0]["r"],
                            star_info["star_colors"][0]["g"],
                            star_info["star_colors"][0]["b"]),
                pygame.Color(star_info["star_colors"][1]["r"],
                            star_info["star_colors"][1]["g"],
                            star_info["star_colors"][1]["b"]),
                pygame.Color(star_info["star_colors"][2]["r"],
                            star_info["star_colors"][2]["g"],
                            star_info["star_colors"][2]["b"])]           
    for _ in range(star_info["number_of_stars"]):
        
        size = pygame.Vector2(1,1)
        pos = pygame.Vector2(random.randint(0, window_info["w"]), random.randint(0, window_info["h"]))
        vel = pygame.Vector2(0, random.randint(star_info["vertical_speed"]["min"], star_info["vertical_speed"]["max"]))
        color = random.choice(color_list)
        
        create_star(world,size,pos,vel,color)






