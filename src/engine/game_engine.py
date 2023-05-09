from src.create.prefab_creator import create_input_player
from src.ecs.systems.s_enemy_basic_firing import system_enemy_basic_firing
from src.ecs.systems.s_enemy_screen_bouncer import system_enemy_screen_bouncer
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_star_controller import system_star_controller
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_star_spawner import system_star_spawner
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_animation import system_animation
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_input_player import system_input_player
import json
import pygame
import esper
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

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            # await asyncio.sleep(0)
        self._clean()

    def _create(self):
        system_star_spawner(self.ecs_world, self.star_cfg, self.window_cfg["size"])
        system_enemy_spawner(self.ecs_world,self.enemy_cfg, self.level_cfg["enemy_spawn_events"])
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        if self.delta_time > 1/30:
         self.delta_time= 1/30

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        
        
        system_star_controller(self.ecs_world,self.screen, self.delta_time, self.bg_color)
        
        if not self._paused:
            system_movement(self.ecs_world, self.delta_time)
            system_enemy_basic_firing(self.ecs_world, self.bullet_cfg["enemy_bullet"])
            self.enemy_movement_right = system_enemy_screen_bouncer(self.ecs_world, self.screen, self.enemy_movement_right, self.enemy_cfg["enemy_speed"])
            
            system_animation(self.ecs_world, self.delta_time)
        
        
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def do_clean(self):
        self._paused = False
    
    def _do_action(self, c_input: CInputCommand):
       
        if c_input.name == "GAME_PAUSE" and c_input.phase == CommandPhase.START:
            self._paused = not self._paused
            #self.p_txt_s.visible = self._paused
