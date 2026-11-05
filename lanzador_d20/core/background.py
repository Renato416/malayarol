import pygame

class AnimatedBackground:
    def __init__(self, speed_x=0.3, speed_y=0.3, tile_size=60, gap=1, corner_radius=12):
        # Velocidad en píxeles por segundo (movimiento suave)
        self.speed_x = speed_x * 600
        self.speed_y = speed_y * 600
        self.tile_size = tile_size
        self.gap = gap
        self.corner_radius = corner_radius
        self.spacing = tile_size + gap
        self.pattern_period = self.spacing * 2
        self.offset_x = 0.0
        self.offset_y = 0.0
        self._tile_surface = self._create_tile_surface()
        self._gradient_cache = {}

    def _create_tile_surface(self):
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        tile_color = (205, 190, 235, 55)
        pygame.draw.rect(
            surface, 
            tile_color, 
            (0, 0, self.tile_size, self.tile_size), 
            border_radius=self.corner_radius
        )
        return surface

    def update(self, dt):
        self.offset_x = (self.offset_x + self.speed_x * dt) % self.pattern_period
        self.offset_y = (self.offset_y + self.speed_y * dt) % self.pattern_period

    def draw(self, surface):
        width, height = surface.get_size()
        base_purple = (112, 52, 212)
        surface.fill(base_purple)
        
        min_col = int((-self.pattern_period - self.offset_x) // self.spacing) - 2
        max_col = int((width + self.pattern_period - self.offset_x) // self.spacing) + 2
        
        min_row = int((-self.pattern_period - self.offset_y) // self.spacing) - 2
        max_row = int((height + self.pattern_period - self.offset_y) // self.spacing) + 2
        
        for col in range(min_col, max_col):
            x = col * self.spacing + self.offset_x
            for row in range(min_row, max_row):
                if (col + row) % 2 == 0:
                    y = row * self.spacing + self.offset_y
                    surface.blit(self._tile_surface, (x, y))
            
        self._draw_bottom_gradient(surface, width, height)

    def _draw_bottom_gradient(self, surface, width, height):
        gradient_height = int(height * 0.40)
        key = (width, gradient_height)
        if key not in self._gradient_cache:
            grad_surf = pygame.Surface((width, gradient_height), pygame.SRCALPHA)
            for y in range(gradient_height):
                progress = y / gradient_height
                alpha = int(230 * (progress ** 1.8))
                pygame.draw.line(grad_surf, (15, 8, 30, alpha), (0, y), (width, y))
            self._gradient_cache[key] = grad_surf
        surface.blit(self._gradient_cache[key], (0, height - gradient_height))