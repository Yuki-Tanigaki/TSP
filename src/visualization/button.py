import pygame
from src.config import Config

class Button:
    def __init__(self, x, y, w, h, text=''):
        font_name = pygame.font.match_font(Config.FONT_NAME)
        if font_name:
            font = pygame.font.Font(font_name, Config.BUTTON_FONT_SIZE) # フォント設定
        else:
            raise ValueError(f"Cannot find font named {Config.FONT_NAME}")
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.text_surface = font.render(text, True, Config.BUTTON_TEXT_COLOR)
        self.active = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = Config.BUTTON_HOVER_COLOR if self.rect.collidepoint(mouse_pos) else Config.BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        screen.blit(self.text_surface, self.text_surface.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

    def onClick(self):
        r = self.active
        self.active = False
        return r
    
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        font_name = pygame.font.match_font(Config.FONT_NAME)
        if font_name:
            self.font = pygame.font.Font(font_name, Config.INPUT_FONT_SIZE) # フォント設定
        else:
            raise ValueError(f"Cannot find font named {Config.FONT_NAME}")
        self.rect = pygame.Rect(x, y, w, h)
        self.color = Config.INPUT_COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
    def handle_event(self, event):
        r = ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = Config.INPUT_COLOR_ACTIVE if self.active else Config.INPUT_COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    r = self.text
                    self.text = ''
                elif event.key == pygame.K_DELETE:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)
        return r
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
