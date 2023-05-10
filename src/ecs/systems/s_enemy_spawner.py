from src.create.prefab_creator import create_enemy
import esper
import pygame

def system_enemy_spawner(world:esper.World, enemies_info:dict, level_info:list):
   
    for enemy_row in level_info:


        
        
        for  i in range(enemy_row["columns"]):
            if enemy_row["enemy_type"]=="Enemy_01":
                pos_adjust=2+(20*i)
            elif enemy_row["enemy_type"]=="Enemy_03":
                pos_adjust=1+(20*i)
            elif enemy_row["enemy_type"]=="Enemy_04" and i >0:
                pos_adjust=40+(20*i)
            else:
               pos_adjust=20*i 

            pos = pygame.Vector2(enemy_row["position"]["x"]+pos_adjust,enemy_row["position"]["y"])

            create_enemy(world, pos, enemies_info,enemy_row["enemy_type"])
        
