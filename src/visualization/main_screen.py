import pygame
from src.config import Config
from src.visualization.button import Button

class Main_Screen:
    # 使用ボタン
    RESET_B, UNDO_B, SETTING_B, QUIT_B = "リセット(R)", "やり直し(Z)", "ゲーム設定(S)", "終了(Q)"
    BUTTONS = [RESET_B, UNDO_B, SETTING_B, QUIT_B]

    def __init__(self, screen):
        """ メイン画面の初期設定 """
        # ボタンリスト
        self.buttons = self._create_buttons(screen)

        # 都市表示円の大きさ
        self.city_radius = Config.MINIMUM_CITY_RADIUS

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.VIDEORESIZE:  # ウィンドウサイズ変更
                print("AAAAAAA")
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.buttons = self._create_buttons(screen)
                width, height = screen.get_size()
                city_radius = min(width, height)*Config.CITY_RADIUS_RATIO
                self.city_radius = min(city_radius, Config.MINIMUM_CITY_RADIUS)

    def draw(self, screen):
        width, height = screen.get_size()
        """ 背景設定 """
        screen.fill(Config.MAIN_BG_COLOR)  # 都市を表示する領域
        pygame.draw.rect(screen, Config.UI_BG_COLOR, (0, height - Config.UI_HEIGHT, width, Config.UI_HEIGHT))  # UI部分の色を変える
        pygame.draw.rect(screen, Config.DSP_BG_COLOR, (0, height - Config.UI_HEIGHT - Config.DSP_HEIGHT, width, Config.DSP_HEIGHT))  # DSP部分の色を変える

        # ボタンの描画
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

        return buttons