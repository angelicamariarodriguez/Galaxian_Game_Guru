from src.create.prefab_creator import create_enemy
import esper
import pygame

def system_enemy_spawner(world:esper.World, enemies_info:dict, level_info:list):
   
    row=0
    for enemy_row in level_info:
        columns=enemy_row["columns"]

        if columns >10:
            columns=10
        elif columns<2:
            columns=2
        elif columns%2!=0:
            columns+=1
        
        if columns>=4:
            pos_x=30+10*(10-columns)       
        else: 
            pos_x = 90  

        pos_y=15+15*row
        for  i in range(columns):
            pos_adjust=20*i 
            if columns==2 and i>0:
                pos_adjust+=40

            if enemy_row["enemy_type"]=="Enemy_03":
                pos_adjust+=1
            elif enemy_row["enemy_type"]=="Enemy_01" :
                pos_adjust+=2          

            pos = pygame.Vector2(pos_x+pos_adjust,pos_y)

            create_enemy(world, pos, enemies_info,enemy_row["enemy_type"])

        
        row+=1
        
