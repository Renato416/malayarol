import pygame
from ui.button import Button
from ui.slider import Slider

class DiceWindow:
    def __init__(self, x, y, dice_class, title="Ventana de Dados"):
        self.rect = pygame.Rect(x, y, 420, 420)
        self.base_w = 420
        self.base_h = 420
        self.scale = 1.0
        self.dice_class = dice_class
        
        self.is_active = True
        self.is_minimized = False
        
        self.dice_count = 1
        self.dices = []
        
        btn_font = pygame.font.SysFont(None, 36)
        small_font = pygame.font.SysFont(None, 24)
        
        self.btn_roll = Button(0, 0, 200, 50, "Lanzar Dados", btn_font)
        self.btn_add = Button(0, 0, 40, 40, "+", btn_font)
        self.btn_sub = Button(0, 0, 40, 40, "-", btn_font)
        self.slider = Slider(0, 0, 8, 160, small_font)
        
        self._rebuild_dices()
        self.update_layout()

    def _rebuild_dices(self):
        self.dices = []
        for i in range(self.dice_count):
            self.dices.append(self.dice_class(0, 0, radius=70, is_gray=(i%2!=0)))

    def update_layout(self):
        cx, cy = self.rect.center
        
        dices_per_row = max(1, min(self.dice_count, 3))
        spacing = 100 * self.scale
        start_x = cx - (spacing * (dices_per_row - 1)) / 2
        
        for i, dice in enumerate(self.dices):
            row = i // 3
            col = i % 3
            dice.x = start_x + col * spacing - 20 * self.scale
            dice.y = (cy - 60 * self.scale) + (row * spacing * 0.8)
            dice.radius = 70 * self.scale * (0.8 if self.dice_count > 3 else 1.0)
            dice.font = pygame.font.SysFont(None, int(dice.radius * 0.5))
        
        btn_w, btn_h = 200 * self.scale, 50 * self.scale
        self.btn_roll.rect.width = btn_w
        self.btn_roll.rect.height = btn_h
        self.btn_roll.rect.centerx = cx - 20 * self.scale
        self.btn_roll.rect.y = self.rect.bottom - 100 * self.scale
        self.btn_roll.font = pygame.font.SysFont(None, int(36 * self.scale))
        
        self.btn_add.rect.width = 40 * self.scale
        self.btn_add.rect.height = 40 * self.scale
        self.btn_add.rect.x = self.btn_roll.rect.right + 10 * self.scale
        self.btn_add.rect.y = self.btn_roll.rect.y + 5 * self.scale
        self.btn_add.font = pygame.font.SysFont(None, int(36 * self.scale))
        
        self.btn_sub.rect.width = 40 * self.scale
        self.btn_sub.rect.height = 40 * self.scale
        self.btn_sub.rect.x = self.btn_roll.rect.left - 50 * self.scale
        self.btn_sub.rect.y = self.btn_roll.rect.y + 5 * self.scale
        self.btn_sub.font = pygame.font.SysFont(None, int(36 * self.scale))

        slider_w = max(4, 8 * self.scale)
        slider_h = 160 * self.scale
        self.slider.rect.width = slider_w
        self.slider.rect.height = slider_h
        self.slider.rect.x = self.rect.right - 40 * self.scale
        self.slider.rect.y = cy - (slider_h / 2)
        self.slider.handle_rect.width = slider_w * 3
        self.slider.handle_rect.height = slider_w * 3
        self.slider.handle_rect.x = self.slider.rect.x - slider_w
        if not self.slider.is_dragging:
            self.slider.handle_rect.y = self.slider.rect.y
        self.slider.font = pygame.font.SysFont(None, int(24 * self.scale))
        
        self.min_h = 32 * self.scale 
        bar_y = self.rect.y + (self.min_h - 20 * self.scale) / 2 if self.is_minimized else self.rect.y + 16 * self.scale

        self.rect_close = pygame.Rect(self.rect.right - 35*self.scale, bar_y, 20*self.scale, 20*self.scale)
        self.rect_min = pygame.Rect(self.rect.right - 65*self.scale, bar_y, 20*self.scale, 20*self.scale)

    def handle_event(self, event):
        if not self.is_active: return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect_close.collidepoint(event.pos):
                self.is_active = False
                return True
            if self.rect_min.collidepoint(event.pos):
                self.is_minimized = not self.is_minimized
                self.update_layout() 
                return True

        if self.is_minimized:
            return False

        if self.slider.handle_event(event) or self.btn_roll.handle_event(event):
            for d in self.dices: d.roll()
            return True
            
        if self.btn_add.handle_event(event) and event.type == pygame.MOUSEBUTTONDOWN:
            if self.dice_count < 6:
                self.dice_count += 1
                self._rebuild_dices()
                self.update_layout()
            return True

        if self.btn_sub.handle_event(event) and event.type == pygame.MOUSEBUTTONDOWN:
            if self.dice_count > 1:
                self.dice_count -= 1
                self._rebuild_dices()
                self.update_layout()
            return True
            
        return False

    def update(self, dt):
        if not self.is_active or self.is_minimized: return
        for d in self.dices:
            d.update(dt)
            d.tension = self.slider.tension

    def draw(self, surface):
        if not self.is_active: return
        
        if self.is_minimized:
            min_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.min_h)
            pygame.draw.rect(surface, (255, 255, 255), min_rect, width=max(1, int(4 * self.scale)), border_radius=int(self.min_h/2))
            self._draw_window_controls(surface)
            return

        pygame.draw.rect(surface, (255, 255, 255), self.rect, width=max(1, int(4 * self.scale)), border_radius=int(40 * self.scale))
        self._draw_window_controls(surface)

        for d in self.dices: d.draw(surface)
        self.btn_roll.draw(surface)
        self.btn_add.draw(surface)
        self.btn_sub.draw(surface)
        self.slider.draw(surface)
        
    def _draw_window_controls(self, surface):
        pygame.draw.line(surface, (255, 255, 255), self.rect_close.topleft, self.rect_close.bottomright, 3)
        pygame.draw.line(surface, (255, 255, 255), self.rect_close.bottomleft, self.rect_close.topright, 3)
        pygame.draw.line(surface, (255, 255, 255), (self.rect_min.left, self.rect_min.centery), (self.rect_min.right, self.rect_min.centery), 3)