from src.ecs.systems.s_display_level_restart_msg import system_display_level_restart_msg
from src.ecs.systems.s_level_restart import system_level_restart
from src.ecs.systems.s_top_ui_diplay import system_top_ui_display
from src.ecs.systems.s_display_game_start import system_display_game_start
from src.ecs.systems.s_pause_text_blinker import system_pause_text_blinker
from src.create.prefab_creator import create_input_player, create_player_bullet, create_player_square
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.systems.s_collision_enemy_bullet_with_player import system_collision_enemy_bullet_with_player
from src.ecs.systems.s_collision_player_bullet_with_enemy import system_collision_player_bullet_with_enemy
from src.ecs.systems.s_end_explosion import system_end_explosion
from src.ecs.systems.s_enemy_basic_firing import system_enemy_basic_firing
from src.ecs.systems.s_enemy_screen_bouncer import system_enemy_screen_bouncer
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_limit_bullet import system_limit_bullet
from src.ecs.systems.s_limit_player import system_limit_player
from src.ecs.systems.s_star_controller import system_star_controller
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_star_spawner import system_star_spawner
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_animation import system_animation
from src.create.prefab_creator import TextAlignment, create_text
import json
import pygame
import esper
import asyncio
class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]),
            pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.enemy_movement_right = False
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()
        self._paused = False
        self.paused_time=0.0
        self.player_score = 0
        self.current_level = 1
        self._game_start = True
        self.game_start_time = 0.0
        self.level_enemies_spawned = False
        self.restart_time =0.0
        self._lvl_restart= False
        self.complete_text_ent=-1
        self.get_ready_text_ent=-1


    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/starfield.json", encoding="utf-8") as starfield_file:
            self.star_cfg = json.load(starfield_file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as enemies_file:
            self.enemy_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as level_file:
            self.level_cfg = json.load(level_file)
        with open("assets/cfg/bullets.json", encoding="utf-8") as bullets_file:
            self.bullet_cfg = json.load(bullets_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/explosion.json") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        
        self._player_entity = create_player_square(self.ecs_world, self.player_cfg)
        self._player_c_vel = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_trans = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        create_input_player(self.ecs_world)
        system_star_spawner(self.ecs_world, self.star_cfg, self.window_cfg["size"])
       

        self.score_text_entity, paused_text_ent, self.game_start_text_ent, self.level_text_entity = system_top_ui_display(self.ecs_world, self.window_cfg)
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = self._paused

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        if self.delta_time > 1/30:
         self.delta_time= 1/30

    def _process_events(self):
        for event in pygame.event.get():
            if not self._game_start:
                system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        
        system_movement(self.ecs_world, self.delta_time,self._paused)
        system_star_controller(self.ecs_world,self.screen, self.delta_time, self.bg_color)
        self.paused_time= system_pause_text_blinker(self.p_txt_s, self._paused, self.paused_time,self.delta_time )
        system_limit_player(self.ecs_world, self._player_entity, self.screen)
        system_limit_bullet(self.ecs_world, self.screen)
        if self._game_start:
            self.game_start_time, self._game_start = system_display_game_start(self.ecs_world,self.game_start_text_ent,self.game_start_time, self.delta_time)
        
        else:
            if not self._paused:
                if not self.level_enemies_spawned:
                    system_enemy_spawner(self.ecs_world,self.enemy_cfg, self.level_cfg["enemy_spawn_events"])
                    self.level_enemies_spawned=True

                
                
                system_enemy_basic_firing(self.ecs_world, self.bullet_cfg["enemy_bullet"])
                self.enemy_movement_right = system_enemy_screen_bouncer(self.ecs_world, self.screen, self.enemy_movement_right, self.enemy_cfg["enemy_speed"])
                
                
                system_enemy_basic_firing(self.ecs_world, self.bullet_cfg["enemy_bullet"])
                self.player_score+= system_collision_player_bullet_with_enemy(self.ecs_world, self.explosion_cfg)
                self.score_text_entity = self.system_display_score(self.score_text_entity, self.player_score)
                
                system_collision_enemy_bullet_with_player(self.ecs_world, self._player_entity, self.explosion_cfg, self.delta_time)
                system_end_explosion(self.ecs_world)
                self.bullets_alive = len(self.ecs_world.get_component(CTagPlayerBullet))
                
                #restart systems
                self.complete_text_ent, self.get_ready_text_ent = system_display_level_restart_msg(self.ecs_world, 
                                                                                                    self.window_cfg,
                                                                                                    self._lvl_restart, 
                                                                                                    self.complete_text_ent, 
                                                                                                    self.get_ready_text_ent)        
                self.restart_time, self._lvl_restart, self.current_level= system_level_restart(self.ecs_world, 
                                                                            self.enemy_cfg, 
                                                                            self.level_cfg["enemy_spawn_events"], 
                                                                            self.delta_time, 
                                                                            self.restart_time,
                                                                            self.complete_text_ent, 
                                                                            self.get_ready_text_ent,
                                                                            self.current_level)
                self.level_text_entity = self.system_display_level(self.level_text_entity, self.current_level)
                
                #pause settings
                system_animation(self.ecs_world, self.delta_time)
                self.p_txt_s.visible = self._paused
                self.paused_time=0
                

     
        
        self.ecs_world._clear_dead_entities()
        
       
    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        self._paused = False
        
        pygame.quit()
           
            

    def _do_action(self, c_input:CInputCommand):
        
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_vel.vel.x += self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_vel.vel.x -= self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_FIRE" and self.bullets_alive == 0:
            if c_input.phase == CommandPhase.START:
                create_player_bullet(self.ecs_world, 
                              self._player_c_trans.pos, 
                              self._player_c_s.area.size, 
                              self.bullet_cfg['player_bullet'])
            elif c_input.phase == CommandPhase.END:
                pass
        if c_input.name == "GAME_PAUSE" and c_input.phase == CommandPhase.START:  
        
            self._paused = not self._paused

    def system_display_score(self,text_entity:int, score:int):

        self.ecs_world.delete_entity(text_entity)

        if score==0:
            text="00"
        else:
            text=str(score)

        text_entity = create_text(self.ecs_world, text, 8, 
                        pygame.Color(255, 255, 255), pygame.Vector2(45, 15), 
                        TextAlignment.CENTER)
        return text_entity  

    def system_display_level(self,text_entity:int, level:int):

        self.ecs_world.delete_entity(text_entity)

        if level==1:
            text="01"
        elif level>=10:
            text = str(level)
        else:
            text="0{}".format(str(level))

        text_entity = create_text(self.ecs_world, text, 8, 
                    pygame.Color(255, 255, 255), pygame.Vector2(self.window_cfg["size"]["w"]-30, 15), 
                    TextAlignment.CENTER)
        return text_entity    
        
            