import pygame

class Slider:
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        # El agarrador "T" será un poco más ancho que la barra
        self.handle_rect = pygame.Rect(x - width, y, width * 3, width * 3)
        self.font = font
        self.is_dragging = False
        self.tension = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.is_dragging = True
                return False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                self.tension = 0.0
                self.handle_rect.y = self.rect.y
                return True # Devuelve True para indicar que se soltó y debe lanzarse
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                new_y = event.pos[1]
                # Limitar el movimiento a los bordes de la barra
                new_y = max(self.rect.top, min(new_y, self.rect.bottom - self.handle_rect.height))
                self.handle_rect.y = new_y
                
                # Calcular la tensión de 0.0 a 1.0
                max_travel = self.rect.height - self.handle_rect.height
                if max_travel > 0:
                    self.tension = (self.handle_rect.y - self.rect.y) / max_travel
                else:
                    self.tension = 0.0
        return False

    def draw(self, surface):
        # Dibujar barra blanca delgada
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=int(self.rect.width/2))
        
        # Dibujar agarrador
        pygame.draw.rect(surface, (220, 220, 230), self.handle_rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), self.handle_rect, width=2, border_radius=4)
        
        # Dibujar la 'T'
        text_surf = self.font.render("T", True, (80, 70, 110))
        text_rect = text_surf.get_rect(center=self.handle_rect.center)
        surface.blit(text_surf, text_rect)