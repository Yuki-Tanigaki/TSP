import pygame
import numpy as np
from config import Config
from tsp import TSP
from src.visualization.main_screen import Main_Screen

class Launcher:
    # 画面の状態を管理
    MAIN_SCREEN = "main"
    SETTINGS_SCREEN = "settings"

    def __init__(self):
        """ Pygameの初期設定 """
        pygame.init()
        pygame.display.set_caption("Multi-objective Traveling Salesman Problem Demonstration")
        self.screen = pygame.display.set_mode((Config.DEFAULT_WIDTH, Config.DEFAULT_HEIGHT + Config.UI_HEIGHT + Config.DSP_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = self.MAIN_SCREEN  # 初期状態はメイン画面

        """ メイン画面の初期設定 """
        self.main_screen = Main_Screen(self.screen)

        """ TSPの初期設定 """
        self.tsp = []
        for _ in range(Config.DEFAULT_OBJECTIVES):
            self.tsp = TSP(num_cities=Config.DEFAULT_CITIES, coord_min=Config.COORD_MIN, coord_max=Config.COORD_MAX)

        """ GAの初期設定 """
        rng = np.random.default_rng(42)

    def run(self):
        """ メインループ """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # バツでソフトを終了
                        self.running = False
            if self.current_screen == self.MAIN_SCREEN:
                self.main_screen.handle_events(pygame.event.get())
                self.main_screen.draw(self.screen)
            # self.screen.fill(Config.BG_COLOR)
            # self.handle_events()
            # self.draw()
            pygame.display.flip()
            self.clock.tick(Config.FPS)

if __name__ == "__main__":
    launcher = Launcher()
    launcher.run()

    pygame.quit()