from dataclasses import dataclass

# デモの設定値はここで一括管理
@dataclass(frozen=True)
class Config:
    """ 画面の状態を管理 """
    MAIN_SCREEN = "main"
    SETTINGS_SCREEN = "settings"

    """ 可視化で使う設定 """
    WHITE = (255, 255, 255)  # 白色
    LIGHT_GRAY: tuple = (200, 200, 200)  # ライトグレー
    GRAY: tuple = (100, 100, 100)  # グレー
    DRAK_GRAY: tuple = (50, 50, 50)  # ダークグレー
    BLACK = (0, 0, 0)  # 黒色
    LIGHT_BLUE = (0, 150, 255)  # ライトブルー
    LIGHT_SKY_BLUE = (141, 182, 205)  # ライトスカイブルー3
    DODGER_BLUE = (28, 134, 238)  # ダガーブルー

    FONT_SIZE: int = 16  # フォントサイズ
    FONT_NAME: str = 'notosansmonocjkjp'  # Ubuntu18.04 標準日本語フォント
    FPS: int = 60  # フレームレート

    """ メイン画面 """
    DEFAULT_WIDTH: int = 800  # 初期画面幅
    DEFAULT_HEIGHT: int = 600  # 初期画面高さ
    UI_HEIGHT: int = 60  # UIエリアの高さ
    DSP_HEIGHT: int = 70  # DSPエリアの高さ

    MAIN_BG_COLOR: tuple = LIGHT_GRAY  # メイン画面の背景色
    CITY_COLOR: tuple = LIGHT_BLUE  # 都市の色
    CITY_COLOR_SELECTED: tuple = DRAK_GRAY  # 選択済み都市の色
    LINE_COLOR: tuple = BLACK  # 経路の線の色
    CITY_RADIUS_RATIO: float = 0.02  # 画面横サイズに対する都市サイズの割合
    MINIMUM_CITY_RADIUS: int = 8  # 都市円の描画サイズの下限
    CITY_FONT_SIZE: int = 18  # 都市のフォントサイズ
    CITY_TEXT_COLOR: tuple = BLACK  # 都市テキストの色
    CITY_TEXT_OFFSET: int = 7  # 都市テキストオフセット

    UI_BG_COLOR: tuple = BLACK  # UI画面の背景色
    BUTTON_COLOR: tuple = DRAK_GRAY  # ボタンの基本色
    BUTTON_HOVER_COLOR: tuple = GRAY  # ホバー時のボタンの色
    BUTTON_WIDTH: int = 120  # ボタンの横幅
    BUTTON_HEIGHT: int = 40  # ボタンの高さ
    BUTTON_GAP: int = 30  # ボタン間の幅
    BUTTON_FONT_SIZE: int = 18  # ボタンのフォントサイズ
    BUTTON_TEXT_COLOR: tuple = WHITE  # ボタンのテキストの色
    
    DSP_BG_COLOR: tuple = WHITE  # DSP画面の背景色
    ROUTE_FONT_SIZE: int = 24  # ボタンのフォントサイズ
    ROUTE_TEXT_COLOR: tuple = BLACK  # ボタンのテキストの色

    """ 設定画面 """
    INPUT_FONT_SIZE: int = 16  # 入力ボックスのフォントサイズ
    INPUT_COLOR_INACTIVE: tuple = LIGHT_SKY_BLUE  # 入力ボックスの色（非アクティブ）
    INPUT_COLOR_ACTIVE: tuple = DODGER_BLUE  # 入力ボックスの色（アクティブ）
    

    MARGIN_RATIO: float = 0.05  # 画面の5%を余白として確保

    """ TSPの設定 """
    DEFAULT_CITIES: int = 10  # 初期都市数
    COORD_MIN: int = 0  # 都市座標のスケール範囲
    COORD_MAX: int = 100  # 都市座標のスケール範囲
    DEFAULT_OBJECTIVES: int = 1  # 初期目的数

    """ 最適化の設定 """
    SEED: int = 42  # 乱数シード