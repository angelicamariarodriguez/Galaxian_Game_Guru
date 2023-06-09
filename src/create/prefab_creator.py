import pygame
import esper
from enum import Enum
import random
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.engine.service_locator import ServiceLocator
from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_animation import CAnimation



def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity

def create_star(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color, blink_rate: float) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    world.add_component(cuad_entity,
                        CTagStar(blink_rate, col))
    return cuad_entity

def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity

def create_enemy(world: esper.World, pos: pygame.Vector2, enemy_info: dict, enemy_type:str):
    enemy_surface = ServiceLocator.images_services.get(enemy_info[enemy_type]["image"])
    vel = pygame.Vector2(enemy_info["enemy_speed"],0)
    enemy_entity = create_sprite(world, pos, vel, enemy_surface)
    
    world.add_component(enemy_entity,
                        CAnimation(enemy_info[enemy_type]["animations"]))
    world.add_component(enemy_entity, CTagEnemy(enemy_info[enemy_type]["score"]))

def create_bullet(world: esper.World,
                  start_pos: pygame.Vector2,
                  shooter_size: pygame.Vector2,
                  bullet_info: dict):

    bullet_size = pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"])
    vel = pygame.Vector2(0,bullet_info["speed"])
    color = pygame.Color(bullet_info["color"]["r"],
                        bullet_info["color"]["g"],
                        bullet_info["color"]["b"])
    start_pos=pygame.Vector2(start_pos.x+shooter_size[0]/2,
                             start_pos.y+shooter_size[1])
    bullet_entity = create_square(world,bullet_size,start_pos,vel,color)
    world.add_component(bullet_entity, CTagEnemyBullet())

class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2

def create_text(world:esper.World, txt:str, size:int, 
                color:pygame.Color, pos:pygame.Vector2, alignment:TextAlignment) -> int:
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pos + origin))
    return text_entity
    

def create_player_bullet(world: esper.World,
                  start_pos: pygame.Vector2,
                  shooter_size: pygame.Vector2,
                  bullet_info: dict):

    bullet_size = pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"])
    vel = pygame.Vector2(0,bullet_info["speed"]*-1)
    color = pygame.Color(bullet_info["color"]["r"],
                        bullet_info["color"]["g"],
                        bullet_info["color"]["b"])
    start_pos=pygame.Vector2(start_pos.x+shooter_size[0]/2,
                             start_pos.y+shooter_size[1])
    bullet_entity = create_square(world,bullet_size,start_pos,vel,color)
    world.add_component(bullet_entity, CTagPlayerBullet())

def create_player_square(world:esper.World, player_info:dict) -> int:
    player_surface = ServiceLocator.images_services.get(player_info["image"])
    size = player_surface.get_size()
    pos = pygame.Vector2(player_info["position"]["x"] - (size[0]/2), player_info["position"]["y"] - (player_surface.get_size()[1]))
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_surface)
    world.add_component(player_entity, CTagPlayer())
    return player_entity

def create_input_player(world:esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()

    input_fire = world.create_entity()
    input_pause = world.create_entity()
   
    
    world.add_component(input_left, 
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, 
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_fire,
                        CInputCommand("PLAYER_FIRE", pygame.K_z))
    world.add_component(input_pause,
                        CInputCommand("GAME_PAUSE", pygame.K_p))

def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_services.get(explosion_info["image"])
    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(explosion_info["sound"])
    return explosion_entity
    