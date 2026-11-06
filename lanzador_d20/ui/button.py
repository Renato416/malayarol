import pygame
import os

class Button:
    def __init__(self, x, y, w, h, text, font, image_path=None, draw_background=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.draw_background = draw_background
        
        # Colores por defecto
        self.color = (60, 60, 100)
        self.hover_color = (90, 90, 130)
        self.text_color = (255, 255, 255)
        self.is_hovered = False
        
        # Soporte de Imagen
        self.image = None
        if image_path:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            target_path = os.path.join(base_dir, image_path)
            
            if not os.path.exists(target_path):
                target_path = image_path
                
            if os.path.exists(target_path):
                try:
                    if target_path.lower().endswith('.jpg') or target_path.lower().endswith('.jpeg'):
                        raw_img = pygame.image.load(target_path).convert()
                        raw_img.set_colorkey((0, 0, 0)) # Elimina el fondo negro
                    else:
                        raw_img = pygame.image.load(target_path).convert_alpha()
                        
                    # Si no dibujamos fondo, la imagen puede ocupar todo el botón
                    margin = 8 if self.draw_background else 0
                    target_w = w - margin
                    target_h = h - margin
                    self.image = pygame.transform.smoothscale(raw_img, (target_w, target_h))
                except Exception as e:
                    print(f"[ERROR] No se pudo cargar imagen del botón {image_path}: {e}")

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

    def draw(self, surface):
        # Efecto visual al pasar el ratón (incluso si no hay fondo)
        if self.is_hovered and not self.draw_background and self.image:
            # Dibuja un leve brillo detrás de la imagen transparente
            pygame.draw.rect(surface, (120, 120, 160, 100), self.rect, border_radius=8)

        if self.draw_background:
            current_color = self.hover_color if self.is_hovered else self.color
            pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
            pygame.draw.rect(surface, (255, 255, 255), self.rect, width=2, border_radius=8)
        
        if self.image:
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)
        else:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)