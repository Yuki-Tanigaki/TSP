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
        # ボタンリスト
        self.buttons = self._create_buttons(screen)

        if font_name:
            self.city_font = pygame.font.Font(font_name, Config.CITY_FONT_SIZE) # フォント設定
            self.route_font = pygame.font.Font(font_name, Config.ROUTE_FONT_SIZE) # フォント設定
        else:
            raise ValueError(f"Cannot find font named {Config.FONT_NAME}")

        # TSP
        self.tsp = None

    def set_tsp(self, tsp):
        self.tsp = tsp

    def handle_events(self, events, screen):
        running = True
        current_screen = Config.MAIN_SCREEN
        for event in events:
            if event.type == pygame.QUIT:  # バツでソフトを終了
                running = False
            if event.type == pygame.VIDEORESIZE:  # ウィンドウサイズ変更
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.buttons = self._create_buttons(screen)
                width, height = screen.get_size()
                city_radius = min(width, height)*Config.CITY_RADIUS_RATIO
                self.city_radius = max(city_radius, Config.MINIMUM_CITY_RADIUS)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running, current_screen = self._handle_click(event.pos, screen)
            elif event.type == pygame.KEYDOWN:
                running, current_screen = self._handle_key(event, screen)

        return running, current_screen, screen

    def draw(self, screen):
        width, height = screen.get_size()
        """ 背景設定 """
        screen.fill(Config.MAIN_BG_COLOR)  # 都市を表示する領域
        pygame.draw.rect(screen, Config.UI_BG_COLOR, (0, height - Config.UI_HEIGHT, width, Config.UI_HEIGHT))  # UI部分の色を変える
        pygame.draw.rect(screen, Config.DSP_BG_COLOR, (0, height - Config.UI_HEIGHT - Config.DSP_HEIGHT, width, Config.DSP_HEIGHT))  # DSP部分の色を変える

        """ 都市ルートの描画 """
        # 都市円の描画
        for i, city in enumerate(self.tsp.cities):
            screen_x, screen_y = self._coord_to_screen(city, screen)
            if i in self.player_route:
                pygame.draw.circle(screen, Config.CITY_COLOR_SELECTED, (screen_x, screen_y), self.city_radius)
            else:
                pygame.draw.circle(screen, Config.CITY_COLOR, (screen_x, screen_y), self.city_radius)
            text_surface = self.city_font.render(str(i), True, Config.CITY_TEXT_COLOR)
            screen.blit(text_surface, (screen_x - self.city_radius - Config.CITY_TEXT_OFFSET, 
                                       screen_y  - self.city_radius - Config.CITY_TEXT_OFFSET))

        # ルートの描画
        if len(self.player_route) > 1:
            for i in range(len(self.player_route) - 1):
                city1 = self._coord_to_screen(self.tsp.cities[self.player_route[i]], screen)
                city2 = self._coord_to_screen(self.tsp.cities[self.player_route[i + 1]], screen)
                pygame.draw.line(screen, Config.LINE_COLOR, city1, city2, 2)

            # 最後の都市から最初の都市へ閉じる（巡回ルート）
            if len(self.player_route) == self.tsp.num_cities:
                pygame.draw.line(screen, Config.LINE_COLOR, 
                                 self._coord_to_screen(self.tsp.cities[self.player_route[-1]], screen), 
                                 self._coord_to_screen(self.tsp.cities[self.player_route[0]], screen), 2)
        
        """ コンソールの描画 """
        width, height = screen.get_size()
        info_text = "ルート: " + " -> ".join(map(str, self.player_route))
        text_surface = self.route_font.render(info_text, True, Config.ROUTE_TEXT_COLOR)
        # y_pos = height - (Config.UI_HEIGHT + Config.DSP_HEIGHT) + (Config.DSP_HEIGHT - Config.FONT_SIZE) // 2
        y_pos = height - (Config.UI_HEIGHT + Config.DSP_HEIGHT)
        screen.blit(text_surface, (10, y_pos))
        if len(self.player_route) == self.tsp.num_cities:
            result_text = f"  総ルート長： {self.tsp.compute_route_distance(self.player_route):.3f}"
            text_surface = self.route_font.render(result_text, True, Config.ROUTE_TEXT_COLOR)
            screen.blit(text_surface, (10, y_pos + Config.ROUTE_FONT_SIZE + 5))

        """ ボタンの描画 """
        for _, b in self.buttons.items():
            b.draw(screen)

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

        """ 入力の配置を動的に決定 """
        x_start = calculate_x_start(len(self.INPUTS))
        y_pos = height - Config.UI_HEIGHT + (Config.UI_HEIGHT - Config.BUTTON_HEIGHT) // 2
        INPUT_box1 = InputBox(100, 100, 140, 32)

        return buttons
    
    def _coord_to_screen(self, coord, screen):
        """ 座標を画面スケールに変換 """
        x, y = coord
        width, height = screen.get_size()
        height += -1 * (Config.UI_HEIGHT + Config.DSP_HEIGHT)
        margin_x = width * Config.MARGIN_RATIO
        margin_y = height * Config.MARGIN_RATIO
        
        screen_x = int(margin_x + (x - Config.COORD_MIN) / (Config.COORD_MAX - Config.COORD_MIN) * (width - 2 * margin_x))
        screen_y = int(margin_y + (y - Config.COORD_MIN) / (Config.COORD_MAX - Config.COORD_MIN) * (height - 2 * margin_y))
        
        return screen_x, screen_y
    
    def _handle_click(self, pos, screen):
        running = True
        current_screen = Config.MAIN_SCREEN
        """ クリック処理（都市 or ボタン） """
        for button_name, button in self.buttons.items():
            if button.rect.collidepoint(pos):
                if button_name == "リセット(R)":
                    self._reset_route()
                elif button_name == "やり直し(Z)":
                    self._undo_last_selection()
                elif button_name == "ゲーム設定(S)":
                    current_screen = Config.SETTINGS_SCREEN  # 設定画面へ移行
                elif button_name == "終了(Q)":
                    running = False

        # 都市の選択処理
        for i, city in enumerate(self.tsp.cities):
            screen_x, screen_y = self._coord_to_screen(city, screen)

            if np.linalg.norm(np.array(pos) - np.array([screen_x, screen_y])) < self.city_radius*1.2:
                if i not in self.player_route:
                    self.player_route.append(i)
        return running, current_screen

    def _handle_key(self, event, screen):
        running = True
        current_screen = Config.MAIN_SCREEN
        if event.key == pygame.K_r:  
            self._reset_route()  # ルートをリセット
        elif event.key == pygame.K_q:  
            running = False  # 終了
        elif event.key == pygame.K_z:  
            self._undo_last_selection()  # 設定したルートをひとつ戻す
        elif event.key == pygame.K_s:
            current_screen = Config.SETTINGS_SCREEN  # 設定画面に移行
        
        return running, current_screen

    def _reset_route(self):
        """ ルートをリセット """
        self.player_route = []

    def _undo_last_selection(self):
        """ 最後の選択を元に戻す """
        if self.player_route:
            self.player_route.pop()
