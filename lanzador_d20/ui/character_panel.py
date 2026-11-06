import pygame
import os

class CharacterToken:
    def __init__(self, x, y, radius, color, label="P1", image_path=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.label = label
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.has_been_moved = False
        
        self.image = None
        # Intentar cargar la imagen si se proporciona una ruta
        if image_path and os.path.exists(image_path):
            try:
                # Cargar imagen y convertir formato
                raw_img = pygame.image.load(image_path).convert()
                # Como son JPG con fondo negro, hacemos el negro transparente
                raw_img.set_colorkey((0, 0, 0))
                # Escalar la imagen al tamaño exacto del token (diámetro = radio * 2)
                self.image = pygame.transform.smoothscale(raw_img, (radius * 2, radius * 2))
            except Exception as e:
                print(f"[ERROR] No se pudo cargar el token {image_path}: {e}")

    def draw(self, surface, font):
        if self.image:
            # Dibujar la imagen centrada
            img_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image, img_rect)
            # Dibujar el borde circular blanco encima para que se vea pulido
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 2)
        else:
            # Dibujo por defecto (Círculo de color + Texto) si no hay imagen
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
            (220, 50, 50),   # P1
            (50, 180, 50),   # P2
            (50, 100, 220),  # P3
            (230, 160, 30),  # P4
            (160, 50, 200),  # P5
            (40, 180, 180)   # P6
        ]
        
        # Nombres de las imágenes para los primeros 5 tokens
        self.image_names = [
            "bomba.png",
            "espada.png",
            "azul.png",
            "martillo.png",
            "villano.png"
        ]
        
        self.btn_minus_rect = pygame.Rect(0, 0, 30, 30)
        self.btn_plus_rect = pygame.Rect(0, 0, 30, 30)
        
        self.tokens = []
        self._add_token()

    def reset(self):
        """Reinicia la ventana a 1 jugador predeterminado en la barra"""
        self.tokens.clear()
        self._add_token()

    def _add_token(self):
        if len(self.tokens) < 6:
            idx = len(self.tokens)
            label = f"P{idx + 1}"
            color = self.colors[idx % len(self.colors)]
            
            # Buscar la ruta de la imagen si corresponde a los primeros 5
            image_path = None
            if idx < len(self.image_names):
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                target_path = os.path.join(base_dir, self.image_names[idx])
                if not os.path.exists(target_path):
                    target_path = self.image_names[idx] # Intento local si falla el base_dir
                
                if os.path.exists(target_path):
                    image_path = target_path

            token = CharacterToken(0, 0, 18, color, label, image_path)
            self.tokens.append(token)
            self.reposition_tokens()

    def _remove_token(self):
        if len(self.tokens) > 1:
            self.tokens.pop()
            self.reposition_tokens()

    def reposition_tokens(self, force_all=False):
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