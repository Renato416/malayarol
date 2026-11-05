import pygame

class CharacterToken:
    def __init__(self, x, y, radius, color, label="P1"):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.label = label
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.has_been_moved = False

    def draw(self, surface, font):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 2)
        txt = font.render(self.label, True, (255, 255, 255))
        surface.blit(txt, txt.get_rect(center=(int(self.x), int(self.y))))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dx = event.pos[0] - self.x
            dy = event.pos[1] - self.y
            if (dx**2 + dy**2) <= self.radius**2:
                self.is_dragging = True
                self.has_been_moved = True
                self.drag_offset_x = dx
                self.drag_offset_y = dy
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.x = event.pos[0] - self.drag_offset_x
            self.y = event.pos[1] - self.drag_offset_y
            return True
        return False

class CharacterPanel:
    def __init__(self, x, y, width, font):
        self.rect = pygame.Rect(x, y, width, 100)
        self.font = font
        
        self.colors = [
            (220, 50, 50),   # P1: Rojo
            (50, 180, 50),   # P2: Verde
            (50, 100, 220),  # P3: Azul
            (230, 160, 30),  # P4: Naranja
            (160, 50, 200),  # P5: Púrpura
            (40, 180, 180)   # P6: Cian
        ]
        
        self.btn_minus_rect = pygame.Rect(0, 0, 30, 30)
        self.btn_plus_rect = pygame.Rect(0, 0, 30, 30)
        
        self.tokens = []
        self.reset()

    def reset(self):
        """Reinicia la ventana a solo 1 jugador y restablece su estado a la barra"""
        self.tokens.clear()
        self._add_token()

    def _add_token(self):
        if len(self.tokens) < 6:
            idx = len(self.tokens)
            label = f"P{idx + 1}"
            color = self.colors[idx % len(self.colors)]
            token = CharacterToken(0, 0, 18, color, label)
            self.tokens.append(token)
            self.reposition_tokens(force_all=True)

    def _remove_token(self):
        if len(self.tokens) > 1:
            self.tokens.pop()
            self.reposition_tokens(force_all=True)

    def reposition_tokens(self, force_all=False):
        """Reorganiza en la ventana las fichas. Si force_all es True, regresa todas a la barra."""
        start_y = self.rect.y + 60
        spacing = 45
        for i, token in enumerate(self.tokens):
            if force_all:
                token.has_been_moved = False
            
            if not token.has_been_moved:
                token.x = self.rect.centerx
                token.y = start_y + (i * spacing)

    def update_button_positions(self):
        btn_y = self.rect.bottom - 25
        self.btn_minus_rect.center = (self.rect.x + 30, btn_y)
        self.btn_plus_rect.center = (self.rect.right - 30, btn_y)

    def update_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.rect.height = 60 + (len(self.tokens) * 45) + 55
        self.update_button_positions()
        self.reposition_tokens()

    def handle_event(self, event):
        for token in reversed(self.tokens):
            if token.handle_event(event):
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_plus_rect.collidepoint(event.pos):
                self._add_token()
                return True
            elif self.btn_minus_rect.collidepoint(event.pos):
                self._remove_token()
                return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, width=2, border_radius=15)
        
        title = self.font.render("Jugadores", True, (255, 255, 255))
        surface.blit(title, (self.rect.centerx - title.get_width() // 2, self.rect.y + 15))
        
        for token in self.tokens:
            token.draw(surface, self.font)

        pygame.draw.rect(surface, (255, 255, 255), self.btn_minus_rect, width=2, border_radius=5)
        txt_minus = self.font.render("-", True, (255, 255, 255))
        surface.blit(txt_minus, txt_minus.get_rect(center=self.btn_minus_rect.center))

        pygame.draw.rect(surface, (255, 255, 255), self.btn_plus_rect, width=2, border_radius=5)
        txt_plus = self.font.render("+", True, (255, 255, 255))
        surface.blit(txt_plus, txt_plus.get_rect(center=self.btn_plus_rect.center))