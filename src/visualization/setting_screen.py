import pygame
import numpy as np

from src.config import Config
from src.visualization.button import Button, InputBox

class Setting_Screen:
    # 使用ボタン
    APPLY_B, RETURN_B = "設定を適用(A)", "ゲームに戻る(R)"
    BUTTONS = [APPLY_B, RETURN_B]
    INPUT_CITIES, INPUT_OBJECTIVES = "都市数", "目的数"
    INPUTS = [INPUT_CITIES, INPUT_OBJECTIVES]

    def __init__(self, screen):
        """ 設定画面の初期設定 """
        font_name = pygame.font.match_font(Config.FONT_NAME)
        if font_name:
            self.city_font = pygame.font.Font(font_name, Config.CITY_FONT_SIZE) # フォント設定
            self.route_font = pygame.font.Font(font_name, Config.ROUTE_FONT_SIZE) # フォント設定
        else:
            raise ValueError(f"Cannot find font named {Config.FONT_NAME}")
        
        # ボタンリスト
        self.buttons = self._create_buttons(screen)
        self.inputs = self._create_inputs(screen)

    def handle_events(self, events, screen, tsp):
        running = True
        current_screen = Config.MAIN_SCREEN
        for event in events:
            if event.type == pygame.QUIT:  # バツでソフトを終了
                running = False
            if event.type == pygame.VIDEORESIZE:  # ウィンドウサイズ変更
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.buttons = self._create_buttons(screen)
                self.inputs = self._create_inputs(screen)
                width, height = screen.get_size()
                city_radius = min(width, height)*Config.CITY_RADIUS_RATIO
                self.city_radius = max(city_radius, Config.MINIMUM_CITY_RADIUS)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running, current_screen = self._handle_click(event.pos, screen)
            elif event.type == pygame.KEYDOWN:
                running, current_screen = self._handle_key(event, screen)

        return running, current_screen, screen

    def draw(self, screen, tsp):
        pass

    def _create_buttons(self, screen):
        """ ボタンの配置を動的に決定 """
        width, height = screen.get_size()
        
        def calculate_x_start(num_buttons):
            return (width - (Config.BUTTON_WIDTH * num_buttons + Config.BUTTON_GAP * 2)) // 2

        x_start = calculate_x_start(len(self.BUTTONS))
        y_pos = height - Config.UI_HEIGHT + (Config.UI_HEIGHT - Config.BUTTON_HEIGHT) // 2
        buttons = {}
        for i, button_name in enumerate(self.BUTTONS):
            buttons[button_name] = Button(x_start + (Config.BUTTON_WIDTH + Config.BUTTON_GAP) * i, y_pos, Config.BUTTON_WIDTH, Config.BUTTON_HEIGHT, text=button_name)

        return buttons
    
    def _create_inputs(self, screen):
        """ 入力の配置を動的に決定 """
        width, height = screen.get_size()

        def calculate_x_start(num_buttons):
            return (width - (Config.BUTTON_WIDTH * num_buttons + Config.BUTTON_GAP * 2)) // 2
        
        x_start = calculate_x_start(len(self.INPUTS))
        y_pos = height - Config.UI_HEIGHT + (Config.UI_HEIGHT - Config.BUTTON_HEIGHT) // 2
        inputs = {}
        for i, input_name in enumerate(self.INPUTS):
            inputs[input_name] = InputBox(x_start + (Config.BUTTON_WIDTH + Config.BUTTON_GAP) * i, y_pos, Config.BUTTON_WIDTH, Config.BUTTON_HEIGHT)

        return inputs
    
    def _handle_click(self, pos, screen):
        pass

    def _handle_key(self, event, screen):
        pass