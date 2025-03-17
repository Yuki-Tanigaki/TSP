import pygame
import numpy as np
from config import Config
from tsp import TSP
from src.visualization.main_screen import Main_Screen
from src.visualization.setting_screen import Setting_Screen

class Launcher:
    def __init__(self):
        """ Pygameの初期設定 """
        pygame.init()
        pygame.display.set_caption("Multi-objective Traveling Salesman Problem Demonstration")
        self.screen = pygame.display.set_mode((Config.DEFAULT_WIDTH, Config.DEFAULT_HEIGHT + Config.UI_HEIGHT + Config.DSP_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = Config.MAIN_SCREEN  # 初期状態はメイン画面

        """ 画面の初期設定 """
        self.main_screen = Main_Screen(self.screen)
        self.setting_screen = Setting_Screen(self.screen)

        """ TSPの初期設定 """
        self.tsp = None
        for _ in range(Config.DEFAULT_OBJECTIVES):
            self.tsp = TSP(num_cities=Config.DEFAULT_CITIES, coord_min=Config.COORD_MIN, coord_max=Config.COORD_MAX)

        self.main_screen.set_tsp(self.tsp)
        self.setting_screen.set_tsp(self.tsp)

        """ GAの初期設定 """
        rng = np.random.default_rng(42)


    def run(self):
        """ メインループ """
        while self.running:
            events = pygame.event.get()
            if self.current_screen == Config.MAIN_SCREEN:
                self.running, self.current_screen, self.screen = self.main_screen.handle_events(events, self.screen)
                self.main_screen.draw(self.screen)
            if self.current_screen == Config.SETTINGS_SCREEN:
                self.running, self.current_screen, self.screen = self.setting_screen.handle_events(events, self.screen)
                self.setting_screen.draw(self.screen)
            # self.screen.fill(Config.BG_COLOR)
            # self.handle_events()
            # self.draw()
            pygame.display.flip()
            self.clock.tick(Config.FPS)

if __name__ == "__main__":
    launcher = Launcher()
    launcher.run()

    pygame.quit()