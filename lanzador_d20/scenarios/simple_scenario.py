import os
import pygame

class SimpleScenario:
    def __init__(self, image_filename="bosque.png"):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        image_path = os.path.join(base_dir, image_filename)

        if not os.path.exists(image_path):
            image_path = image_filename

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except Exception as e:
            print(f"[ERROR] No se pudo cargar la imagen: {image_path} | Info: {e}")
            self.image = pygame.Surface((800, 600), pygame.SRCALPHA)
            self.image.fill((220, 220, 220))
            font = pygame.font.SysFont(None, 30)
            txt = font.render(f"Coloca la imagen en la raíz: {image_filename}", True, (50, 50, 50))
            self.image.blit(txt, (40, 40))

        self.invisible_button_rect = None

    def get_scaled_size(self, max_width, max_height):
        img_w, img_h = self.image.get_size()
        scale = min(max_width / img_w, max_height / img_h)
        return int(img_w * scale), int(img_h * scale)

    def handle_event(self, event):
        pass

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