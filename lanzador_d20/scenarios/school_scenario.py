import pygame
from ui.button import Button

class SchoolScenario:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        
        try:
            raw_img = pygame.image.load("61816.png").convert_alpha()
            clean_img = self._remove_black_background(raw_img)
            self.image = self._crop_to_content(clean_img)
        except FileNotFoundError:
            self.image = pygame.Surface((800, 1000), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            
        self.invisible_button_rect = None

        # Posiciones relativas (rel_x, rel_y) con los reajustes aplicados
        self.room_data = [
            {"id": "01", "rel_x": 0.75, "rel_y": 0.88},  # Más a la derecha y más abajo
            {"id": "02", "rel_x": 0.43, "rel_y": 0.88},  # Más abajo
            {"id": "03", "rel_x": 0.78, "rel_y": 0.67},
            {"id": "04", "rel_x": 0.54, "rel_y": 0.35},  # Más arriba
            {"id": "05", "rel_x": 0.76, "rel_y": 0.14},  # Más a la derecha
            {"id": "06", "rel_x": 0.13, "rel_y": 0.28},  # Más a la izquierda
            {"id": "07", "rel_x": 0.77, "rel_y": 0.35},  # Más arriba
            {"id": "08", "rel_x": 0.44, "rel_y": 0.10},  # Más a la izquierda
            {"id": "09", "rel_x": 0.14, "rel_y": 0.45},  # Más a la izquierda
        ]
        
        self.room_buttons = []
        for r in self.room_data:
            btn = Button(0, 0, 36, 26, r["id"], self.font)
            btn.color = (255, 255, 255)
            btn.hover_color = (230, 230, 230)
            btn.text_color = (0, 0, 0)
            self.room_buttons.append({"btn": btn, "rel_x": r["rel_x"], "rel_y": r["rel_y"]})

    def _remove_black_background(self, surface):
        surf = surface.copy()
        surf.set_colorkey((0, 0, 0))
        return surf

    def _crop_to_content(self, surface):
        bounding_box = surface.get_bounding_rect()
        cropped_surf = pygame.Surface((bounding_box.width, bounding_box.height), pygame.SRCALPHA)
        cropped_surf.blit(surface, (0, 0), bounding_box)
        return cropped_surf

    def get_scaled_size(self, max_width, max_height):
        img_w, img_h = self.image.get_size()
        scale = min(max_width / img_w, max_height / img_h)
        return int(img_w * scale), int(img_h * scale)

    def handle_event(self, event):
        for item in self.room_buttons:
            item["btn"].handle_event(event)

    def update(self, dt):
        pass

    def draw(self, surface, rect):
        img_w, img_h = self.image.get_size()
        scale = min(rect.width / img_w, rect.height / img_h)
        
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        scaled_img = pygame.transform.smoothscale(self.image, (new_w, new_h))
        
        offset_x = rect.x + (rect.width - new_w) // 2
        offset_y = rect.y + (rect.height - new_h) // 2
        
        surface.blit(scaled_img, (offset_x, offset_y))
        
        for item in self.room_buttons:
            bx = offset_x + int(item["rel_x"] * new_w)
            by = offset_y + int(item["rel_y"] * new_h)
            
            item["btn"].rect.center = (bx, by)
            item["btn"].draw(surface)
            
        stair_x = offset_x + int(0.12 * new_w)
        stair_y = offset_y + int(0.57 * new_h)
        stair_w = int(0.14 * new_w)
        stair_h = int(0.16 * new_h)
        
        self.invisible_button_rect = pygame.Rect(stair_x, stair_y, stair_w, stair_h)